#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Fail if tracked source files are missing an SPDX identifier."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable

SPDX_LINE = "SPDX-License-Identifier: MPL-2.0"

CHECK_EXTENSIONS = {
    ".py",
    ".sh",
    ".bash",
    ".ps1",
    ".psm1",
    ".yml",
    ".yaml",
    ".toml",
    ".cfg",
    ".ini",
    ".env",
}

SPECIAL_NAMES = {"Dockerfile", "Makefile"}


def iter_tracked_files() -> Iterable[Path]:
    from subprocess import run, PIPE

    git_files = Path(".git")
    if not git_files.exists():
        raise SystemExit("This script must be run from the repository root")
    result = run(['git', 'ls-files'], check=True, stdout=PIPE, text=True)
    for line in result.stdout.splitlines():
        path = Path(line)
        if not path.exists() or path.is_dir():
            continue
        yield path


def missing_header(path: Path) -> bool:
    text = path.read_text(errors="ignore")
    if SPDX_LINE in text:
        return False
    if path.suffix in CHECK_EXTENSIONS:
        return True
    if path.name in SPECIAL_NAMES:
        return True
    if text.startswith("#!"):
        return True
    return False


def main() -> int:
    missing = []
    for path in iter_tracked_files():
        if missing_header(path):
            missing.append(str(path))
    if missing:
        print("Missing SPDX header in:")
        for path in missing:
            print(f" - {path}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
