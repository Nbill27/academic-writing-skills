---
name: audit
description: "Audit academic and professional documents against applicable guides, genre, evidence, methodology, citations, language, and formatting. Uses universal checks, genre modules, applicability statuses, traceability, and prioritized findings."
version: 1.1.0
license: MIT
compatibility: "Hermes, CodeBuddy, Claude Code, OpenCode, Codex, and any agent that reads the Agent Skills format."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Audit

Audit the supplied document against requirements and evidence that actually apply. Do not use an unrelated campus template or generic five-chapter structure as a universal standard. Read `../shared/workflow-contract.md`; reuse a completed profile or use `../shared/institution-profile.md` as a template.

## Principles

- Establish genre, purpose, scope, stage, and inspection limits before judging compliance.
- Current official program/faculty/university/journal/client rules outrank general convention. Record provenance and conflicts.
- Separate universal checks from genre-specific requirements.
- Every criterion receives **Pass**, **Needs work**, **Not applicable**, or **Not verifiable**.
- Not applicable is not a failure; Not verifiable is not proof of non-compliance.
- Audit partial drafts only within their available scope. Run final-package checks only for final-readiness requests.
- Never claim inaccessible pages/files were inspected or claim formal approval/guaranteed grades.

## Workflow

1. Establish genre, purpose, program/level if relevant, stage, target reader, files available, and audit depth.
2. Resolve rules from guide/rubric/journal instructions. Record issuer, version, page/section, and conflicting requirements. Presets are fallbacks only.
3. Inventory only artifacts actually accessible and inspected.
4. Load exactly one matching module: `references/genre-research.md`, `references/genre-article.md`, or `references/genre-internship-report.md`. For other reports, use universal checks and explain the chosen scope.
5. Run applicable gates in `references/gates.md`. A failed prerequisite blocks only dependent checks.
6. Run `references/layered-qc.md`, applying genre-specific checks only when relevant.
7. Verify sources by type using `references/reference-verification.md`. DOI resolution is required only when a DOI is assigned or claimed.
8. Produce findings using `references/finding-report.md`.

## Universal dimensions

- Identity, purpose, scope, target audience, and confidentiality.
- Genre-appropriate structure, section purpose, and reader logic.
- Evidence traceability; separation of fact, analysis, assumption, and proposal.
- Consistency of numbers, names, dates, terms, findings, tables, diagrams, and appendices.
- Method/process/technical validity only where the artifact makes such claims.
- Citation, language, terminology, and formatting under applicable rules.
- Properties that cannot be established from files are Not verifiable.

## Severity

- **Critical:** fabricated/forged evidence, serious ethics/confidentiality breach, invalid core evidence, or fundamental contradiction.
- **Major:** required component missing, method unfit, central claim unsupported, or traceability broken.
- **Moderate:** materially consequential citation, formatting, numbering, terminology, diagram, or clarity defect.
- **Minor:** local language or presentation improvement.

Severity describes impact, not certainty. Mark suspected issues and request verification.

## Required output

1. Overall status: Ready for next review stage / Needs revision / Cannot assess completely.
2. Scope inspected: files, pages/sections, genre, stage, guide version, exclusions.
3. Applicability summary: counts for all four statuses.
4. Findings table: ID, severity, status, location, finding, impact, rule/evidence basis, corrective action, evidence needed.
5. Traceability assessment where applicable.
6. Missing information and unverifiable items.
7. Prioritized revision plan.
8. Disclaimer: assistant review, not formal institutional/editorial approval.

## Integrity

Never invent sources, facts, respondents, page numbers, results, approvals, or guide rules. Never forge signatures/stamps or silently rewrite a document during audit. Similarity or machine-pattern signals are not proof of misconduct.

## References

- [Stage gates](references/gates.md)
- [Layered quality control](references/layered-qc.md)
- [Reference verification](references/reference-verification.md)
- [Finding report](references/finding-report.md)
- [Research module](references/genre-research.md)
- [Article module](references/genre-article.md)
- [Internship report module](references/genre-internship-report.md)
