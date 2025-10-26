#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Add an SPDX header to files in place."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable, Dict, Iterable

SPDX_LINE = "SPDX-License-Identifier: MPL-2.0"

Commenter = Callable[[str], str]


def python_comment(_: str) -> str:
    return f"# {SPDX_LINE}\n"


def shell_comment(content: str) -> str:
    lines = content.splitlines()
    if lines and lines[0].startswith("#!"):
        shebang = lines[0] + "\n"
        rest = "\n".join(lines[1:])
        if rest and not rest.endswith("\n"):
            rest += "\n"
        return f"{shebang}# {SPDX_LINE}\n{rest}"
    return f"# {SPDX_LINE}\n"


def ps_comment(_: str) -> str:
    return f"# {SPDX_LINE}\n"


def yaml_comment(_: str) -> str:
    return f"# {SPDX_LINE}\n"


def docker_comment(_: str) -> str:
    return f"# {SPDX_LINE}\n"


def make_comment(_: str) -> str:
    return f"# {SPDX_LINE}\n"


def markdown_comment(_: str) -> str:
    return f"<!-- {SPDX_LINE} -->\n"

COMMENTERS: Dict[str, Commenter] = {
    ".py": python_comment,
    ".sh": shell_comment,
    ".bash": shell_comment,
    ".ps1": ps_comment,
    ".psm1": ps_comment,
    ".yml": yaml_comment,
    ".yaml": yaml_comment,
    ".toml": python_comment,
    ".cfg": python_comment,
    ".ini": python_comment,
    ".env": python_comment,
    ".md": markdown_comment,
}

SPECIAL_FILES: Dict[str, Commenter] = {
    "Dockerfile": docker_comment,
    "Makefile": make_comment,
}


def ensure_header(path: Path) -> None:
    text = path.read_text()
    if SPDX_LINE in text:
        return
    suffix = path.suffix
    commenter = COMMENTERS.get(suffix)
    if commenter is None:
        commenter = SPECIAL_FILES.get(path.name)
    if commenter is None and text.startswith('#!'):
        commenter = shell_comment
    if commenter is None:
        return
    header = commenter(text)
    if suffix == ".md" and text.startswith("# "):
        path.write_text(header + "\n" + text)
        return
    if suffix in {".py", ".toml", ".cfg", ".ini", ".env"}:
        path.write_text(header + text)
        return
    if suffix in {".sh", ".bash"} and text.startswith("#!"):
        first_newline = text.find("\n")
        if first_newline == -1:
            path.write_text(text + "\n# " + SPDX_LINE + "\n")
        else:
            rest = text[first_newline + 1 :]
            path.write_text(text[: first_newline + 1] + f"# {SPDX_LINE}\n" + rest)
        return
    if suffix in {".ps1", ".psm1"} and text.startswith("#!"):
        first_newline = text.find("\n")
        if first_newline == -1:
            path.write_text(text + "\n# " + SPDX_LINE + "\n")
        else:
            rest = text[first_newline + 1 :]
            path.write_text(text[: first_newline + 1] + f"# {SPDX_LINE}\n" + rest)
        return
    if commenter is shell_comment:
        path.write_text(header)
        return
    path.write_text(header + text)


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ensure files have SPDX headers")
    parser.add_argument("files", nargs="+", help="Files to process")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    for filename in args.files:
        path = Path(filename)
        if not path.exists() or path.is_dir():
            continue
        ensure_header(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
