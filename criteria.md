# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. _"Retrieval works"_ is an opinion. _"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"_ is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; _"80% seemed reasonable"_ does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->

**Why this target:**

I wrote my five questions against documents I had already read, so every one of
them has an answer that exists somewhere in the corpus: the walking time across
Brightwater, the shop hours in Elder Ness, what there is to see in Pellew
Sands. The questions are relevant to the chunks by construction. That means
this criterion is not testing whether my corpus covers the questions — I
already know it does. It is testing whether retrieval can find the chunk that
covers them, which is a different thing and the only part that can fail.

I'm allowing one miss rather than demanding 5 of 5 because my questions are not
worded the way the guides are. The guides are organised under section headings
like `## Getting around` and `## When to go`, written in flat declarative
sentences. My questions are phrased the way a person would actually ask one —
"If I need to get basic items; what time should I got shopping in Elder Ness?"
Where a question and the sentence holding its answer share almost no
vocabulary, embedding similarity has to bridge that gap on meaning alone, and I
expect it to fail on at least one of the five.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->

**Why this target:**

All five, because citing a source is a requirement of this system rather than a
score to average. Every answer has to point back at the document it came from —
an answer about Pellew Sands that doesn't say `guide_pellew_sands.md` gives me
no way to check it, and an uncheckable answer is the thing this whole pipeline
exists to avoid. Four out of five would mean one answer a run that the reader
has to take on trust. There is no version of that I'd accept, so the target is
the only one the criterion can honestly have.

It's achievable at 100% because naming a source isn't left to the model's
discretion. Two separate things produce one. `generate.py` puts
`[from <filename>]` above every excerpt in the prompt and its system
instruction tells the model to name the document it used — but even if the
model ignores that, `app.py` prints `Sources retrieved:` from the retrieval
results themselves, before generation is involved at all. One of those two
paths is deterministic.

For this to come out below 5 of 5, something would have to break upstream of
the model: retrieval returning nothing, or a chunk reaching the prompt without
the `source` field that `Chunk` carries from `ingest.py`. Both would be bugs in
my own code rather than the model behaving unpredictably. Note that this
criterion only asks whether a source is _named_, not whether it is the right
one — criterion 5 is where the content gets checked against the chunk.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->

**Why this target:**

The two groups don't overlap at all. My worst real question (Elder Ness, 0.510)
and the closest out-of-corpus one (Mongolia, 0.803) are 0.293 apart, and
nothing lands in between — so any cutoff in that range separates them
perfectly. I kept `THRESHOLD = 0.6`, which sits in the lower half of the gap
on purpose: it leaves 0.09 of headroom above the Elder Ness question, which is
my worst-worded one and the one most likely to drift, while still refusing
"What is the weather like in Tokyo in April?" at 0.66 — a question that borrows
this corpus's vocabulary of months and seasons and would have slipped through a
0.7 cutoff.

Against distances that clean, 4 of 5 is a conservative target and I expect 5 of
5 — these five questions are from a different world entirely, and nothing about
a diesel engine or the 1994 World Cup resembles a travel guide. The margin is
there for a different reason: the gate has to keep working when the question is
_nearly_ in scope, and the genuinely hard cases aren't in `OUT_OF_SCOPE` at
all. Questions that borrow this corpus's vocabulary without being answerable
from it — a cinema in Marchwood, a hotel with a pool in Brightwater — score
between 0.47 and 0.53, inside my in-corpus range, and no distance cutoff can
refuse them without also refusing real questions. Those get caught by the
grounding instruction in the prompt instead, not by this gate. So this
criterion measures the easy half of refusal honestly, and I'd rather it say
that plainly than claim a perfect score that a harder set of questions
wouldn't support.

---

## 4. Something about your chunks

Only information from the relevant chunk is used as the source, so as not to
confuse the output LLM.

Stated as a target: at least 4 of 5 sampled chunks contain material from
exactly one `##` section of their source document. No chunk spans two topics.

**Why this target:**

My documents are all built the same way — `## Getting there`, `## Getting
around`, `## Eat and drink`, `## Where to stay`, `## When to go`,
`## Practical notes` — and the plain 800-character chunker ignores every one of
those boundaries. `guide_corry_vale.md#2` is a single chunk carrying three
sections at once: where to stay, when to go, and practical notes. If someone
asks where to stay in Corry Vale and that chunk comes back, the model also
receives the gritting schedule and the location of the nearest hospital, and
has to decide on its own to ignore them. That's the confusion I want to
prevent, and one topic per chunk is the version of it I can actually count.

I'm allowing one miss in five because a couple of these sections are long
enough that they have to be split, and a chunk that is half of one section is
still only about one topic — I'd rather the target tolerate that than punish
it.

---

## 5. Your choice

I think the response should be able to not only take right context to answer
the question, but also reason on it. For example if the chunk says that the
store is open from 12-4 and the user asks what times to avoid, it should give
times outside 12-4.

Stated as a target: for at least 4 of my 5 test questions, the answer states
the conclusion in the terms the question asked for, rather than only the fact
it was derived from. I score each answer yes/no against the chunk it came
from: did it hand me the answer, or did it hand me the raw fact and leave the
last step to me?

**Why this target:**

Four of my five questions are built this way on purpose. `guide_elder_ness.md`
never says when to go shopping — it says the shop "closes at 5pm and all day
Sunday". A passing answer has to turn that into _go before 5pm, not on a
Sunday_; an answer that just repeats the closing time has retrieved correctly
and still not answered me. Same shape for the Marchwood budget question and
the Kestrelford meetup question: the fact is in the corpus, the form I asked
for is not.

I'm allowing one miss rather than demanding 5 of 5 because a question whose
chunk never arrives can't be reasoned over at all, and criterion 1 already
allows one retrieval failure. Without that allowance this criterion would just
be measuring retrieval a second time.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
