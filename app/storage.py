from pathlib import Path
import shutil

def copy_file(src,dst):
 Path(dst).parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(src,dst)
