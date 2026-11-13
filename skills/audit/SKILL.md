---
name: audit
description: "Audit an Indonesian academic draft against its campus guide and its own evidence: structure, argument traceability, analysis methods, diagrams, formatting, citations, and submission readiness. Gates per stage plus four layered checks, a severity rubric, and a prioritized findings report. Use for audit report, check skripsi, check Chapter I to V, check bibliography, check formatting, or ready for defense."
license: MIT
compatibility: "Hermes, CodeBuddy, Claude Code, OpenCode, Codex, and any agent that reads the Agent Skills format."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Audit

Review the document against its guide and its own evidence, not against an arbitrary standard. A good audit finds what is wrong, says where it is, says why it matters, and says how to fix it. It never guarantees a grade and never calls a report officially approved.

## Audit stance

- Use the document the user supplied. Establish the program, the report stage, and whether the file is a complete report or a partial draft. If the program is unknown, do a structural review but mark program-dependent checks "cannot be verified yet".
- Never claim to have inspected pages or files that are not actually accessible.
- Never state "100 percent compliant", "guaranteed pass", or "approved". Mark uncertain checks transparently and identify where physical or institutional verification is required.
- Never report as verified what the file cannot show: paper weight, print sidedness, actual logo dimensions, text color, physical stamps and signatures, and approval authenticity.

## Workflow

1. Confirm the campus variables first. Read the filled 14 variables from the `outline` skill or fill them from the guide with `references/guide-adapter.md` in the outline skill. When there is no guide, mark every campus-dependent check `[CHECK: campus guide]`.
2. Run the stage gates in `references/gates.md`, Gate 0 to Gate 6. A failed gate means stop, fix, then continue. Never skip a failed gate.
3. Run the four layered checks in `references/layered-qc.md`, in order. Layer 1 Style, Layer 2 Mechanics and EYD, Layer 3 Semantics, Layer 4 Red-team. A failed layer is a blocker for the next layer.
4. Verify the references with `references/reference-verification.md`. Every in-text citation must have a matching bibliography entry and every entry must be cited in the text. Verify that every reference exists before accepting it. Never guess a DOI, a year, a volume, an issue, or page numbers.
5. Write the finding report with `references/finding-report.md`: overall status, scope inspected, findings table, cross-chapter traceability, unverifiable items, and a prioritized revision plan.

## Audit phases

- Phase A, identity and scope: program and level, title, host, dates, current stage, topic alignment, minimum scope represented, factual claims without evidence, confidential information needing redaction or authorization.
- Phase B, structure: front matter and end matter, then every required heading. The program outline is mandatory. Check Chapter I 1.1 to 1.6, Chapter II 2.1 to 2.2, Chapter III, Chapter IV, and Chapter V, with the exact wording where practical.
- Phase C, argument and traceability: background uses real host facts and at least one prior journal citation, identification problems are declarative statements grounded in the background, boundaries control Chapter IV and Chapter V, formulation questions reflect identified and bounded issues, objectives answer those questions, literature concepts are relevant to the analysis, related work compares ISSN-bearing research from the stated period, the existing state is not confused with the proposed state, conclusions answer the formulation and objectives and derive from the discussion, and suggestions are actionable.
- Phase D, analysis method validation: when PIECES is used, check all six dimensions are meaningfully considered and never demand a fabricated finding for an inapplicable dimension. When SWOT is used, distinguish internal Strengths and Weaknesses from external Opportunities and Threats, check factors are supported by case evidence, and assess SO, ST, WO, and WT logic when a strategy matrix is included. When information characteristics are used, check relevance, accuracy, timeliness, economics, efficiency, reliability, and usefulness.
- Phase E, diagrams and design artifacts: each diagram represents a real process or current architecture or a clearly labeled proposed design, has consistent actors, symbols, labels, flow direction, and terminology, is explained in adjacent prose and referenced in the report, has its caption below and centered for figures and above and centered for tables, and is numbered by chapter.
- Phase F, technical formatting: paper, margins, font, spacing, cover, chapter and page numbering, figure and table numbering. Check only what the file shows.
- Phase G, citation and bibliography: direct quotes match the original wording, spelling, and punctuation. Short quotes under 5 lines are double-spaced, integrated, and quoted. Long quotes of 5 lines or more are single-spaced, indented, and unquoted. Bibliography is alphabetical, holds full author names, omits honorific titles, and uses single spacing inside entries with double spacing between entries. Internet sources must come from an official URL. Blogspot, Wordpress, and Wikipedia are excluded.
- Phase H, ethics and submission readiness: host permission, legal host, professional conduct and confidentiality, consent for data and screenshots, minimum supervisor consultations recorded, host assessment form and completion letter on official letterhead with stamp and original authorized signature, supervisor approval signature, and a complete PDF package for submission.

## Severity rubric

- Critical: wrong program outline, fabricated or forged evidence, host or eligibility contradiction, missing central analysis or recommendation, severe scope or ethics issue.
- Major: required chapter or section missing, argument traceability broken, unsupported core claim, incorrect method or diagram, mandatory supporting document missing.
- Moderate: formatting, citation, numbering, caption, bibliography, or clarity defect likely to affect academic compliance or readability.
- Minor: grammar, consistency, or small presentation improvement.

## Required audit output

1. Overall status: Ready for supervisor review, Needs revision, or Cannot assess completely.
2. Scope inspected: file name, pages and sections reviewed, program assumed or confirmed, known limitations.
3. Findings table: ID, severity, location, finding, impact, rule basis, corrective action, evidence needed.
4. Cross-chapter traceability findings.
5. Missing information and unverifiable items.
6. Prioritized revision plan, fixing blockers first.
7. Explicit disclaimer that this is an assistant review, not formal university approval.

## Honesty rules

- Never invent data, respondents, sources, numbers, or results.
- Mark anything missing as `[NEED: ...]` and anything unverified as `[CHECK: ...]`.
- Refuse ghostwriting requests and requests to disguise AI output as the student own writing.
- Never produce a forged signature, stamp, assessment, letter, or backdated consultation record. Offer legitimate request templates and checklists only.

## References

- `references/gates.md`: stage gates Gate 0 to Gate 6, including the qualitative gate.
- `references/layered-qc.md`: four layered checks, red-team questions, and the pass rubric.
- `references/reference-verification.md`: reference verification through Garuda, SINTA, OpenAlex, and Crossref.
- `references/finding-report.md`: finding report template and revision sequence.

## Sources and credit

Audit phases, severity rubric, and finding report are adapted from kp-quality-audit in the Bina Insani KP Companion by Muhammad Nabil Deja (MIT). Stage gates and layered QC are adapted from quality-gates.md in proposal-skripsi-skill by Bima Januri (MIT). See the repo README for the full attribution list.
