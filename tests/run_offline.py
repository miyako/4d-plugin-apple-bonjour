#!/usr/bin/env python3
"""Run every offline regression and fail if any test is skipped."""

from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
directory = Path(__file__).resolve().parent
sys.path.insert(0, str(directory))
suite = unittest.defaultTestLoader.discover(str(directory))
result = unittest.TextTestRunner(verbosity=2).run(suite)
if result.skipped:
    print("Offline regression skips are forbidden.", file=sys.stderr)
sys.exit(0 if result.wasSuccessful() and not result.skipped else 1)
