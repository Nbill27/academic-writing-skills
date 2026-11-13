---
name: draft
description: "Draft Indonesian academic prose chapter by chapter from the student material: Chapter I to Chapter V for skripsi (undergraduate thesis), proposal, tesis, and KP reports, plus abstracts, company profiles, running-system analysis, and proposed systems. Evidence first, one chapter at a time, with traceability from problem to conclusion, and export to Markdown and DOCX. Use for draft chapter, background, literature review, research methods, results and discussion, conclusions, or export docx."
license: MIT
compatibility: "Hermes, CodeBuddy, Claude Code, OpenCode, Codex, and any agent that reads the Agent Skills format."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Draft

Draft from evidence, one chapter at a time. A defensible report is built from the student own material, not from invented facts. Work as a writing and analysis partner, not a fiction generator.

Start from a finished outline. If there is no outline, run the `outline` skill first. If the outline exists, follow it and do not change its structure silently.

## Evidence discipline

Before drafting a factual section, classify every input.

- Verified evidence: direct notes, approved documents, authorized screenshots, measured output, source files, official company profile, supervisor-approved information.
- Student recollection: useful, but confirm it for exact dates, figures, roles, and process details.
- Assumption or hypothesis: not reportable as fact until verified.
- Proposed design: future-state proposal, clearly labeled as proposal rather than current implementation.

Tag claims inside each paragraph while drafting.

- E: evidence-backed fact.
- C: citation-backed concept or research statement.
- A: analysis or inference derived explicitly from E or C.
- P: proposal or future design.
- U: unsupported or unknown, replaced with a placeholder or a question for data.

Never blend E and P in one sentence in a way that implies a proposal already exists. Use "Based on observation, the running system ..." only when actual observation evidence exists. Use "The proposed system ..." for future design.

Use placeholders such as `[NEED: unit name, confirm]`, `[NEED: date, verify]`, or `[NEED: count, based on company data]` instead of inventing facts. Ask for the smallest missing evidence set. Never claim a system has been implemented, tested, deployed, or accepted unless evidence supports it.

## Chapter logic

Maintain traceability through the whole document.

field facts, to identified problems, to scope, to research questions, to objectives and benefits, to theory and related research, to object and running process, to problem analysis, to proposed improvement, to conclusions and suggestions.

If the user supplies a topic or section that breaks this chain, explain the mismatch and repair the logic before polishing prose.

## Workflow

1. Confirm the level and the depth. S1 skripsi applies or tests theory in a local context, about 20 to 30 pages for a proposal. S2 thesis develops or expands a conceptual framework, about 40 to 60 pages for a proposal. S3 dissertation claims a theoretical contribution, about 70 to 120 pages for a proposal. Depth follows the level.
2. Gather the evidence folder first: guide file, repo or system artifacts, master data, interview and observation notes, company documents, and references. Draft only from what is in the folder. Every empirical claim needs a source marker.
3. Draft one chapter at a time, in order, following the reference file for that chapter. Finish and check a chapter before drafting the next one.
4. Build a term list with the exact spelling of every key term and a point of view list with the voice used in the text, before Chapter I. Use the same terms and the same voice in every chapter.
5. Verify the numbers, citations, and quotes of a chapter while drafting that chapter. Do not leave all verification to the end.
6. Report the result per chapter when the chapter is done, including the `[NEED: ...]` and `[CHECK: ...]` items that chapter still needs.
7. When all chapters are drafted, run the `audit` skill before export.

## Draft delivery format

When asked to draft a section, provide the section heading exactly as the outline requires, draft prose ready for revision, `[NEED: ...]` placeholders with a short list of the specific evidence needed, a traceability note (which identified issue or objective it supports and where it connects next), and a brief self-check against the guide.

When asked to revise existing writing, preserve the student factual meaning and flag unsupported assertions rather than silently rewriting them as facts. Use the editing scopes in the `edit` skill.

## Quantitative and qualitative paths

- Quantitative: name the design, population, sampling technique, and sample size, state the instrument and the origin of its items, plan validity and reliability tests, and give each hypothesis exactly one analysis technique. Every dataset number must come from a real calculation on the user dataset, never from memory.
- Qualitative: pick one design (case study, phenomenology, grounded theory, thematic analysis, or descriptive) with a reason, state the paradigm and approach, define informant inclusion and exclusion criteria and the stopping rule (saturation), attach the interview guide and the consent sheet in the appendices, and write the analysis stages in order (transcription, open coding, categorization, thematic). Plan member checking or triangulation. Never quote, code, or count anything that is not in the transcript.
- R and D or prototyping: name the development model and justify it, describe the design, and report implementation and test results.

## Export

Read `references/export.md` for the export workflow. Produce Markdown first, then DOCX through Pandoc with the campus template variables (margins, font, spacing, cover). Produce PDF through Typst when the campus template supports it. Export citations to BibTeX or RIS on request. Never present an export as final until the `audit` skill passes it.

## Honesty rules

- Never invent data, respondents, sources, numbers, or results.
- Mark anything missing as `[NEED: ...]` and anything unverified as `[CHECK: ...]`.
- Refuse ghostwriting requests and requests to disguise AI output as the student own writing. Offer to draft from the student own material and to revise the student own words instead.
- Never forge a letter, assessment, signature, stamp, attendance record, or interview.

## References

- `references/chapter1-introduction.md`: Chapter I drafting, funnel, identification, boundaries, formulation, objectives.
- `references/chapter2-literature.md`: Chapter II drafting, theory and related research.
- `references/chapter3-methods.md`: Chapter III drafting, quantitative, qualitative, and R and D paths.
- `references/chapter4-results.md`: Chapter IV drafting, running system, problems, alternatives, proposed system, results.
- `references/chapter5-conclusions.md`: Chapter V drafting, conclusions and suggestions.
- `references/export.md`: Markdown, DOCX, PDF, and citation export.

## Sources and credit

Chapter drafting guidance and the evidence-first workflow are adapted from kp-report-authoring in the Bina Insani KP Companion by Muhammad Nabil Deja (MIT) and from the proposal pipeline in proposal-skripsi-skill by Bima Januri (MIT). See the repo README for the full attribution list.
