import pytest

from app.bank.account import BankAccount


class TestBankAccount:
    @pytest.fixture(autouse=True)
    def account(self):
        return BankAccount(
            active_card=True,
            available_limit=1000
        )

    def test_available_limit_getter(self, account):
        assert account.available_limit == 1000

    def test_available_limit_setter_raise_type_error(self, account):
        with pytest.raises(TypeError):
            account.available_limit = '123'

    def test_available_limit_setter_normal_value(self, account):
        account.available_limit = 123

        assert account.available_limit == 123

    def test_active_card_getter(self, account):
        assert account.active_card

    def test_active_card_setter_raise_type_error(self, account):
        with pytest.raises(TypeError):
            account.active_card = 'true'

    def test_active_card_setter_normal_value(self, account):
        account.active_card = False

        assert not account.active_card

    def test_transactions_getter(self, account):
        assert account.transactions == []

    def test_transactions_setter_raise_type_error(self, account):
        with pytest.raises(TypeError):
            account.transactions = 10

    def test_transactions_setter_normal_value(self, account):
        account.transactions = [{'transaction': {'some': 'value'}}]

        assert len(account.transactions) == 1

    def test_account_to_dict_normal_condition(self, account):
        expected_value = {
            "account": {
                "active-card": True,
                "available-limit": 1000
            }
        }

        account_dict = account.to_dict()

        assert account_dict == expected_value
