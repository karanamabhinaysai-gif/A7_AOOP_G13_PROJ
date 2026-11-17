package com.bookmyshow.booking;

import com.bookmyshow.catalog.Cinema;
import com.bookmyshow.common.Money;
import com.bookmyshow.common.SeatId;
import com.bookmyshow.inventory.Show;
import com.bookmyshow.inventory.ShowInventory;
import com.bookmyshow.inventory.ShowSeat;
import com.bookmyshow.payments.PaymentGateway;
import com.bookmyshow.payments.PaymentResult;
import com.bookmyshow.pricing.PricingStrategy;

import java.time.Duration;
import java.time.Instant;
import java.util.*;

/**
 * U5: Hold -> Pay -> Confirm Saga Orchestrator.
 * Coordinates multi-step transaction across Inventory and Payments bounded contexts.
 * Executes compensating transactions (releases held seats) on payment rejection or timeout.
 */
public class BookingSagaOrchestrator {
    private final ShowInventory inventory;
    private final Cinema cinema;
    private final PricingStrategy pricingStrategy;
    private final PaymentGateway paymentGateway;
    private final Duration holdDuration;

    public BookingSagaOrchestrator(
            ShowInventory inventory,
            Cinema cinema,
            PricingStrategy pricingStrategy,
            PaymentGateway paymentGateway,
            Duration holdDuration) {
        this.inventory = Objects.requireNonNull(inventory, "inventory cannot be null");
        this.cinema = Objects.requireNonNull(cinema, "cinema cannot be null");
        this.pricingStrategy = Objects.requireNonNull(pricingStrategy, "pricingStrategy cannot be null");
        this.paymentGateway = Objects.requireNonNull(paymentGateway, "paymentGateway cannot be null");
        this.holdDuration = Objects.requireNonNull(holdDuration, "holdDuration cannot be null");
    }

    public record BookingRequest(
            String customerId,
            List<SeatId> requestedSeats,
            boolean addPopcorn,
            boolean addCoke,
            boolean addNachos
    ) {}

    public record BookingOutcome(
            boolean successful,
            Optional<Ticket> ticket,
            String message
    ) {
        public static BookingOutcome success(Ticket ticket) {
            return new BookingOutcome(true, Optional.of(ticket), "Booking confirmed successfully");
        }

        public static BookingOutcome failure(String message) {
            return new BookingOutcome(false, Optional.empty(), message);
        }
    }

    /**
     * Executes the Hold -> Pay -> Confirm Saga.
     */
    public BookingOutcome executeBooking(BookingRequest request) {
        Show show = inventory.getShow();
        String customerId = request.customerId();
        List<SeatId> requestedSeats = request.requestedSeats();

        // ---------------------------------------------------------------------
        // SAGA STEP 1: HOLD SEATS (INVENTORY CONTEXT)
        // ---------------------------------------------------------------------
        Optional<HoldToken> holdTokenOpt = inventory.holdSeats(requestedSeats, customerId, holdDuration);
        if (holdTokenOpt.isEmpty()) {
            return BookingOutcome.failure("Seats unavailable: one or more requested seats are already held or sold");
        }

        HoldToken holdToken = holdTokenOpt.get();

        // ---------------------------------------------------------------------
        // SAGA STEP 2: CALCULATE PRICING & APPLY DECORATOR COMBOS (BOOKING CONTEXT)
        // ---------------------------------------------------------------------
        Instant now = Instant.now();
        double occupancy = inventory.getOccupancyRate(now);

        List<BookingItem> items = new ArrayList<>();
        Money totalCost = Money.zero();

        for (SeatId seatId : requestedSeats) {
            ShowSeat showSeat = inventory.getSeat(seatId);
            Money seatPrice = pricingStrategy.calculatePrice(showSeat.getCategory(), show, occupancy);

            BookingItem item = new SeatTicketItem(seatId, showSeat.getCategory(), seatPrice);

            if (request.addPopcorn()) {
                item = new PopcornDecorator(item);
            }
            if (request.addCoke()) {
                item = new CokeDecorator(item);
            }
            if (request.addNachos()) {
                item = new NachosDecorator(item);
            }

            items.add(item);
            totalCost = totalCost.add(item.getCost());
        }

        // ---------------------------------------------------------------------
        // SAGA STEP 3: PROCESS PAYMENT (PAYMENTS CONTEXT)
        // ---------------------------------------------------------------------
        PaymentResult paymentResult;
        try {
            paymentResult = paymentGateway.processPayment(holdToken.holdId(), customerId, totalCost);
        } catch (Exception ex) {
            paymentResult = PaymentResult.failure("Payment gateway error: " + ex.getMessage());
        }

        // Check if hold has expired during payment processing
        boolean isExpired = holdToken.isExpired(Instant.now());

        if (!paymentResult.successful() || isExpired) {
            // -----------------------------------------------------------------
            // SAGA COMPENSATION: RELEASE SEATS ON PAYMENT FAILURE OR TIMEOUT
            // -----------------------------------------------------------------
            inventory.releaseSeats(requestedSeats, customerId);

            String reason = isExpired
                    ? "Payment took too long: Seat hold expired before confirmation"
                    : "Payment failed (" + paymentResult.failureReason() + ")";
            return BookingOutcome.failure(reason);
        }

        // ---------------------------------------------------------------------
        // SAGA STEP 4: CONFIRM SEATS & ISSUE TICKET (TERMINAL SUCCESS)
        // ---------------------------------------------------------------------
        try {
            inventory.confirmSeats(requestedSeats, customerId);
        } catch (Exception ex) {
            // In the rare event of confirmation failure, release and fail
            inventory.releaseSeats(requestedSeats, customerId);
            return BookingOutcome.failure("Failed to confirm seats: " + ex.getMessage());
        }

        String bookingId = "BMS-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
        List<String> itemsSummary = items.stream().map(BookingItem::getDescription).toList();

        Ticket ticket = new Ticket(
                bookingId,
                show.showId(),
                show.movie().title(),
                cinema.name(),
                show.screen().name(),
                show.startTime(),
                requestedSeats,
                itemsSummary,
                totalCost,
                customerId,
                Instant.now()
        );

        return BookingOutcome.success(ticket);
    }
}
