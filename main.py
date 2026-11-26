# news-image-20261126 entrypoint: put the finished front page where the
# grader expects it. Deliberately standard-library only, so the program
# behaves the same in the grading sandbox as it does on this machine.
# It copies the image that render.py drew (entry.png, beside this file)
# into $MAKEFUN_OUTPUT_DIR, then proves the copy is exact by hashing
# both files and refusing to finish when the hashes differ.
from pathlib import Path
import hashlib as _hashlib
import os as _os
import shutil as _shutil
import sys as _sys

ROOT = Path(__file__).resolve().parent
IMAGE_NAME = "entry.png"


def _digest(path):
    digest = _hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(1 << 16)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def _place_image():
    source = ROOT / IMAGE_NAME
    if not source.exists():
        print("entry image not found in " + str(ROOT), file=_sys.stderr)
        raise SystemExit(2)
    target_dir = Path(_os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / IMAGE_NAME
    _shutil.copyfile(source, target)
    before, after = _digest(source), _digest(target)
    if before != after:
        print("hash mismatch after copy", file=_sys.stderr)
        raise SystemExit(3)
    print("entry.png ready at " + str(target) + " sha256=" + after)


if __name__ == "__main__": _place_image()
