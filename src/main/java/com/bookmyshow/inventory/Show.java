package com.bookmyshow.inventory;

import com.bookmyshow.catalog.Movie;
import com.bookmyshow.catalog.Screen;
import com.bookmyshow.common.ShowId;

import java.time.Instant;
import java.util.Objects;

/**
 * U7: Show Inventory Context - An instance of a Movie screened at a specific time and screen.
 */
public record Show(
        ShowId showId,
        Movie movie,
        Screen screen,
        Instant startTime,
        Instant endTime
) {
    public Show {
        Objects.requireNonNull(showId, "showId cannot be null");
        Objects.requireNonNull(movie, "movie cannot be null");
        Objects.requireNonNull(screen, "screen cannot be null");
        Objects.requireNonNull(startTime, "startTime cannot be null");
        Objects.requireNonNull(endTime, "endTime cannot be null");
        if (!endTime.isAfter(startTime)) {
            throw new IllegalArgumentException("Show endTime must be after startTime");
        }
    }
}
