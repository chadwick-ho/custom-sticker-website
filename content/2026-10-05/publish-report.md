# RP Labels publishing record - 2026-10-05

Content commit: `afb5004` (pushed to `main`). GitHub reported the Vercel check as [success](https://vercel.com/chadwick-hos-projects/custom-sticker-website/GsTEGs8WbWeZaN7nEWDhh7S4QrWy). The custom domain returned Hostinger headers and served all five new pages, so live verification was performed against `rplabels.com` directly rather than inferred from the Vercel check.

| Title | Live canonical URL |
| --- | --- |
| Peptide Vial Labels in Trays: Test Scuffing Before You Order the Roll | https://rplabels.com/peptide-vial-label-tray-friction-scuff-proof |
| Peptide Vial Labels for Camera Inspection: Approve the Applied View | https://rplabels.com/peptide-vial-label-camera-inspection-orientation-proof |
| Supplement Stick Packs and Cartons: Decide Which Copy Lives Where | https://rplabels.com/supplement-stick-pack-carton-label-hierarchy |
| Supplement Labels: Leave a Real Place for Net Contents on the Front | https://rplabels.com/supplement-label-net-contents-front-panel-proof |
| Hologram Plus QR Labels: Give Visual and Digital Checks Separate Jobs | https://rplabels.com/hologram-label-visual-authentication-vs-qr-check |

## Verification

- Each live page returned HTTP 200 and contained its expected unique title and canonical. Each full-size WebP and thumbnail returned HTTP 200 with `image/webp`. Live blog and sitemap included all five slugs; sitemap has 128 unique URLs locally.
- `py scripts/check-guides-20261005.py`: five articles passed, including JSON-LD Article and BreadcrumbList, alt text, local assets and links, canonical, hub links and word count.
- `py scripts/audit-static-seo.py`: 0 errors, 0 warnings across 128 sitemap URLs. `py scripts/check-whatsapp-links.py`: 711 CTAs across 133 pages passed. `node --test scripts/quote-tools.test.cjs`: four tests passed. `git diff --check`: passed.
- Chromium desktop and 390px mobile screenshots were visually inspected for article and blog first-screen layout. The local static server needs `.html` paths, while the public host serves canonical clean URLs.
- Existing `Submit-IndexNow.ps1` submitted the five new pages plus blog, HTML sitemap and three category hubs. IndexNow returned HTTP 200 and `UrlCount=10`; this is receipt, not a search-indexing guarantee.

## Editorial and image scope

- The articles cover five distinct buying decisions and cite relevant primary FDA, HERMA, Avery Dennison and GS1 references. They do not claim RP factory test results, specific customer cases, certifications or regulatory approval.
- Five original AI-generated, photographic-style illustrations were visually inspected and optimized into ten WebP assets. Labels show original RP Research, RP Wellness and RP Secure designs with icons and plausible packaging structure. Formulas, Facts figures, lot fields and QR art in the images are fictional and explicitly qualified in captions; none is proof of compliance or scan performance. No third-party watermarked image was used.
- The built-in official image generation tool did not disclose its exact model version. Image 2.5 therefore cannot be confirmed, despite the requested visual style being produced.
- The earlier 50-topic planning list was not found in the accessible repository. The 123 previously published sitemap URLs and recent batches were used to avoid duplicate topics. No unrelated or parallel user changes were overwritten.
