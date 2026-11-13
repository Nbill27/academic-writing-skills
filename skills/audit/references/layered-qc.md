# Layered checks

Stage gates answer "is this stage done". Layers answer "is this draft ready to submit". Both are mandatory, and the layers run in order and cannot be skipped. A failed layer is a blocker for the next layer, because manual checking at a higher layer wastes time while mechanical errors remain.

## Layer 1, Style

Purpose: remove machine-writing patterns and keep the meaning. This layer cleans the style of the student own writing. It does not disguise AI output and it does not help evade detectors.

- Machine patterns from the `edit` skill checked (ai-patterns codes).
- No generic chapter opening or closing sentences.
- The thesis sentence of each subchapter exists and is not a repeat of the title.
- No dash used as a connector.
- Excessive intensifiers and adverbs reduced.
- Facts unchanged: numbers, quotes, markers, and the problem formulation stay intact.

## Layer 2, Mechanics and EYD

Purpose: spelling, punctuation, capitalization, and standard forms. Fully checkable by script.

- Spelling, particle, and vague-formula findings are zero.
- Decimal, spacing, and non-Latin findings are zero.
- Absorbed terms are decided, not ignored.
- Every plagiarism-signal finding is verified manually and recorded.
- Note on plagiarism signals: a run of matching words is a signal, not proof. Standard terms, instrument names, and standard definitions will always trigger signals. What is checked is whether every finding has a recorded decision, not whether the count is zero.

## Layer 3, Semantics

Purpose: the draft is right in meaning, not only in mechanics.

- Terminology is consistent: one concept, one term, in the whole draft.
- 1 to 1 match: problem formulation equals objectives equals hypotheses equals the Chapter III tests.
- No claim without a source: every empirical claim has a marker.
- No unmarked inference: agent reasoning is marked as inference.
- Numbers are consistent: values in Chapter I, Chapter III, and the abstract match.
- No leap of logic: every conclusion has premises from the analysis.
- Definitions and theory carry references, not rewrites from another source.
- The analysis design matches the true dataset profile.
- Chapter II is not a list of summaries: each subchapter ends with an implication for the research.

## Layer 4, Red-team (read as the supervisor)

Purpose: read the draft like a supervisor who rejects, not like a writer who defends. One accent, one persona, one-sheet verdict.

| Red-team question | Required answer |
|---|---|
| Can I approve this proposal right now? | Yes or no, with a reason |
| What is the single most fatal weakness? | One item, specific |
| Is the research gap real, not only read about? | Provable from sources |
| Is the method feasible with the data and time at hand? | Yes or no |
| Is the scope too broad for one proposal? | Yes or no |
| Do the hypotheses have a theoretical basis? | Yes or no |
| Is there any part that feels copied? | Name the location |
| Which chapter would I reject first? | Name the chapter |
| If I were the student, would I understand this proposal? | Yes or no |

When any answer is "no" without a fix, Layer 4 fails.

## Pass rubric

| Aspect | Weight | Score | Note |
|---|---|---|---|
| Clarity of the problem formulation | 25 | | |
| Theory basis and gap position | 20 | | |
| Method and data fit | 20 | | |
| Originality and novelty | 15 | | |
| Language and structure quality | 20 | | |

Pass mark: total score at least 75 and no aspect scored 0. Below that, return to the relevant stage, not to Layer 1.

All layers must pass before the draft is handed to the user.

## Sources and credit

Adapted from references/quality-gates.md in proposal-skripsi-skill by Bima Januri (MIT).
