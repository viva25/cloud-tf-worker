import json
import logging
import time

from queue import Empty
from app.queue import (
    event_queue,
    dead_letter_queue
)

from app.storage import copy_file
from app.idempotency import (
    already_processed,
    mark_processed
)

from app.metrics import (
    success,
    failure
)

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

MAX_RETRIES = 3

def process_event(event):

    event_id = event["eventId"]

    if already_processed(event_id):
        logging.info(
            json.dumps({
                "event": event_id,
                "status": "duplicate"
            })
        )
        return

    attempt = 0

    while attempt < MAX_RETRIES:

        try:

            copy_file(
                event["source"]["path"],
                event["destination"]["path"]
            )

            mark_processed(event_id)

            success()

            logging.info(
                json.dumps({
                    "event": event_id,
                    "status": "success"
                })
            )

            return

        except Exception as ex:

            attempt += 1

            logging.error(
                json.dumps({
                    "event": event_id,
                    "attempt": attempt,
                    "error": str(ex)
                })
            )

            time.sleep(2 ** attempt)

    dead_letter_queue.put(event)

    failure()
