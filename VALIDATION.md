# Validation of the public export

Validated on 12 November 2026 against published version 55, source commit `14f65250890867d5981cb5054cc9f596189f666e`.

- All 52 application files match the retained published-source SHA-256 manifest exactly; local assets and module imports resolve.
- Homepage, search JavaScript and evidence JSON were compared with live public responses. The HTML-only difference was the hosting provider's injected Cloudflare security script, not application source.
- `npm test`: passed, including 24 matcher tests, portfolio filters, safe DOM rendering, 94 skill evidence entries and 121-row pagination.
- `npm run test:architecture`: passed geometry, navigation, runtime-stage, routing and dated-image checks.
- `npm run build`: passed, producing 52 static files without downloading dependencies.
- `npm run regenerate` in a separate copy: passed; all 52 resulting application files still matched the published baseline byte for byte.
- `CHROMIUM_PATH=/snap/bin/chromium npm run test:browser`: passed in Chromium 157.0.8103.38, including responsive widths 320/390/768/1440, three pages, 11 project cards, search/clear/pagination/theme, inert markup and zero search-time network requests.

The complete application is static. Public badge images and external destination sites remain external dependencies, as on the original. Browser checks establish the exercised UI paths, not availability of external sites or exact rendering on every browser. Hosting-provider security injection, owner credentials, original deployment identity and private editing history are intentionally not reproduced.

No live deployment was changed. The public export preserves existing third-party notices and does not introduce a blanket license over third-party or personal content.
