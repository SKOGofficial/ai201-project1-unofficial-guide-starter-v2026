# The Unofficial Guide

**Name:** <!-- your name here -->  
**Corpus:** `city_guides` — 14 regional travel guides, 28,958 characters.

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Chunk size:** 400 characters (a ceiling, not a fixed width)
**Overlap:** 100 characters
**Minimum:** 50 characters

I split on paragraph boundaries rather than character counts. One paragraph is
one chunk, unless it runs over 400 characters, in which case it is cut into
overlapping windows at sentence ends.

**Why these numbers.** I measured my corpus before choosing. In `city_guides`
the median body paragraph is 243 characters, and each paragraph is one idea —
bus frequencies, or opening hours, or where to park. 400 sits above almost all
of them: only 1 of 115 paragraphs exceeds it, so the ceiling almost never
fires, and when it does the 100-character overlap keeps a sentence that
straddles the cut whole in one of the two pieces. The 50-character minimum is
there because anything shorter in these documents is a fragment or a bare
heading, never a thought.

**What the starter did first.** `python app.py index` on the original
`fallback_split` reported:

```
chunked  51 chunks, 650 characters on average (shortest 24, longest 800), produced by chunker.py::fallback_split
```

Two things in that line pushed me off fixed-width chunking. The shortest chunk
was 24 characters — `guide_kestrelford.md#3` was a leftover tail, two half
sentences about a minor injuries unit and nothing else, produced only because
the document didn't divide evenly by 800. And the 800-character window ignored
the section headings every one of my documents is built around
(`## Getting there`, `## Eat and drink`, `## Where to stay`…). One chunk,
`guide_corry_vale.md#2`, carried three sections at once: where to stay, when to
go, and practical notes. A question about accommodation would pull back the
gritting schedule and the nearest hospital along with it.

After the change:

```
chunked  117 chunks, 246 characters on average (shortest 71, longest 393), produced by chunker.py::split_documents
```

The 246-character average against a 243-character median paragraph is the
strategy doing what it claims: one paragraph, one chunk.

**One thing I changed partway through.** My first version used length alone to
decide whether a block was too small to stand on its own. That let
`guide_eating.md#0` and `guide_seasons.md#0` through as pure heading stacks —
`# Eating across the region` followed by `## The pattern worth knowing`, 55
characters of headings with no content under them. Two short headings stacked
together clear a 50-character floor. I added `_headings_only()` so a block with
no actual content is always carried forward onto the paragraph beneath it,
whatever its length. That is also why 80% of my chunks now open with the
heading they belong to, which matters for retrieval: without it,
`guide_regional_transport.md#7` reads "Cycling is pleasant on the river path
and unpleasant on Mill Road" and never says which region it is describing.

**Milestone 3 answer — would splitting on headings be better?** For this corpus
it would work well: the median `##` section is 282 characters, already close to
my ceiling, and a heading is a *labelled* boundary where a blank line is not.
But it doesn't replace what I built. 11 of 98 sections are over 400 characters
(the longest is 708), so a size ceiling and splitting logic are still needed
underneath it. And it doesn't travel: `campus_life` and `advice_threads` have
no markdown headings at all across 111 documents, where a heading-only chunker
would degrade to one chunk per document. Paragraph splitting works on all
three. What I have is effectively the hybrid — headings bound the outside and
get carried onto their content, paragraphs subdivide within them, 400 caps it.

## Sample Chunks

Produced by `chunker.py::split_documents`, printed with `python app.py chunks -n 5`.

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
# Getting around the region with limited mobility
An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Chunk 2** — source: `guide_corry_vale.md#4` — produced by: `chunker.py::split_documents`

```
## What to see
The valley itself is the attraction. The footpath network is dense and well marked, and a circuit taking in three of the four villages is about nine miles with 500 metres of ascent. The chapel in the second village is 12th century and always unlocked.
```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
## Getting around
Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.
```

**Chunk 4** — source: `guide_marchwood.md#1` — produced by: `chunker.py::split_documents`

```
## Getting there
Every railway line in the region meets here, which is the city's defining feature. Trains to Brightwater run every 40 minutes until 11pm. The airport is 20 minutes out by a dedicated bus that runs every 15 minutes and costs more than the equivalent taxi shared between three people.
```

**Chunk 5** — source: `guide_seasons.md#0` — produced by: `chunker.py::split_documents`

```
# When to visit the region
## Spring, March to May
Days lengthen quickly and businesses that closed for winter reopen through
March and April. By May everything is open and the weather is reliable enough
to plan around. Late May is arguably the best week of the year in Brightwater —
long days, everything running, and the students gone.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**

**Answer:**

```
```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
|  |  |  |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**

**2.**

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
