# Public export and provenance

## Current version-56 runtime

- Published Sites source: `03997393bb021ee7bd58b8f77a512120e41bd8f2`.
- Public repository runtime synchronization: `f0700c824123cbe6c16c6bea6bc3399c76b67b83`.
- Version 56 published successfully on 13 November 2026 at 04:07:50 UTC (15:07:50 AEDT).
- All 52 runtime files are represented by `published-assets.sha256.json`. Exactly four files changed from v55: `index.html`, `portfolio.css`, `portfolio.js` and `recruiters.html`. The original v55 hashes remain in `published-assets.v55.sha256.json`.
- The update reuses the existing world-map image with fixed positioning and Australia-focused mobile cropping, replaces the homepage/recruiter theme selector with a persistent light/dark switch, and aligns project card content.
- Search implementation, evidence corpus, architecture runtime, assets and third-party notices are unchanged.
- This follow-through updates documentation, hashes and tests only; it changes no runtime bytes and performs no deployment.

## Original version-55 export (historical)

- Original published Site version: 55.
- Source commit: `14f65250890867d5981cb5054cc9f596189f666e`.
- Live origin: `https://aldous.info`.
- Application payload: 52 static files in `dist/`, recorded individually in `published-assets.sha256.json`. The hosting deployment archive has one additional hosting-manifest file; that owner-specific binding is not included.

The original full tracked source was obtained from the original editor's retained, clean source checkout through a private artifact handoff. It was not reconstructed from browser screenshots or an obsolete GitHub/Netlify copy.

## Version-55 included scope (historical)

At the original export, all 52 version-55 application files were retained byte-for-byte. The current recruiter generator and data, current architecture diagram generators/layout inputs, focused tests and public-only geometry review fixtures are included. README and portable build/browser verification tooling were added for independent recreation.

Some original tests still expected an older ten-card portfolio and two Morgan-image placements. The public export's test fixtures were corrected to the actual version-55 eleven-card portfolio and single Morgan project-card placement. No runtime application bytes were changed to satisfy those tests.

## Original export exclusions

No `.git` history, credentials, `.env` files, original hosting identity, private Library/workspace links, internal coordination documents, historical CV/provenance working notes or superseded architecture experiments are published. These are not needed to run the current application. The original export did not alter source or the live Site; the later version-56 update is recorded separately above.

## Original export verification boundary (historical)

Source privacy checks cover the curated export, including public runtime files and generator inputs. The known current runtime scripts and search corpus were compared with the public live responses. Homepage/recruiter HTML was identical apart from the live host's added Cloudflare security script. That hosting code is deliberately not copied into the application.

Clean-build, search and browser results are described in `VALIDATION.md`. Byte parity does not reproduce a hosting provider's account, DNS, TLS, anti-bot configuration, remote badge service, external linked products or future site changes.
