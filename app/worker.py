
import json
import logging
import time

from app.idempotency import already_processed, mark_processed
from app.queue import dead_letter_queue
from app.storage import copy_file

logger = logging.getLogger(__name__)

MAX_RETRIES = 3


def process_event(event):
    event_id = event["eventId"]

    if already_processed(event_id):
        logger.info(
            json.dumps({"event": event_id, "status": "duplicate"})
        )
        return

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            copy_file(
                event["source"]["path"],
                event["destination"]["path"],
            )

            mark_processed(event_id)
            success()

            logger.info(
                json.dumps({"event": event_id, "status": "success"})
            )
            return

        except OSError as ex:
            logger.error(
                json.dumps({
                    "event": event_id,
                    "attempt": attempt,
                    "error": str(ex),
                })
            )

            if attempt < MAX_RETRIES:
                time.sleep(2 ** attempt)

    dead_letter_queue.put(event)
    failure()
