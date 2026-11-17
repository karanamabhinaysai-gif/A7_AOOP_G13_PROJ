package com.bookmyshow.pricing;

import com.bookmyshow.common.Money;
import com.bookmyshow.inventory.SeatCategory;
import com.bookmyshow.inventory.Show;

/**
 * U4: Strategy Pattern - Demand-Based Surge Pricing (for blockbuster first-day rush)
 */
public class DemandSurgePricingStrategy implements PricingStrategy {
    @Override
    public String strategyName() {
        return "DEMAND_SURGE";
    }

    @Override
    public Money calculatePrice(SeatCategory category, Show show, double occupancyRate) {
        double multiplier = 1.0;
        if (occupancyRate >= 0.80) {
            multiplier = 1.50; // 50% surge when occupancy >= 80%
        } else if (occupancyRate >= 0.50) {
            multiplier = 1.25; // 25% surge when occupancy >= 50%
        } else if (occupancyRate >= 0.25) {
            multiplier = 1.10; // 10% surge when occupancy >= 25%
        }
        return category.basePrice().multiply(multiplier);
    }
}
