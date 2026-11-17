package com.bookmyshow.inventory;

import java.time.Instant;
import java.util.Objects;

/**
 * U4: State Pattern - Held State
 * Supports temporary reservation with automatic expiration check.
 */
public final class HeldState implements SeatState {
    private final String heldByUserId;
    private final Instant expiresAt;

    public HeldState(String heldByUserId, Instant expiresAt) {
        this.heldByUserId = Objects.requireNonNull(heldByUserId, "heldByUserId cannot be null");
        this.expiresAt = Objects.requireNonNull(expiresAt, "expiresAt cannot be null");
    }

    @Override
    public boolean isAvailable(Instant now) {
        // Expired hold becomes available again
        return now.isAfter(expiresAt);
    }

    @Override
    public SeatState hold(String userId, Instant expiresAt, Instant now) {
        if (isAvailable(now)) {
            // Previous hold has expired; grant hold to new requester
            return new HeldState(userId, expiresAt);
        }
        throw new IllegalStateException("Seat is currently held by user: " + heldByUserId);
    }

    @Override
    public SeatState confirm(String userId, Instant now) {
        if (now.isAfter(expiresAt)) {
            throw new IllegalStateException("Hold has expired at " + expiresAt + "; cannot confirm");
        }
        if (!this.heldByUserId.equals(userId)) {
            throw new IllegalStateException(
                    "Seat hold belongs to user '" + heldByUserId + "', cannot be confirmed by '" + userId + "'");
        }
        return new SoldState(userId, now);
    }

    @Override
    public SeatState release(String userId) {
        if (!this.heldByUserId.equals(userId)) {
            throw new IllegalStateException(
                    "Hold belongs to user '" + heldByUserId + "', cannot be released by '" + userId + "'");
        }
        return FreeState.INSTANCE;
    }

    public String getHeldByUserId() {
        return heldByUserId;
    }

    public Instant getExpiresAt() {
        return expiresAt;
    }

    @Override
    public String statusName() {
        return "HELD";
    }

    @Override
    public String toString() {
        return "HeldState[by=" + heldByUserId + ", expiresAt=" + expiresAt + "]";
    }
}
