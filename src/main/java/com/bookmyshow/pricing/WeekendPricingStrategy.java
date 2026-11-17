package com.bookmyshow.pricing;

import com.bookmyshow.common.Money;
import com.bookmyshow.inventory.SeatCategory;
import com.bookmyshow.inventory.Show;

import java.time.DayOfWeek;
import java.time.ZoneId;

/**
 * U4: Strategy Pattern - Weekend Surcharge Pricing
 */
public class WeekendPricingStrategy implements PricingStrategy {
    private final double weekendMultiplier;

    public WeekendPricingStrategy(double weekendMultiplier) {
        this.weekendMultiplier = weekendMultiplier;
    }

    public WeekendPricingStrategy() {
        this(1.25); // 25% premium for weekends
    }

    @Override
    public String strategyName() {
        return "WEEKEND_SURCHARGE";
    }

    @Override
    public Money calculatePrice(SeatCategory category, Show show, double occupancyRate) {
        DayOfWeek day = show.startTime().atZone(ZoneId.systemDefault()).getDayOfWeek();
        boolean isWeekend = (day == DayOfWeek.FRIDAY || day == DayOfWeek.SATURDAY || day == DayOfWeek.SUNDAY);
        return isWeekend ? category.basePrice().multiply(weekendMultiplier) : category.basePrice();
    }
}
