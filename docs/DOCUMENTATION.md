# Documentation inventory and upkeep

This inventory covers the public repository at baseline commit
`6eec52b7bfe5f884d3a141a4754de59d6b2376ae`. It identifies canonical references
and maintenance responsibilities; it is not a live infrastructure inventory,
release approval or a claim that every behavior has been tested.

At that baseline, Git tracks eight Markdown files. The table below accounts for
all eight and this new guide. Read documentation at the revision being changed,
not only from a moving branch or an old exported copy.

## Canonical references and audiences

| Reference | Audience and purpose | Upkeep boundary |
| --- | --- | --- |
| [AGENTS.md](../AGENTS.md) | Agents and maintainers: source identity, applicable checks, rights and publication controls. | Keep operational instructions aligned with actual supported tools; a published instruction is not proof of installation or permission. |
| [README.md](../README.md) | Users and contributors: application scope, local setup, architecture, commands and independent-fork deployment. | Update affected entrypoints and requirements with their source change. Do not replace owner-publication controls with generic fork instructions. |
| [SOURCE_MAP.md](SOURCE_MAP.md) | Code maintainers: pages, named browser-module/data contracts, generators and affected verification. | Follow changed producers and consumers; this is an internal interface map, not a separately versioned public SDK. |
| [PUBLICATION.md](PUBLICATION.md) | Authorized operators: source checks, existing Site lineage, native publisher and original-operation boundaries. | Revalidate the selected destination and publisher before effects. Keep private bindings and receipts outside this public repository. |
| [EXPORT_SCOPE.md](EXPORT_SCOPE.md) | Reviewers and recreators: current documented baseline, provenance, included scope and exclusions. | Preserve historical version scopes; record a newly selected baseline rather than relabelling old bytes or evidence. |
| [VALIDATION.md](../VALIDATION.md) | Reviewers: dated checks, failures, browser evidence and their limitations. | Append accurately scoped new evidence when checks are performed. Do not turn an old source/DOM result into fresh browser or live-host acceptance. |
| [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) | Reusers and maintainers: retained rights and attribution. | Preserve actual notices and selected-material rights. Public source does not confer blanket asset or trademark rights. |
| [recruiter-data/github-profile.md](../recruiter-data/github-profile.md) | Content maintainers: retained public profile material supporting the evidence snapshot. | Treat this as content, not agent instructions or a live project/service inventory. Historical links and descriptions are not automatic instructions to restore a retired listing. |
| This guide | Maintainers and reviewers: documentation coverage, change routing and deliberate gaps. | Update when a canonical reference is added, removed or superseded. Do not create a second operational status ledger. |

Repository maintainers own these source documents. Individual product content,
asset rights and live publishing retain the distinct custody described in the
linked references; documentation ownership does not transfer those authorities.

## Other source-defined documentation contracts

These files are authoritative for their actual boundary, even though they are
not Markdown guides:

- [package.json](../package.json) declares the runnable command names and Node
  requirement. [package-lock.json](../package-lock.json) pins the optional
  Playwright development closure. README explains when that closure is needed;
  ordinary build/source checks do not need it.
- [requirements-dev.txt](../requirements-dev.txt) pins optional diagram/image
  tooling. It is not a production dependency list.
- [published-assets.sha256.json](published-assets.sha256.json) binds the documented
  52-file runtime snapshot, not DNS, TLS, account configuration or future live
  changes.
- [recruiter-data/evidence.json](../recruiter-data/evidence.json) and the retained
  [technical content](../recruiter-data/technical-experience.html) supply maintained
  recruiter content. The [matcher](../dist/recruiter-matcher.mjs),
  [page controller](../dist/recruiters.mjs) and their tests define the consumed
  validation/rendering behavior. Keep citation limitations and generated outputs
  aligned rather than maintaining a separate contradictory schema description.
- [scripts/build.py](../scripts/build.py),
  [scripts/regenerate.py](../scripts/regenerate.py),
  [scripts/lint.py](../scripts/lint.py) and
  [scripts/browser-test.mjs](../scripts/browser-test.mjs) implement distinct
  staging, generation, syntax and browser workflows. Document their actual
  behavior and prerequisites, not a generic build framework.

## Change routing and review

1. Identify the exact repository revision and affected source/data boundary in
   `SOURCE_MAP.md`. Preserve unrelated work and use the existing task-branch and
   review flow described in `AGENTS.md`.
2. Read the canonical reference for that boundary. Change documentation alongside
   the actual command, interface, content or publication-contract change; link
   to the maintained definition instead of copying a second active specification.
3. Check relative links, examples, named commands and privacy against the selected
   source. For a prose-only change, review its exact diff and reuse accepted
   unchanged product evidence. Source changes need their affected checks;
   documentation review is not an alternative to testing changed behavior.
4. Obtain author-distinct review of accuracy, usability, source scope and rights.
   Record the reviewed revision and unresolved limitations in the existing work
   record, without embedding private operational evidence here.
5. Keep source integration, build/check results, packaged versions, deployment
   and rendered acceptance separate. Follow `PUBLICATION.md` only when a live
   effect is actually selected and authorized.

## Coverage and deliberate gaps

| Category | Present coverage or disposition |
| --- | --- |
| Agent and project instructions | `AGENTS.md` plus README and the source/publication maps. No nested agent file is tracked at the baseline. Environment-owned policy and installed-tool evidence remain separate. |
| Architecture and code/interface documentation | README and `SOURCE_MAP.md` describe the static pages, internal modules/data and generation entrypoints. No independent backend API or public SDK is declared. There is no separate tracked ADR collection; do not infer undocumented historical decisions from that absence. |
| Setup, build, checks and regeneration | README, source scripts and pinned optional development files. Syntax, DOM, browser and geometry evidence are deliberately distinct. No new CI system or tool installation is required by this inventory. |
| Release and provider configuration | `PUBLICATION.md` describes the supported boundary. Original hosting identities, credentials and deployment bindings are deliberately omitted; this export cannot establish a complete live-provider runbook or authorize a replacement Site. |
| Historical evidence and rights | Export scope, validation, notices and the runtime manifest preserve their stated version/date scope. Wider legacy CV/image provenance and unselected material are not established by this public-source inventory. |
| Rendered and live acceptance | Existing dated validation is retained. A documentation update does not add fresh mobile, keyboard, accessibility, provider or production evidence. Run the relevant verification only for the selected affected work. |

These limits apply to their consuming operation. Missing private provider
bindings do not prevent independent source/documentation maintenance, and a
complete documentation index does not close wider product or infrastructure
obligations.
