# Built-in libraries
import sys
import json
from datetime import datetime
from typing import Generator


def parse_input_events() -> Generator[dict, None, None]:
    """
    Generates a list from received events from standard input (stdin).
    Classify events into a type and converts time fields to python datetime format.

    Yield:
        data (dict): Formatted events received from standard input (stdin).
    """

    for order, value in enumerate(sys.stdin.readlines()):
        data = json.loads(value)

        if 'account' in data:
            event_type = 'account_creation'

        elif 'transaction' in data:
            event_type = 'transaction'

            # Converting time field to python datetime
            t = data.get('transaction', {})
            t.update(
                {'time': datetime.strptime(t.get('time', ''), '%Y-%m-%dT%H:%M:%S.%fZ')}
            )

        else:
            event_type = 'unknown'

        data.update({
            'event_type': event_type,
            'order': order
        })

        yield data
