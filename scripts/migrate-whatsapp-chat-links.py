"""Replace the old WhatsApp Business short link with a controlled chat message."""

from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "custom-labels-stickers-website"
OLD_URL = "https://api.whatsapp.com/message/VLGQGDJCIUFAF1?autoload=1&app_absent=0"
OLD_HTML_URL = OLD_URL.replace("&", "&amp;")
MESSAGE = (
    "Hi RP Labels, I saw your custom labels on rplabels.com. "
    "I'd like a quote and free design help for my project. Can we chat?"
)
NEW_URL = "https://wa.me/8613285455519?text=" + quote(MESSAGE, safe="")
OLD_SCRIPT = "main.js?v=20260929-whatsapp"
NEW_SCRIPT = "main.js?v=20261008-chat"

paths = [*SITE.glob("*.html"), *ROOT.glob("scripts/publish-guides-*.py")]
changed = 0
for path in paths:
    text = path.read_text(encoding="utf-8")
    updated = text.replace(OLD_HTML_URL, NEW_URL).replace(OLD_URL, NEW_URL)
    updated = updated.replace(OLD_SCRIPT, NEW_SCRIPT)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        changed += 1

print(f"Updated {changed} site pages and publisher templates.")
