package com.bookmyshow.inventory;

import com.bookmyshow.common.Money;

public record PlatinumSeat(Money basePrice) implements SeatCategory {
    public PlatinumSeat() {
        this(new Money(400.00));
    }

    @Override
    public String name() {
        return "PLATINUM";
    }

    @Override
    public String description() {
        return "Elite VIP seating with premier viewing angle";
    }
}
