"""Validate published batch metadata, local references and discoverability."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'custom-labels-stickers-website'
items = json.loads((ROOT / 'content/2026-10-01/manifest.json').read_text(encoding='utf-8'))

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []
        self.schemas = []
        self.schema = None
        self.words = []
    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        self.elements.append((tag, attr))
        if tag == 'script' and attr.get('type') == 'application/ld+json':
            self.schema = ''
    def handle_endtag(self, tag):
        if tag == 'script' and self.schema is not None:
            self.schemas.append(json.loads(self.schema))
            self.schema = None
    def handle_data(self, data):
        if self.schema is not None:
            self.schema += data
        else:
            self.words.extend(data.split())

tree = ET.parse(SITE / 'sitemap.xml')
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = [e.text for e in tree.findall('.//s:loc', ns)]
assert len(urls) == len(set(urls)), 'Duplicate sitemap URLs'
all_titles = []
for item in items:
    path = SITE / (item['slug'] + '.html')
    html = path.read_text(encoding='utf-8')
    page = Page()
    page.feed(html)
    assert sum(t == 'h1' for t,a in page.elements) == 1, path
    url = 'https://rplabels.com/' + item['slug']
    assert any(t == 'link' and a.get('rel') == 'canonical' and a.get('href') == url for t,a in page.elements), path
    assert not any(t == 'style' or 'style' in a or any(k.startswith('on') for k in a) for t,a in page.elements), 'Inline code conflicts with CSP'
    article = next(s for s in page.schemas if s.get('@type') == 'Article')
    assert article['datePublished'] == '2026-10-01'
    assert article['headline'] == item['title']
    assert url in urls
    ids = [a['id'] for t,a in page.elements if 'id' in a]
    assert len(ids) == len(set(ids)), 'Duplicate IDs'
    for tag, attr in page.elements:
        for key in ['href', 'src']:
            if key not in attr: continue
            value = attr[key]
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc: continue
            if value.startswith('#'):
                assert parsed.fragment in ids, value
                continue
            relative = unquote(parsed.path).lstrip('/')
            target = SITE / (relative or 'index.html')
            if not target.suffix: target = target.with_suffix('.html')
            assert target.is_file(), (path.name, value)
        if tag == 'img':
            assert attr.get('alt') and attr.get('width') and attr.get('height'), path
    for hub in ['blog.html', 'site-map.html', item['categoryUrl'] + '.html']:
        assert '/' + item['slug'] in (SITE / hub).read_text(encoding='utf-8'), (path,hub)
    assert len(page.words) > 850, (path, len(page.words))
    all_titles.append(item['title'])
    print(path.name + ': OK; ' + str(len(page.words)) + ' page words')
assert len(all_titles) == len(set(all_titles))
print('PASS: 5 pages, valid JSON-LD, local links, assets, hub links; ' + str(len(urls)) + ' unique sitemap URLs.')
