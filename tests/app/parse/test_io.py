import pytest

from app.parse.io import parse_input_events


class TestParseInputEvents:
    TRANSACTION_EVENTS = [
        '{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}',
        '{"transaction": {"merchant": "Habbibs", "amount": 90, "time": "2019-02-13T11:00:00.000Z"}}',
        '{"transaction": {"merchant": "McDonalds", "amount": 30, "time": "2019-02-13T12:00:00.000Z"}}',
    ]

    ACCOUNT_EVENTS = [
        '{"account": {"active-card": true, "available-limit": 100}}',
        '{"account": {"active-card": false, "available-limit": 100}}'
    ]

    UNKNOWN_EVENTS = [
        '{"some_other_key": {"event": "info"}}',
        '{"random_key": {"another": "event"}}'
    ]

    def test_parse_account_events(self):
        pass

    def test_parse_transaction_events(self):
        pass

    def test_parse_unknown_events(self):
        pass

    def parse_empty_events(self):
        pass
