# Built-in libraries
import sys
import json

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

        auth = Authorizer(
            events=events,
            validations=[
                CardNotActiveValidation,
                InsufficientLimitValidation,
                HighFreqSmallIntervalValidation,
                DoubledTransaction
            ]
        )

        for processed_event in auth.process():
            # Write event to stdout
            sys.stdout.write(
                f"{json.dumps(processed_event, default=str, sort_keys=True)}\n"
            )

        logger.info("Done! All events have been processed.")

    else:
        logger.warning('No events found. Skipping execution.')


if __name__ == '__main__':
    main()
