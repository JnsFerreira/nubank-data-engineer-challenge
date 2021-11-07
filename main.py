# Project libraries
from app.parse.io import parse_input_events
from app.auth.validation.custom_validation import *
from app.auth.authorizer import Authorizer
from app.service.logging import logger


def main():
    events = parse_input_events()
    auth = Authorizer(
        events=events,
        validations=[
            CardNotActiveValidation,
            InsufficientLimitValidation,
            HighFreqSmallIntervalValidation,
            DoubleTransaction
        ]
    )

    if events:
        logger.log_entry(
            message='Starting events processing.',
            severity='INFO'
        )
        auth.process()

    else:
        logger.log_entry(
            message='No events founded. Skipping execution.',
            severity='WARNING'
        )


if __name__ == '__main__':
    main()
