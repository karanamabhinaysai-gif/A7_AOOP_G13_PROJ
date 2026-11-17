package com.bookmyshow.booking;

import com.bookmyshow.common.Money;

/**
 * U4: Decorator Pattern - Adds Mexican Cheese Nachos combo.
 */
public class NachosDecorator extends BookingItemDecorator {
    private static final Money NACHOS_PRICE = new Money(220.00);

    public NachosDecorator(BookingItem decoratedItem) {
        super(decoratedItem);
    }

    @Override
    public String getDescription() {
        return decoratedItem.getDescription() + " + Mexican Salsa & Cheese Nachos";
    }

    @Override
    public Money getCost() {
        return decoratedItem.getCost().add(NACHOS_PRICE);
    }
}
