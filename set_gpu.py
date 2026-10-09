#!/usr/bin/env python3
"""Toggle GPU support in pyproject.toml.

Adds or removes "gpu" in [tool.uv] default-groups. Because the group is a
default, plain `uv sync` keeps onnxruntime-gpu installed instead of pruning it.
"""

import re
import sys
from pathlib import Path

PYPROJECT = Path(__file__).resolve().parent / "pyproject.toml"
GROUPS_RE = re.compile(r"^default-groups\s*=\s*\[(.*?)\]\s*$", re.MULTILINE)


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in {"enable", "disable"}:
        print("Usage: set_gpu.py [enable|disable]")
        return 2

    text = PYPROJECT.read_text()
    match = GROUPS_RE.search(text)
    if not match:
        print("default-groups not found in pyproject.toml")
        return 1

    groups = [item.strip().strip('"') for item in match.group(1).split(",") if item.strip()]
    if sys.argv[1] == "enable":
        if "gpu" not in groups:
            groups.append("gpu")
    else:
        groups = [group for group in groups if group != "gpu"]

    rendered = "[" + ", ".join(f'"{group}"' for group in groups) + "]"
    PYPROJECT.write_text(GROUPS_RE.sub(f"default-groups = {rendered}", text, count=1))
    print(f"GPU support {'enabled' if sys.argv[1] == 'enable' else 'disabled'}: default-groups = {rendered}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
