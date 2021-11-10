from app.auth.authorizer import Authorizer

import pytest


class TestAuthorizer:
    EVENTS = []
    VALIDATIONS = []

    @pytest.fixture
    def authorizer(self):
        return Authorizer(
            events=self.EVENTS,
            validations=self.VALIDATIONS
        )

    def test_process(self):
        pass

    def test_process_account_creation(self):
        ...

    def test_process_transaction(self):
        ...

    def test_process_unknown(self):
        ...

    def test_apply_validations(self):
        ...
