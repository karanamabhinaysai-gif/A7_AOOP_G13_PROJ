package com.bookmyshow.booking;

import com.bookmyshow.common.Money;
import com.bookmyshow.common.SeatId;
import com.bookmyshow.inventory.SeatCategory;

import java.util.Objects;

/**
 * U4: Decorator Pattern - Concrete Component representing a reserved Seat.
 */
public class SeatTicketItem implements BookingItem {
    private final SeatId seatId;
    private final SeatCategory category;
    private final Money price;

    public SeatTicketItem(SeatId seatId, SeatCategory category, Money price) {
        this.seatId = Objects.requireNonNull(seatId, "seatId cannot be null");
        this.category = Objects.requireNonNull(category, "category cannot be null");
        this.price = Objects.requireNonNull(price, "price cannot be null");
    }

    public SeatId getSeatId() {
        return seatId;
    }

    public SeatCategory getCategory() {
        return category;
    }

    @Override
    public String getDescription() {
        return "Seat " + seatId + " [" + category.name() + "]";
    }

    @Override
    public Money getCost() {
        return price;
    }

    @Override
    public String toString() {
        return getDescription() + " - " + getCost();
    }
}
