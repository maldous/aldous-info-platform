# Public source and interface map

This map describes the source at baseline commit
`239ff5e8bc6e135a109a6102e1ebaecc8bb164e7`, not a live provider inventory.
It covers the three static pages, their named module/data boundaries and the
repository's supported maintenance commands. It is not an exhaustive symbol
index, a new release gate or acceptance of external linked products.

For work on this repository, read [AGENTS](../AGENTS.md), the
[README](../README.md), [export scope](EXPORT_SCOPE.md),
[notices](../THIRD_PARTY_NOTICES.md) and the
[controlled publication boundary](PUBLICATION.md). Keep dated accepted evidence
in its original scope; source integration, build output, live publication and
rendered behavior are separate results.

## Application surfaces

| Surface | Source boundary | Inputs and outputs |
| --- | --- | --- |
| Portfolio `/` | [index.html](../dist/index.html), [portfolio.js](../dist/portfolio.js), [portfolio.css](../dist/portfolio.css) | Static public content, category-filter buttons, responsive navigation and theme switch. External project links do not recreate those projects. |
| Recruiters `/recruiters.html` | [recruiters.html](../dist/recruiters.html), [recruiters.mjs](../dist/recruiters.mjs), [matcher](../dist/recruiter-matcher.mjs), [styles](../dist/recruiters.css) | Loads the bundled evidence JSON; pasted requirements produce per-line cited evidence and paginated DOM results. Clear removes input/results from the page. |
| Architecture `/architecture.html` | [architecture.html](../dist/architecture.html), [app.js](../dist/app.js), [capability view](../dist/capability-view.js), [graph navigation](../dist/graph-navigation.js) | Loads operating-model and engineering JSON, renders cumulative capability diagrams, chapter navigation and resource/connection details. |
| Shared theme | [theme-init.js](../dist/theme-init.js), [theme.js](../dist/theme.js), [brand styles](../dist/brand-theme.css) | Initial system preference and explicit light/dark preference. Only theme preference uses browser local storage; it is separate from pasted recruiter text. |

The editable application is `dist/`, despite that historical name. The published
baseline manifest lists its 52 files. The application has no backend API,
authentication service, database, LLM invocation or production package install.
HTTP hosting is needed for local JSON fetches. Remote badge images and public
outbound links remain external dependencies described in the README.

## Named module contracts

- `recruiter-matcher.mjs` exports `compile(corpus)` and
  `searchRequirements(input, compiled)`. `compile` validates skill/citation
  structure and HTTPS citation URLs, then prepares normalized alias patterns.
  `searchRequirements` accepts text up to 30,000 characters, normalizes nonempty
  lines and returns per-line matches, status, review flags and matched skill IDs.
  It does not calculate a suitability percentage or infer that every qualifier,
  seniority, duration or unknown requirement has been satisfied.
- `recruiters.mjs` owns page events, static evidence loading, safe text-node
  rendering and result pagination. It does not transmit pasted text to a search
  backend, URL or telemetry endpoint. Citation/context navigation is distinct
  from the search computation.
- `theme.js` exports `themeKey`, `normalizePreference`, `resolveTheme`,
  `loadPreference` and `initTheme`. Storage/media failures fall back to the
  available system/default behavior; the returned controller supports applying
  or setting preference. The two page controllers update their own switches.
- `app.js` exports `validateFrames`; it checks the seven-stage operating-model
  structure and stage-appropriate communication endpoints. `capability-view.js`
  exports the capability definitions and coverage/graphic helpers.
  `graph-navigation.js` exports viewport, point mapping, region/overview/frame
  helpers and `installGraphNavigation` for pan/zoom/overview interaction.
  These are internal browser-module boundaries, not separately versioned SDKs.

The matcher is pure: no DOM, networking, storage or telemetry. Other browser
modules intentionally depend on the DOM and static assets. Source/DOM tests do
not by themselves prove real mobile, keyboard, touch or accessibility behavior.

## Content, generation and build

- Maintain recruiter evidence in
  [recruiter-data/evidence.json](../recruiter-data/evidence.json) and its retained
  [technical content](../recruiter-data/technical-experience.html).
  [build-recruiters.py](../build-recruiters.py) generates the page/corpus outputs.
  Preserve citation kinds, limitations and public attribution context.
- Diagram generators consume the retained graph/layout inputs:
  [current-architecture.json](../current-architecture.json),
  [layout](../layout), [mesh-layout.json](../mesh-layout.json) and the Python
  layout/render modules. [scripts/regenerate.py](../scripts/regenerate.py)
  invokes the recruiter and two current graph generators. Regeneration is
  optional for serving the already retained baseline.
- [scripts/build.py](../scripts/build.py) replaces the ignored `build/` directory
  with a byte-preserving copy of `dist/`. It refuses a symlinked build directory;
  it is not a compiler, bundler, download step or provider deployment.
- [package.json](../package.json) declares the actual command entrypoints.
  Ordinary build/source checks need the standard library and Node, not an npm
  dependency installation. Optional regeneration/geometry and pinned Playwright
  browser workflows have separate development dependencies.

## Verification and effect boundaries

| Changed input | Applicable evidence, not an automatic blanket replay |
| --- | --- |
| Documentation only | Exact source/diff/link/privacy review; reuse unchanged product evidence. |
| JavaScript, Python or JSON syntax | Declared `lint` parser boundary and relevant checker contracts; not style, security or rendered acceptance. |
| Page/matcher behavior | Affected source/search/DOM contracts and, for rendered interactions, actual supported browser checks. |
| Runtime assets or generated content | Review intended bytes and links; update the documented asset manifest for the selected new baseline rather than claiming old parity. |
| Geometry/navigation generation | Separate declared architecture workflow and its applicable dependency closure. |
| Hosting, domain or release inputs | Existing owner/source/artifact/destination binding and native publisher transaction in `PUBLICATION.md`; a local build is not deployment. |

The public repository can contain public-safe provider configuration, domain
information, public certificates and deployable assets without putting them on
the homepage. It must not contain secrets, private account/binding details,
private operational paths, raw receipts or telemetry. The separate observability
subdomain is not this application's backend. Preserve the existing Site,
selected design, asset rights and notices; do not create a replacement publisher
or broaden data collection as a side effect of documentation work.
