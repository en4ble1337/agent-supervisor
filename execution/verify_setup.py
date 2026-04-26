#!/usr/bin/env python3
import sys
from pathlib import Path


def check():
    checks = [
        ("Python 3.11+", lambda: sys.version_info[:2] >= (3, 11)),
        (".env exists", lambda: Path(".env").exists()),
        ("Requirements", lambda: Path("requirements.txt").exists()),
        ("Methodology", lambda: Path("docs/methodology/review-gates.md").exists()),
    ]
    all_pass = True
    for name, func in checks:
        passed = func()
        print(f"[{'✓' if passed else '✗'}] {name}")
        if not passed:
            all_pass = False
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(check())
