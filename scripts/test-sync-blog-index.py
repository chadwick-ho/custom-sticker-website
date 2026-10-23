"""Regression checks for duplicate archive entries after article updates."""
import json
import runpy
import tempfile
import unittest
from pathlib import Path

from bs4 import BeautifulSoup

TOOLS = runpy.run_path(str(Path(__file__).with_name('sync-blog-index.py')))


def card(slug='sample', classes='blog-card blog-photo-card', title='Old heading'):
    return (f'<article class="{classes}"><a href="/{slug}"><img src="assets/images/old-thumb.webp" '
            'alt="Old illustration" loading="eager" fetchpriority="high"></a><div class="blog-card-body">'
            f'<h2><a href="/{slug}">{title}</a></h2><p class="blog-date">Published October 1, 2026</p>'
            '<p>Old summary</p></div></article>')


class ArchiveTests(unittest.TestCase):
    def test_update_replaces_extra_classes_and_removes_duplicate_only(self):
        original = '<div class="container blog-list">' + card() + card('other') + card(classes='blog-card') + '</div>'
        updated = TOOLS['upsert_card'](original, card(title='Approved heading'))
        soup = BeautifulSoup(updated, 'html.parser')
        self.assertEqual(len(soup.select('article')), 2)
        self.assertEqual(soup.select_one('h2').get_text(), 'Approved heading')
        self.assertIsNotNone(soup.select_one('h2 a[href="/other"]'))
        self.assertEqual(TOOLS['upsert_card'](updated, card(title='Approved heading')), updated)

    def test_new_url_inserted_once_when_container_has_extra_classes(self):
        original = '<div id="guides" class="container blog-list additional">' + card('other') + '</div>'
        updated = TOOLS['upsert_card'](original, card())
        self.assertEqual(len(BeautifulSoup(updated, 'html.parser').select('article')), 2)
        self.assertEqual(TOOLS['upsert_card'](updated, card()), updated)

    def test_sync_preserves_dates_links_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as folder:
            site = Path(folder)
            schema = {'@type': 'Article', 'datePublished': '2026-10-01', 'dateModified': '2026-10-23'}
            (site / 'sample.html').write_text('<head><link rel="canonical" href="https://rplabels.com/sample">'
                '<meta name="description" content="New decision summary">'
                '<script type="application/ld+json">' + json.dumps(schema) + '</script></head>'
                '<main><h1>Approved heading</h1><img src="/assets/images/rp-new.webp" '
                'alt="RP illustrated packaging" width="1536" height="1024"></main>', encoding='utf-8')
            archive_schema = {'@type': 'Blog', 'blogPost': [{'url': 'https://rplabels.com/sample', 'headline': 'Old heading'}]}
            original = '<script type="application/ld+json">' + json.dumps(archive_schema) + '</script>' + card() + card(classes='blog-card')
            updated, report = TOOLS['synchronize'](original, site)
            soup = BeautifulSoup(updated, 'html.parser')
            self.assertEqual(len(soup.select('article')), 1)
            self.assertEqual(report['unique_articles'], 1)
            self.assertEqual(soup.h2.get_text(), 'Approved heading')
            self.assertEqual(soup.img['src'], '/assets/images/rp-new.webp')
            self.assertEqual(soup.select_one('.blog-date').get_text(), 'Published October 1, 2026 · Updated October 23, 2026')
            self.assertIn('href="/sample"', updated)
            self.assertFalse(TOOLS['synchronize'](updated, site)[1]['changed'])


if __name__ == '__main__':
    unittest.main()
