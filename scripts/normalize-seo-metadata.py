"""Keep canonical sharing metadata and RP organization identity consistent."""

import json
import re
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path
from urllib.parse import urlparse


SITE = Path(__file__).resolve().parents[1] / "custom-labels-stickers-website"
ORIGIN = "https://rplabels.com"
ORG_ID = ORIGIN + "/#organization"
LOGO = ORIGIN + "/assets/icons/favicon.svg"

DESCRIPTION_UPDATES = {
    "/": "Custom bottle and jar labels for small supplement brands. Plan pack fit, artwork and quantity per design, with research vial and holographic options too.",
    "/custom-3d-holographic-labels": "Custom holographic security labels and QR seals for bottles and cartons. Compare materials, code placement and sample checks before ordering.",
}
TITLE_UPDATES = {
    "/custom-supplement-labels": "Custom Supplement Labels | Bottle Label Printing | RP",
}


def set_meta(head, attribute, key, value):
    tag = f'<meta {attribute}="{key}" content="{escape(value, quote=True)}">'
    pattern = rf'<meta\b[^>]*\b{attribute}=["\']{re.escape(key)}["\'][^>]*>'
    if re.search(pattern, head, re.I):
        return re.sub(pattern, lambda _: tag, head, count=1, flags=re.I)
    return head.rstrip() + "\n  " + tag + "\n"


def update_organization(value):
    if isinstance(value, list):
        for item in value:
            update_organization(item)
    elif isinstance(value, dict):
        types = value.get("@type", [])
        types = [types] if isinstance(types, str) else types
        if (
            "Organization" in types
            and value.get("name") in {"RP", "RP Labels", "RP Custom Labels"}
            and value.get("url", "").rstrip("/") == ORIGIN
        ):
            value.setdefault("@id", ORG_ID)
            value.setdefault("logo", LOGO)
        for child in list(value.values()):
            update_organization(child)


def normalize_page(path, url):
    original = path.read_text(encoding="utf-8")
    head, body = original.split("</head>", 1)
    route = urlparse(url).path
    if route in DESCRIPTION_UPDATES:
        head = set_meta(head, "name", "description", DESCRIPTION_UPDATES[route])
        head = set_meta(head, "property", "og:description", DESCRIPTION_UPDATES[route])
    if route in TITLE_UPDATES:
        title = TITLE_UPDATES[route]
        head = re.sub(r"<title>.*?</title>", f"<title>{escape(title)}</title>", head, count=1, flags=re.S)
        head = set_meta(head, "property", "og:title", title)
        head = set_meta(head, "name", "twitter:title", title)

    article = False

    def schema(match):
        nonlocal article
        value = json.loads(match.group(2))
        if isinstance(value, dict):
            types = value.get("@type", [])
            types = [types] if isinstance(types, str) else types
            article = article or bool({"Article", "BlogPosting"}.intersection(types))
        before = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        update_organization(value)
        after = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        # Preserve all unmodified JSON-LD formatting.
        return match.group(0) if before == after else match.group(1) + after + match.group(3)

    head = re.sub(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', schema, head, flags=re.S)
    head = set_meta(head, "property", "og:site_name", "RP Labels")
    head = set_meta(head, "property", "og:type", "article" if article else "website")
    head = set_meta(head, "property", "og:url", url)
    updated = head + "</head>" + body
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main():
    urls = [node.text for node in ET.parse(SITE / "sitemap.xml").findall(".//{*}loc")]
    changed = 0
    for url in urls:
        route = urlparse(url).path
        name = "index.html" if route == "/" else route.lstrip("/") + ".html"
        changed += normalize_page(SITE / name, url)
    print(f"Checked {len(urls)} canonical pages; updated {changed}.")


if __name__ == "__main__":
    main()
