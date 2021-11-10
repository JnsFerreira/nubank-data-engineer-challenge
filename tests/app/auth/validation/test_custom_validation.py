import pytest

from app.bank.account import BankAccount
from app.auth.validation.custom_validation import *


class TestCardNotActiveValidation:
    INPUT = [
        {"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T11:00:00.000Z"}},
        {"transaction": {"merchant": "Habbib's", "amount": 15, "time": "2019-02-13T11:15: 00.000Z"}}
    ]
    NORMAL_OUTPUT = ['', '']
    VIOLATION_OUTPUT = ['card-not-active', 'card-not-active']

    @pytest.fixture
    def validator(self):
        return CardNotActiveValidation()

    @pytest.fixture
    def account_with_not_active_card(self):
        return BankAccount(
            active_card=False,
            available_limit=100
        )

    @pytest.fixture
    def account_with_active_card(self):
        return BankAccount(
            active_card=True,
            available_limit=100
        )

    @pytest.mark.parametrize('transaction, output_violation', zip(INPUT, VIOLATION_OUTPUT))
    def test_validation_violation_founded(
        self,
        validator,
        account_with_not_active_card,
        transaction,
        output_violation

    ):
        violation = validator.validate(
            account=account_with_not_active_card,
            transaction=transaction
        )

        assert violation == output_violation

    @pytest.mark.parametrize('transaction, output_violation', zip(INPUT, NORMAL_OUTPUT))
    def test_validation_no_violation_founded(
            self,
            validator,
            account_with_active_card,
            transaction,
            output_violation
    ):
        violation = validator.validate(
            account=account_with_active_card,
            transaction=transaction
        )

        assert violation == output_violation


class TestInsufficientLimitValidation:
    INPUT = [
        {"transaction": {"merchant": "Vivara", "amount": 1250, "time": "2019-02-13T11:00: 00.000Z"}},
        {"transaction": {"merchant": "Samsung", "amount": 2500, "time": "2019-02-13T11: 00:01.000Z"}},
        {"transaction": {"merchant": "Nike", "amount": 800, "time": "2019-02-13T11: 01:01.000Z"}}
    ]

    OUTPUT = ["insufficient-limit", "insufficient-limit", '']

    @pytest.fixture
    def validator(self):
        return InsufficientLimitValidation()

    @pytest.fixture
    def account(self):
        return BankAccount(
            active_card=True,
            available_limit=1000
        )

    @pytest.mark.parametrize('transaction, output_violation', zip(INPUT, OUTPUT))
    def test_validation(self, validator, account, transaction, output_violation):
        violation = validator.validate(
            account=account,
            transaction=transaction
        )

        assert violation == output_violation


class TestHighFreqSmallIntervalValidation:
    INPUT = [
        {"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T11:00:00.000Z"}},
        {"transaction": {"merchant": "Habbib's", "amount": 20, "time": "2019-02-13T11:00:01.000Z"}},
        {"transaction": {"merchant": "McDonald's", "amount": 20, "time": "2019-02-13T11:01:01.000Z"}},
        {"transaction": {"merchant": "Subway", "amount": 20, "time": "2019-02-13T11:01:31.000Z"}},
        {"transaction": {"merchant": "Burger King", "amount": 10, "time": "2019-02-13T12:00:00.000Z"}},
    ]

    OUTPUT = ['', '', '', 'high-frequency-small-interval', '']

    @pytest.fixture
    def validator(self):
        return HighFreqSmallIntervalValidation()

    @pytest.fixture
    def account(self):
        return BankAccount(
            active_card=True,
            available_limit=100
        )

    @pytest.mark.parametrize('transaction, output_violation', zip(INPUT, OUTPUT))
    def test_validation(
            self,
            validator,
            account,
            transaction,
            output_violation
    ):
        transaction_info = transaction.get('transaction', {})
        transaction_info.update(
            {'time': datetime.strptime(transaction_info.get('time', ''), '%Y-%m-%dT%H:%M:%S.%fZ')}
        )

        violation = validator.validate(
            account=account,
            transaction=transaction
        )

        assert violation == output_violation


class TestDoubledTransaction:
    INPUT = [
        {"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T11:00:00.000Z"}},
        {"transaction": {"merchant": "McDonald's", "amount": 10, "time": "2019-02-13T11:00:01.000Z"}},
        {"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T11:00:02.000Z"}},
        {"transaction": {"merchant": "Burger King", "amount": 15, "time": "2019-02-13T11:00:03.000Z"}},
    ]
    OUTPUT = ['', '', 'doubled-transaction', ''],

    @pytest.fixture
    def validator(self):
        return DoubledTransaction()

    @pytest.fixture
    def account(self):
        return BankAccount(
            active_card=True,
            available_limit=100
        )

    @pytest.mark.parametrize('transaction, output_violation', zip(INPUT, OUTPUT))
    def test_validation(
            self,
            validator,
            account,
            transaction,
            output_violation
    ):
        transaction_info = transaction.get('transaction', {})
        transaction_info.update(
            {'time': datetime.strptime(transaction_info.get('time', ''), '%Y-%m-%dT%H:%M:%S.%fZ')}
        )

        violation = validator.validate(
            account=account,
            transaction=transaction
        )

        assert violation == output_violation
