from abc import ABC, abstractmethod

from app.bank.account import BankAccount


class BaseValidation(ABC):
    """
    An abstract class to represent the a transaction validator to be used on Authorizer.
    To implement custom validations, just implement this class. The 'validate' method is the responsible for return the
    final value of validation. Feel free to add others methods to the class.
    """
    @abstractmethod
    def validate(self, account: BankAccount, transaction: dict) -> str:
        """
        Validate a single transaction based on rules defined here.

        Args:
            account: An 'BankAccount' object that represents an account bank where the transaction will be validated. Can't be None or empty.
            transaction: A dict with the transaction to be validated

        Returns:

        """
        raise NotImplementedError
