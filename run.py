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
        logger.info('Starting events processing.')

        Authorizer(
            events=events,
            validations=[
                CardNotActiveValidation,
                InsufficientLimitValidation,
                HighFreqSmallIntervalValidation,
                DoubledTransaction
            ]
        ).process()

    else:
        logger.warning('No events founded. Skipping execution.')


if __name__ == '__main__':
    main()
