package com.bookmyshow.booking;

import com.bookmyshow.common.Money;
import com.bookmyshow.common.SeatId;
import com.bookmyshow.common.ShowId;

import java.time.Instant;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

/**
 * U1-2 & U5: Issued Movie Ticket upon successful saga completion.
 */
public record Ticket(
        String bookingId,
        ShowId showId,
        String movieTitle,
        String cinemaName,
        String screenName,
        Instant showTime,
        List<SeatId> seats,
        List<String> itemsSummary,
        Money totalAmount,
        String customerId,
        Instant bookedAt
) {
    public Ticket {
        Objects.requireNonNull(bookingId, "bookingId cannot be null");
        Objects.requireNonNull(showId, "showId cannot be null");
        Objects.requireNonNull(movieTitle, "movieTitle cannot be null");
        seats = Collections.unmodifiableList(Objects.requireNonNull(seats, "seats cannot be null"));
        itemsSummary = Collections.unmodifiableList(Objects.requireNonNull(itemsSummary, "itemsSummary cannot be null"));
        Objects.requireNonNull(totalAmount, "totalAmount cannot be null");
        Objects.requireNonNull(customerId, "customerId cannot be null");
        Objects.requireNonNull(bookedAt, "bookedAt cannot be null");
    }
}
