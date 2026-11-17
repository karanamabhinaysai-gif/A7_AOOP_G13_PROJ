package com.bookmyshow.payments;

import java.time.Instant;

/**
 * U7: Payments Context - Outcome of payment attempt
 */
public record PaymentResult(
        boolean successful,
        String transactionId,
        String failureReason,
        Instant processedAt
) {
    public static PaymentResult success(String txId) {
        return new PaymentResult(true, txId, null, Instant.now());
    }

    public static PaymentResult failure(String reason) {
        return new PaymentResult(false, null, reason, Instant.now());
    }
}
