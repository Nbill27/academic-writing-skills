---
name: outline
description: "Build and check the outline of any Indonesian academic document before drafting, or condense existing files into one outline. Covers skripsi (undergraduate thesis), tesis, disertasi, proposal, internship and KP reports, papers, and reports. Starts from a core map of the gap, adapts to any campus guide through 14 variables, and gives the title last. Use for build outline, create outline, thesis outline, internship outline, check title readiness, or condense files into an outline."
license: MIT
compatibility: "Hermes, CodeBuddy, Claude Code, OpenCode, Codex, and any agent that reads the Agent Skills format."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Outline

Build the frame first. A weak document almost never fails at the sentence level. It fails because nobody decided, before writing, who reads it, what gap it closes, and what each section must prove. Fixing the outline once does more than rewriting sentences ten times.

This skill produces an outline, not finished prose. When the outline passes the check, hand drafting to the `draft` skill and editing to the `edit` skill.

## Hard rules

- Never invent facts. No made-up numbers, sources, quotes, survey results, company names, or regulations. Anything the user must supply is written as `[NEED: ...]`. Anything not sure is written as `[CHECK: ...]`.
- Citations only from sources the user gave. If a claim needs a source that is not there, write `[CHECK: source for ...]`. Never guess a year, volume, or page.
- Title last. The title is written after the outline and the check. If checks fail only because the user data is missing, still give the titles but label them provisional. If a check fails for a structural reason such as no gap or an orphan question, fix the outline first and give no title.
- Campus rules win. University guidelines differ. When a structure is a convention, not a law, say so and add `[CHECK: campus guide]`.
- No orphans. Every question, claim, or promise in the outline must have a section that answers it and evidence that supports it. Every section must serve one of them.
- Ask at most one question before starting. If information is missing, fill with `[NEED: ...]` and keep going. The user should get a usable outline in one reply.

## Workflow

### Step 0, classify

Decide four things silently. Do not ask if the user already said them.

- Language: Indonesian, English, or another language.
- Genre: research (skripsi, proposal, tesis, disertasi, journal article), report (internship report, KP, PKL, activity report), or study (mind map, summary).
- Reader: examiner, supervisor, decision maker, or another reader.
- Mode: From scratch (topic only), From material (notes, data, draft), or Condense (existing files into one outline).
- Campus: if the user names a campus, read `references/guide-adapter.md` and fill the 14 variables before the outline. If the user gives a guide file, read it and fill the variables from it. If there is no guide, use the defaults and mark every risky item `[CHECK: campus guide]`.

### Step 1, core map

Every useful document closes a gap between how things should be and how they are. Fill this table before any outline.

- Should: theory, norm, regulation, or target.
- Is: field facts and data.
- Gap: the research problem, stated as the difference between Should and Is.
- Reader: who reads and judges the document.
- Core claim: the answer the research will test, written as one sentence a stranger understands. If the claim cannot be written in one sentence, the outline is not ready.
- Proof: method and data.
- Action: contribution and recommendation.

Rule: if Should and Is do not differ, there is no document yet. Say so and ask for a fact from the field, or propose two candidate gaps marked `[CHECK: ...]`.

### Step 2, outline from the genre template

Open the genre file and fill its template. For research use `references/genre-research.md`. For reports use `references/genre-report.md`. For each section write the heading, the job (what the section must make the reader believe or do, in one line), 2 to 5 content points (facts or `[NEED: ...]`), the evidence (data, source, example, or `[NEED: ...]` or `[CHECK: ...]`), and a length hint (words, pages, or slides).

Order sections by what the reader needs next, not by the order the writer learned things.

### Step 3, check

Run `references/checklist.md`: the universal checks first, then the genre checks. Report the result as a short table with item, status, and fix. Fix failures in the outline, then re-run only the failed items. Two rounds maximum. If still failing, show what is blocked and why, usually missing user data.

### Step 4, title and handoff

- Give 3 title options, each built from the core claim. Follow the campus title rules from the filled variables, for example a word limit.
- List every `[NEED: ...]` and `[CHECK: ...]` item in one block at the end, so the user knows exactly what to bring.
- Write one line for the next step, for example "Discuss with the supervisor with the source notes attached" or "Continue to the draft skill for drafting".

## Output format

Use this skeleton. Keep it in the user language. No emoji. No motivational filler.

```
## 1. Core map
(table from Step 1)

## 2. Outline
(numbered sections, each with Job, Content, Evidence, Length)

## 2b. Appendix outline
(appendix n. Title [MANDATORY/USUALLY/IF APPLICABLE], Job, Content, Referenced from, When collected)

## 3. Check result
| Item | Status | Fix |

## 4. Title options
1. ...

## 5. What you need to complete
- [NEED: ...]
- [CHECK: ...]
```

## Modes of depth

- Quick (default for short reports and study maps): Step 1 table with 5 rows (Reader, Should, Is, Gap, Action), outline, checks U1, U2, U4, U8, U9, U13 plus every check of the genre file.
- Full (default for skripsi, tesis, disertasi, proposal, and internship reports): everything above, plus section 2b and the mapping table required by the genre file, for research that is question to objective to chapter to evidence to conclusion to recommendation.

The user can override with "quick version" or "full version".

## What this skill will not do

- Write a full skripsi, tesis, or assignment for submission as the student own work. It builds the outline and explains the reasoning so the student can write it and defend it.
- Promise a plagiarism or AI-detector score. Clean structure and honest wording lower similarity. No tool can guarantee a number.
- Fabricate data, respondents, or literature to fill a gap.
- Disguise AI output as the student own writing. Offer to draft from the student own material instead.

## References

- `references/guide-adapter.md`: adapt the outline to any campus guide, 14 variables, authority order, adaptation checks A1 to A8.
- `references/checklist.md`: universal checks U1 to U15 and check statuses.
- `references/genre-research.md`: research outline template, Chapter I to Chapter V, with the traceability mapping.
- `references/genre-report.md`: report outline template for internships, KP, and work reports.

## Sources and credit

The core map, title-last rule, checklist, and adapter design are adapted from rangka by Bryan Kwandou (MIT). See the repo README for the full attribution list.
