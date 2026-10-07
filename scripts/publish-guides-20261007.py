"""Publish the October 7 editorial batch using the established site layout."""

from pathlib import Path


original = Path(__file__).with_name("publish-guides-20261001.py")
source = original.read_text(encoding="utf-8")
changes = {
    "2026-10-01": "2026-10-07",
    "October 1, 2026": "October 7, 2026",
    "peptide-vial-condensation-label-application.webp": "peptide-vial-peel-back-booklet-label-buying-guide.webp",
    " · By ": " - By ",
    "Primary FDA, GS1, HERMA and Avery Dennison references support the identified technical points.": "The primary references linked below support the identified technical points.",
}
for old, new in changes.items():
    if old not in source:
        raise ValueError(f"Expected template text not found: {old}")
    source = source.replace(old, new)
exec(compile(source, str(original), "exec"), {"__file__": str(__file__)})
