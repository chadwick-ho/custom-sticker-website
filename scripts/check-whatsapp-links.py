"""Check every published WhatsApp CTA and the cache-busted link controller."""

from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "custom-labels-stickers-website"
URL = (
    "https://wa.me/8613285455519?text=Hi%20RP%20Labels%2C%20I%20saw%20your%20"
    "custom%20labels%20on%20rplabels.com.%20I%27d%20like%20a%20quote%20and%20"
    "free%20design%20help%20for%20my%20project.%20Can%20we%20chat%3F"
)
SCRIPT = "main.js?v=20261008-chat"


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
    assert "api.whatsapp.com/message/VLGQGDJCIUFAF1" not in source, page
    assert "ytrplabels.com" not in source, page
    assert parser.whatsapp, (page, "no WhatsApp CTA")
    assert all(href == URL for href in parser.whatsapp), (page, parser.whatsapp)
    assert len(parser.scripts) == 1 and parser.scripts[0].endswith(SCRIPT), (page, parser.scripts)
    buttons += len(parser.whatsapp)

controller = (ROOT / "assets/js/main.js").read_text(encoding="utf-8")
assert f'const whatsappUrl = "{URL}";' in controller
assert "ytrplabels.com" not in controller
print(f"PASS: {buttons} WhatsApp CTAs across {len(pages)} pages use the new URL and JS version.")
