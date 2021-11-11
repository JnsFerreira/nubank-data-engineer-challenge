# Built-in libraries
from typing import Generator
from datetime import datetime

# Project libraries
from app.bank.account import BankAccount


class BankStatement:
    """An helper class to register and read transactions from an 'BankAccount'"""
    @classmethod
    def register(cls, account: BankAccount, transaction: dict) -> None:
        """
        Register a transaction to an 'BankAccount'

        Args:
            account (dict): Account where transactions will be registered
            transaction (dict): A transaction to be registered at account

        Returns:
            None
        """
        try:
            # Debit the amount from the available limit
            transaction_amount = transaction.get('transaction', {}).get('amount', 0)
            account.available_limit -= transaction_amount


            # Register the transaction
            account.transactions.append(transaction)

        except Exception as e:
            # TODO: Maybe add an custom exception
            raise Exception(f"Could not registry transaction. Details: {e}")

    @classmethod
    def query_by_field(cls, account: BankAccount, field: str, value: any) -> Generator[dict, None, None]:
        """
        Query transactions on a bank account based on key: value pair

        Args:
            account (BankAccount): Account where transactions will be searched
            field (str): Field to search for value
            value (any): Value to be searched for

       Yield:
            t (dict): Transactions that meet the criteria
        """
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
    ) -> Generator[dict, None, None]:
        """
        Query transactions from a bank account based on a time interval.
        Will me yielded transactions where que date field is gather or equals to start_date and lower than end_date.

        Expression: start_date <= field < end_date

        Args:
            account (BankAccount): Account where transactions will be searched
            field (str): Date field to be compared. Data type of field must be a python datetime.
            start_date (datetime): Start date to search for
            end_date (datetime):  End date to search for

        Yield:
            t (dict): Transactions that meet the criteria
        """

        for t in account.transactions:
            if start_date <= t.get('transaction', {}).get(field) < end_date:
                yield t
