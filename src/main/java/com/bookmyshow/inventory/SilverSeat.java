package com.bookmyshow.inventory;

import com.bookmyshow.common.Money;

public record SilverSeat(Money basePrice) implements SeatCategory {
    public SilverSeat() {
        this(new Money(150.00));
    }

    @Override
    public String name() {
        return "SILVER";
    }

    @Override
    public String description() {
        return "Standard comfortable cinema seating";
    }
}
