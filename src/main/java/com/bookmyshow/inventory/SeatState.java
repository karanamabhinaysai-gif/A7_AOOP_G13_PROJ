package com.bookmyshow.inventory;

import java.time.Instant;

/**
 * U4: State Pattern for Seat Lifecycle.
 * Valid states: Free, Held, Sold.
 */
public interface SeatState {
    boolean isAvailable(Instant now);
    SeatState hold(String userId, Instant expiresAt, Instant now);
    SeatState confirm(String userId, Instant now);
    SeatState release(String userId);
    String statusName();
}
