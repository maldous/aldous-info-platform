# Validation of the public application

## Later product-source correction (13 November 2026)

This source revision removes maintenance-environment names from current product labels, anchors, local asset names and evidence context links. It fixes the Recruiters-page switch to use click handling, accessible checked state and system/preference synchronization, and updates the generator to retain that markup and script version.

Verified against this corrected source:

- Build produces 52 static files; all current manifest hashes and local asset/module references pass.
- Existing focused product/static/DOM checks and 24 matcher cases pass. Obsolete pre-switch and retired project-status assertions were aligned with the already approved product behavior.
- Real Chromium 157.0.8103.38 passes across all 3 pages and widths 320,390,768,1440: filters, search,94 evidence skills,121-row pagination, safe text, initial system light/dark, system changes and persistent accessible switches on both pages. Search-time network requests: 0.
- Recruiter-page regeneration reproduces the corrected HTML exactly.

This is repository-source validation. The last separately verified live publication remains version 56; no newer Site publication is established by these checks. The dated regression result below describes the earlier source and is retained as history.

## Current version-56 follow-through (13 November 2026)

The runtime baseline is Sites source `03997393bb021ee7bd58b8f77a512120e41bd8f2`, synchronized into this repository at `f0700c824123cbe6c16c6bea6bc3399c76b67b83`. Version 56 publication succeeded at 04:07:50 UTC (15:07:50 AEDT). This documentation/test follow-through changes no application bytes and does not redeploy the site.

- `node test-portfolio.mjs`: passed the updated light/dark switch harness and existing portfolio interactions.
- `python3 test-portfolio.py`: passed after updating obsolete selector/preheading assertions to the actual v56 markup.
- `python3 scripts/check-export.py`: passed all 52 runtime hashes and asset/module references. The current manifest differs from v55 only for the four intended runtime files; the original manifest is retained in the [version-55 export commit](https://github.com/maldous/aldous-info-platform/blob/a8f2451e66bb9cdda7be2386873a0a2a92d2611a/docs/published-assets.sha256.json).
- `npm run build`: passed, producing 52 static files.
- `npm ci --ignore-scripts`: succeeded with the existing lockfile unchanged.
- `CHROMIUM_PATH=/snap/bin/chromium npm run test:browser`: **failed** on the added Recruiters-page switch assertion (`light` remained `light` after a click expected to select `dark`). Homepage system-preference changes, explicit selection, reload persistence and navigation persistence passed before that assertion. The existing responsive/search checks also ran before it. No complete v56 browser pass is claimed.

Source inspection identifies the mismatch: `dist/recruiters.html` now renders a button switch, while `dist/recruiters.mjs` still binds the old selector's `change` event. The new regression assertion is retained. Fixing application/runtime source requires the separate Sites editing scope; this follow-through has not changed it. Historical v55 checks below remain valid for their dated baseline, not as v56 acceptance.

## Historical version-55 validation

Validated on 12 November 2026 against published version 55, source commit `14f65250890867d5981cb5054cc9f596189f666e`.

- All 52 application files match the retained published-source SHA-256 manifest exactly; local assets and module imports resolve.
- Homepage, search JavaScript and evidence JSON were compared with live public responses. The HTML-only difference was the hosting provider's injected Cloudflare security script, not application source.
- `npm test`: passed, including 24 matcher tests, portfolio filters, safe DOM rendering, 94 skill evidence entries and 121-row pagination.
- `npm run test:architecture`: passed geometry, navigation, runtime-stage, routing and dated-image checks.
- `npm run build`: passed, producing 52 static files without downloading dependencies.
- `npm run regenerate` in a separate copy: passed; all 52 resulting application files still matched the published baseline byte for byte.
- `CHROMIUM_PATH=/snap/bin/chromium npm run test:browser`: passed in Chromium 157.0.8103.38, including responsive widths 320/390/768/1440, three pages, 11 project cards, search/clear/pagination/theme, inert markup and zero search-time network requests.

The complete application is static. Public badge images and external destination sites remain external dependencies, as on the original. Browser checks establish the exercised UI paths, not availability of external sites or exact rendering on every browser. Hosting-provider security injection, owner credentials, original deployment identity and private editing history are intentionally not reproduced.

A fresh local Git clone containing only the 115 exported files passed `npm ci --ignore-scripts`, build, both test suites and the real Chromium browser checks. No source editor checkout, private archive or outside application data was used by that recreation. Python development packages and Chromium were installed system tools as documented.

No live deployment was changed. The public export preserves existing third-party notices and does not introduce a blanket license over third-party or personal content.
