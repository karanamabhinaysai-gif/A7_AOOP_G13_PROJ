package com.bookmyshow.common;

/**
 * U3: Thrown when a method precondition, postcondition, or class invariant fails.
 */
public class ContractViolationException extends DomainException {
    public ContractViolationException(String message) {
        super(message);
    }
}
