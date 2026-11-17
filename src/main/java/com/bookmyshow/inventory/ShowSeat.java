package com.bookmyshow.inventory;

import com.bookmyshow.common.SeatId;

import java.time.Instant;
import java.util.Objects;
import java.util.concurrent.locks.ReentrantLock;

/**
 * U1-2 & U6: Represents a physical seat within the context of a specific Show.
 * Contains per-seat concurrency lock and current SeatState.
 */
public class ShowSeat {
    private final SeatId seatId;
    private final SeatCategory category;
    private final ReentrantLock lock = new ReentrantLock(true); // Fair lock for FIFO fairness
    private SeatState state;

    public ShowSeat(SeatId seatId, SeatCategory category) {
        this.seatId = Objects.requireNonNull(seatId, "seatId cannot be null");
        this.category = Objects.requireNonNull(category, "category cannot be null");
        this.state = FreeState.INSTANCE;
    }

    public SeatId getSeatId() {
        return seatId;
    }

    public SeatCategory getCategory() {
        return category;
    }

    public ReentrantLock getLock() {
        return lock;
    }

    public SeatState getState() {
        return state;
    }

    public boolean isAvailable(Instant now) {
        return state.isAvailable(now);
    }

    /**
     * Attempts to transition to HELD state. Caller MUST hold the seat's lock.
     */
    public boolean tryHold(String userId, Instant expiresAt, Instant now) {
        if (!lock.isHeldByCurrentThread()) {
            throw new IllegalStateException("Thread must hold the seat lock before mutating state");
        }
        if (state.isAvailable(now)) {
            this.state = state.hold(userId, expiresAt, now);
            return true;
        }
        return false;
    }

    /**
     * Transitions from HELD to SOLD state. Caller MUST hold the seat's lock.
     */
    public void confirm(String userId, Instant now) {
        if (!lock.isHeldByCurrentThread()) {
            throw new IllegalStateException("Thread must hold the seat lock before mutating state");
        }
        this.state = state.confirm(userId, now);
    }

    /**
     * Transitions from HELD back to FREE state. Caller MUST hold the seat's lock.
     */
    public void release(String userId) {
        if (!lock.isHeldByCurrentThread()) {
            throw new IllegalStateException("Thread must hold the seat lock before mutating state");
        }
        this.state = state.release(userId);
    }
}
