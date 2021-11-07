from app.bank.account import BankAccount
from app.auth.validation.base_validation import BaseValidation


class CardNotActiveValidation(BaseValidation):
    def validate(self, account: BankAccount, transaction: dict) -> str:
        if not account.active_card:
            return 'card-not-active'
        return ''


class InsufficientLimitValidation(BaseValidation):
    def validate(self, account: BankAccount, transaction: dict) -> str:
        transaction_amount = transaction.get('transaction', {}).get('amount')

        if account.available_limit < transaction_amount:
            return 'insufficient-limit'
        return ''


class HighFreqSmallIntervalValidation(BaseValidation):
    def validate(self, account: BankAccount, transaction: dict) -> str:
        return ''


class DoubleTransaction(BaseValidation):
    def validate(self, account: BankAccount, transaction: dict) -> str:
        return ''
