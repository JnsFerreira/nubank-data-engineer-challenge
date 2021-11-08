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
        events: Iterable[dict],
        validations: Iterable[BaseValidation]
    ):
        """
        Constructor method for Authorizer class

        Args:
            events (Iterable[dict]): An iterable object of dictionaries, where dicts are the events to be validated
            validations (Iterable[BaseValidation]): An iterable object of 'BaseValidation',
            that will be used to validate the transactions contained on 'events' parameter
        """
        self.events = events
        self.validations = validations
        self.account = None

    def process(self) -> None:
        """
        Starts the validations for all transactions.

        Returns:
            None
        """
        for event in self.events:
            # Gets event type metadata
            event_type = event.get('event_type', 'unknown')

            # Apply verifications based on event type
            process_method = getattr(self, f"process_{event_type}")
            response = process_method(event=event)

            # Write event to stdout
            sys.stdout.write(json.dumps(response, default=str, indent=4, sort_keys=True))

    def process_account_creation(self, event: dict) -> dict:
        """
        Process events related to account creation. Creates a new account instance if it wasn't created yet.
        If account already been created, return 'account-already-initialized' violation

        Args:
            event (dict): Event with information related to account creation.

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
        Process events related to account transactions. Creates a new key value pair at event containing,
        if founded, any violations based on predefined validations.

        Args:
            event (dict): Event with information related to an account transaction

        Returns:
            event (dict): The original event with possible founded violations.
            If wasn't founded any violation, violations field will be an empty list.
        """
        # Checks if account exists
        if not self.account:
            event.update({'violations': ['account-not-initialized']})

        else:
            violations = self.apply_validations(transaction=event)
            event.update({'violations': [v for v in violations]})

        return event

    def process_unknown(self, event: dict) -> dict:
        """
        Process unknown events. Just add 'unknown-error' to violation field

        Args:
            event (dict): Event that wasn't in any expected type, like 'account_creation' or 'transaction'

        Returns:
            event (dict): The original event with violations field
        """
        event.update({'violations': ['unknown-error']})

        return event

    def apply_validations(self, transaction: dict) -> Generator[str]:
        """
        Apply validations specified on constructor to a single transaction.

        Args:
            transaction (dict): An transaction of type 'transaction' to be validated

        Yield:
            violation (dict): Violation founded on validator
        """
        # Apply validations
        for validator in self.validations:
            violation = validator().validate(
                account=self.account,
                transaction=transaction
            )

            # If violations was founded, returns yields the violation
            if violation:
                yield violation

            # When no violations was founded, register the transaction to account
            else:
                BankStatement.register(
                    account=self.account,
                    transaction=transaction
                )
