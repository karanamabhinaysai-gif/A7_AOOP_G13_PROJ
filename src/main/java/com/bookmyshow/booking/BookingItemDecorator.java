package com.bookmyshow.booking;

import java.util.Objects;

/**
 * U4: Decorator Pattern - Abstract Decorator base class.
 */
public abstract class BookingItemDecorator implements BookingItem {
    protected final BookingItem decoratedItem;

    public BookingItemDecorator(BookingItem decoratedItem) {
        this.decoratedItem = Objects.requireNonNull(decoratedItem, "decoratedItem cannot be null");
    }

    public BookingItem getDecoratedItem() {
        return decoratedItem;
    }
}
