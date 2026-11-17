package com.bookmyshow;

import com.bookmyshow.booking.*;
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
 * Comprehensive Automated Verification Suite for Units U1 through U7.
 */
public class BookingSystemTests {
    private static int totalPassed = 0;
    private static int totalFailed = 0;

    public static void main(String[] args) {
        System.out.println("Running BookingSystemTests suite...\n");

        testU1_U2_ValueObjectsAndSingleSaleInvariant();
        testU3_ContractsOnHoldSeatsAndExpiry();
        testU3_SealedSeatCategoryHierarchy();
        testU4_StatePatternLifecycle();
        testU4_StrategyPatternDynamicPricing();
        testU4_DecoratorPatternFoodCombos();
        testU5_HoldPayConfirmSagaSuccess();
        testU5_SagaCompensationOnPaymentFailure();
        testU5_SagaCompensationOnTimeout();
        testU6_HighConcurrencyFirstDayFirstShowRush();
        testU7_BoundedContextsSeparation();

        System.out.println("\n" + "=".repeat(60));
        System.out.println("TEST RESULTS: Passed: " + totalPassed + ", Failed: " + totalFailed);
        System.out.println("=".repeat(60));

        if (totalFailed > 0) {
            System.exit(1);
        }
    }

    private static void assertEquals(Object expected, Object actual, String message) {
        if (!Objects.equals(expected, actual)) {
            totalFailed++;
            System.err.println("❌ FAILED: " + message + " (Expected: " + expected + ", Actual: " + actual + ")");
        } else {
            totalPassed++;
            System.out.println("✅ PASSED: " + message);
        }
    }

    private static void assertTrue(boolean condition, String message) {
        assertEquals(true, condition, message);
    }

    private static void assertFalse(boolean condition, String message) {
        assertEquals(false, condition, message);
    }

    // -------------------------------------------------------------
    // TEST U1-U2
    // -------------------------------------------------------------
    private static void testU1_U2_ValueObjectsAndSingleSaleInvariant() {
        System.out.println("\n[U1-U2] Testing Value Objects and Single-Sale Invariant");

        ShowId s1 = new ShowId("SHOW-1");
        SeatId seatA1 = new SeatId("A", 1);
        Money m1 = new Money(150.0);
        Money m2 = new Money(50.0);

        assertEquals("SHOW-1", s1.value(), "ShowId value check");
        assertEquals("A1", seatA1.toString(), "SeatId string representation");
        assertEquals(new Money(200.0), m1.add(m2), "Money addition");

        // Single-sale invariant: Once SOLD, confirming again must throw
        ShowSeat seat = new ShowSeat(seatA1, new GoldSeat());
        seat.getLock().lock();
        try {
            seat.tryHold("user1", Instant.now().plusSeconds(60), Instant.now());
            seat.confirm("user1", Instant.now());
            assertTrue(seat.getState() instanceof SoldState, "Seat is in SoldState");

            boolean threw = false;
            try {
                seat.confirm("user2", Instant.now());
            } catch (IllegalStateException e) {
                threw = true;
            }
            assertTrue(threw, "Sold seat cannot be confirmed again (single-sale invariant)");
        } finally {
            seat.getLock().unlock();
        }
    }

    // -------------------------------------------------------------
    // TEST U3
    // -------------------------------------------------------------
    private static void testU3_ContractsOnHoldSeatsAndExpiry() {
        System.out.println("\n[U3] Testing Contracts on holdSeats (Preconditions and Expiry Postcondition)");

        ShowInventory inventory = createTestInventory();

        // Precondition 1: Empty seat list
        boolean preconditionFailed = false;
        try {
            inventory.holdSeats(Collections.emptyList(), "user1", Duration.ofMinutes(5));
        } catch (ContractViolationException e) {
            preconditionFailed = true;
        }
        assertTrue(preconditionFailed, "Precondition violated on empty requested seats");

        // Precondition 2: Null/blank user
        preconditionFailed = false;
        try {
            inventory.holdSeats(List.of(new SeatId("A", 1)), "", Duration.ofMinutes(5));
        } catch (ContractViolationException e) {
            preconditionFailed = true;
        }
        assertTrue(preconditionFailed, "Precondition violated on blank userId");

        // Expiry postcondition: Token expiresAt matches hold duration
        Instant before = Instant.now();
        Optional<HoldToken> token = inventory.holdSeats(List.of(new SeatId("A", 1)), "user1", Duration.ofSeconds(10));
        Instant after = Instant.now();

        assertTrue(token.isPresent(), "Hold token issued");
        assertTrue(!token.get().expiresAt().isBefore(before.plusSeconds(10)), "Hold expiry postcondition >= 10s");
        assertTrue(!token.get().expiresAt().isAfter(after.plusSeconds(10)), "Hold expiry postcondition <= 10s");
    }

    private static void testU3_SealedSeatCategoryHierarchy() {
        System.out.println("\n[U3] Testing Sealed SeatCategory Hierarchy");
        SeatCategory silver = new SilverSeat();
        SeatCategory gold = new GoldSeat();
        SeatCategory platinum = new PlatinumSeat();
        SeatCategory recliner = new ReclinerSeat();

        assertEquals("SILVER", silver.name(), "Silver seat category");
        assertEquals("GOLD", gold.name(), "Gold seat category");
        assertEquals("PLATINUM", platinum.name(), "Platinum seat category");
        assertEquals("RECLINER", recliner.name(), "Recliner seat category");
    }

    // -------------------------------------------------------------
    // TEST U4
    // -------------------------------------------------------------
    private static void testU4_StatePatternLifecycle() {
        System.out.println("\n[U4] Testing State Pattern (Free -> Held -> Sold & Free -> Held -> Free)");
        SeatState free = FreeState.INSTANCE;
        assertTrue(free.isAvailable(Instant.now()), "Free state is available");

        Instant expiresAt = Instant.now().plusSeconds(5);
        SeatState held = free.hold("user1", expiresAt, Instant.now());
        assertEquals("HELD", held.statusName(), "Held state transition");
        assertFalse(held.isAvailable(Instant.now()), "Held state is unavailable before expiry");

        // Confirm
        SeatState sold = held.confirm("user1", Instant.now());
        assertEquals("SOLD", sold.statusName(), "Sold state transition");
        assertFalse(sold.isAvailable(Instant.now()), "Sold state is permanently unavailable");
    }

    private static void testU4_StrategyPatternDynamicPricing() {
        System.out.println("\n[U4] Testing Strategy Pattern for Dynamic Pricing");
        Show show = createTestShow();
        PricingStrategy standard = new StandardPricingStrategy();
        PricingStrategy surge = new DemandSurgePricingStrategy();

        SeatCategory gold = new GoldSeat(); // Base price 250.00
        Money standardPrice = standard.calculatePrice(gold, show, 0.10);
        assertEquals(new Money(250.00), standardPrice, "Standard pricing matches base price");

        Money surgePriceLow = surge.calculatePrice(gold, show, 0.10);
        assertEquals(new Money(250.00), surgePriceLow, "Low occupancy has no surge");

        Money surgePriceHigh = surge.calculatePrice(gold, show, 0.85);
        assertEquals(new Money(375.00), surgePriceHigh, "High occupancy triggers 50% surge (250 * 1.5 = 375)");
    }

    private static void testU4_DecoratorPatternFoodCombos() {
        System.out.println("\n[U4] Testing Decorator Pattern for Food Combos");
        SeatId id = new SeatId("A", 1);
        BookingItem ticket = new SeatTicketItem(id, new SilverSeat(), new Money(150.00));

        BookingItem withPopcorn = new PopcornDecorator(ticket);
        assertEquals(new Money(430.00), withPopcorn.getCost(), "Ticket + Popcorn (150 + 280 = 430)");

        BookingItem withPopcornAndCoke = new CokeDecorator(withPopcorn);
        assertEquals(new Money(580.00), withPopcornAndCoke.getCost(), "Ticket + Popcorn + Coke (430 + 150 = 580)");

        BookingItem fullCombo = new NachosDecorator(withPopcornAndCoke);
        assertEquals(new Money(800.00), fullCombo.getCost(), "Ticket + Popcorn + Coke + Nachos (580 + 220 = 800)");
        assertTrue(fullCombo.getDescription().contains("Caramel Popcorn"), "Decorator description chains correctly");
    }

    // -------------------------------------------------------------
    // TEST U5
    // -------------------------------------------------------------
    private static void testU5_HoldPayConfirmSagaSuccess() {
        System.out.println("\n[U5] Testing Saga: Happy Path (Hold -> Pay -> Confirm)");
        ShowInventory inventory = createTestInventory();
        Cinema cinema = createTestCinema();
        MockPaymentGateway paymentGateway = new MockPaymentGateway();
        BookingSagaOrchestrator saga = new BookingSagaOrchestrator(
                inventory, cinema, new StandardPricingStrategy(), paymentGateway, Duration.ofSeconds(10)
        );

        BookingSagaOrchestrator.BookingRequest request = new BookingSagaOrchestrator.BookingRequest(
                "user1", List.of(new SeatId("A", 1)), true, false, false
        );

        BookingSagaOrchestrator.BookingOutcome outcome = saga.executeBooking(request);
        assertTrue(outcome.successful(), "Saga completes successfully");
        assertTrue(outcome.ticket().isPresent(), "Ticket is issued");
        assertEquals("SOLD", inventory.getSeat(new SeatId("A", 1)).getState().statusName(), "Seat confirmed to SOLD");
    }

    private static void testU5_SagaCompensationOnPaymentFailure() {
        System.out.println("\n[U5] Testing Saga Compensation: Payment Failure Releases Seats");
        ShowInventory inventory = createTestInventory();
        Cinema cinema = createTestCinema();
        MockPaymentGateway paymentGateway = new MockPaymentGateway();
        paymentGateway.setShouldFail(true); // Payment will fail

        BookingSagaOrchestrator saga = new BookingSagaOrchestrator(
                inventory, cinema, new StandardPricingStrategy(), paymentGateway, Duration.ofSeconds(10)
        );

        BookingSagaOrchestrator.BookingRequest request = new BookingSagaOrchestrator.BookingRequest(
                "user1", List.of(new SeatId("A", 2)), false, false, false
        );

        BookingSagaOrchestrator.BookingOutcome outcome = saga.executeBooking(request);
        assertFalse(outcome.successful(), "Saga fails on declined payment");
        assertTrue(inventory.getSeat(new SeatId("A", 2)).isAvailable(Instant.now()),
                "Compensating transaction released seat back to FREE");
    }

    private static void testU5_SagaCompensationOnTimeout() {
        System.out.println("\n[U5] Testing Saga Compensation: Hold Timeout Releases Seats");
        ShowInventory inventory = createTestInventory();
        Cinema cinema = createTestCinema();
        MockPaymentGateway paymentGateway = new MockPaymentGateway();
        // Payment takes 300ms, but hold duration is only 100ms
        paymentGateway.setSimulatedDelayMs(300);

        BookingSagaOrchestrator saga = new BookingSagaOrchestrator(
                inventory, cinema, new StandardPricingStrategy(), paymentGateway, Duration.ofMillis(100)
        );

        BookingSagaOrchestrator.BookingRequest request = new BookingSagaOrchestrator.BookingRequest(
                "user1", List.of(new SeatId("A", 3)), false, false, false
        );

        BookingSagaOrchestrator.BookingOutcome outcome = saga.executeBooking(request);
        assertFalse(outcome.successful(), "Saga fails due to hold timeout");
        assertTrue(outcome.message().contains("expired"), "Failure message cites hold expiration");
    }

    // -------------------------------------------------------------
    // TEST U6
    // -------------------------------------------------------------
    private static void testU6_HighConcurrencyFirstDayFirstShowRush() {
        System.out.println("\n[U6] Testing High-Concurrency FDFS Rush (Race Conditions & Deadlock Prevention)");
        ShowInventory inventory = createTestInventory();
        Cinema cinema = createTestCinema();
        MockPaymentGateway paymentGateway = new MockPaymentGateway();
        BookingSagaOrchestrator saga = new BookingSagaOrchestrator(
                inventory, cinema, new StandardPricingStrategy(), paymentGateway, Duration.ofSeconds(5)
        );

        int threads = 16;
        ExecutorService executor = Executors.newFixedThreadPool(threads);
        CyclicBarrier barrier = new CyclicBarrier(threads);
        AtomicInteger successCount = new AtomicInteger(0);
        List<Future<?>> futures = new ArrayList<>();

        // All 16 threads fight for Seat A4
        for (int i = 0; i < threads; i++) {
            final String uId = "rush-user-" + i;
            futures.add(executor.submit(() -> {
                try {
                    barrier.await();
                    BookingSagaOrchestrator.BookingRequest req =
                            new BookingSagaOrchestrator.BookingRequest(uId, List.of(new SeatId("A", 4)), false, false, false);
                    BookingSagaOrchestrator.BookingOutcome out = saga.executeBooking(req);
                    if (out.successful()) {
                        successCount.incrementAndGet();
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }));
        }

        for (Future<?> f : futures) {
            try {
                f.get();
            } catch (Exception ignored) {}
        }
        executor.shutdown();

        assertEquals(1, successCount.get(), "Exactly one user out of 16 won contested Seat A4");
        assertEquals("SOLD", inventory.getSeat(new SeatId("A", 4)).getState().statusName(), "Contested seat is SOLD");
    }

    // -------------------------------------------------------------
    // TEST U7
    // -------------------------------------------------------------
    private static void testU7_BoundedContextsSeparation() {
        System.out.println("\n[U7] Testing Bounded Contexts Separation");
        CatalogService catalog = new CatalogService();
        Movie m = new Movie("M1", "Inception", "EN", "SciFi", Duration.ofMinutes(148), "UA");
        catalog.addMovie(m);

        assertTrue(catalog.findMovieById("M1").isPresent(), "Catalog Context operates independently");
    }

    // Helper factories
    private static Show createTestShow() {
        Map<SeatId, SeatCategory> layout = new HashMap<>();
        for (int i = 1; i <= 6; i++) {
            layout.put(new SeatId("A", i), new PlatinumSeat());
            layout.put(new SeatId("B", i), new GoldSeat());
        }
        Screen screen = new Screen("SCR-1", "Screen 1", layout);
        Movie movie = new Movie("M1", "Test Movie", "EN", "Action", Duration.ofMinutes(120), "UA");
        return new Show(new ShowId("S1"), movie, screen, Instant.now().plusSeconds(3600), Instant.now().plusSeconds(10800));
    }

    private static ShowInventory createTestInventory() {
        return new ShowInventory(createTestShow());
    }

    private static Cinema createTestCinema() {
        return new Cinema("C1", "PVR Cinemas", "Mumbai", List.of());
    }
}
