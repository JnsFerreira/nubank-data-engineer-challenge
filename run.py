# Project libraries
from app.service.logging import logger
from app.auth.authorizer import Authorizer
from app.parse.io import parse_input_events
from app.auth.validation.custom_validation import *


def main() -> None:
    """
    Runs the entire application flow

    Returns:
        None
    """
    events = parse_input_events()
    if events:
        logger.log_entry(
            message='Starting events processing.',
            severity='INFO'
        )

        Authorizer(
            events=events,
            validations=[
                CardNotActiveValidation,
                InsufficientLimitValidation,
                HighFreqSmallIntervalValidation,
                DoubleTransaction
            ]
        ).process()

    else:
        logger.log_entry(
            message='No events founded. Skipping execution.',
            severity='WARNING'
        )


if __name__ == '__main__':
    main()
