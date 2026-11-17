package com.bookmyshow.payments;

import com.bookmyshow.common.Money;

/**
 * U7: Payments Context - Gateway Interface
 */
public interface PaymentGateway {
    PaymentResult processPayment(String paymentReferenceId, String customerId, Money amount);
}
