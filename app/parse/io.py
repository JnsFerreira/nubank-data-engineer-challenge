# Built-in libraries
import json
import fileinput
from typing import Iterable
from datetime import datetime


def parse_input_events() -> Iterable:
    """Generates a list from received events from stdin"""

    for order, value in enumerate(fileinput.input()):
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
