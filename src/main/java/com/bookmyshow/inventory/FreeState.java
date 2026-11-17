package com.bookmyshow.inventory;

import java.time.Instant;

/**
 * U4: State Pattern - Free (Available) State
 */
public final class FreeState implements SeatState {
    public static final FreeState INSTANCE = new FreeState();

    private FreeState() {}

    @Override
    public boolean isAvailable(Instant now) {
        return true;
    }

    @Override
    public SeatState hold(String userId, Instant expiresAt, Instant now) {
        return new HeldState(userId, expiresAt);
    }

    @Override
    public SeatState confirm(String userId, Instant now) {
        throw new IllegalStateException("Cannot confirm a seat that is in Free state (must be held first)");
    }

    @Override
    public SeatState release(String userId) {
        return this; // No-op if already free
    }

    @Override
    public String statusName() {
        return "FREE";
    }

    @Override
    public String toString() {
        return "FreeState";
    }
}
