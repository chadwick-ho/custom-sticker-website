# RP Labels publishing record - 2026-10-01

Content commit: `6fc1b53a07ace18975483cb7d448dcf6b360a7d5`

| Title | Intended canonical URL | Public status at verification |
| --- | --- | --- |
| Peptide Vial Label Revisions: Keep Old and New Rolls Apart | https://rplabels.com/peptide-vial-label-artwork-version-changeover | Not live (404) |
| Peptide Vial Label Height: Leave the Cap, Shoulder and Viewing Area Clear | https://rplabels.com/peptide-vial-label-cap-shoulder-clearance | Not live (404) |
| Supplement Bottle Front Panels: Reserve Identity and Net Quantity First | https://rplabels.com/supplement-label-front-panel-identity-net-quantity | Not live (404) |
| Supplement Label Barcodes: Do Flavor and Count Variants Need Separate GTINs? | https://rplabels.com/supplement-sku-gtin-flavor-count-labels | Not live (404) |
| Hologram Seals on Curved Bottle Caps: Test the Fold Before Ordering | https://rplabels.com/hologram-seal-curved-bottle-cap-adhesion | Not live (404) |

## Completed in repository

- Five new English guides and five photographic-style AI-generated illustrations, each exported as a full WebP and thumbnail. The built-in image tool did not disclose its exact model version, so Image 2.5 cannot be independently confirmed. Captions disclose illustrative samples rather than verified factory output.
- Blog index, three product-category hubs, `site-map.html`, `sitemap.xml`, and `llms.txt` updated. Each page has a unique title, description, H1, canonical, Article and Breadcrumb structured data, relevant internal links, image alt text, and a quote CTA.
- `py scripts/check-guides-20261001.py`: passed for all five pages and 108 unique sitemap URLs.
- `py scripts/check-whatsapp-links.py`: passed for 671 CTAs across 113 pages.
- `node --test scripts/quote-tools.test.cjs`: four tests passed.
- Desktop and 390px mobile preview inspected; article images loaded and no horizontal overflow was observed. Git diff checks passed.
- Content commit was pushed to GitHub `main`. GitHub's Vercel deployment status reported success (deployment 6773814743).

## Public deployment blocker

The canonical domain is currently served by Hostinger (`platform: hostinger`, `Server: hcdn`) instead of the Vercel deployment. On October 1, `https://rplabels.com/sitemap.xml` and the new article paths returned 404; the root returned 403. The Vercel deployment preview URL redirected to a Vercel login page, so it cannot be used to prove public availability. GitHub/Vercel build success is **not** equivalent to publication on `rplabels.com`.

The domain's apex A and `www` CNAME records must be checked against the exact values in this Vercel project's Domains settings, while preserving MX/TXT records for email and verification. No DNS changes were made in this run. Recheck the five canonical pages, images, blog, and sitemap after domain routing is fixed.

IndexNow was **not submitted** because the canonical URLs and sitemap were not live. Submit only after public HTTP verification succeeds. IndexNow acceptance does not guarantee crawling or Google index inclusion.

The previously discussed 50-topic source list was not found in the accessible repository; existing published slugs and recent batches were checked for duplication. No unrelated or user-authored changes were overwritten.
