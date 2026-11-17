package com.bookmyshow.inventory;

import java.time.Instant;
import java.util.Objects;

/**
 * U4: State Pattern - Sold State (Terminal State for a Show).
 * Enforces U1-2 invariant: a seat is sold at most once per show.
 */
public final class SoldState implements SeatState {
    private final String bookedByUserId;
    private final Instant bookedAt;

    public SoldState(String bookedByUserId, Instant bookedAt) {
        this.bookedByUserId = Objects.requireNonNull(bookedByUserId, "bookedByUserId cannot be null");
        this.bookedAt = Objects.requireNonNull(bookedAt, "bookedAt cannot be null");
    }

    @Override
    public boolean isAvailable(Instant now) {
        return false;
    }

    @Override
    public SeatState hold(String userId, Instant expiresAt, Instant now) {
        throw new IllegalStateException("Seat is already permanently SOLD to user: " + bookedByUserId);
    }

    @Override
    public SeatState confirm(String userId, Instant now) {
        throw new IllegalStateException("Seat is already permanently SOLD to user: " + bookedByUserId);
    }

    @Override
    public SeatState release(String userId) {
        throw new IllegalStateException("Cannot release a SOLD seat; booking is already finalized");
    }

    public String getBookedByUserId() {
        return bookedByUserId;
    }

    public Instant getBookedAt() {
        return bookedAt;
    }

    @Override
    public String statusName() {
        return "SOLD";
    }

    @Override
    public String toString() {
        return "SoldState[bookedBy=" + bookedByUserId + ", bookedAt=" + bookedAt + "]";
    }
}
