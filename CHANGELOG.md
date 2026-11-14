# Changelog

All notable changes to this repository. Versions refer to the five skills in `skills/`.

## 1.0.0 — 2026-11-14

First versioned release. The package now has five skills instead of four, with a workflow dispatcher, genre routing, and per-genre audit modules. The corrections below fix architecture and over-strict audit rules; the honesty rules are unchanged.

### Added

- `skills/academic-writing/SKILL.md` — workflow dispatcher that routes a task to the smallest suitable skill or chain (outline, draft, edit, audit) and records genre, applicable rules, evidence, and the next step.
- `shared/workflow-contract.md` — shared routing, evidence labels (E/C/A/P/U), provenance, and handoff contract for all five skills.
- `skills/audit/references/genre-research.md`, `genre-article.md`, `genre-internship-report.md` — per-genre audit modules; each loads only for its own genre.
- `skills/outline/references/genre-article.md` and `skills/draft/references/article-manuscript.md` — journal and conference manuscript outline and drafting.
- `tests/test_validate_package.py` — unit tests for the validator.
- `.github/workflows/validate.yml` — CI that runs the validator, the unit tests, and the installer smoke test on ubuntu-24.04 (Python 3.10/3.12/3.13) and macos-latest (Python 3.13). Note: this file is applied through the GitHub web UI, not by the API push, because the GitHub App used for pushes has no `workflows` permission.
- `version: 1.0.0` in every `SKILL.md` frontmatter.

### Changed

- All four specialist skills now read the shared workflow contract and route by genre. Journal articles are no longer forced into the Chapter I to V thesis structure, and internship reports are no longer assumed for technical reports.
- Audit criteria now use Pass / Needs work / Not applicable / Not verifiable. A criterion that does not apply is not a failure, and a criterion that cannot be verified is not proof of non-compliance.
- The universal DOI requirement is removed. DOI resolution is checked only when a DOI is assigned or claimed; books, reports, datasets, regulations, and interviews have their own verification routes.
- `shared/presets/generic.yml` now covers all 14 structure variables instead of a subset.
- `shared/institution-profile.md` rewritten as a task profile template with a source register, the 14-variable adapter, formatting profile, and evidence table.
- `scripts/validate_package.py` replaced with broader packaging checks (five skills, preset keys, local links) and a clear statement of what it does not test.
- `install.sh` copies five skills plus `shared/`.
- README updated for five skills.

### Notes

- The update arrived as an overlay bundle; its bundle README was not applied, the repository README is the documentation.
