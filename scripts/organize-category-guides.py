"""Turn appended single-link guide bands into one navigable category guide hub."""

from html import escape
from pathlib import Path
import re

from bs4 import BeautifulSoup


SITE = Path(__file__).resolve().parents[1] / "custom-labels-stickers-website"
PAGES = {
    "custom-peptide-vial-labels.html": {
        "heading": "Peptide Vial Label Buying Guides",
        "intro": "Start with bottle fit, application conditions and SKU control before approving a label roll.",
        "featured": [
            "/peptide-label-roll-core-outer-diameter-machine-fit",
            "/peptide-vial-condensation-label-application",
            "/multi-sku-peptide-vial-label-visual-inspection",
        ],
    },
    "custom-supplement-labels.html": {
        "heading": "Supplement Label Buying Guides",
        "intro": "Check pack geometry, information-panel space and barcode quality before releasing artwork.",
        "featured": [
            "/tapered-supplement-bottle-labels",
            "/supplement-facts-panel-dieline-width",
            "/supplement-label-barcode-verification",
        ],
    },
    "custom-3d-holographic-labels.html": {
        "heading": "Hologram and QR Label Buying Guides",
        "intro": "Choose the seal surface and verification workflow before deciding on a visual effect.",
        "featured": [
            "/hologram-seal-curved-bottle-cap-adhesion",
            "/holographic-qr-label-scan-contrast-testing",
            "/hologram-label-visual-authentication-vs-qr-check",
        ],
    },
}

GENERATED_SECTION = re.compile(
    r'^<section class="recent-guide-links"><div class="container"><h2>'
    r'Production and Purchasing Guides</h2>.*?</div></section>\r?\n?',
    re.MULTILINE,
)
ORGANIZED_SECTION = re.compile(
    r'^<section class="recent-guide-links" aria-labelledby="category-guides-heading">'
    r'.*?</section>\r?\n?',
    re.MULTILINE | re.DOTALL,
)


def render_hub(config, links):
    featured = [url for url in config["featured"] if url in links]
    archive = [url for url in links if url not in featured]
    if len(featured) != len(config["featured"]):
        raise ValueError(f"Missing featured links: {set(config['featured']) - set(featured)}")

    lines = [
        '<section class="recent-guide-links" aria-labelledby="category-guides-heading">',
        '  <div class="container">',
        f'    <h2 id="category-guides-heading">{escape(config["heading"])}</h2>',
        f'    <p>{escape(config["intro"])}</p>',
        '    <div class="guide-priority-grid">',
    ]
    lines.extend(
        f'      <a href="{escape(url, quote=True)}">{escape(links[url])}</a>'
        for url in featured
    )
    lines.extend(
        [
            '    </div>',
            '    <details class="guide-archive">',
            f'      <summary>Browse all {len(links)} production guides</summary>',
            '      <div class="guide-archive-grid">',
        ]
    )
    lines.extend(
        f'        <a href="{escape(url, quote=True)}">{escape(links[url])}</a>'
        for url in archive
    )
    lines.extend(['      </div>', '    </details>', '  </div>', '</section>'])
    return "\n".join(lines) + "\n"


def organize(path, config):
    source = path.read_text(encoding="utf-8")
    generated = list(GENERATED_SECTION.finditer(source))
    organized = list(ORGANIZED_SECTION.finditer(source))
    if len(organized) > 1:
        raise ValueError(f"Multiple organized guide hubs in {path.name}")
    if not generated and organized:
        print(f"{path.name}: guide hub already current")
        return
    matches = sorted(generated + organized, key=lambda match: match.start())
    if not matches:
        raise ValueError(f"No guide sections in {path.name}")
    if any(source[left.end():right.start()].strip() for left, right in zip(matches, matches[1:])):
        raise ValueError(f"Guide sections are not contiguous in {path.name}")

    links = {}
    for match in matches:
        fragment = BeautifulSoup(match.group(), "html.parser")
        for anchor in fragment.select("a[href]"):
            url = anchor["href"]
            title = anchor.get_text(" ", strip=True)
            if url in links and links[url] != title:
                raise ValueError(f"Conflicting title for {url}")
            links[url] = title

    rewritten = source[:matches[0].start()] + render_hub(config, links) + source[matches[-1].end():]
    path.write_text(rewritten, encoding="utf-8", newline="")
    print(f"{path.name}: {len(generated)} new bands -> one hub, {len(links)} unique links")


if __name__ == "__main__":
    for filename, settings in PAGES.items():
        organize(SITE / filename, settings)
