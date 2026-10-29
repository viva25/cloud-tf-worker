import os
import tempfile

from app.worker import process_event


def test_file_transfer():
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "source.txt")
        dst = os.path.join(tmpdir, "destination.txt")

        with open(src, "w", encoding="utf-8") as file:
            file.write("test content")

        # Build your event using src and dst,
        # then call process_event(event).
