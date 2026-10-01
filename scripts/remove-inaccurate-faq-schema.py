"""Remove FAQ JSON-LD whose questions or answers are absent from visible HTML."""

import argparse
import importlib.util
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "custom-labels-stickers-website"
spec = importlib.util.spec_from_file_location("static_seo_audit", Path(__file__).with_name("audit-static-seo.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

SCRIPT = re.compile(
    r'<script\b(?P<attrs>[^>]*)>(?P<body>.*?)</script>',
    re.DOTALL,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write the mechanical cleanup")
    args = parser.parse_args()
    changed = []

    for path in sorted(SITE.glob("*.html")):
        original = path.read_bytes().decode("utf-8")
        page = audit.PageParser()
        page.feed(original)
        visible = audit.normalize(" ".join(page.visible_text))

        def replace(match):
            if not re.search(r'''\btype\s*=\s*["']application/ld\+json["']''', match.group("attrs"), re.I):
                return match.group(0)
            try:
                schema = json.loads(match.group("body"))
            except json.JSONDecodeError:
                return match.group(0)
            if not isinstance(schema, dict) or schema.get("@type") != "FAQPage":
                return match.group(0)
            for question in schema.get("mainEntity", []):
                name = audit.normalize(question.get("name", ""))
                answer = audit.normalize(question.get("acceptedAnswer", {}).get("text", ""))
                if not name or name not in visible or not answer or answer not in visible:
                    return ""
            return match.group(0)

        updated = SCRIPT.sub(replace, original)
        if updated != original:
            changed.append(path.relative_to(ROOT))
            if args.apply:
                path.write_bytes(updated.encode("utf-8"))

    print(f"{'Cleaned' if args.apply else 'Would clean'} {len(changed)} pages")
    for path in changed:
        print(path)


if __name__ == "__main__":
    main()
