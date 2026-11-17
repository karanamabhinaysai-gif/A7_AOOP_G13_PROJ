package com.bookmyshow.catalog;

import com.bookmyshow.common.SeatId;
import com.bookmyshow.inventory.SeatCategory;

import java.util.Collections;
import java.util.Map;
import java.util.Objects;

/**
 * U7: Catalog Context - Screen within a Cinema
 */
public record Screen(
        String screenId,
        String name,
        Map<SeatId, SeatCategory> layout
) {
    public Screen(String screenId, String name, Map<SeatId, SeatCategory> layout) {
        this.screenId = Objects.requireNonNull(screenId, "screenId cannot be null");
        this.name = Objects.requireNonNull(name, "name cannot be null");
        this.layout = Collections.unmodifiableMap(Objects.requireNonNull(layout, "layout cannot be null"));
    }

    public int totalSeats() {
        return layout.size();
    }
}
