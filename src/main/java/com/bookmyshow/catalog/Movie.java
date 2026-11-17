package com.bookmyshow.catalog;

import java.time.Duration;
import java.util.Objects;

/**
 * U7: Catalog Context - Movie Entity
 */
public record Movie(
        String movieId,
        String title,
        String language,
        String genre,
        Duration duration,
        String certificateRating
) {
    public Movie {
        Objects.requireNonNull(movieId, "movieId cannot be null");
        Objects.requireNonNull(title, "title cannot be null");
    }
}
