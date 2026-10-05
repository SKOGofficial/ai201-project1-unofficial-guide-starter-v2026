# The Unofficial Guide — AI201 Project 1

A retrieval-augmented question answering system over a corpus of fictional
regional travel guides. Unit 1 built it and filed five acceptance criteria
before any results existed. Unit 2 tests it against those criteria.

## Working on Unit 2

Run the `unit2-test` skill. It drives the whole assignment: the eval run,
scoring all five criteria, verdicts, diagnoses, one measured improvement, and
the README write-up.

The split it enforces: the agent writes all the code and runs everything. The
user makes the design and judgment calls — what to change and why, every
verdict, every diagnosis, every criterion revision. A knob whose value encodes
a tradeoff counts as a design call and gets surfaced, not buried in a diff.

## Environment

This is Windows. Always use the venv interpreter explicitly rather than a bare
`python`:

```bash
.venv/Scripts/python.exe app.py ask "your question"
```

The Bash tool here is Git Bash, not PowerShell. Use heredocs for multi-line
strings, never PowerShell here-string syntax.

## Commands

| Command | What it does |
|---|---|
| `test.py` | Environment check, ten assertions |
| `app.py index` | Build the vector index |
| `app.py ask "q"` | Answer one question |
| `app.py retrieve "q"` | Show distances only, no model call |
| `app.py chunks` | Print sample chunks |
| `run_eval.py --label X` | Three runs per question, writes to `results/` |

## Pipeline

Five stages, and any failure belongs to one of them: loading in `ingest.py`,
chunking in `chunker.py`, embedding and retrieval in `store.py`, the relevance
gate in `gate.py`, generation in `generate.py`.

Distances are cosine and lower is better. The gate refuses anything whose best
distance is above `THRESHOLD` in `config.py`, currently 0.6.

## Conventions

- `results/` is deliberately tracked, not ignored. Run logs are evidence.
- `criteria.md` originals are never edited. Revisions are appended underneath
  with a reason, so the pre-result version stays visible.
- Unit 1 README sections are never rewritten. Unit 2 content is added below.
- Do not delete or recreate this repository. The commit history is what proves
  the criteria predate the results.

## Grading context

Missing a criterion costs nothing when it is diagnosed honestly. Quietly
loosening a target to make it pass removes the thing being graded. Never soften
a number to make a table look better.
