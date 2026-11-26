# news-image-20261126 entrypoint.
#
# The grader runs this program with no network and expects the finished
# front page at $MAKEFUN_OUTPUT_DIR/entry.png. The image is drawn by
# render.py and shipped beside this file as entry.png, so all this program
# does is copy it into place and check the copy byte for byte. It uses
# only the standard library, so it behaves the same in the grading
# sandbox as it does on this machine: a failed copy or a hash mismatch
# exits non-zero instead of handing the grader a broken file.
import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAME = "entry.png"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run():
    src = HERE / NAME
    if not src.is_file():
        print(f"missing {NAME} next to {__file__}", file=sys.stderr)
        return 2
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / NAME
    shutil.copyfile(src, dst)
    if sha256_of(src) != sha256_of(dst):
        print("copy failed the hash check", file=sys.stderr)
        return 3
    print(f"{NAME} placed at {dst} sha256={sha256_of(dst)}")
    return 0


if __name__ == "__main__":
    sys.exit(run())
