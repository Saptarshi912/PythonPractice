from abc import ABC, abstractmethod

# Abstract Product: Defines the interface for payment processors
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

# Concrete Products: Different payment processors
class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing credit card payment of ${amount}")
        # Simulate credit card processing logic
        return True

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing PayPal payment of ${amount}")
        # Simulate PayPal processing logic
        return True

class CryptoProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing cryptocurrency payment of ${amount}")
        # Simulate crypto processing logic
        return True

# Factory: Creates the appropriate payment processor
class PaymentProcessorFactory:
    @staticmethod
    def get_payment_processor(payment_type: str) -> PaymentProcessor:
        if payment_type.lower() == "credit_card":
            return CreditCardProcessor()
        elif payment_type.lower() == "paypal":
            return PayPalProcessor()
        elif payment_type.lower() == "crypto":
            return CryptoProcessor()
        else:
            raise ValueError(f"Unknown payment type: {payment_type}")

# Client code: Uses the factory to process payments
def process_order(amount: float, payment_type: str):
    try:
        # Get the appropriate payment processor from the factory
        payment_processor = PaymentProcessorFactory.get_payment_processor(payment_type)
        # Process the payment
        if payment_processor.process_payment(amount):
            print("Payment successful!")
        else:
            print("Payment failed!")
    except ValueError as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    # Simulate different payment scenarios
    process_order(100.50, "credit_card")  # Output: Processing credit card payment of $100.5, Payment successful!
    process_order(50.25, "paypal")       # Output: Processing PayPal payment of $50.25, Payment successful!
    process_order(75.00, "crypto")       # Output: Processing cryptocurrency payment of $75.0, Payment successful!
    process_order(200.00, "bank")        # Output: Error: Unknown payment type: bank