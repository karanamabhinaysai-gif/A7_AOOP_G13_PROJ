package com.bookmyshow.booking;

import com.bookmyshow.common.SeatId;
import com.bookmyshow.common.ShowId;

import java.time.Instant;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

/**
 * U3: Proof of successful seat hold with strict expiry postcondition.
 */
public record HoldToken(
        String holdId,
        ShowId showId,
        List<SeatId> seats,
        String userId,
        Instant expiresAt
) {
    public HoldToken(String holdId, ShowId showId, List<SeatId> seats, String userId, Instant expiresAt) {
        this.holdId = Objects.requireNonNull(holdId, "holdId cannot be null");
        this.showId = Objects.requireNonNull(showId, "showId cannot be null");
        this.seats = Collections.unmodifiableList(Objects.requireNonNull(seats, "seats cannot be null"));
        this.userId = Objects.requireNonNull(userId, "userId cannot be null");
        this.expiresAt = Objects.requireNonNull(expiresAt, "expiresAt cannot be null");
    }

    public boolean isExpired(Instant now) {
        return now.isAfter(expiresAt);
    }
}
