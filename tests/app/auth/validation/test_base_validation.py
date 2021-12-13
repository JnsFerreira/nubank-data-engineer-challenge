import pytest

from app.bank.account import BankAccount
from app.auth.validation.base_validation import BaseValidation


class ConcreteBaseValidation(BaseValidation):
    def validate(self, account: BankAccount, transaction: dict) -> str:
        return ''


class TestBaseValidation:
    @pytest.fixture
    def concrete_base_validation(self):
        return ConcreteBaseValidation()

    @pytest.fixture
    def account(self):
        return BankAccount(
            active_card=True,
            available_limit=100
        )

    def test_validation_dummy_implementation(self, concrete_base_validation, account):
        violation = concrete_base_validation.validate(
            account=account,
            transaction={"transaction": {}}
        )

        assert violation == ''

    def test_check_abstract_methods(self):
        assert BaseValidation.__abstractmethods__ == set(['validate'])
