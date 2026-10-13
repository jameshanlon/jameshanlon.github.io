#!/usr/bin/env python
"""
Write a manifest of every output path with a hash of its contents.
"""

import hashlib
import sys
from pathlib import Path


def entries(root: Path):
    """
    Yield "<path> <sha256-or-dash>" for every file under root, sorted.
    """
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        if rel.startswith("thumbs/"):
            yield f"{rel} -"
        else:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            yield f"{rel} {digest}"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "output")
    lines = list(entries(root))
    Path("tests/url_manifest.txt").write_text("\n".join(lines) + "\n")
    print(f"Wrote {len(lines)} entries from {root}")


if __name__ == "__main__":
    main()
