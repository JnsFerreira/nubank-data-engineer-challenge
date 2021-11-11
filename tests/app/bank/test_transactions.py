# Built-in libraries
from datetime import datetime

# Project libraries
from app.bank.account import BankAccount
from app.bank.transactions import BankStatement

# External libraries
import pytest


class TestTransactions:

    @pytest.fixture
    def bank_account(self):
        return BankAccount(
            available_limit=10000,
            active_card=True
        )

    @pytest.fixture
    def bank_statement(self):
        return BankStatement()

    def test_register_transaction(self, bank_account, bank_statement):
        qty_of_transactions = len(bank_account.transactions)

        bank_statement.register(
            account=bank_account,
            transaction={"transaction": {"merchant": "Uber Eats", "amount": 25, "time": "2020-12-01T11:07:00.000Z"}, 'event_type': 'transaction'}
        )

        assert len(bank_account.transactions) == (qty_of_transactions + 1)

    def test_query_by_field(self, bank_account, bank_statement):
        bank_statement.register(
            account=bank_account,
            transaction={"transaction": {"merchant": "Uber Eats", "amount": 30, "time": "2020-12-01T11:07:00.000Z"}, 'event_type': 'transaction'}
        )

        query_result = bank_statement.query_by_field(
            account=bank_account,
            field='amount',
            value=30
        )

        assert len(list(query_result)) == 1

    def test_query_by_date(self, bank_account, bank_statement):
        bank_statement.register(
            account=bank_account,
            transaction={"transaction": {"merchant": "Uber Eats", "amount": 30, "time": datetime(2021, 10, 10)},
                         'event_type': 'transaction'}
        )

        query_result = bank_statement.query_by_date(
            account=bank_account,
            field='time',
            start_date=datetime(2021, 10, 9),
            end_date=datetime(2021, 10, 11)
        )

        assert len(list(query_result)) == 1
