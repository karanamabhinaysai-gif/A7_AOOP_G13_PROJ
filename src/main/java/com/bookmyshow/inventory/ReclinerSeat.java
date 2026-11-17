package com.bookmyshow.inventory;

import com.bookmyshow.common.Money;

public record ReclinerSeat(Money basePrice) implements SeatCategory {
    public ReclinerSeat() {
        this(new Money(550.00));
    }

    @Override
    public String name() {
        return "RECLINER";
    }

    @Override
    public String description() {
        return "Luxury motorized plush recliner with in-seat service";
    }
}
