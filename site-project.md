# RP Labels site project

Updated: 2026-10-20. This file records working context, not confidential access details.

## Daily publishing authorization and current batch

On 2026-10-20 the user explicitly changed the recurring task to a target of 50 distinct English B2B SEO articles with matched images per daily execution, authorizing publication through this repository and the existing deployment route. This supersedes the earlier draft-only daily-article restriction. Keep the existing 23:30 Asia/Shanghai trigger. Only count distinct live URLs after checking the deployed article and assets; report new pages and substantive existing-page updates separately. Do not create synonymous pages, recycle the same advice under different keywords, or lower image/readability checks to reach the number. The original 30-item plan is a candidate pool, not 50 completed articles. No paid-service purchases or unrelated site changes are authorized by this instruction.

The first 2026-10-20 publication candidate updates the existing low-MOQ supplement guide with a buyer quantity-versus-quoted-quantity decision, an explicit 500-to-650 hypothetical scenario, differing buyer conditions, a matched RP illustration and usable quote-sheet downloads. It preserves the original URL and original publication date. Local checks include the sitemap SEO audit with omitted unchanged image paths verified in the sparse Git tree, physical new-image decoding, and desktop/mobile previews. Confirm production deployment before recording it as live.

## Confirmed project facts

- Site: https://rplabels.com/; English B2B custom-label website.
- Source: `custom-labels-stickers-website/` in GitHub repository `chadwick-ho/custom-sticker-website`; local checkout is a static HTML/CSS/JS site.
- Main product entry points: `/custom-peptide-vial-labels`, `/custom-supplement-labels`, `/custom-3d-holographic-labels`.
- Conversion routes: `/contact` and the site's WhatsApp quote links.
- First-party search baseline and its limitations: [precision-buyer-brief.md](content/strategy/precision-buyer-brief.md). The GSC export is a dated snapshot, not a measure of qualified leads.

## Working positioning hypothesis

Primary test: small supplement brands preparing their first bottle/jar label run or adding several formulas, flavors or counts. The buyer may be an owner, brand manager or packaging coordinator; the observable fit is a real pack, per-design quantity and a route to approving product copy. Research-vial and hologram/QR projects remain specialist paths. This is a positioning hypothesis, not a proven conversion result; see [primary-buyer-positioning-2026-10-17.md](content/strategy/primary-buyer-positioning-2026-10-17.md).

## Content architecture decisions

| Intent cluster | Primary URL | Supporting task pages | Next step |
| --- | --- | --- | --- |
| Buy custom supplement labels | `/custom-supplement-labels` | Bottle fit, facts-panel space, barcode quality and SKU variants | Measure quote inquiries from this category. |
| Buy custom peptide vial labels | `/custom-peptide-vial-labels` | Vial size, application temperature, roll fit and SKU control | Separate commercial buyers from informational size-chart readers. |
| Buy hologram or QR security labels | `/custom-3d-holographic-labels` | Seal substrate, scan contrast and verification workflow | Do not imply a printed QR code includes an authentication service. |

Use one primary URL per buying intent. Add a new guide only for a distinct decision; update an existing guide when the task overlaps. Keep all relevant support links discoverable from the corresponding category without repeating identical page headings.

## Decisions and evidence

| Date | Decision | Status | Evidence / review condition |
| --- | --- | --- | --- |
| 2026-10-17 | Prioritize small-brand packaging decisions over broad label traffic. | Hypothesis | GSC export and buyer-question examples in the buyer brief; review against qualified inquiries. |
| 2026-10-17 | Consolidate repeated category guide bands into a single navigable guide hub per product category. | Deployed in commit `385461b` | Each category page had 15 identical guide headings. All 27, 30 and 18 existing guide links were preserved; local desktop and 390px mobile checks found no horizontal overflow. |
| 2026-10-17 | Test a smaller, task-defined supplement buyer segment on the homepage and category route. | Deployed in commit `78ebc36` | GSC export shows commercial supplement queries and a supplement category page with impressions but no clicks in the dated export. Review qualified inquiries and progress to proof/quote before keeping or reversing this emphasis. |

## Work log

| Date | Work | Verification | Remaining |
| --- | --- | --- | --- |
| 2026-10-18 | Prepared SEO metadata and responsive hero-image changes after a read-only xiangyu-search-seo-cli 2.8.3 audit. Canonical sitemap pages now include sharing URL/type/site name and a consistent RP organization reference/logo where applicable. Refined the supplement title and two descriptions. Added 11 WebP image variants for the homepage and three category heroes, with matching responsive preloads. | Live baseline: all 158 sitemap URLs returned 200; CLI reported no canonical/noindex conflicts or sitemap-graph orphans. Local source audit: 158 URLs, 0 errors/warnings; sparse checkout image references checked against the tracked Git tree. Existing quote-tool tests: 5 passed. Four category/home previews at 390px loaded the responsive heroes without horizontal page overflow. | Prepared on a review branch; not deployed. PageSpeed anonymous API returned 429, so no CWV improvement claim. Review metadata and image changes, deploy, then recheck the live pages. |
| 2026-10-17 | Built three category guide hubs, cleaned duplicate CSS loads, and added `scripts/organize-category-guides.py` for future article batches. | Static SEO audit: 158 sitemap URLs, 0 errors and 0 warnings. Append-and-rerun test passed. | Confirm production deployment and monitor inquiries. |
| 2026-10-17 | Aligned homepage, products, supplement category and contact brief to the primary supplement-buyer test while keeping vial and hologram routes. Added the first-run decision path and text/code approval stage. | Static SEO audit: 158 URLs, 0 errors/warnings; quote-tool tests: 5 passed. Local desktop/mobile preview: no horizontal overflow; quote preselection and brief generation worked. Live pages and hero image returned 200; IndexNow accepted 4 canonical URLs. | Compare qualified inquiries, not clicks alone. |

## Next review

Compare GSC queries and landing pages with inquiry briefs (product, container, SKU count, quantity per design, and application method). Refresh older high-intent pages before publishing a near-synonym article. Do not infer conversion, ranking improvement or Google indexing from a successful deployment.
After adding category-page guide links in a content batch, run `python scripts/organize-category-guides.py` and `python scripts/audit-static-seo.py` before publishing; the latter rejects repeated category guide sections.
