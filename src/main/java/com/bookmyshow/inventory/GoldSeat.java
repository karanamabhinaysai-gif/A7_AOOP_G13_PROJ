package com.bookmyshow.inventory;

import com.bookmyshow.common.Money;

public record GoldSeat(Money basePrice) implements SeatCategory {
    public GoldSeat() {
        this(new Money(250.00));
    }

    @Override
    public String name() {
        return "GOLD";
    }

    @Override
    public String description() {
        return "Premium seating with extra legroom";
    }
}
