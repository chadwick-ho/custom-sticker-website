# RP Labels publishing record - 2026-10-06

Content commit: `162e05c` (pushed to `main`). GitHub reported the [Vercel deployment](https://vercel.com/chadwick-hos-projects/custom-sticker-website/CLTaxT2CmAY9LB2Avc2qJF7nzdBC) as successful. The public custom domain was checked independently.

| Title | Live canonical URL |
| --- | --- |
| Peptide Vial Labels with Detachable Record Tabs: Proof Both Identities | https://rplabels.com/peptide-vial-detachable-record-tab-label-proof |
| Peptide Vial Labels with a Clear Viewing Window: Keep the Vial Inspectable | https://rplabels.com/peptide-vial-label-clear-viewing-window-layout |
| Supplement Label Claims: Freeze Reviewed Copy Before You Print | https://rplabels.com/supplement-label-claims-copy-prepress-review |
| Supplement Facts on Dark Bottles: Proof the Opaque Information Panel | https://rplabels.com/supplement-facts-dark-bottle-opaque-panel-proof |
| Hologram Labels with Scratch-Off Codes: Specify the Data Handoff | https://rplabels.com/hologram-scratch-off-code-data-handoff |

## Verification

- Each of the five live pages returned HTTP 200 and contained its expected title and canonical. All five full-size images and five thumbnails returned HTTP 200 with `image/webp`. Live blog and sitemap contained all five slugs.
- `py scripts/check-guides-20261006.py`: five pages passed, including H1, canonical, Article and BreadcrumbList JSON-LD, alt text, local links/assets and hub links; page word counts were 957, 927, 914, 899 and 922. The local sitemap contains 133 unique URLs.
- `py scripts/audit-static-seo.py`: 0 errors and 0 warnings across 133 URLs. `py scripts/check-whatsapp-links.py`: 721 CTAs across 138 pages passed. `node --test scripts/quote-tools.test.cjs`: four tests passed. `git diff --check`: passed.
- Chromium screenshots of a desktop article, a 390px mobile article and the mobile blog entry were inspected for layout, legibility and image loading. The temporary local server requires `.html` paths; the live host serves canonical clean URLs.
- `Submit-IndexNow.ps1` submitted the five new pages plus blog, HTML sitemap and three category hubs. IndexNow returned HTTP 200 and `UrlCount=10`; receipt does not guarantee indexing.

## Editorial and image scope

- Five distinct purchasing decisions were checked against the existing 128 sitemap URLs. Technical/regulatory points link to primary HERMA, Avery Dennison, FDA and GS1 sources. No RP factory test result, customer story, certification or regulatory approval was invented.
- Five original photographic-style AI illustrations were visually inspected, including replacement of an image that falsely suggested final artwork approval and another whose demo serial/code sheet did not match. Labels show complete original RP Research, RP Wellness and RP Secure designs rather than blank stock. Captions identify fictional formulas, lots and demo codes; no image proves compliance, scan success, optical performance or security.
- The official built-in image generation tool did not expose an exact model version, so Image 2.5 cannot be confirmed. No third-party watermarked source image was used.
- The previously discussed 50-topic source list was not found in the accessible repository. Existing sitemap pages and recent batches were checked to avoid duplicate topics. No unrelated or concurrent user changes were overwritten.
