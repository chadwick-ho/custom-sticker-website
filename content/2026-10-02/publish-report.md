# RP Labels publishing record - 2026-10-02

Content commit: `8f9fc5f629aabda20b2b75a5ad29f4625ea376e0`

| Title | Intended canonical URL | Public status at verification |
| --- | --- | --- |
| Peptide Vial Barcodes on Curved Glass: Choose Orientation by Scan Test | https://rplabels.com/peptide-vial-linear-barcode-curved-surface | Not live (404) |
| Peptide Vial DataMatrix or QR Code? Start With the Scanner | https://rplabels.com/peptide-vial-datamatrix-vs-qr-scan-workflow | Not live (404) |
| Supplement Label Ingredients and Allergen Copy: Reserve the Right Panel Space | https://rplabels.com/supplement-ingredients-allergen-panel-proof | Not live (404) |
| Supplement Bottle Labels: Who Goes on the Business Name and Address Line? | https://rplabels.com/supplement-label-business-address-information-panel | Not live (404) |
| Hologram Seals for Folding Cartons: Design the Perforation Around the Opening | https://rplabels.com/hologram-carton-seal-perforation-tear-path | Not live (404) |

## Completed in repository

- Five distinct English buyer guides, each with a photographic-style AI-generated branded image and an optimized WebP thumbnail. The available image tool did not disclose its exact model version, so Image 2.5 cannot be confirmed. Captions clearly identify illustrative artwork, not verified factory tests or approved legal copy.
- Blog, three product-category hubs, `site-map.html`, `sitemap.xml`, and `llms.txt` updated. Each guide includes a unique title and description, H1/H2, canonical, Article and Breadcrumb JSON-LD, image alt text, internal links, a quote CTA, and linked primary sources.
- `py scripts/check-guides-20261002.py`: passed for five pages and 113 unique sitemap URLs. `py scripts/audit-static-seo.py`: 0 errors, 0 warnings.
- `py scripts/check-whatsapp-links.py`: 681 CTAs across 118 pages passed. `node --test scripts/quote-tools.test.cjs`: four tests passed. `git diff --check`: passed.
- Local HTTP checks: all five pages, full images, and thumbnails returned 200. Desktop and 390px mobile preview showed image loading and no horizontal overflow.
- Content commit pushed to GitHub `main`; Vercel status reported success for deployment `6799119101`.

## Public deployment blocker

On October 2, `https://rplabels.com/` returned 403. The blog, sitemap, five new guide paths, and a new image returned 404. DNS resolved the apex to `91.108.100.169` and `77.37.48.149`, with `www` pointing to `www.rplabels.com.cdn.hstgr.net`; the custom domain is still routed to Hostinger, not this Vercel deployment. The Vercel deployment URL redirected to a login page, so it is not a public substitute.

The apex and `www` records should be reconciled with the exact values in this Vercel project's Domains settings while preserving email and verification records. No DNS changes were made. Do not call these articles live or submit IndexNow until the public canonical URLs and assets return the expected pages. IndexNow was not submitted.

The earlier 50-topic planning list was not found in the accessible repository. Existing guide slugs and recent batches were checked to avoid duplication. No unrelated user changes were overwritten.
