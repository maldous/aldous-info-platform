# Public export and provenance

## Baseline

- Original published Site version: 55.
- Source commit: `14f65250890867d5981cb5054cc9f596189f666e`.
- Live origin: `https://aldous.info`.
- Application payload: 52 static files in `dist/`, recorded individually in `published-assets.sha256.json`. The hosting deployment archive has one additional hosting-manifest file; that owner-specific binding is not included.

The current full tracked source was obtained from the original editor's retained, clean source checkout through a private artifact handoff. It was not reconstructed from browser screenshots or an obsolete GitHub/Netlify copy.

## Included

Every current published application file is retained byte-for-byte. The current recruiter generator and data, current architecture diagram generators/layout inputs, focused tests and public-only geometry review fixtures are included. README and portable build/browser verification tooling were added for independent recreation.

Some original tests still expected an older ten-card portfolio and two Morgan-image placements. The public export's test fixtures were corrected to the actual version-55 eleven-card portfolio and single Morgan project-card placement. No runtime application bytes were changed to satisfy those tests.

## Excluded

No `.git` history, credentials, `.env` files, original hosting identity, private Library/workspace links, internal coordination documents, historical CV/provenance working notes or superseded architecture experiments are published. These are not needed to run the current application. Original source and the live Site remain unchanged.

## Verification boundary

Source privacy checks cover the curated export, including public runtime files and generator inputs. The known current runtime scripts and search corpus were compared with the public live responses. Homepage/recruiter HTML was identical apart from the live host's added Cloudflare security script. That hosting code is deliberately not copied into the application.

Clean-build, search and browser results are described in `VALIDATION.md`. Byte parity does not reproduce a hosting provider's account, DNS, TLS, anti-bot configuration, remote badge service, external linked products or future site changes.
