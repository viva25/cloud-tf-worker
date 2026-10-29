import tempfile
import os

from app.worker import process_event

def test_file_transfer():

    src = tempfile.NamedTemporaryFile(
        delete=False
    )

    src.write(
        b"hello"
    )

    src.close()

    dst = src.name + ".copy"

    event = {
        "eventId": "1",
        "source": {
            "path": src.name
        },
        "destination": {
            "path": dst
        }
    }

    process_event(event)

    assert os.path.exists(dst)
