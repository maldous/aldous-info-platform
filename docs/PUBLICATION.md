# Source checks and controlled publication

This document describes the Cloud infrastructure boundary. It does not grant
account access, credentials, source rights, release approval or a new publisher.
Public configuration and domains may be versioned here; private provider
bindings, secrets, raw receipts and operational telemetry stay in their existing
operator-controlled custody.

## Current source and build environment

The public repository's editable application is `dist/`. Its standard-library
build stages the same bytes into ignored `build/`; ordinary commands require
Python 3.12+ and Node 18+ but no package installation. The accepted source-check
edition was integrated by PR 4, tree
`e62ca71e659c85a5a9d8cb5b0f2d31b39dd28420`.

| Command | Actual boundary |
| --- | --- |
| `npm run build` | Stage static application bytes |
| `npm run lint` | Parse tracked JavaScript/Python/JSON; not style or security qualification |
| `npm run test:lint` | Synthetic checker contracts |
| `npm test` | Declared source/static/search/DOM/export contracts, not browser layout |
| `npm run test:architecture` | Separate optional geometry/tooling closure |
| `npm run test:browser` | Separate real-browser workflow described in README |

When selected, the deployed Foo `project_checks` catalogue binds `cloud` to this
repository and exposes `environment`, `lint_contracts`, `lint`, `build`,
`test` and `check`. Read the current deployed schema/catalogue, not this dated
summary. Pass a **bare task branch**, an immutable full expected commit and a
distinct original operation ID for each affected target. Reconcile that same
operation after uncertainty. The qualified runner uses Node 24.16.0,
npm 11.13.0 and Python 3.12.3, with network-disabled checks and bounded resources.
Its current publication capability is **unsupported**. A build is not a release.

Reuse accepted unaffected evidence. Documentation-only changes do not justify
replaying product suites; changed runtime, build, dependency, check or publishing
inputs require their applicable source-bound checks.

## Two repositories, different purposes

The public export is not the existing Site's authenticated publishing checkout.
The current documented runtime baseline is Site version 58, source
`bb8d422dddfdbe7e1a83dd7f700cd35081a9ee03`. Its 52 application files are recorded
by `docs/published-assets.sha256.json`; a deployment archive also contains the
owner-specific hosting manifest that this export intentionally omits.

For an update to **the existing aldous.info**:

1. Reconcile its current owner, original intent and latest saved/deployed version.
   Open its existing source through the official Sites source workflow into an
   isolated clean checkout. Retain the returned source identity and existing
   audience. Do not create a replacement Site because this export lacks its ID.
2. Compare the selected runtime files and current published manifest. Stop an
   overwrite if the live source has newer or unrelated changes. Apply only the
   selected reviewed application change; preserve the existing hosting manifest,
   source history and third-party notices. Public-source integration alone
   does not update that checkout or authorize a live effect.
3. Validate the affected exact source and package through the supported source
   helper. Reuse the complete opening result, supply remaining checks as ordered
   argument arrays, and retain its pushed commit and unchanged archive hash.
   Keep credentials in session memory/hidden stdin, never commands, files or
   generic Foo job arguments.
4. Save the matching Site version, then deploy that exact returned version ID
   through its existing audience-appropriate native MCP action. Reconcile a
   pending or uncertain original deployment before another attempt. Do not
   publish solely to test the publisher.
5. Record the actual terminal provider result and source/artifact/version binding.
   Keep source integration, packaged version, successful deployment and rendered
   desktop/mobile behavior separate.

For an independent fork, follow README's generic static-host instructions using
the fork's own identity, rights and chosen destination. That is not an update
to aldous.info.

## Other existing Cloud surfaces

Cloudflare/Netlify operations reuse the selected existing account/site/Worker,
its current source and deployment configuration, authorized audience and sole
publisher. Enumerate the real action before enabling it. A reachable connector,
a CLI version, a provider fixture or a manifest name is not proof of every
permission or a source-to-production binding.

The public observability subdomain is a separate deployment surface. Its
sanitized aggregate-only asset snapshot, privacy allowlist and original provider
receipt must stay distinct from the portfolio source, private observations and
product runtimes. Client polling does not itself publish new server data.
No extra scheduler or provider credential is introduced by this document.

## Typed handoff, not self-issued authority

A publication adapter must distinguish `catalog`, effect-free `plan`,
source-bound `build`/`test`, actual `publish` and original-operation `status`.
A minimal handoff carries:

- action and stable original operation identity;
- repository/ref/full commit/tree and the exact selected changed scope;
- target provider, logical destination, environment and current audience;
- immutable artifact format, byte size and SHA-256 when an artifact is consumed;
- source-bound review/check references and the current original publisher;
- original intent, current supported custody and uncertain-effect disposition;
- resulting provider operation/version and terminal receipt, when actually run.

These fields are evidence references, not executable permission or fencing.
Resolve them through the real provider and existing owner controls at the action
boundary. Caller-supplied `verified` flags cannot authorize an effect. Never
copy highly sensitive provider credentials into a new service to make a shared
interface appear complete.

Return `passed`, `failed`, `not_run`, `unsupported`, `input_blocked` or
`uncertain` for the actual selected action. Do not translate source checks into
production readiness. A missing destination or release condition blocks only
its consuming action, not unrelated projects. Keep the product release matrix
and each product's exact source/artifact/rights/registry requirements under its
own existing publisher; Cloud's infrastructure adapter is not a global release
gate.
