import shutil
from pathlib import Path


def copy_file(src, dst):
    source = Path(src)
    destination = Path(dst)

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
