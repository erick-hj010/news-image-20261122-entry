#!/usr/bin/env python3
"""Entry program for the make.fun bounty ``news-image-20261122``.

The deliverable image ships inside this repository as ``entry_src.png``.
Running the program publishes that image, byte for byte, to the
destination the harness expects: the path named by the ``OUTPUT_PATH``
environment variable, or ``/output/entry.png`` when the variable is
not set.

Only the Python standard library is used. The program performs no
network access, uses no randomness and reads no clock, so repeated
runs always produce exactly the same bytes. After copying, it prints
the SHA-256 digest of what it wrote, so a run can be checked against
``VERIFY.md`` without any extra tooling.
"""

import hashlib
import os
from pathlib import Path

SOURCE_NAME = "entry_src.png"
FALLBACK_DESTINATION = "/output/entry.png"
BLOCK_SIZE = 1024 * 1024


def resolve_destination() -> Path:
    """Return the output path chosen for this run."""
    override = os.environ.get("OUTPUT_PATH")
    if override:
        return Path(override)
    return Path(FALLBACK_DESTINATION)


def publish(source: Path, destination: Path) -> int:
    """Copy ``source`` to ``destination`` in fixed-size blocks.

    The destination's parent directory is created when it does not
    exist yet. Returns the number of bytes copied.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    copied = 0
    with source.open("rb") as src, destination.open("wb") as dst:
        while True:
            block = src.read(BLOCK_SIZE)
            if not block:
                break
            dst.write(block)
            copied += len(block)
    return copied


def digest(path: Path) -> str:
    """Return the SHA-256 hex digest of a file, read in blocks."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(BLOCK_SIZE)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    destination = resolve_destination()
    copied = publish(source, destination)
    print(f"wrote {copied} bytes to {destination}")
    print(f"sha256: {digest(destination)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
