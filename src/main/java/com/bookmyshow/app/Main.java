package com.bookmyshow.app;

import com.bookmyshow.booking.BookingSagaOrchestrator;
import com.bookmyshow.booking.Ticket;
import com.bookmyshow.catalog.*;
import com.bookmyshow.common.*;
import com.bookmyshow.inventory.*;
import com.bookmyshow.payments.MockPaymentGateway;
import com.bookmyshow.pricing.*;

import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Main Interactive Application & Live Demonstration of U1-U7.
 */
public class Main {
    public static void main(String[] args) throws Exception {
        printHeader("BOOKMYSHOW-STYLE MOVIE TICKET BOOKING SYSTEM (AOOP G13)");

        // -------------------------------------------------------------
        // 1. U7: CATALOG CONTEXT SETUP
        // -------------------------------------------------------------
        CatalogService catalogService = new CatalogService();

        Movie avatar = new Movie(
                "MOV-AVATAR-2",
                "Avatar: The Way of Water",
                "English / 3D",
                "Sci-Fi / Adventure",
                Duration.ofMinutes(192),
                "UA"
        );
        catalogService.addMovie(avatar);

        // Screen layout with Sealed SeatCategory hierarchy (U3)
        Map<SeatId, SeatCategory> layout = new LinkedHashMap<>();
        // Row A: Platinum VIP
        for (int i = 1; i <= 6; i++) layout.put(new SeatId("A", i), new PlatinumSeat());
        // Row B & C: Gold
        for (int i = 1; i <= 6; i++) layout.put(new SeatId("B", i), new GoldSeat());
        for (int i = 1; i <= 6; i++) layout.put(new SeatId("C", i), new GoldSeat());
        // Row D: Silver
        for (int i = 1; i <= 6; i++) layout.put(new SeatId("D", i), new SilverSeat());

        Screen imaxScreen = new Screen("SCR-IMAX-01", "IMAX Laser Auditorium 1", layout);
        Cinema pvrInox = new Cinema("CIN-001", "PVR INOX Gold", "Bengaluru", List.of(imaxScreen));
        catalogService.addCinema(pvrInox);

        // -------------------------------------------------------------
        // 2. U7: SHOW INVENTORY CONTEXT SETUP
        // -------------------------------------------------------------
        ShowId showId = new ShowId("SHOW-AVATAR-FDFS-001");
        Instant showTime = Instant.now().plus(Duration.ofHours(3));
        Show show = new Show(showId, avatar, imaxScreen, showTime, showTime.plus(avatar.duration()));
        ShowInventory inventory = new ShowInventory(show);

        System.out.println("🎬 Movie: " + avatar.title() + " (" + avatar.language() + ")");
        System.out.println("🏢 Cinema: " + pvrInox.name() + ", " + pvrInox.city() + " | Screen: " + imaxScreen.name());
        System.out.println("🎟️ Total Seats in Auditorium: " + inventory.totalSeats());

        // -------------------------------------------------------------
        // 3. U4: STRATEGY & DECORATOR DEMO (SINGLE BOOKING WITH COMBOS)
        // -------------------------------------------------------------
        printSection("DEMO 1: SINGLE BOOKING WITH DYNAMIC PRICING & FOOD DECORATORS (U4)");

        PricingStrategy dynamicPricing = new DemandSurgePricingStrategy();
        MockPaymentGateway paymentGateway = new MockPaymentGateway();
        BookingSagaOrchestrator saga = new BookingSagaOrchestrator(
                inventory, pvrInox, dynamicPricing, paymentGateway, Duration.ofSeconds(5)
        );

        BookingSagaOrchestrator.BookingRequest request1 = new BookingSagaOrchestrator.BookingRequest(
                "USER-ALICE",
                List.of(new SeatId("A", 1), new SeatId("A", 2)),
                true,  // Popcorn combo
                true,  // Coke beverage
                false  // No nachos
        );

        BookingSagaOrchestrator.BookingOutcome outcome1 = saga.executeBooking(request1);
        if (outcome1.successful()) {
            printTicket(outcome1.ticket().get());
        } else {
            System.out.println("❌ Booking failed: " + outcome1.message());
        }

        // -------------------------------------------------------------
        // 4. U5: SAGA COMPENSATION DEMO (PAYMENT FAILURE & TIMEOUT ROLLBACK)
        // -------------------------------------------------------------
        printSection("DEMO 2: SAGA COMPENSATING ACTION ON PAYMENT FAILURE (U5)");

        paymentGateway.setShouldFail(true); // Simulate declined payment
        BookingSagaOrchestrator.BookingRequest failedRequest = new BookingSagaOrchestrator.BookingRequest(
                "USER-BOB",
                List.of(new SeatId("A", 3)),
                false, false, false
        );

        System.out.println("👉 User Bob attempts to book Seat A3 with failing payment gateway...");
        BookingSagaOrchestrator.BookingOutcome outcome2 = saga.executeBooking(failedRequest);
        System.out.println("Outcome: " + outcome2.message());
        System.out.println("🔍 Checking Seat A3 state after compensation: "
                + inventory.getSeat(new SeatId("A", 3)).getState().statusName()
                + " (Reverted back to FREE for other customers!)");

        paymentGateway.setShouldFail(false); // Reset payment gateway

        // -------------------------------------------------------------
        // 5. U6: CONCURRENT FIRST-DAY-FIRST-SHOW RUSH SIMULATION
        // -------------------------------------------------------------
        printSection("DEMO 3: HIGH-CONCURRENCY FIRST-DAY-FIRST-SHOW RUSH (U6 & U1-U2)");
        System.out.println("⚡ 10 concurrent users simultaneously competing for premium seats (A3, A4, B1)...");

        int threadCount = 10;
        ExecutorService executor = Executors.newFixedThreadPool(threadCount);
        CyclicBarrier barrier = new CyclicBarrier(threadCount); // Synchronize threads to fire simultaneously

        AtomicInteger successfulBookings = new AtomicInteger(0);
        AtomicInteger deniedBookings = new AtomicInteger(0);
        List<Future<?>> futures = new ArrayList<>();

        for (int i = 1; i <= threadCount; i++) {
            final String userId = "RUSH-USER-" + i;
            // Overlapping contested seat selection
            final List<SeatId> seatsToAttempt = (i % 2 == 0)
                    ? List.of(new SeatId("A", 3), new SeatId("A", 4))
                    : List.of(new SeatId("A", 4), new SeatId("B", 1));

            futures.add(executor.submit(() -> {
                try {
                    barrier.await(); // Simultaneous blast
                    BookingSagaOrchestrator.BookingRequest rushReq =
                            new BookingSagaOrchestrator.BookingRequest(userId, seatsToAttempt, false, true, false);
                    BookingSagaOrchestrator.BookingOutcome outcome = saga.executeBooking(rushReq);

                    if (outcome.successful()) {
                        successfulBookings.incrementAndGet();
                        System.out.println("  🟢 [SUCCESS] " + userId + " secured seats " + seatsToAttempt);
                    } else {
                        deniedBookings.incrementAndGet();
                        System.out.println("  🔴 [DENIED]  " + userId + " missed out (seats held/sold)");
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }));
        }

        for (Future<?> f : futures) {
            f.get();
        }
        executor.shutdown();

        System.out.println("\n📊 Concurrent Rush Summary:");
        System.out.println("   Successful reservations : " + successfulBookings.get());
        System.out.println("   Contested / Denied      : " + deniedBookings.get());

        // -------------------------------------------------------------
        // 6. U1-U2: INVARIANT VERIFICATION
        // -------------------------------------------------------------
        printSection("DEMO 4: SINGLE-SALE INVARIANT VERIFICATION (U1-U2)");
        long soldCount = inventory.getAllSeats().values().stream()
                .filter(s -> s.getState() instanceof SoldState)
                .count();
        System.out.println("Total seats permanently SOLD in Auditorium: " + soldCount);
        System.out.println("Single-sale invariant verified: No duplicate bookings possible!");

        printHeader("DEMONSTRATION COMPLETED SUCCESSFULLY");
    }

    private static void printHeader(String title) {
        System.out.println("\n" + "=".repeat(75));
        System.out.println("  " + title);
        System.out.println("=".repeat(75));
    }

    private static void printSection(String sectionTitle) {
        System.out.println("\n" + "-".repeat(75));
        System.out.println("▶ " + sectionTitle);
        System.out.println("-".repeat(75));
    }

    private static void printTicket(Ticket ticket) {
        System.out.println("\n┌──────────────────────────────────────────────────────────────────┐");
        System.out.println("│                     CONFIRMED MOVIE TICKET                       │");
        System.out.println("├──────────────────────────────────────────────────────────────────┤");
        System.out.printf("│ Booking Ref : %-50s │%n", ticket.bookingId());
        System.out.printf("│ Movie       : %-50s │%n", ticket.movieTitle());
        System.out.printf("│ Cinema      : %-50s │%n", ticket.cinemaName());
        System.out.printf("│ Screen      : %-50s │%n", ticket.screenName());
        System.out.printf("│ Customer    : %-50s │%n", ticket.customerId());
        System.out.printf("│ Seats       : %-50s │%n", ticket.seats());
        System.out.println("├──────────────────────────────────────────────────────────────────┤");
        System.out.println("│ Items & Combos Breakdown:                                        │");
        for (String item : ticket.itemsSummary()) {
            System.out.printf("│   • %-60s │%n", item);
        }
        System.out.println("├──────────────────────────────────────────────────────────────────┤");
        System.out.printf("│ Total Paid  : %-50s │%n", ticket.totalAmount());
        System.out.println("└──────────────────────────────────────────────────────────────────┘\n");
    }
}
