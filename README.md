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

This is a question-answering system built over `corpora/city_guides` — 14
travel guides to a fictional English region, covering towns and villages like
Brightwater, Marchwood, Kestrelford and Elder Ness, each written in labelled
sections on getting there, getting around, eating, staying, and when to visit.
You ask it a question in plain English; it finds the five passages of those
guides closest to your question, checks that the closest one is actually
related to what you asked, and then has a language model answer using only
those passages, naming the guide the answer came from. Questions the guides
don't cover — the capital of Mongolia, the dosage of ibuprofen — are refused
before the model is ever called, so the system says "I don't have enough
information about that" rather than inventing an answer. It handles specific
factual questions ("how long does it take to walk across Brightwater?") far
better than open-ended ones, and its known weak spot is questions that sound
like the corpus but aren't in it — a hotel with a pool, the best sushi in the
region — which get past the relevance gate and are caught only by the
grounding instruction in the prompt.

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

**Question:** What is there to see in Pellew Sands?

**Answer:**

```
$ python app.py ask "What is there to see in Pellew Sands?"
  (best distance 0.330, cutoff 0.6)

In Pellew Sands, there is an 1890s pier (with the surviving half open and free), municipal gardens located behind the seafront, and a two-mile beach of hard sand (*guide_pellew_sands.md*).

Sources retrieved: guide_accessibility.md, guide_eating.md, guide_elder_ness.md, guide_pellew_sands.md
```

And an off-topic question, refused by the gate before the model is ever called:

```
$ python app.py ask "What is the capital of Mongolia?"
  (best distance 0.803, cutoff 0.6)

I don't have enough information about that.

0 model calls this session
```

**My relevance cutoff:** `THRESHOLD = 0.6` (kept the starter value, now backed
by measurement). `TOP_K = 5`.

| Question | In corpus? | Best distance |
|---|---|---|
| How long does it take to walk the town of Brightwater? | Yes | 0.253 |
| What is there to see in Pellew Sands? | Yes | 0.330 |
| When is the best time to book a hotel in Marchwood if I am on a low budget? | Yes | 0.407 |
| What is a central location for my friends to meetup … in Kestrelford? | Yes | 0.483 |
| If I need to get basic items; what time should I got shopping in Elder Ness? | Yes | 0.510 |
| What is the capital of Mongolia? | No | 0.803 |
| How do I write a for loop in Rust? | No | 0.813 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.849 |
| How do I change the oil in a diesel engine? | No | 0.892 |
| Who won the 1994 World Cup? | No | 0.975 |

**The two groups.** In-corpus questions landed between 0.25 and 0.51;
out-of-corpus between 0.80 and 0.97. The gap runs from 0.51 to 0.80, and 0.6
sits in its lower half on purpose: it leaves 0.09 of headroom above my
worst-scoring real question (the Elder Ness one, which has a typo in it and is
worded loosely), while still refusing "What is the weather like in Tokyo in
April?" at 0.66 — a question that borrows this corpus's vocabulary of months
and seasons and would have slipped through a 0.7 cutoff.

**What 0.6 gets wrong.** I also tried questions that *sound* like they belong
but that the guides don't answer: a cinema in Marchwood (0.50), a hotel with a
pool in Brightwater (0.47), the best sushi in the region (0.53), an airport taxi
fare to Thornby Wells (0.52). They land inside the in-corpus range, so no
distance cutoff can separate them — dropping the cutoff far enough to refuse
them would also refuse two real questions. All four pass the gate. The
grounding instruction in `generate.py` caught every one of them ("I don't have
enough information…"), so I left it as the starter wrote it: the gate handles
the clear misses, the prompt handles these.

**A low distance is not a correct chunk.** The Brightwater walking question had
the *best* distance of all ten (0.253) and its top 5 did not contain the answer.
They were river-path and train-time chunks that share the words "Brightwater",
"walk" and "minutes". The real answer ("walkable end to end in about 35
minutes", `guide_brightwater.md`) ranks 15th at 0.416, because that chunk only
carries its `## Getting around` heading, never the town's name. Raising top-k
to 15 to reach it would bury every other answer in noise, so I left top-k at 5
(4 would have lost the Kestrelford answer, which sits at rank 5). The model
correctly said it didn't have enough information rather than guessing. This is
a chunking problem — carrying the document title onto each chunk — and a
candidate for the Unit 2 improvement.

## How I Used AI

**1. Writing the chunker from my numbers, and catching what it got wrong.**
I had already decided on 400 characters maximum, 50 minimum and 100 overlap,
and my reason for them — that paragraphs in these guides are around 300
characters and each one is a separate idea. I asked Claude to replace
`split_documents` with that strategy. What came back worked and respected all
three numbers, but it decided whether a block was "too small to stand alone"
using length and nothing else. That let two chunks through that were pure
heading stacks: `guide_eating.md#0` was `# Eating across the region` followed
by `## The pattern worth knowing` and nothing else — 55 characters of headings,
which cleared my 50-character floor precisely because two headings had been
glued together. It is exactly the "heading with no content under it" case the
brief warns about, and a length check can't see it. The fix was to test for
content rather than size: `_headings_only()` in `chunker.py` now carries any
block with no body text forward onto the paragraph beneath it, whatever its
length. That dropped city_guides from 119 chunks to 117 and moved the shortest
chunk from 50 characters to 71.

**2. Turning a vague criterion into one I could count.** For acceptance
criterion 4 I wrote "only information from the relevant chunk is used as the
source as to not confuse the output llm." I knew what I meant but it had no
number in it and no way to come out true or false, so I asked Claude to make it
measurable. The first thing it came back with was an argument that my sentence
belonged under criterion 5 instead, because it described what the generator
does with context rather than anything about the chunks — and it rewrote
criterion 5 around it. I disagreed and put it back under 4, because the thing I
actually cared about was that a chunk shouldn't arrive carrying three topics at
once. Restating it as a property of the chunk rather than of the model gave me
something countable: at least 4 of 5 sampled chunks contain material from
exactly one `##` section. The evidence for why it was worth measuring came out
of the starter's own output — `guide_corry_vale.md#2` was a single 800-character
chunk holding where to stay, when to go, and practical notes together.

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

Produced by `run_eval.py::main` (the five questions) and
`run_eval.py::check_out_of_scope` (the gate), three runs per question, caching
off, 2026-10-04 22:42. Full log: `results/run_2026-10-04_2242_before.md`.

Criterion 3 is measured in one deterministic pass rather than three, so the
same number goes in all three run columns. Criterion 1 is also deterministic —
retrieval does not vary between runs unless the index changes — so it too is
constant across the three. Criteria 2 and 5 are the only ones that can move.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4 | 4 | 4 |  |
| 2. Every answer names a source | 5 of 5 | 5 | 5 | 5 |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 | 5 | 5 |  |
| 4. One `##` section per chunk | 4 of 5 sampled | 5 | 5 | 5 |  |
| 5. Answer states the conclusion in the form asked for | 4 of 5 | 2 | 3 | 3 |  |

### A note on measurement, before the numbers

Before scoring anything I audited the `expects` field on all five questions in
`questions.py` against the corpus. Three of them described things the corpus
does not say — a 9 AM to 12 PM shopping window in Elder Ness, an off-season
fall-and-winter answer for Marchwood that the guide directly contradicts, and a
lighthouse and art gallery in Pellew Sands that do not exist. A fourth said
"town square" where `guide_kestrelford.md` says "market square". All five were
also written as full sentences, so no substring check could ever have matched
one.

I corrected all five to short key phrases drawn from the corpus. This is a
**measurement correction, not a system change** — `expects` only feeds a scorer
and there is no scorer, so no pipeline behaviour moved and the before run above
stayed valid without re-running it. It does not consume the one-change budget
for this unit. The originals are preserved in comments in `questions.py`.

### Criterion 1 — retrieved chunks contain the answer

Scored by reading the retrieved chunk text directly out of `store.py::search`,
not from the answer. Four of five questions had their answer in the top five.

| Question | Answer in retrieved chunks? | Where |
|---|---|---|
| Brightwater walking time | **No** | `guide_brightwater.md` never appears in the top five |
| Elder Ness shop hours | Yes | `guide_eating.md#8`, rank 1 |
| Marchwood booking | Yes | `guide_marchwood.md#6`, rank 2 |
| Pellew Sands sights | Yes | `guide_pellew_sands.md#4`, rank 3 |
| Kestrelford meetup | Yes | `guide_kestrelford.md#2`, rank 5 |

The Brightwater miss, in full. The sentence that answers the question is in
`guide_brightwater.md`: "The town is walkable end to end in about 35 minutes."
Here is what retrieval returned instead:

```
--- [1] guide_walking.md#0  dist=0.2526 ---
# Walking in the region
## Easy, on good surfaces
The **Brightwater river path** runs four miles upstream from the town to a weir,
on a made surface, flat throughout. It is the most-walked route in the region
and deservedly so. Continuing downstream from Givens Mill reaches Brightwater in
about three hours.

--- [2] guide_walking.md#7  dist=0.2803 ---
## Seasonal notes
Add four minutes to any Brightwater walking estimate in winter; the path past
the pond ices over and people take the long way round.

--- [3] guide_pellew_sands.md#1  dist=0.2812 ---
## Getting there
... Driving is 50 minutes from Brightwater. ...

--- [4] guide_marchwood.md#1  dist=0.2835 ---
## Getting there
... Trains to Brightwater run every 40 minutes until 11pm. ...

--- [5] guide_thornby_wells.md#1  dist=0.2972 ---
## Getting there
... Driving from Brightwater is 45 minutes on good roads. ...
```

Every one of the five mentions Brightwater. None of them is about walking
around Brightwater. Note also that Kestrelford's answer chunk landed in the
last available slot — at `TOP_K = 4` this criterion would have scored 3 of 5.

### Criterion 2 — every answer names a source

5 of 5 in all three runs, 15 of 15 answers. Real output, run 1:

```
Based on the provided documents, the text does not mention how long it takes to
walk around the town of Brightwater itself. However, it notes that the
Brightwater river path runs four miles upstream from the town to a weir, and
continuing downstream from Givens Mill reaches Brightwater in about three hours
(guide_walking.md).
```

```
In Elder Ness, the shop closes at 5pm and is closed on Sundays (guide_eating.md).
```

```
According to `guide_marchwood.md`, you should avoid conference weeks in March
and October, as they fill the hotels and double the prices.
```

```
Based on the provided documents, what there is to see in Pellew Sands includes
the 1890s pier (whose surviving half is open and free after being partly
destroyed by fire in 1978), the municipal gardens behind the seafront, and the
two-mile beach of hard sand.

Source: `guide_pellew_sands.md`
```

```
Everything in Kestrelford is within a ten-minute walk of the market square
(`guide_kestrelford.md`).
```

The three Brightwater answers are worth noting here: all three correctly
declined to invent a walking time, and all three still named a source. The
criterion asks only whether a source is named, not whether it was the right
one, and this is exactly the case that separates the two.

### Criterion 3 — the relevance gate

Produced by `run_eval.py::check_out_of_scope`, cutoff 0.6. Refused 5 of 5.

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.803 | refused |
| How do I change the oil in a diesel engine? | 0.892 | refused |
| Who won the 1994 World Cup? | 0.975 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.849 | refused |
| How do I write a for loop in Rust? | 0.813 | refused |

The closest out-of-corpus question sits 0.29 above the worst in-corpus one. The
gap I measured in Milestone 4 held.

### Criterion 4 — one `##` section per chunk

From `app.py chunks`, which prints five chunks spread across the corpus,
produced by `chunker.py::split_documents`. All five carry exactly one topic:

```
Chunk 1  |  source: guide_accessibility.md#0
# Getting around the region with limited mobility
An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.

Chunk 2  |  source: guide_corry_vale.md#4
## What to see
The valley itself is the attraction. The footpath network is dense and well
marked, and a circuit taking in three of the four villages is about nine miles
with 500 metres of ascent. The chapel in the second village is 12th century and
always unlocked.

Chunk 3  |  source: guide_givens_mill.md#2
## Getting around
Everything is on one street along the river. The mill is at one end and the
church at the other, eight minutes apart. The riverside path continues in both
directions for as far as you want to walk.

Chunk 4  |  source: guide_marchwood.md#1
## Getting there
Every railway line in the region meets here, which is the city's defining
feature. Trains to Brightwater run every 40 minutes until 11pm. The airport is
20 minutes out by a dedicated bus that runs every 15 minutes and costs more than
the equivalent taxi shared between three people.

Chunk 5  |  source: guide_seasons.md#0
# When to visit the region
## Spring, March to May
Days lengthen quickly and businesses that closed for winter reopen through March
and April. By May everything is open and the weather is reliable enough to plan
around.
```

Two of these are judgement calls I should name rather than hide.
`guide_accessibility.md#0` has *zero* `##` headings — it is the document
preamble under a `#` title. `guide_seasons.md#0` carries the `#` document title
plus one `##` section. I scored both as passes on the standard the criterion
actually states — "no chunk spans two topics" — rather than on a literal count
of `##` lines, and neither spans two topics.

Because the five-chunk sample is small and the two borderline calls could be
argued, I also checked every chunk in the corpus. **Zero of 117 chunks span
more than one `##` section.** The specific failure named in criteria.md —
`guide_corry_vale.md#2` carrying where-to-stay, when-to-go and practical-notes
in one chunk — no longer exists. The paragraph-based chunker from Milestone 3
closed this before unit 2 started, which means this criterion was already
satisfied by work done before any of it was measured.

### Criterion 5 — states the conclusion in the form asked for

The criterion that moved between runs, and the only one that did.

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Brightwater walking time | ✗ | ✗ | ✗ |
| Elder Ness shop hours | ✗ | ✓ | ✓ |
| Marchwood booking | ✗ | ✗ | ✗ |
| Pellew Sands sights | ✓ | ✓ | ✓ |
| Kestrelford meetup | ✓ | ✓ | ✓ |
| **Count** | **2 of 5** | **3 of 5** | **3 of 5** |

Elder Ness is the clearest evidence in the whole log, because retrieval was
byte-identical across all three runs and the answers were not.

Run 1 — scored ✗, the raw fact with the last step left to me:

```
In Elder Ness, the shop closes at 5pm and is closed on Sundays (guide_eating.md).
```

Run 2 — scored ✓, same chunk, conclusion handed over:

```
Elder Ness has one shop, which is closed on Sundays and after 5pm, so you should
go shopping before 5pm on days other than Sunday (guide_eating.md).
```

Marchwood failed all three runs in the same way. The chunk it was given opens
with the words "Any time":

```
## When to go
Any time. This is the one place in the region that works in winter, since almost
everything is indoors and nothing closes seasonally. Conference weeks in March
and October fill the hotels and double the prices; check before booking.
```

Every run returned only the second half of that:

```
You should avoid booking during the conference weeks in March and October, as
these weeks fill the hotels and double the prices (guide_marchwood.md).
```

I asked when to book. It told me when not to.

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
