#!/usr/bin/env python

import os
import sys
from importlib import import_module
from pathlib import Path

import pytest


filepath, mode = sys.argv[1:3]
if not os.path.exists(filepath):
    print(f"File {filepath!r} not found")
    exit(1)

filepath = Path(filepath)
os.chdir(filepath.parent)
sys.path.append(".")
mod = import_module(filepath.stem, package=".")


if mode == "test":
    lines = mod.test_lines.strip().split("\n")
    expected = mod.expected_test_result
elif mode == "real":
    lines = [x.strip() for x in open("input", "rt")]
    expected = None
elif mode == "unit":
    pytest.main([filepath] + sys.argv[3:])
    exit(0)
else:
    print("Bad mode")
    exit(1)

result = mod.run(lines)
if expected is None:
    print("----- Result:")
    print(repr(result))
else:
    if result == expected:
        print("ok :)")
    else:
        print("----- Debería:")
        print(repr(expected))
        print("----- Obtuvimos:")
        print(repr(result))
