from abc import ABC, abstractmethod

from app.bank.account import BankAccount


class BaseValidation(ABC):
    @abstractmethod
    def validate(self, account: BankAccount, transaction: dict) -> str:
        raise NotImplementedError
