from datetime import datetime
from app.bank.account import BankAccount


class BankStatement:
    @classmethod
    def register(cls, account: BankAccount, transaction: dict):
        account.transactions.append(transaction)

    @classmethod
    def query_by_field(cls, account: BankAccount, field: str, value: any):
        return next(
            (t for t in account.transactions if t.get('transaction', {}).get(field, '') == value), {}
        )

    @classmethod
    def query_by_date(
        cls,
        account: BankAccount,
        field: str,
        start_date: datetime,
        end_date: datetime
    ):
        for t in account.transactions:
            if start_date <= t.get('transaction', {}).get(field) < end_date:
                yield t
