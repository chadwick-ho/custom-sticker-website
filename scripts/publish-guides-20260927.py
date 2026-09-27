"""Build this dated editorial batch from reviewed source fragments; no network writes."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'custom-labels-stickers-website'
SOURCE = ROOT / 'content' / '2026-09-27'
DATE = '2026-09-27'
BASE = 'https://rplabels.com'
items = json.loads((SOURCE / 'manifest.json').read_text(encoding='utf-8'))
template = (SITE / 'contact.html').read_text(encoding='utf-8')
header = '<header' + template.split('<header', 1)[1].split('</header>', 1)[0] + '</header>'
footer = '<footer' + template.split('<footer', 1)[1].split('</footer>', 1)[0] + '</footer>'
css = '<link rel="stylesheet" href="/assets/css/editorial-guides.css?v=20260927">'

def structured(value):
    return '<script type="application/ld+json">' + json.dumps(value, ensure_ascii=True, separators=(',', ':')).replace('</', '<\\/') + '</script>'

def once_insert(text, marker, addition):
    if addition in text:
        return text
    if text.count(marker) != 1:
        raise ValueError('Insertion anchor not unique: ' + marker)
    return text.replace(marker, addition + marker, 1)

def link(slug, title):
    return '<a href="/' + escape(slug, quote=True) + '">' + escape(title) + '</a>'

for item in items:
    url = BASE + '/' + item['slug']
    image = '/assets/images/' + item['image'] + '.webp'
    body = (SOURCE / (item['slug'] + '.html')).read_text(encoding='utf-8')
    headings = []
    def heading(match):
        anchor = 'section-' + str(len(headings) + 1)
        headings.append((anchor, match.group(1)))
        return '<h2 id="' + anchor + '">' + match.group(1) + '</h2>'
    body = re.sub(r'<h2>(.*?)</h2>', heading, body)
    figure = '<figure class="editorial-photo"><img src="' + image + '" srcset="' + image.replace('.webp', '-thumb.webp') + ' 768w, ' + image + ' 1536w" sizes="(max-width: 900px) calc(100vw - 40px), 850px" alt="' + escape(item['alt'], quote=True) + '" width="1536" height="1024" loading="eager" fetchpriority="high" decoding="async"><figcaption>' + escape(item['caption']) + '</figcaption></figure>'
    pieces = body.split('</p>', 2)
    body = pieces[0] + '</p>' + pieces[1] + '</p>' + figure + pieces[2]
    schema = {
        '@context': 'https://schema.org', '@type': 'Article', 'headline': item['title'],
        'description': item['description'], 'datePublished': DATE, 'dateModified': DATE,
        'inLanguage': 'en', 'mainEntityOfPage': url,
        'image': {'@type': 'ImageObject', 'url': BASE + image, 'width': 1536, 'height': 1024, 'caption': item['caption']},
        'author': {'@type': 'Organization', 'name': 'RP Labels', 'url': BASE + '/about'},
        'publisher': {'@type': 'Organization', 'name': 'RP', 'url': BASE + '/'}
    }
    breadcrumbs = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': BASE + '/blog'},
        {'@type': 'ListItem', 'position': 3, 'name': item['title'], 'item': url}]}
    sources = '<section class="editorial-sources"><h2>Sources and scope</h2><p>Reviewed September 27, 2026. Supplier and standards references support the technical points identified above. Buying scenarios, checklists and numerical examples are editorial guidance, not reported customer results or universal acceptance standards.</p><ul>' + ''.join('<li><a href="' + escape(u, quote=True) + '">' + escape(t) + '</a></li>' for t,u in item['sources']) + '</ul></section>'
    related = '<div class="article-related"><h2>Related guides and custom options</h2>' + link(item['categoryUrl'], item['category']) + ''.join(link(s,t) for s,t in item['related']) + link('contact', 'Prepare a custom label inquiry') + '</div>'
    toc = ''.join('<a href="#' + a + '">' + h + '</a>' for a,h in headings)
    tags = ''.join('<span>' + escape(t) + '</span>' for t in item['tags'])
    title, desc = escape(item['title'], quote=True), escape(item['description'], quote=True)
    page = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(item['seoTitle'])}</title><meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE + image}"><meta property="og:image:alt" content="{escape(item['alt'], quote=True)}"><meta property="article:published_time" content="{DATE}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{BASE + image}">
<link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/css/style.css?v=20260926-planner">{css}
{structured(schema)}
{structured(breadcrumbs)}
</head><body class="article-page editorial-guide">
{header}
<main><article><section class="article-hero"><div class="container"><div class="breadcrumbs"><a href="/">Home</a> / <a href="/blog">Blog</a> / {escape(item['category'])}</div><span class="eyebrow">{escape(item['category'])}</span><h1>{title}</h1><p>{escape(item['intro'])}</p><p class="article-meta">Published <time datetime="{DATE}">September 27, 2026</time> · By <a href="/about">RP Labels</a></p><div class="article-tags">{tags}</div></div></section>
<section class="section"><div class="container article-layout"><aside class="article-sidebar"><h2>In this guide</h2>{toc}</aside><div class="article-content">
{body}
{sources}
{related}
</div></div></section></article></main>
<section class="section section-dark final-cta"><div class="container"><h2>Plan Your Custom Label Order</h2><p>Send your container reference, finished size, quantity per artwork and application method. Ask for a quote and a production-representative sample plan.</p><a class="btn btn-primary" data-whatsapp href="https://api.whatsapp.com/message/LXEW2FWSFWGPJ1?autoload=1&amp;app_absent=0">Discuss My Label Project</a></div></section>
{footer}<script src="/assets/js/main.js?v=20260926-inquiry"></script></body></html>
'''
    (SITE / (item['slug'] + '.html')).write_text(page, encoding='utf-8')

blog_path = SITE / 'blog.html'
blog = blog_path.read_text(encoding='utf-8')
blog = once_insert(blog, '</head>', css + '\n')
cards = []
for index,item in enumerate(items):
    img = 'assets/images/' + item['image'] + '-thumb.webp'
    load = 'loading="eager" fetchpriority="high"' if index == 0 else 'loading="lazy"'
    cards.append('<article class="blog-card blog-photo-card"><a class="blog-card-image" href="/' + item['slug'] + '"><img src="' + img + '" alt="' + escape(item['alt'], quote=True) + '" width="768" height="512" decoding="async" ' + load + '></a><div class="blog-card-body"><span class="eyebrow">' + escape(item['category']) + '</span><h2>' + link(item['slug'], item['title']) + '</h2><p class="blog-date">Published September 27, 2026</p><p>' + escape(item['description']) + '</p><a class="btn btn-primary" href="/' + item['slug'] + '">Read Guide</a></div></article>')
batch_marker = '<!-- Guides published 2026-09-27 -->'
if batch_marker not in blog:
    blog = blog.replace('loading="eager" fetchpriority="high"', 'loading="lazy"')
    anchor = '<div class="container blog-list">'
    if blog.count(anchor) != 1: raise ValueError('Missing blog list')
    blog = blog.replace(anchor, anchor + '\n' + batch_marker + '\n' + '\n'.join(cards), 1)
    latest = {'@context':'https://schema.org', '@type':'ItemList', 'name':'RP label guides published September 27, 2026', 'itemListElement':[
        {'@type':'ListItem','position':i+1,'name':a['title'],'url':BASE+'/'+a['slug']} for i,a in enumerate(items)]}
    blog = once_insert(blog, '</head>', structured(latest) + '\n')
    old_img = 'https://rplabels.com/assets/images/digital-vs-flexo-peptide-vial-labels.webp'
    blog = blog.replace(old_img, BASE + '/assets/images/' + items[0]['image'] + '.webp')
blog_path.write_text(blog, encoding='utf-8')

for cat in sorted({a['categoryUrl'] for a in items}):
    path = SITE / (cat + '.html')
    text = path.read_text(encoding='utf-8')
    text = once_insert(text, '</head>', css + '\n')
    addition = '<section class="recent-guide-links"><div class="container"><h2>Production and Purchasing Guides</h2>' + ''.join(link(a['slug'], a['title']) for a in items if a['categoryUrl'] == cat) + '</div></section>\n'
    text = once_insert(text, '</main>', addition)
    path.write_text(text, encoding='utf-8')

path = SITE / 'site-map.html'
text = path.read_text(encoding='utf-8')
addition = '<article class="sitemap-card"><h2>New Guides: September 27, 2026</h2>' + ''.join(link(a['slug'],a['title']) for a in items) + '</article>'
anchor = '<div class="container sitemap-grid">'
if addition not in text:
    if text.count(anchor) != 1: raise ValueError('Missing HTML sitemap grid')
    text = text.replace(anchor, anchor + '\n' + addition, 1)
path.write_text(text, encoding='utf-8')

path = SITE / 'llms.txt'
text = path.read_text(encoding='utf-8')
addition = '\nGuides published September 27, 2026:\n' + '\n'.join('- ' + a['title'] + ': ' + BASE + '/' + a['slug'] for a in items) + '\n'
if addition not in text: text += addition
path.write_text(text, encoding='utf-8')

path = SITE / 'sitemap.xml'
ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('', ns)
tree = ET.parse(path)
root = tree.getroot()
existing = {u.find('{' + ns + '}loc').text: u for u in root}
for slug in ['blog','site-map'] + sorted({a['categoryUrl'] for a in items}):
    existing[BASE + '/' + slug].find('{' + ns + '}lastmod').text = DATE
for a in items:
    url = BASE + '/' + a['slug']
    if url not in existing:
        element = ET.SubElement(root, '{' + ns + '}url')
        for tag,value in [('loc',url),('lastmod',DATE),('changefreq','monthly'),('priority','0.8')]:
            ET.SubElement(element, '{' + ns + '}' + tag).text = value
# Preserve the repository's compact one-URL-per-line XML layout.
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="' + ns + '">\n'
for u in root:
    xml += '  <url>' + ''.join('<' + c.tag.split('}')[-1] + '>' + escape(c.text or '') + '</' + c.tag.split('}')[-1] + '>' for c in u) + '</url>\n'
path.write_text(xml + '</urlset>\n', encoding='utf-8')
print('Built five articles and updated blog, category links, llms.txt and sitemaps.')
