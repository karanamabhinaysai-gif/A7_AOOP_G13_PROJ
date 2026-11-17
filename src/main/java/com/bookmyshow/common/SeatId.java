package com.bookmyshow.common;

import java.util.Objects;

/**
 * U1-2: Strongly typed immutable Seat identifier.
 * Implements Comparable for canonical sorted ordering to prevent deadlocks in concurrent locking (U6).
 */
public record SeatId(String row, int number) implements Comparable<SeatId> {
    public SeatId {
        Objects.requireNonNull(row, "Seat row cannot be null");
        row = row.trim().toUpperCase();
        if (row.isEmpty()) {
            throw new IllegalArgumentException("Seat row cannot be empty");
        }
        if (number <= 0) {
            throw new IllegalArgumentException("Seat number must be strictly positive: " + number);
        }
    }

    @Override
    public int compareTo(SeatId other) {
        int rowComparison = this.row.compareTo(other.row);
        if (rowComparison != 0) {
            return rowComparison;
        }
        return Integer.compare(this.number, other.number);
    }

    @Override
    public String toString() {
        return row + number;
    }
}
