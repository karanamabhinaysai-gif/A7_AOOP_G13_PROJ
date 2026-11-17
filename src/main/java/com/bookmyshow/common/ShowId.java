package com.bookmyshow.common;

import java.util.Objects;

/**
 * U1-2: Strongly typed identifier for a Movie Show.
 */
public record ShowId(String value) {
    public ShowId {
        Objects.requireNonNull(value, "ShowId cannot be null");
        if (value.trim().isEmpty()) {
            throw new IllegalArgumentException("ShowId cannot be blank");
        }
    }

    @Override
    public String toString() {
        return value;
    }
}
