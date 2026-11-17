package com.bookmyshow.booking;

import com.bookmyshow.common.Money;

/**
 * U4: Decorator Pattern - Adds a Tub of Caramel Popcorn to the ticket item.
 */
public class PopcornDecorator extends BookingItemDecorator {
    private static final Money POPCORN_PRICE = new Money(280.00);

    public PopcornDecorator(BookingItem decoratedItem) {
        super(decoratedItem);
    }

    @Override
    public String getDescription() {
        return decoratedItem.getDescription() + " + Jumbo Caramel Popcorn";
    }

    @Override
    public Money getCost() {
        return decoratedItem.getCost().add(POPCORN_PRICE);
    }
}
