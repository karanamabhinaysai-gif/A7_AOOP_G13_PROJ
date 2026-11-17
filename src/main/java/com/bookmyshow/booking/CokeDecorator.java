package com.bookmyshow.booking;

import com.bookmyshow.common.Money;

/**
 * U4: Decorator Pattern - Adds a Large Chilled Beverage.
 */
public class CokeDecorator extends BookingItemDecorator {
    private static final Money COKE_PRICE = new Money(150.00);

    public CokeDecorator(BookingItem decoratedItem) {
        super(decoratedItem);
    }

    @Override
    public String getDescription() {
        return decoratedItem.getDescription() + " + Large Chilled Coke";
    }

    @Override
    public Money getCost() {
        return decoratedItem.getCost().add(COKE_PRICE);
    }
}
