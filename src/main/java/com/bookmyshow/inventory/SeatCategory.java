package com.bookmyshow.inventory;

import com.bookmyshow.common.Money;

/**
 * U3: Sealed hierarchy for SeatCategory.
 * Permits only explicitly defined seat tiers with their standard attributes and pricing.
 */
public sealed interface SeatCategory permits SilverSeat, GoldSeat, PlatinumSeat, ReclinerSeat {
    String name();
    Money basePrice();
    String description();
}
