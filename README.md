# aldous.info platform

The complete static application behind [aldous.info](https://aldous.info): Matthew Aldous's portfolio, browser-local recruiter evidence search, and interactive architecture explorer. This is a new, independently reproducible public repository, not a change to the existing live deployment.

## What is included

- Homepage, all project cards and filters, career history, technical experience, themes and responsive navigation.
- Recruiter search over 94 cited skills, literal/alias matching, per-line evidence, safe rendering and paginated results.
- Architecture explorer with chapter navigation, pan/zoom, component and connection detail views, and its diagram-generation inputs.
- All 52 application files from published version 55, including fonts, images, résumé PDF, styles, JavaScript and JSON.
- Current generators, focused tests, clean-build scripts and a per-file SHA-256 snapshot manifest.

The source baseline is published version **55**, source commit `14f65250890867d5981cb5054cc9f596189f666e`. See [export scope](docs/EXPORT_SCOPE.md) and [asset hashes](docs/published-assets.sha256.json).

## Quick start

Requirements: **Python 3.12+** and **Node.js 18+** (validated with Python 3.12 and Node 24.22.2). No account, API key, database or paid service is needed to run the application.

```sh
git clone https://github.com/maldous/aldous-info-platform.git
cd aldous-info-platform
npm run build
npm start
```

Open `http://127.0.0.1:8080/`, `/recruiters.html` and `/architecture.html`.

The default build and server need no npm packages or Python packages: they use the standard library. `npm` is only a convenient command runner. Equivalent commands are:

```sh
python3 scripts/build.py
python3 -m http.server 8080 --bind 127.0.0.1 --directory build
```

Use HTTP rather than opening files directly: the search page loads its bundled evidence JSON with `fetch`.

## Architecture and languages

This is a **buildless static web application**, not a hosted AI search service. The historical directory name `dist/` contains the editable, unminified application source. `scripts/build.py` stages an identical copy in ignored `build/`; it performs no code transformation or remote download.

| Area | Source | Responsibility |
| --- | --- | --- |
| Portfolio | `dist/index.html`, `portfolio.css`, `portfolio.js` | Content, project filtering, responsive navigation and visual presentation |
| Themes | `dist/theme-init.js`, `theme.js` | Apply and switch the light/dark/system preference |
| Search UI | `dist/recruiters.html`, `recruiters.css`, `recruiters.mjs` | Load the local corpus, render citations safely, clear input and paginate results |
| Search engine | `dist/recruiter-matcher.mjs` | Pure `compile(corpus)` and `searchRequirements(input, compiled)` functions |
| Search content | `recruiter-data/evidence.json`, `technical-experience.html` | Maintained evidence and generated recruiter-page content |
| Architecture | `dist/architecture.html`, `app.js`, `capability-view.js`, `graph-navigation.js` | Interactive story, navigation and accessible details |
| Diagram data | `current-architecture.json`, `layout/`, `mesh-layout.json` | Component graph, selected layout and routing geometry |
| Diagram generators | `approved_layout.py`, `mesh_render.py`, `mesh_layout.py`, `selected_layout.py` | Deterministic SVG/JavaScript generation from retained graph/layout inputs |
| Assets | `dist/portfolio-assets/`, `dist/fonts/`, PDF | The published local visual and document assets |

Languages are HTML, CSS, modern JavaScript ES modules, JSON and Python. There is no production framework, server-side library, npm runtime dependency, database, authentication service or LLM dependency. Python diagram tooling optionally uses Pillow; extended geometry checks also use lxml. Playwright is a pinned **development-only** browser-test dependency. Roboto fonts and their SIL Open Font License are bundled.

### Search behavior and privacy

`compile` validates the corpus/citations and prepares Unicode-aware, boundary-aware alias patterns. `searchRequirements` normalizes lines, matches known terms and returns cited evidence without assigning a suitability percentage. It limits input to 30,000 characters and retains unknown requirements for human review. A match does not assert that experience duration, seniority, recency or every qualifier is satisfied.

The page makes one static request for `recruiter-evidence.json`. Pasted requirements stay in the browser tab: the search does not send them to a backend, store them, put them in the URL or use telemetry. Rendering uses DOM text nodes, not HTML interpolation. Theme preference is separate from search input.

## Editing and regeneration

Edit the homepage and application modules directly in `dist/`. Update evidence in `recruiter-data/evidence.json`, preserving its public citation, kind, limitation and optional local context-link fields. Rebuild the recruiter page with:

```sh
python3 build-recruiters.py
```

To regenerate current architecture diagrams as well:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
npm run regenerate
npm run build
```

`generate-graphs.py` and `generate-current-architecture.py` use the retained approved layout; they do not invoke an external service. Generated review geometry is not a production dependency. The export preserves the original runtime files so regeneration is optional for running or deploying this baseline.

## Tests

```sh
npm test                       # source/static checks, 24 search tests and DOM behavior tests
# With requirements-dev.txt installed:
npm run test:architecture       # geometry, navigation and captured-image checks
```

`scripts/check-export.py` verifies all 52 runtime files against the published baseline and checks local asset/module links. When intentionally changing the application, review the changes and update `docs/published-assets.sha256.json` for the new documented baseline. Do not describe altered bytes as version-55 parity.

For real browser checks:

```sh
npm ci
npx playwright install chromium
npm run build
npm run test:browser
```

Alternatively use an already installed compatible Chromium without downloading a browser:

```sh
CHROMIUM_PATH=/path/to/chromium npm run test:browser
```

The browser test starts and stops its own loopback server. It covers the homepage, responsive widths, project filters, 94-skill search, unknown terms, inert markup, clear, 121-row pagination, theme changes, architecture loading and zero search-time network requests. Node DOM harness tests are reported separately from actual browser tests.

## Deployment and configuration

Run `npm run build` and publish **only `build/`** to any static host, for example GitHub Pages, Cloudflare Pages, Netlify, an object-store website or an ordinary web server. Build command: `npm run build`; publish directory: `build`. Ensure `.mjs` is served as JavaScript and `.json` as JSON. No SPA fallback is necessary: the three pages have real `.html` paths.

For Sites, use your own Site identity and a hosting manifest whose `static.directory` is `build`. This export deliberately omits the original owner's hosting identity, credentials and deployment bindings. Creating or deploying your own Site is a separate operation; none of these commands alter the existing aldous.info deployment.

There are no application environment variables or secrets. The local server port/bind address are command-line options. If you publish a fork under a new identity or domain, review the personal content, contact details, résumé, canonical URLs and evidence citation URLs. Preserve the citation context or replace it with your own evidence rather than making unsupported claims.

### External dependencies and parity limits

- Badge images use public `img.shields.io` URLs, as on the live site. Internet access is needed for those images; the local application and search corpus are bundled.
- Public links open separate project sites, GitHub, LinkedIn and articles. This repository does not recreate those other products or their private backends.
- The Morgan image is an explicitly dated captured screenshot, not a live monitoring feed.
- The live host may inject Cloudflare challenge/security scripts. Those host-managed scripts, DNS/TLS and provider configuration are not application source and are not reproduced here.
- Content and evidence are the version-55 snapshot, not an automatic ongoing sync of the live site, résumé or GitHub.

## Rights and public-export boundary

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Publication of this repository does **not** grant a blanket license over photographs, logos, résumé content or third-party artwork. Existing notices and public attributions are retained; the Roboto font license remains in `dist/fonts/Roboto-OFL.txt`. No new broad license has been imposed.

Internal working history, private provenance links, editor credentials, repository history and unrelated historical experiments are excluded. All current published application files and the inputs needed for the included current regeneration commands are retained. No live service, account, domain or permission was changed by this export.
