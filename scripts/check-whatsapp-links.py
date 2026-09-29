"""Check every published WhatsApp CTA and the cache-busted link controller."""

from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "custom-labels-stickers-website"
URL = "https://api.whatsapp.com/message/VLGQGDJCIUFAF1?autoload=1&app_absent=0"
SCRIPT = "main.js?v=20260929-whatsapp"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.whatsapp = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "data-whatsapp" in attrs:
            self.whatsapp.append(attrs.get("href"))
        if tag == "script" and "main.js" in attrs.get("src", ""):
            self.scripts.append(attrs["src"])


pages = list(ROOT.glob("*.html"))
buttons = 0
for page in pages:
    source = page.read_text(encoding="utf-8")
    parser = Links()
    parser.feed(source)
    assert "https://wa.me/8613285455519" not in source, page
    assert parser.whatsapp, (page, "no WhatsApp CTA")
    assert all(href == URL for href in parser.whatsapp), (page, parser.whatsapp)
    assert len(parser.scripts) == 1 and parser.scripts[0].endswith(SCRIPT), (page, parser.scripts)
    buttons += len(parser.whatsapp)

controller = (ROOT / "assets/js/main.js").read_text(encoding="utf-8")
assert f'const whatsappUrl = "{URL}";' in controller
print(f"PASS: {buttons} WhatsApp CTAs across {len(pages)} pages use the new URL and JS version.")
