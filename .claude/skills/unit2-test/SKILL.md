---
name: unit2-test
description: Walk through AI201 Project 1 Unit 2 (Testing) end to end — run the eval, score all five criteria, reach verdicts, diagnose misses, make one measured improvement, and fill in the README. Use when the user says "unit 2", "run my eval", "score my criteria", "diagnose my misses", "do the improvement", or asks to continue the testing assignment.
---

# AI201 Unit 2 — Testing walkthrough

Drive the whole Unit 2 assignment. You do every mechanical step. The user makes
every judgment call.

## Division of labor — non-negotiable

**You do, without asking:** run commands, read result files, count passes and
fails, quote evidence, print chunks, trace failures through the pipeline, edit
README and criteria.md once wording is agreed, stage and commit.

**You ask, always:** every MET/MISSED verdict, every criterion revision, which
improvement to make, every diagnosis before it is written down, and all
"what I'd do differently" and "why I stopped" content.

Never score a criterion silently and move on. Propose the count, show the
evidence, let the user confirm or overrule. Their call is final even when you
disagree. If you disagree, say so once in a sentence, then record their call.

## Hard rules from the assignment

1. **Three runs minimum.** A rate target needs repeated trials.
2. **Verdicts use the Unit 1 target.** Never a new one. Counts of 4, 3, 4
   against a target of 4 of 5 is MISSED.
3. **Missing costs nothing. Loosening a target to pass costs the diagnosis.**
   Never soften a number to make it green.
4. **Revisions go underneath originals in criteria.md, never over them.** Only
   a measurement problem justifies one. "I missed it" does not.
5. **Exactly one system change this unit.** If the user wants a second, it is
   stretch credit and must be declared in the README first.
6. **At least four new commits.** Commit at the end of every phase.
7. Do not delete or recreate the repo. History is the proof.

## Repo facts

Paths and commands, all from the repo root with the venv Python:

- Run the eval: `.venv/Scripts/python.exe run_eval.py --label before`
- Inspect retrieval: `.venv/Scripts/python.exe app.py retrieve "question"`
- Sample chunks: `.venv/Scripts/python.exe app.py chunks`
- Rebuild index: `.venv/Scripts/python.exe app.py index`
- Corpus docs live under `corpora/city_guides/documents/`
- Results land in `results/`, which is deliberately tracked, not ignored.
- The README Unit 2 scaffold already exists with all six required sections and
  empty tables. Fill them. Do not rewrite Unit 1 above them.
- `scorer.py` does not exist, so the Run columns in `results/` come out blank.
  That is allowed by the assignment. Judge from the pasted transcript instead.

Verify anything below before relying on it. It was true when this skill was
written and the repo moves.

## Criterion-to-measurement map

This is the step people get wrong. The file in `results/` has one row per
question. The README wants one row per criterion. They are not the same table.

| # | Criterion | Target | Where the number comes from |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | 4 of 5 | Sources and chunk text in the transcript. Does any retrieved chunk hold the answer? |
| 2 | Every answer names a source | 5 of 5 | The answer text. Does it name a `.md` file? |
| 3 | Gate stops out-of-corpus questions | 4 of 5 | Already measured. The gate table in the results file. One deterministic pass, so the same number goes in all three run columns. |
| 4 | One section heading per chunk | 4 of 5 sampled | From `app.py chunks`. Not from the questions at all. Sample five chunks and count how many span more than one heading. |
| 5 | Answer states the conclusion in the asked-for form | 4 of 5 | The answer text against the chunk it came from. Did it hand over the answer, or the raw fact? |

Criterion 1 is per run, but retrieval is deterministic, so it will not move
between runs unless the index changed. Criteria 2 and 5 are the ones that vary.

---

# Phase 0 — Preflight and test definitions

## 0.1 Check state

Run these and report anything broken:

```bash
git status --short
```

If there is no index, run the index command. If `test.py` fails on something it
passed last unit, run `pip install -r requirements.txt` inside the activated
venv first.

## 0.2 Audit the expects fields — ASK

The `expects` field in `questions.py` is what "correct" means. If it does not
match the corpus, every score downstream is meaningless. Check all five before
scoring anything.

For each question, grep the corpus for the claim and build this table:

| Question | What expects claims | What the corpus says | Status |
|---|---|---|---|

Known state as of 2026-10-04. Re-verify it:

- **Brightwater.** Expects 35 minutes. The corpus agrees, in the Brightwater
  guide. Retrieval never returns that chunk. The expects is fine and the system
  fails.
- **Elder Ness.** Expects 9 AM to 12 PM. The corpus only says the shop closes
  at 5pm and all day Sunday. Not supported.
- **Marchwood.** Expects off-season, fall and winter. The corpus says the
  opposite. It works any time, winter is explicitly fine, and the thing to
  avoid is conference weeks in March and October. Contradicts the corpus.
- **Pellew Sands.** Expects a historic lighthouse and a local art gallery.
  Neither exists. The corpus has an 1890s pier, municipal gardens, and a
  two-mile beach. Invented.
- **Kestrelford.** Expects town square. The corpus says market square. Right
  place, wrong word.

There is also a format problem. The docstring asks for a short phrase a correct
answer would contain, and all five are written as full sentences, so no
substring check can ever match.

**Ask the user** with AskUserQuestion:

> Three of your five expects describe things your corpus does not say. Scoring
> against them would mark correct answers as failures. Fix them first?

Options: fix all five and shorten each to a key phrase, recommended; fix only
the three that contradict the corpus; leave them and score as written.

If they fix, tell them this changes no system behavior and needs no re-run,
because expects only feeds a scorer and there is no scorer. Any existing
before-run output stays valid. Say that so they do not waste a run.

Record it in the README as a measurement correction, not a system change. It
does not consume the one-change budget.

## 0.3 Commit

Commit the corrected questions file before moving on.

---

# Phase 1 — Milestone 1: the before run

## 1.1 Produce or reuse the run

If a before-labelled file already exists in `results/` and the system has not
changed since, reuse it and say so rather than burning model calls. Otherwise:

```bash
.venv/Scripts/python.exe run_eval.py --label before
```

## 1.2 Score it

Read the full results file. For criteria 1, 2 and 5, go question by question
and run by run. For each cell, quote the line you scored on. Build a per-run
count out of five.

For criterion 4, run the chunks command, sample five chunks, and count how many
carry more than one section heading. Report which chunk and which headings.

Criterion 3 is already in the file. Copy that number into all three columns and
note that one deterministic pass is the whole measurement.

## 1.3 Present the proposed table — ASK

Show the filled table. For every cell you were unsure about, quote the text and
explain why it was borderline. Then ask the user to confirm or correct the
counts before anything gets written down.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|

Leave the Verdict column blank at this stage. That is Phase 2.

## 1.4 Fill the README

Write the agreed table into the Run Log — Before section. Underneath it, paste
the real output for each criterion from one run, as text, not as a description.
Name the producing file and function. That is `run_eval.py::main` for the
questions and `run_eval.py::check_out_of_scope` for the gate.

## 1.5 Commit

---

# Phase 2 — Milestone 2: verdicts

## 2.1 Propose verdicts — ASK

For each criterion state the target, the three run counts, and the verdict the
numbers force. Apply the rule plainly. The target has to hold on every run, not
on average and not usually.

Ask the user to confirm all five. Use one AskUserQuestion per criterion where
the call is close. Where it is not close, state it and move on.

## 2.2 Offer the adversarial check

The assignment suggests arguing the opposite verdict. Offer it once:

> Want me to argue the opposite verdict on any of these as hard as I can before
> you commit to it?

Only do it if they say yes.

## 2.3 Criterion revisions — ASK

A revision earns credit only when the criterion could not be measured
consistently. Flag any criterion where you had to make an arbitrary call.

Criterion 5 is the likely candidate. "States the conclusion in the terms the
question asked for" was ambiguous on Marchwood, where every run answered with
what to avoid rather than when to go. That is a measurement problem rather than
a result problem, so it qualifies. A workable revised rule: a pass requires the
answer to name something the reader could act on, so a "when" question needs a
time or a range, and an answer that only names times to avoid fails.

Also worth raising. Criterion 5 only bites on three of the five questions.
Pellew Sands is a plain listing with nothing to infer, and Brightwater cannot be
scored at all while retrieval misses the chunk. A target of 4 of 5 over an
effective sample of 3 is worth saying out loud in the write-up.

If the user revises, append underneath the original in `criteria.md` using the
format shown at the bottom of that file. Never touch the original line.

## 2.4 Fill the README and commit

Write the verdict table with one sentence of reasoning per row.

---

# Phase 3 — Milestone 3: diagnoses

## 3.1 Investigate each miss yourself

Work backwards. For every missed criterion, run the check before proposing
anything:

```bash
.venv/Scripts/python.exe app.py retrieve "the question"
```

Then print the retrieved chunk text directly, so you can see what the model
actually received rather than guessing from a preview. Write a short throwaway
script to a temp path that calls `search` from `store.py` and prints each
result's source, label, distance and full text, then run it with the venv
Python.

The split is simple. If the answer is in none of the chunks, the failure is at
or before retrieval. If it is sitting in a chunk and the answer still came out
wrong, the failure is generation. That one check separates most failures.

## 3.2 Name stage and mechanism

Five stages: loading, chunking, embedding, retrieval, generation. A stage name
alone is not a diagnosis. You need what happened there.

Known leads. Re-verify before using:

- **Brightwater, retrieval.** Best distance 0.253 passes the gate comfortably
  and the Brightwater guide never appears in the top five. The walking-time
  sentence sits in a getting-around section, and the question's wording pulls
  the general walking guide instead. A confident score on the wrong document.
- **Marchwood, generation.** The retrieved chunk opens with the words "Any
  time" and all three runs returned only the conference-weeks warning. The
  model had the answer in the first two words of the chunk and returned its
  complement.

Look for the pattern across misses. Several failures sharing one cause is a
single finding and is worth more than three separate explanations.

Worth raising with the user: the question that scored the best distance is the
one that failed hardest. That weakens distance alone as a confidence signal and
is a sharper observation than a clean pass would have been.

## 3.3 Confirm before writing — ASK

Present each diagnosis as stage, then mechanism, then the evidence you ran. Ask
the user to confirm, correct, or replace it. Write only what they approve.

If nothing was missed, say so, then ask which criterion they would tighten and
to what. A clean sweep usually means safe targets rather than a strong system.

## 3.4 Fill the README and commit

---

# Phase 4 — Milestone 4: one improvement, measured

## 4.1 Pick it — ASK

This is the user's decision. Do not choose for them. Present the menu with the
diagnosis each option would address, and say plainly which diagnoses it would
not touch.

- **Hybrid search with BM25.** Already in requirements.txt, so no install.
  Targets retrieval misses where the question shares proper nouns with the
  right document. Most likely to fix Brightwater, since the town name is a
  literal term the keyword half would match and the semantic half glides past.
- **A different chunking strategy.** Size, overlap, or splitting on section
  headings. Targets criterion 4 directly and may move criterion 1.
- **Tighten the grounding prompt.** Targets generation misses like Marchwood,
  where the model held the right chunk and answered adjacent to the question.
- **Tune the gate or top-k.** Only if a diagnosis pointed there.

Ask them to connect the fix to a specific diagnosis in one sentence. If they
cannot, say so plainly, because that is the sign of a fix picked for looking
impressive rather than one the evidence pointed at.

Then do what the assignment asks and argue against their choice. Give two or
three sentences on why it might not work, before building it.

## 4.2 Build exactly one thing

One change. If the work starts sprawling into a second fix, stop and confirm
which one they meant.

## 4.3 Re-run and re-score identically

```bash
.venv/Scripts/python.exe run_eval.py --label after
```

If chunking changed, rebuild the index first.

Score with the same rules as the before run. Using a looser rule on the after
run is the easiest way to lose credit in this unit.

## 4.4 Did it help — ASK

Present both tables side by side with the deltas. Then ask the user for their
own call on whether it helped, in their words. A change that made things worse
earns full credit when reported honestly, so do not soften a regression.

## 4.5 Fill the README and commit

Fill in what changed, why it was picked, the after table, and the did-it-help
answer.

---

# Phase 5 — Milestone 5: what's left, and submit

## 5.1 What's Still Broken — ASK

For every criterion still missed, draft what you would do next based on the
diagnoses. The user supplies why they stopped. Do not invent a reason for them.
Running out of time is acceptable when true, and better than pretending the
work is finished.

## 5.2 What I'd Do Differently — ASK

Which of the five criteria they would write differently next unit, and why.
Offer candidates from what the scoring actually ran into. The choice and the
reasoning are theirs.

## 5.3 Update How I Used AI

Unit 1 already has this section. Append what happened this unit, especially any
use of a model to spot patterns across failures. Ask the user to confirm the
description is accurate before writing it.

## 5.4 Final check

Confirm and report:

- README has all six Unit 2 sections filled, with no scaffold comments left
  sitting where content belongs
- criteria.md originals intact, revisions appended underneath
- results/ holds both the before and after run logs, committed
- At least four new commits this unit
- Working tree clean

```bash
git log --oneline -10
```

Then tell the user to submit the same repository URL as Unit 1, and not to
create a new repo.

## 5.5 Offer to push

Ask before pushing. Never push unprompted.
