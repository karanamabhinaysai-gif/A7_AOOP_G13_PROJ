package com.bookmyshow.booking;

import com.bookmyshow.common.Money;

/**
 * U4: Decorator Pattern - Component interface for bookable items (Seats and Add-on Combos).
 */
public interface BookingItem {
    String getDescription();
    Money getCost();
}
