---
name: edit
description: "Edit and revise Indonesian academic prose without changing its facts: spelling and EYD V, KBBI word choice, effective sentences, and removal of machine-writing patterns, with clear editing scopes from typo fix to rewrite. Keeps the author voice, protects legitimate conventions, and never invents data. Use for check language, check spelling, edit manuscript, fix sentences, remove AI patterns, or revise chapter."
license: MIT
compatibility: "Hermes, CodeBuddy, Claude Code, OpenCode, Codex, and any agent that reads the Agent Skills format."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Edit

Edit the language, keep the meaning. A good edit makes the writer sound like a clearer version of themselves. It never changes a fact, a number, a claim, or a citation, and it never invents a fact to fill a gap.

Start from the user text. If there is no text yet, hand the work to the `draft` skill.

## Editing scopes

Ask which scope the user wants when the request is unclear. Default to the narrowest scope, Correction, when the user only asks to check the text. Say which scope is used.

- Correction: fix typos, punctuation, and spelling only. Change no wording, no claim, and no structure.
- Editing: fix grammar, clarity, and flow. Keep every fact, number, claim, and citation exactly as it is.
- Rewriting: restructure a section or rewrite its sentences. Keep every fact and every claim. Flag any claim that cannot be kept.
- Writing: draft new text from the user material. Mark every missing fact as `[NEED: ...]` and every unverified fact as `[CHECK: ...]`.

Read `references/editing-scopes.md` for the full boundary table of what each scope may and may not change.

## Workflow

1. Confirm the scope and the text to edit. For a long document, work one chapter at a time and report per chapter.
2. Check spelling and EYD V first, with `references/eyd-kbbi.md`. Fix what breaks a rule. Leave what the rule allows.
3. Remove machine patterns with `references/ai-patterns.md`. Tag each finding with its code (K for rule, G for style, AI for machine cliche) and show the before and after.
4. Check the do-not-correct list with `references/keep-it.md`. Restore anything the edit broke by over-correcting.
5. Check consistency: one concept one term, one spelling for every key term, the same voice in every chapter, figure and table numbers matching the lists.
6. Report the result as a table with location, issue, code, and fix. Never rewrite silently. Never present a revised text as the user original.

## Machine patterns

The catalog in `references/ai-patterns.md` lists the patterns in order of strength, from cosmic openers and empty intensifiers to English calques, repeated connectors, inflated claims, and flat rhythm. All patterns are signals, not proof. A human writer also uses them. A pattern marked weak alone is acted on only when it appears together with other signs or repeats.

Fixing a pattern must use only facts already in the text. When a fix needs a fact that is not there, use `[NEED: ...]` or `[CHECK: ...]` and ask the user, never invent it.

## What this skill will not do

- Rewrite a text so it passes an AI detector or hides that AI helped write it. Removing machine patterns from the user own writing is honest editing. Disguising AI output as the user own writing is not editing, and this skill refuses it.
- Change numbers, data, citations, quotes, or findings.
- Flatten the author voice into sterile prose. A consistent author style is worth more than a sterilized text.
- Promise a plagiarism or AI-detector score.

## References

- `references/editing-scopes.md`: what each editing scope may and may not change.
- `references/eyd-kbbi.md`: EYD V and KBBI essentials for academic prose.
- `references/ai-patterns.md`: machine-pattern catalog with codes and before-after examples.
- `references/keep-it.md`: legitimate conventions that must not be corrected.

## Sources and credit

Editing scopes, machine patterns, and the do-not-correct list are adapted from naskah-id by nothinx (MIT). The language routing follows indonesian-academic-writing by azkadani214 (MIT). See the repo README for the full attribution list.
