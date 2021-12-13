# Built-in libraries
from io import StringIO

# Project libraries
from app.parse.io import parse_input_events

# External libraries
import pytest


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

    EMPTY_EVENTS = []

    @pytest.mark.parametrize('event', ACCOUNT_EVENTS)
    def test_parse_account_events(self, monkeypatch, event):
        monkeypatch.setattr('sys.stdin', StringIO(event))

        for parsed_event in parse_input_events():
            assert parsed_event.get('event_type') == 'account_creation'

    @pytest.mark.parametrize('event', TRANSACTION_EVENTS)
    def test_parse_transaction_events(self, monkeypatch, event):
        monkeypatch.setattr('sys.stdin', StringIO(event))

        for parsed_event in parse_input_events():
            assert parsed_event.get('event_type') == 'transaction'

    @pytest.mark.parametrize('event', UNKNOWN_EVENTS)
    def test_parse_unknown_events(self, monkeypatch, event):
        monkeypatch.setattr('sys.stdin', StringIO(event))

        for parsed_event in parse_input_events():
            assert parsed_event.get('event_type') == 'unknown'

    @pytest.mark.parametrize('event', EMPTY_EVENTS)
    def parse_empty_events(self, monkeypatch, event):
        monkeypatch.setattr('sys.stdin', StringIO(event))

        for parsed_event in parse_input_events():
            assert parsed_event.get('event_type', '') == ''
