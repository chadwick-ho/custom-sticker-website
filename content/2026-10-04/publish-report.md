# RP Labels publishing record - 2026-10-04

Content commit: `1e016e8c5d626309c5d0adb39df6172f22f1dce2`

| Title | Canonical URL | Public verification |
| --- | --- | --- |
| Screw-Cap vs Crimp Vials: Do Not Reuse the Same Peptide Label Dieline | https://rplabels.com/screw-cap-vs-crimp-vial-label-layout | HTTP 200; title and canonical match |
| Preprinted Peptide Vial Labels: Test the Thermal-Transfer Lot Window | https://rplabels.com/peptide-vial-label-thermal-transfer-overlaminate-proof | HTTP 200; title and canonical match |
| Powder Supplement Tub Labels: Size the Front and Facts Panels on the Real Tub | https://rplabels.com/powder-supplement-tub-label-panel-layout | HTTP 200; title and canonical match |
| Supplement Pouch Labels: Keep Required Copy Clear of the Zipper and Seals | https://rplabels.com/supplement-pouch-label-zipper-facts-clearance | HTTP 200; title and canonical match |
| Holographic QR Labels on Automatic Lines: Specify the Roll and Sensor Test | https://rplabels.com/holographic-qr-label-automatic-applicator-roll-sensor | HTTP 200; title and canonical match |

## Deployment and checks

- GitHub `main` received the content commit. Vercel reported `success` for [the deployment](https://vercel.com/chadwick-hos-projects/custom-sticker-website/J9eayvEbrSfM5wgonTfxdGdtqxcz). The public custom domain also served all five exact new pages, so publication does not rely only on Vercel status.
- All five full WebP images and five thumbnails returned HTTP 200 with `image/webp`; live blog and sitemap contained all five new URLs. The live sitemap had 123 unique URLs.
- `py scripts/check-guides-20261004.py`: five pages passed, including local links, assets, Article/Breadcrumb JSON-LD, canonical and hub links.
- `py scripts/audit-static-seo.py`: 0 errors and 0 warnings across 123 sitemap URLs. `py scripts/check-whatsapp-links.py`: 701 CTAs across 128 pages passed. `node --test scripts/quote-tools.test.cjs`: four tests passed. `git diff --check`: passed.
- Desktop and 390px mobile screenshots were inspected for article image loading, legibility and overflow. Blog mobile first screen showed the new first image.
- The existing `Submit-IndexNow.ps1` script submitted five new and five updated canonical URLs. IndexNow returned HTTP 200 and `UrlCount=10`; this acknowledges receipt, not Google/Bing indexing.

## Editorial and image scope

- Each guide addresses a separate buyer decision and cites primary sources from FDA, DWK, HERMA, Avery Dennison or GS1 as relevant. Scenarios are practical guidance, not reported RP factory tests or customer cases.
- Five original photographic-style AI-generated illustrations and ten optimized WebP assets were saved under `custom-labels-stickers-website/assets/images/`, using each manifest `image` name for full and `-thumb` files. Captions identify fictional formula, lot and QR artwork where applicable. No third-party watermarked source images were used.
- Image prompts covered: screw-cap versus crimp vial geometry; thermal-transfer lot printing on finished custom vial labels; powder tub front/Facts wrap layout; supplement pouch zipper/Facts clearance; and holographic QR rolls passing an automatic applicator sensor. The available official built-in image-generation tool did not disclose its exact model version, so Image 2.5 cannot be confirmed.
- The earlier 50-topic planning list was not found in the accessible repository. Existing sitemap guide slugs and recent batches were checked to avoid duplicate topics. No unrelated user changes were overwritten.
