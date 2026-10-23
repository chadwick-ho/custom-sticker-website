"""Keep the static blog archive aligned with existing canonical article pages.

Run without --check to repair; --check is a read-only publication gate.
No article body, canonical URL or article publication date is changed.
"""
import argparse
import datetime as dt
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

SITE = Path(__file__).resolve().parents[1] / 'custom-labels-stickers-website'
ORIGIN = 'https://rplabels.com'
CARD = re.compile(r'<article\b[^>]*>.*?</article>', re.S | re.I)
LD = re.compile(r'(<script\b[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>)(.*?)(</script>)', re.S | re.I)


def clean(value):
    return ' '.join(value.split())


def canonical(href):
    parsed = urlparse(urljoin(ORIGIN + '/', href))
    if parsed.netloc != 'rplabels.com':
        raise ValueError(f'Unexpected external archive target: {href}')
    return ORIGIN + parsed.path.removesuffix('.html').rstrip('/')


def schemas(soup):
    result = []
    def walk(value):
        if isinstance(value, dict):
            kind = value.get('@type', [])
            if any(k in (kind if isinstance(kind, list) else [kind]) for k in ['Article', 'BlogPosting']):
                result.append(value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    for tag in soup.select('script[type="application/ld+json"]'):
        walk(json.loads(tag.string or tag.get_text()))
    return result


def get_article(site, url):
    file = site / (urlparse(url).path.strip('/') + '.html')
    soup = BeautifulSoup(file.read_text(encoding='utf-8'), 'html.parser')
    assert len(soup.select('h1')) == 1, url
    assert canonical(soup.select_one('link[rel=canonical]')['href']) == url, url
    description = soup.select_one('meta[name=description]')['content']
    image = soup.select_one('main img')
    data = next((x for x in schemas(soup) if canonical(x.get('mainEntityOfPage', url) if isinstance(x.get('mainEntityOfPage', url), str) else url) == url), {})
    return {'title': clean(soup.h1.get_text(' ', strip=True)), 'description': description,
            'image': dict(image.attrs) if image else None,
            'datePublished': data.get('datePublished'), 'dateModified': data.get('dateModified')}


def format_date(value):
    return dt.date.fromisoformat(value[:10]).strftime('%B %d, %Y').replace(' 0', ' ')


def upsert_card(text, new_card):
    """Replace all class variants of one URL, or insert a new card once."""
    incoming = BeautifulSoup(new_card, 'html.parser').select_one('article.blog-card')
    url = canonical(incoming.select_one('h2 a')['href'])
    found = False
    def replace(match):
        nonlocal found
        card = BeautifulSoup(match[0], 'html.parser').select_one('article.blog-card')
        link = card.select_one('h2 a[href]') if card else None
        if not link or canonical(link['href']) != url:
            return match[0]
        if found:
            return ''
        found = True
        return new_card
    updated = CARD.sub(replace, text)
    if not found:
        soup = BeautifulSoup(updated, 'html.parser')
        container = soup.select_one('.blog-list')
        assert container is not None, 'Blog list container is missing'
        # The existing opening element is stable; avoid serializing the document.
        opening = str(container).split('>', 1)[0] + '>'
        exact = re.search(r'<div\b[^>]*class=[\"\'][^\"\']*\bblog-list\b[^\"\']*[\"\'][^>]*>', updated)
        assert exact is not None, opening
        updated = updated[:exact.end()] + '\n' + new_card + updated[exact.end():]
    return updated


def synchronize(text, site=SITE):
    seen = set()
    entries = {}
    changes = []
    duplicates = []
    position = 0

    def replace_card(match):
        nonlocal position
        soup = BeautifulSoup(match[0], 'html.parser')
        card = soup.select_one('article.blog-card')
        if card is None:
            return match[0]
        link = card.select_one('h2 a[href]')
        assert link is not None, 'Blog card has no heading link'
        url = canonical(link['href'])
        if url in seen:
            duplicates.append(url)
            return ''
        seen.add(url)
        entry = get_article(site, url)
        entries[url] = entry
        reasons = []
        if clean(link.get_text(' ', strip=True)) != entry['title']:
            link.string = entry['title']
            reasons.append('title')
        body = card.select_one('.blog-card-body') or card
        excerpt = next((p for p in body.find_all('p', recursive=False) if 'blog-date' not in p.get('class', [])), None)
        if excerpt is not None and clean(excerpt.get_text(' ', strip=True)) != clean(entry['description']):
            excerpt.string = entry['description']
            reasons.append('description')
        date = card.select_one('.blog-date')
        if date is not None and entry['datePublished']:
            value = 'Published ' + format_date(entry['datePublished'])
            if entry['dateModified'] and entry['dateModified'][:10] != entry['datePublished'][:10]:
                value += ' · Updated ' + format_date(entry['dateModified'])
            if clean(date.get_text()) != value:
                date.string = value
                reasons.append('date')
        image = card.find('img')
        hero = entry['image']
        if image is not None and hero:
            # Existing purpose-made thumbnails remain valid for unchanged artwork.
            # New packet images have a content ID, so the old thumbnail is stale.
            hero_src = hero.get('src', '')
            old_src = image.get('src', '')
            expected_thumb = hero_src.rsplit('.', 1)[0] + '-thumb.' + hero_src.rsplit('.', 1)[-1]
            if urljoin(ORIGIN + '/', old_src) not in [urljoin(ORIGIN + '/', hero_src), urljoin(ORIGIN + '/', expected_thumb)]:
                for attr in ['src', 'alt', 'width', 'height']:
                    if attr in hero:
                        image[attr] = hero[attr]
                for attr in ['srcset', 'sizes']:
                    image.attrs.pop(attr, None)
                reasons.append('image')
            desired = 'eager' if position == 0 else 'lazy'
            if image.get('loading') != desired:
                image['loading'] = desired
                reasons.append('loading')
            if position == 0:
                if image.get('fetchpriority') != 'high':
                    image['fetchpriority'] = 'high'
                    reasons.append('priority')
            elif 'fetchpriority' in image.attrs:
                image.attrs.pop('fetchpriority')
                reasons.append('priority')
            image['decoding'] = 'async'
        position += 1
        if reasons:
            changes.append({'url': url, 'fields': reasons})
            return str(card)
        return match[0]

    updated = CARD.sub(replace_card, text)
    schema_changes = []
    def replace_schema(match):
        data = json.loads(match[2])
        original = json.dumps(data, sort_keys=True)
        def walk(value):
            if isinstance(value, dict):
                if value.get('@type') == 'Blog' and 'blogPost' in value:
                    unique = []
                    used = set()
                    for post in value['blogPost']:
                        url = canonical(post['url'])
                        if url in used:
                            schema_changes.append({'url': url, 'field': 'duplicate_blogPost'})
                            continue
                        used.add(url)
                        entry = entries.get(url)
                        if entry:
                            for key in ['headline', 'description', 'datePublished', 'dateModified']:
                                wanted = entry['title'] if key == 'headline' else entry.get(key)
                                if wanted and post.get(key) != wanted:
                                    post[key] = wanted
                                    schema_changes.append({'url': url, 'field': key})
                        unique.append(post)
                    value['blogPost'] = unique
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)
        walk(data)
        if json.dumps(data, sort_keys=True) == original:
            return match[0]
        return match[1] + json.dumps(data, ensure_ascii=False) + match[3]
    updated = LD.sub(replace_schema, updated)
    return updated, {'unique_articles': len(seen), 'duplicate_cards_removed': duplicates,
                     'changed_cards': changes, 'schema_changes': schema_changes,
                     'changed': updated != text}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Report drift without editing the blog')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    file = SITE / 'blog.html'
    text = file.read_text(encoding='utf-8')
    updated, report = synchronize(text)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    if report['changed'] and not args.check:
        file.write_text(updated, encoding='utf-8')
    print(json.dumps({'unique_articles': report['unique_articles'], 'duplicates': len(report['duplicate_cards_removed']),
                      'changed_cards': len(report['changed_cards']), 'schema_changes': len(report['schema_changes']),
                      'changed': report['changed'], 'mode': 'check' if args.check else 'sync'}))
    return int(args.check and report['changed'])


if __name__ == '__main__':
    raise SystemExit(main())
