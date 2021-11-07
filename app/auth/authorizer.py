# Built-in libraries
import sys
import json
from typing import Iterable, Generator

# Project libraries
from app.bank.account import BankAccount
from app.bank.transactions import BankStatement
from app.auth.validation.base_validation import BaseValidation


class Authorizer:
    """Authorizer class that performs validations for each transaction"""
    def __init__(
        self,
        events: Iterable,
        validations: Iterable[BaseValidation]
    ):
        """
        Constructor method for Authorizer class

        Args:
            events (Iterable):
            validations (Iterable[BaseValidation]):
        """
        self.events = events
        self.validations = validations
        self.account = None

    def process(self) -> None:
        """

        Returns:
            None
        """
        for event in self.events:
            # Gets event type metadata
            event_type = event.get('event_type', 'unknown')

            # Apply verifications based on event type
            process_method = getattr(self, f"process_{event_type}")
            response = process_method(event=event)

            # Update event dict
            event.update(response)

            # Write event to stdout
            sys.stdout.write(json.dumps(response, default=str, indent=4, sort_keys=True))

    def process_account_creation(self, event: dict) -> dict:
        """
        Process events related to account creation. Creates a new account instance if it wasn't created yet.
        If account already been created, return 'account-already-initialized' violation

        Args:
            event (dict): Event with information related to account.

        Returns:
            event (dict): An dictionary with updated information related to account creation and possible violations
        """
        if not self.account:
            account_info = event.get('account', {})

            self.account = BankAccount(
                available_limit=account_info.get('available-limit'),
                active_card=account_info.get('active-card')
            )

            event.update({'violations': []})

        else:
            event.update({'violations': ["account-already-initialized"]})

        return event

    def process_transaction(self, event: dict) -> dict:
        """

        Args:
            event:

        Returns:

        """
        if not self.account:
            return {'violations': ['account-not-initialized']}

        else:
            violations = self.apply_validations(transaction=event)
            return {'violations': [v for v in violations]}

    def process_unknown(self, event: dict) -> dict:
        """

        Args:
            event:

        Returns:

        """
        return {'violations': ['unknown-error']}

    def apply_validations(self, transaction: dict) -> Generator[str]:
        """

        Args:
            transaction:

        Returns:

        """
        for validator in self.validations:
            violation = validator().validate(
                account=self.account,
                transaction=transaction
            )

            if violation:
                yield violation
