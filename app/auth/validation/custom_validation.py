# Built-in libraries
from datetime import datetime, timedelta

# Project libraries
from app.bank.account import BankAccount
from app.bank.transactions import BankStatement
from app.auth.validation.base_validation import BaseValidation


# TODO: CHECK BUSINESS RULES
class CardNotActiveValidation(BaseValidation):
    """
    Validation to founded transactions where card isn't active on account.

    Given an account with the card inactive ( active-card: false ) when any transaction operation is
    submitted, the Authorizer must reject the operation and return the violation card-not-active.

    #Input
    {"account": {"active-card": false, "available-limit": 100}}
    {"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T11:00:00.000Z"}}

    # Output
     {"account": {"active-card": false, "available-limit": 100}, "violations": []}
     {"account": {"active-card": false, "available-limit": 100}, "violations": ["card-not-active"]}
    """
    def validate(self, account: BankAccount, transaction: dict) -> str:
        if not account.active_card:
            return 'card-not-active'
        return ''


class InsufficientLimitValidation(BaseValidation):
    """
    Validation to found transactions where account limit is insufficient

    Given an account with active card ( active-card: true ) and available limit of 1000 ( available-limit: 1000 ),
    for any transaction operation with the amount attribute above the threshold value of 1000 o
    Authorizer must reject the operation and return the insufficient-limit violation.

    # Input
    {"account": {"active-card": true, "available-limit": 1000}}
    {"transaction": {"merchant": "Vivara", "amount": 1250, "time": "2019-02-13T11:00:00.000Z"}}

    # Output
    {"account": {"active-card": true,"available-limit": 1000}, "violations": []}
    {"account": {"active-card": true,"available-limit": 1000}, "violations": ["insufficient-limit"]}
    """
    def validate(self, account: BankAccount, transaction: dict) -> str:
        transaction_amount = transaction.get('transaction', {}).get('amount')

        if account.available_limit < transaction_amount and account.active_card:
            return 'insufficient-limit'
        return ''


class HighFreqSmallIntervalValidation(BaseValidation):
    """
    Validation to detect a high volume of transactions in a small interval.

    Given an account with an active card ( active-card: true ), available limit of 100
    ( available-limit: 100 ) and 3 transactions successfully occurred in the last 2 minutes.
    The Authorizer must reject the new transaction operation and return the high-frequency-small-interval violation

    # Input
    {"account": {"active-card": true, "available-limit": 100}}
    {"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T11:00:00.000Z"}}
    {"transaction": {"merchant": "Habbib's", "amount": 20, "time": "2019-02-13T11:00:01.000Z"}}
    {"transaction": {"merchant": "McDonald's", "amount": 20, "time": "2019-02-13T11:01:01.000Z"}}
    {"transaction": {"merchant": "Subway", "amount": 20, "time": "2019-02- 13T11:01:31.000Z"}}
    {"transaction": {"merchant": "Burger King", "amount": 10, "time": "2019-02-13T12:00:00.000Z"}}

    # Output
    {"account": {"active-card": true, "available-limit": 100}, "violations": []}
    {"account": {"active-card": true, "available-limit": 80}, "violations": []}
    {"account": {"active-card": true, "available-limit": 60}, "violations": []}
    {"account": {"active-card": true, "available-limit": 40}, "violations": []}
    {"account": {"active-card": true, "available-limit": 40}, "violations": ["highfrequency-small-interval"]}
    {"account": {"active-card": true, "available-limit": 30}, "violations": []}
    """
    def validate(self, account: BankAccount, transaction: dict) -> str:
        end_time = transaction.get('transaction', {}).get('time')
        start_time = end_time - timedelta(minutes=2)

        transactions = BankStatement.query_by_date(
            account=account,
            field='time',
            start_date=start_time,
            end_date=end_time
        )

        if len(list(transactions)) >= 3:
            return 'high-frequency-small-interval'

        return ''


class DoubledTransaction(BaseValidation):
    """
    Validation to detected double transaction, known as financial chargeback.

    Given an account with an active card ( active-card: true ), available limit of 100
    ( available-limit: 100 ) and some successful transactions in the last 2 minutes. The Authorizer must reject the
    new transaction operation if it shares the same amount and commercially (merchant)
    with any of the previously accepted transactions and return the doubled-transaction violation

    # Input
    {"account": {"active-card": true, "available-limit": 100}}
    {"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T11:00:00.000Z"}}
    {"transaction": {"merchant": "McDonald's", "amount": 10, "time": "2019-02-13T11:00:01.000Z"}}
    {"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T11:00:02.000Z"}}
    {"transaction": {"merchant": "Burger King", "amount": 15, "time": "2019-02-13T11:00:03.000Z"}}
    # Output
    {"account": {"active-card": true, "available-limit": 100}, "violations": []}
    {"account": {"active-card": true, "available-limit": 80}, "violations": []}
    {"account": {"active-card": true, "available-limit": 70}, "violations": []}
    {"account": {"active-card": true, "available-limit": 70}, "violations": ["doubled-transaction"]}
    {"account": {"active-card": true, "available-limit": 55}, "violations": []}
    """
    def validate(self, account: BankAccount, transaction: dict) -> str:
        transaction_info = transaction.get('transaction', {})
        end_time = transaction_info.get('time')
        start_time = end_time - timedelta(minutes=2)

        transactions = BankStatement.query_by_date(
            account=account,
            field='time',
            start_date=start_time,
            end_date=end_time
        )

        amount = transaction_info.get('amount', '')
        merchant = transaction_info.get('merchant', '')

        for t in transactions:
            t_info = t.get('transaction', {})
            past_transaction_amount = t_info.get('amount', '')
            past_transaction_merchant = t_info.get('merchant', '')

            if (past_transaction_merchant == merchant) and \
                    (past_transaction_amount == amount):
                return 'doubled-transaction'

        return ''
