package com.bookmyshow.pricing;

import com.bookmyshow.common.Money;
import com.bookmyshow.inventory.SeatCategory;
import com.bookmyshow.inventory.Show;

/**
 * U4: Strategy Pattern - Standard Base Pricing
 */
public class StandardPricingStrategy implements PricingStrategy {
    @Override
    public String strategyName() {
        return "STANDARD";
    }

    @Override
    public Money calculatePrice(SeatCategory category, Show show, double occupancyRate) {
        return category.basePrice();
    }
}
