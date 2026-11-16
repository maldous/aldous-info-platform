"""Dependency-free syntax lint for tracked JavaScript, Python and JSON source.

This is parser validation, not formatting, security review or browser acceptance.
"""
from __future__ import annotations

import ast
import json
import os
from pathlib import Path
import shutil
import subprocess

MAX_SOURCE_BYTES = 16 << 20


def git_environment() -> dict[str, str]:
    return {"PATH": os.environ.get("PATH", os.defpath), "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull, "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_OPTIONAL_LOCKS": "0"}


def tracked_paths(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "-c", "core.fsmonitor=false", "-C", str(root), "ls-files", "-z"],
        check=True, capture_output=True, timeout=30, env=git_environment(),
    )
    paths = []
    for value in result.stdout.decode("utf-8").split("\0"):
        if not value:
            continue
        path = root / value
        if path.suffix not in {".js", ".mjs", ".py", ".json"}:
            continue
        if path.is_symlink() or not path.resolve(strict=True).is_relative_to(root):
            raise ValueError("Tracked lint input must be a contained regular source file")
        if not path.is_file() or path.stat().st_size > MAX_SOURCE_BYTES:
            raise ValueError("Tracked lint input exceeds regular-file or size boundary")
        paths.append(path)
    return paths


def reject_nonfinite(_: str) -> None:
    raise ValueError("Non-finite JSON number")


def check_syntax(path: Path, node: str) -> bool:
    if path.suffix == ".py":
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=path.name)
        except (SyntaxError, UnicodeError):
            return False
        return True
    if path.suffix == ".json":
        try:
            json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_nonfinite)
        except (ValueError, UnicodeError):
            return False
        return True
    result = subprocess.run(
        [node, "--check", str(path)], stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30,
        env={"PATH": os.defpath},
    )
    return result.returncode == 0


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    node = shutil.which("node")
    if node is None:
        print("Syntax lint requires the documented Node.js toolchain.")
        return 1
    try:
        paths = tracked_paths(root)
        invalid = [str(path.relative_to(root)) for path in paths if not check_syntax(path, node)]
    except (OSError, ValueError, subprocess.SubprocessError):
        print("Syntax lint could not read or validate the selected tracked source.")
        return 1
    for name in invalid:
        print("Invalid syntax: " + name)
    print(f"Syntax lint: {len(paths)} tracked files, {len(invalid)} invalid; no formatter/security claim.")
    return int(bool(invalid))


if __name__ == "__main__":
    raise SystemExit(main())
