# RP Labels technical SEO follow-up - 2026-10-01

Scope: the 108 canonical URLs in `custom-labels-stickers-website/sitemap.xml`, plus the currently reachable public host. This follows the crawl/index, internal-link, on-page, and structured-data priorities in the supplied SEO reference folder.

## P0: Public domain routing blocks crawling

Observed on October 1: `https://rplabels.com/` and `https://www.rplabels.com/` returned 403, while `/robots.txt` and `/sitemap.xml` returned 404. Response headers showed `platform: hostinger` and `Server: hcdn`, not the GitHub-linked Vercel site. A successful Vercel deployment cannot be treated as publication on this domain. No DNS or security settings were changed.

Next action: compare the domain's apex A and `www` CNAME records in the Hostinger DNS panel with the exact records in the Vercel project's Domains panel. Preserve all email MX/TXT and verification records. After propagation, verify the home page, robots.txt, sitemap, representative product/category/article pages, their images, and canonical redirects. Only then submit live URLs to IndexNow and inspect them in Google Search Console. IndexNow acceptance does not guarantee Google indexing.

## Code fixes made

- Removed 59 FAQPage JSON-LD blocks whose questions or answers did not match text visible on those pages. Existing article, service, organization, and breadcrumb data remained intact. The dedicated FAQ page's shipping answer was aligned with its visible copy.
- Removed the homepage Organization `sameAs` value that pointed back to the same site's own URL instead of a verified external profile.
- Added a whole-site audit command, `py scripts/audit-static-seo.py`, checking sitemap targets, title/description/canonical/H1/noindex, JSON-LD syntax and FAQ content parity, local images and links, duplicate metadata, and inlinks. Added a dry-run-first cleanup command for inaccurate FAQ markup.

## Verification

- `py scripts/audit-static-seo.py`: 108 sitemap URLs; 0 local errors and 0 warnings after fixes.
- `py scripts/remove-inaccurate-faq-schema.py`: 0 remaining changes (idempotent).
- `py scripts/check-guides-20261001.py`: passed all five October 1 guides.
- `py scripts/check-whatsapp-links.py`: passed 671 CTAs across 113 pages.
- `node --test scripts/quote-tools.test.cjs`: four tests passed.
- The live-domain 403/404 issue remains outside this repository. No claim of restored crawling, indexing, rankings, or rich results is made.

Reference: [Google's general structured-data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) require marked-up information to reflect user-visible page content.
