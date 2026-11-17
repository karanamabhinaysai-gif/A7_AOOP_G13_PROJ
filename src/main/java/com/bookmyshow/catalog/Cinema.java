package com.bookmyshow.catalog;

import java.util.Collections;
import java.util.List;
import java.util.Objects;

/**
 * U7: Catalog Context - Cinema / Theatre
 */
public record Cinema(
        String cinemaId,
        String name,
        String city,
        List<Screen> screens
) {
    public Cinema(String cinemaId, String name, String city, List<Screen> screens) {
        this.cinemaId = Objects.requireNonNull(cinemaId, "cinemaId cannot be null");
        this.name = Objects.requireNonNull(name, "name cannot be null");
        this.city = Objects.requireNonNull(city, "city cannot be null");
        this.screens = Collections.unmodifiableList(Objects.requireNonNull(screens, "screens cannot be null"));
    }
}
