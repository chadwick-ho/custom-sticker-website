"""Validate the October 3 guides against the established batch checks."""

from pathlib import Path


original = Path(__file__).with_name("check-guides-20261001.py")
source = original.read_text(encoding="utf-8")
if "2026-10-01" not in source:
    raise ValueError("Expected date not found in validation template")
source = source.replace("2026-10-01", "2026-10-03")
exec(compile(source, str(original), "exec"), {"__file__": str(__file__)})
