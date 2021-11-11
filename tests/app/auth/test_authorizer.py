# Project libraries
from app.auth.authorizer import Authorizer
from app.auth.validation.custom_validation import *

# External libraries
import pytest


class TestAuthorizer:
    ALL_VALIDATIONS = [
        CardNotActiveValidation,
        InsufficientLimitValidation,
        HighFreqSmallIntervalValidation,
        DoubledTransaction
    ]

    ACCOUNT_EVENTS = [
        {"account": {"active-card": False, "available-limit": 750}, 'event_type': 'account_creation'},
        {"account": {"active-card": True, "available-limit": 1000}, 'event_type': 'account_creation'}
    ]

    ACCOUNT_OUTPUTS = [
        {"account": {"active-card": False, "available-limit": 750}, "violations": []},
        {"account": {"active-card": True, "available-limit": 1000}, "violations": []}
    ]

    UNKNOWN_EVENTS = [
        {'some_event': {'key': 'value'}, 'event_type': 'unknown'},
        {'some_event2': {'key': 'value'}, 'event_type': 'unknown'}
    ]

    def authorizer(self, events, validations):
        return Authorizer(
            events=events,
            validations=validations
        )

    @pytest.mark.parametrize('event, expected_output', zip(ACCOUNT_EVENTS, ACCOUNT_OUTPUTS))
    @pytest.mark.parametrize('validations', ALL_VALIDATIONS)
    def test_process_account_creation_new_account(self, event, expected_output, validations):
        auth = self.authorizer(
            events=[event],
            validations=validations
        )

        for processed_event in auth.process():
            assert processed_event == expected_output

    @pytest.mark.parametrize('event', ACCOUNT_EVENTS)
    @pytest.mark.parametrize('validations', ALL_VALIDATIONS)
    def test_process_account_creation_account_already_initialized(self, event, validations):
        new_account = {"account": {"active-card": True, "available-limit": 130}, 'event_type': 'account_creation'}

        auth = self.authorizer(
            events=[event, new_account],
            validations=validations
        )

        expected_output = [[], ["account-already-initialized"]]

        for processed_event, output in zip(auth.process(), expected_output):
            assert processed_event.get('violations', []) == output

    def test_process_transaction(self):
        events = [
            {"transaction": {"merchant": "Uber Eats", "amount": 25, "time": "2020-12-01T11:07:00.000Z"}, 'event_type': 'transaction'},
            {"account": {"active-card": True, "available-limit": 225}, 'event_type': 'account_creation'},
            {"transaction": {"merchant": "Uber Eats", "amount": 25, "time": "2020-12-01T11: 07:00.000Z"}, 'event_type': 'transaction'}
        ]

        expected_output = [
            ['account-not-initialized'], [], []
        ]

        auth = self.authorizer(
            events=events,
            validations=[
                CardNotActiveValidation,
                InsufficientLimitValidation
            ]
        )

        for processed_event, output in zip(auth.process(), expected_output):
            assert processed_event.get('violations', []) == output

    @pytest.mark.parametrize('event', UNKNOWN_EVENTS)
    @pytest.mark.parametrize('validations', ALL_VALIDATIONS)
    def test_process_unknown(self, event, validations):
        auth = self.authorizer(
            events=[event],
            validations=validations
        )

        for processed_event in auth.process():
            assert processed_event.get('violations', []) == ['unknown-error']

    def test_apply_validations(self):
        auth = self.authorizer(
            events=[],
            validations=[
                CardNotActiveValidation
            ]
        )

        # Register account
        auth.account = BankAccount(
            active_card=False,
            available_limit=1000
        )

        event = {"transaction": {"merchant": "Uber Eats", "amount": 25, "time": "2020-12-01T11: 07:00.000Z"}, 'event_type': 'transaction'}
        violations = auth.apply_validations(transaction=event)

        assert violations == ['card-not-active']
