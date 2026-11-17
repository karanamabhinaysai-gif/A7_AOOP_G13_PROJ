package com.bookmyshow.inventory;

import com.bookmyshow.booking.HoldToken;
import com.bookmyshow.common.ContractViolationException;
import com.bookmyshow.common.SeatId;
import com.bookmyshow.common.ShowId;

import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * U1-2, U3, U6: Show Inventory Aggregate Root.
 * Manages all seats for a given show, enforces single-sale invariant,
 * contract preconditions/postconditions on holdSeats, and deadlock-free concurrent holds.
 */
public class ShowInventory {
    private final Show show;
    private final Map<SeatId, ShowSeat> seatMap = new ConcurrentHashMap<>();

    public ShowInventory(Show show) {
        this.show = Objects.requireNonNull(show, "show cannot be null");
        // Initialize seats from screen layout
        show.screen().layout().forEach((seatId, category) ->
                seatMap.put(seatId, new ShowSeat(seatId, category)));
    }

    public Show getShow() {
        return show;
    }

    public ShowId getShowId() {
        return show.showId();
    }

    public ShowSeat getSeat(SeatId seatId) {
        return seatMap.get(seatId);
    }

    public int totalSeats() {
        return seatMap.size();
    }

    /**
     * U3 & U6: Contracted Seat Holding Method with Expiry Postcondition.
     *
     * Preconditions:
     * - requestedSeats is not null or empty.
     * - userId is not null or blank.
     * - holdDuration is positive.
     * - All requested seats must exist in the show's layout.
     *
     * Invariants & Concurrency:
     * - Seats are acquired in canonical lexicographical order to eliminate lock-ordering deadlocks (U6).
     * - Atomic all-or-nothing: if any seat is unavailable, none are held.
     *
     * Postconditions:
     * - If successful, returns an active HoldToken with expiresAt = now + holdDuration.
     * - Each held seat's state is HELD with matching userId and expiresAt.
     */
    public Optional<HoldToken> holdSeats(List<SeatId> requestedSeats, String userId, Duration holdDuration) {
        // --- PRECONDITION CHECKS (U3) ---
        if (requestedSeats == null || requestedSeats.isEmpty()) {
            throw new ContractViolationException("Precondition failed: requestedSeats cannot be null or empty");
        }
        if (userId == null || userId.trim().isEmpty()) {
            throw new ContractViolationException("Precondition failed: userId cannot be null or blank");
        }
        if (holdDuration == null || holdDuration.isNegative() || holdDuration.isZero()) {
            throw new ContractViolationException("Precondition failed: holdDuration must be strictly positive");
        }

        Instant now = Instant.now();
        Instant expiresAt = now.plus(holdDuration);

        // Sort seats in canonical natural order to prevent deadlocks (U6)
        List<SeatId> sortedSeatIds = new ArrayList<>(new HashSet<>(requestedSeats));
        Collections.sort(sortedSeatIds);

        List<ShowSeat> lockedSeats = new ArrayList<>();
        try {
            // 1. Acquire fine-grained locks in sorted order
            for (SeatId id : sortedSeatIds) {
                ShowSeat seat = seatMap.get(id);
                if (seat == null) {
                    throw new ContractViolationException("Precondition failed: Seat " + id + " does not exist in show");
                }
                seat.getLock().lock();
                lockedSeats.add(seat);
            }

            // 2. Atomic all-or-nothing check: ensure every seat is available
            for (ShowSeat seat : lockedSeats) {
                if (!seat.isAvailable(now)) {
                    return Optional.empty(); // Hold rejected due to conflict
                }
            }

            // 3. Apply hold state to all seats
            for (ShowSeat seat : lockedSeats) {
                boolean held = seat.tryHold(userId, expiresAt, now);
                if (!held) {
                    throw new IllegalStateException("Unexpected state transition failure while holding seat: " + seat.getSeatId());
                }
            }

            // --- POSTCONDITION VERIFICATION (U3) ---
            for (ShowSeat seat : lockedSeats) {
                SeatState state = seat.getState();
                if (!(state instanceof HeldState hs) || !hs.getHeldByUserId().equals(userId) || !hs.getExpiresAt().equals(expiresAt)) {
                    throw new ContractViolationException("Postcondition failed: Seat state did not reflect valid hold parameters");
                }
            }

            HoldToken token = new HoldToken(UUID.randomUUID().toString(), show.showId(), sortedSeatIds, userId, expiresAt);
            return Optional.of(token);

        } finally {
            // Always unlock all seats in reverse or same order
            for (ShowSeat seat : lockedSeats) {
                seat.getLock().unlock();
            }
        }
    }

    /**
     * Confirms held seats, transitioning them permanently to SOLD.
     * Enforces the single-sale invariant (U1-2).
     */
    public void confirmSeats(List<SeatId> seats, String userId) {
        Instant now = Instant.now();
        List<SeatId> sortedSeats = new ArrayList<>(new HashSet<>(seats));
        Collections.sort(sortedSeats);

        for (SeatId id : sortedSeats) {
            ShowSeat seat = seatMap.get(id);
            if (seat == null) throw new IllegalArgumentException("Seat " + id + " does not exist");

            seat.getLock().lock();
            try {
                seat.confirm(userId, now);
            } finally {
                seat.getLock().unlock();
            }
        }
    }

    /**
     * Releases held seats back to FREE state (compensating transaction for payment timeout / cancellation).
     */
    public void releaseSeats(List<SeatId> seats, String userId) {
        List<SeatId> sortedSeats = new ArrayList<>(new HashSet<>(seats));
        Collections.sort(sortedSeats);

        for (SeatId id : sortedSeats) {
            ShowSeat seat = seatMap.get(id);
            if (seat == null) continue;

            seat.getLock().lock();
            try {
                if (seat.getState() instanceof HeldState hs && hs.getHeldByUserId().equals(userId)) {
                    seat.release(userId);
                }
            } finally {
                seat.getLock().unlock();
            }
        }
    }

    /**
     * Computes current occupancy rate (sold + non-expired held seats).
     */
    public double getOccupancyRate(Instant now) {
        long occupied = seatMap.values().stream()
                .filter(s -> !s.isAvailable(now))
                .count();
        return (double) occupied / seatMap.size();
    }

    public Map<SeatId, ShowSeat> getAllSeats() {
        return Collections.unmodifiableMap(seatMap);
    }
}
