"""Check crawl-critical SEO fields for pages listed in the XML sitemap."""

import json
import posixpath
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse


SITE = Path(__file__).resolve().parents[1] / "custom-labels-stickers-website"
ORIGIN = "https://rplabels.com"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = []
        self.h1_count = 0
        self.description = None
        self.canonical = None
        self.robots = None
        self.links = []
        self.images = []
        self.json_ld = []
        self.visible_text = []
        self._capture = None
        self._script = []
        self._hidden = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style"):
            self._hidden = tag
        if tag == "title":
            self._capture = "title"
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "script" and attrs.get("type") == "application/ld+json":
            self._capture = "script"
            self._script = []
        elif tag == "meta":
            if attrs.get("name", "").lower() == "description":
                self.description = attrs.get("content")
            if attrs.get("name", "").lower() == "robots":
                self.robots = attrs.get("content")
        elif tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonical = attrs.get("href")
        elif tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        elif tag == "img":
            self.images.append(attrs)

    def handle_endtag(self, tag):
        if tag == self._capture:
            if tag == "script":
                self.json_ld.append("".join(self._script))
            self._capture = None
        if tag == self._hidden:
            self._hidden = None

    def handle_data(self, data):
        if self._capture == "title":
            self.title.append(data)
        elif self._capture == "script":
            self._script.append(data)
        elif not self._hidden:
            self.visible_text.append(data)


def normalize(value):
    return " ".join(unescape(value).lower().split())


def local_file(url):
    path = urlparse(url).path
    if path in ("", "/"):
        return SITE / "index.html"
    relative = path.lstrip("/")
    if not posixpath.splitext(relative)[1]:
        relative += ".html"
    return SITE / relative


def main():
    tree = ET.parse(SITE / "sitemap.xml")
    urls = [node.text for node in tree.findall(".//{*}loc")]
    errors = []
    warnings = []
    titles = defaultdict(list)
    descriptions = defaultdict(list)
    inlinks = Counter()
    canonical_urls = set(urls)

    for url in urls:
        file = local_file(url)
        if not file.is_file():
            errors.append(f"Missing sitemap target: {url}")
            continue
        page = PageParser()
        page.feed(file.read_text(encoding="utf-8"))
        title = " ".join(" ".join(page.title).split())
        if not title:
            errors.append(f"Missing title: {url}")
        else:
            titles[title].append(url)
        if not page.description:
            warnings.append(f"Missing meta description: {url}")
        else:
            descriptions[page.description].append(url)
        if page.canonical != url:
            errors.append(f"Canonical mismatch: {url} -> {page.canonical}")
        if page.robots and "noindex" in page.robots.lower():
            errors.append(f"Noindex page in sitemap: {url}")
        if page.h1_count != 1:
            warnings.append(f"Expected one H1, found {page.h1_count}: {url}")
        visible = normalize(" ".join(page.visible_text))
        for block in page.json_ld:
            try:
                data = json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"Invalid JSON-LD: {url}: {exc}")
                continue
            schemas = data.get("@graph", [data]) if isinstance(data, dict) else data
            for schema in schemas:
                if schema.get("@type") != "FAQPage":
                    continue
                for question in schema.get("mainEntity", []):
                    name = normalize(question.get("name", ""))
                    answer = normalize(question.get("acceptedAnswer", {}).get("text", ""))
                    if not name or name not in visible:
                        warnings.append(f"FAQ schema question absent from visible page: {url}: {name}")
                    if not answer or answer not in visible:
                        warnings.append(f"FAQ schema answer absent from visible page: {url}: {name}")
        for image in page.images:
            if "alt" not in image:
                warnings.append(f"Image missing alt: {url} -> {image.get('src')}")
            source = image.get("src", "")
            if source and not source.startswith(("data:", "//")):
                target = urljoin(url, source)
                if urlparse(target).netloc == urlparse(ORIGIN).netloc:
                    asset = SITE / urlparse(target).path.lstrip("/")
                    if not asset.is_file():
                        errors.append(f"Missing image: {url} -> {source}")
        for href in page.links:
            target = urljoin(url, href)
            parsed = urlparse(target)
            if parsed.scheme not in ("http", "https") or parsed.netloc != urlparse(ORIGIN).netloc:
                continue
            target = ORIGIN + parsed.path.rstrip("/") if parsed.path != "/" else ORIGIN + "/"
            if target in canonical_urls:
                inlinks[target] += 1
            elif not local_file(target).is_file():
                warnings.append(f"Missing local link target: {url} -> {href}")

    for label, values in (("title", titles), ("description", descriptions)):
        for value, pages in values.items():
            if len(pages) > 1:
                warnings.append(f"Duplicate {label} ({len(pages)} pages): {value[:90]}")
    for url in urls:
        if url != ORIGIN + "/" and not inlinks[url]:
            warnings.append(f"No sitemap-page inlinks: {url}")

    print(f"Audited {len(urls)} sitemap URLs: {len(errors)} errors, {len(warnings)} warnings")
    for issue in errors:
        print("ERROR " + issue)
    for issue in warnings:
        print("WARN  " + issue)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
