package com.bookmyshow.pricing;

import com.bookmyshow.common.Money;
import com.bookmyshow.inventory.SeatCategory;
import com.bookmyshow.inventory.Show;

/**
 * U4: Strategy Pattern for Dynamic Pricing.
 */
public interface PricingStrategy {
    String strategyName();
    Money calculatePrice(SeatCategory category, Show show, double occupancyRate);
}
