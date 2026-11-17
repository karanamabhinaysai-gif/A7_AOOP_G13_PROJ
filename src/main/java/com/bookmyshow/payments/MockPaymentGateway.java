package com.bookmyshow.payments;

import com.bookmyshow.common.Money;

import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * U7: Payments Context - Mock implementation for testing and demo.
 */
public class MockPaymentGateway implements PaymentGateway {
    private final AtomicBoolean shouldFail = new AtomicBoolean(false);
    private long simulatedDelayMs = 0;

    public void setShouldFail(boolean fail) {
        this.shouldFail.set(fail);
    }

    public void setSimulatedDelayMs(long ms) {
        this.simulatedDelayMs = ms;
    }

    @Override
    public PaymentResult processPayment(String paymentReferenceId, String customerId, Money amount) {
        if (simulatedDelayMs > 0) {
            try {
                Thread.sleep(simulatedDelayMs);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return PaymentResult.failure("Payment processing was interrupted");
            }
        }

        if (shouldFail.get()) {
            return PaymentResult.failure("Insufficient funds / payment declined by bank");
        }

        return PaymentResult.success("TXN-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase());
    }
}
