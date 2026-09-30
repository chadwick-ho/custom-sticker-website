# RP Labels publishing record — 2026-09-30

Content commit: `84030b5c8e3c88340965b579caa2e74d1daa0a8a`

| Title | Live URL |
| --- | --- |
| Peptide Vial Labels and Condensation: Apply to Dry Glass, Not a Cold Fog | https://rplabels.com/peptide-vial-condensation-label-application |
| Supplement Facts Panel Space: Set the Dieline Before Styling the Bottle | https://rplabels.com/supplement-facts-panel-dieline-width |
| HDPE Supplement Bottle Labels: Check the Plastic Before Choosing Adhesive | https://rplabels.com/hdpe-supplement-bottle-label-adhesion |
| Hologram Seals on Corrugated Cartons: Test the Tear, Not Just the Shine | https://rplabels.com/hologram-seal-corrugated-carton-fiber-tear |
| Duplicate QR Scans on Security Labels: Write the Response Before Printing | https://rplabels.com/duplicate-scan-qr-security-label-response |

Validation:

- `py scripts/check-guides-20260930.py`: passed, five Article and Breadcrumb JSON-LD pages, one H1 each, canonical, internal links, assets, blog/category/HTML sitemap links, 103 unique XML sitemap URLs. Page word counts: 1054, 979, 895, 915, 965 including layout.
- `py scripts/check-whatsapp-links.py`: passed, 661 calls to action across 108 pages using the latest requested WhatsApp link.
- `node --test scripts/quote-tools.test.cjs`: four tests passed.
- `git diff --check` and `git diff --cached --check`: passed before commit.
- Desktop and 390px mobile browser screenshots of the new article and blog inspected; layout and first image visible without clipping or overlap.
- GitHub `main` received the content commit; GitHub Vercel status: success, "Deployment has completed."
- Live HTTP HEAD: all five article URLs and each full/thumbnail WebP image returned 200. Live blog, HTML sitemap and XML sitemap returned 200 and contain all five slugs.
- IndexNow: HTTP 200 for ten canonical URLs (five new guides, blog, three category pages and HTML sitemap). Receipt is not proof of crawling or Google index inclusion.
- Five photorealistic editorial assets generated with the built-in official image tool; exact model version not disclosed by that tool, so "Image 2.5" cannot be independently confirmed. Images and captions disclose their illustrative status. No third-party watermarks used.

The previously discussed 50-topic source list was not found in the accessible repository, so topic duplication was checked against the site's published article slugs and latest batches. No user-authored files were overwritten outside the dated publishing surfaces.
