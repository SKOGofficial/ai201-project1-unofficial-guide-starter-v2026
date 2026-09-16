"""
Your test questions.

Milestone 2 asks you to write five questions your system should be able to
answer from your corpus, specific enough to have a right answer.

  ✗ "What are good dining halls?"          — no right answer
  ✓ "What do students say about wait times at Commons during lunch?"

Fill in `QUESTIONS` below. `expects` is a word or short phrase you'd expect a
correct answer to contain — you'll use it in unit 2 when you build a scorer,
and having written it now means you decided what "correct" meant before you saw
any results.

`OUT_OF_SCOPE` holds five questions your documents clearly don't cover. You
need these in Milestone 4 to find where your relevance cutoff belongs, and
again in unit 2, where `run_eval.py` runs them through the gate and writes what
happened into your run log — that's the evidence for criterion 3.

Swap them for your own if you like. Keep five of them either way: criterion 3
names a target of "4 of 5", and four of three is not a thing.
"""

QUESTIONS = [
    # {"question": "...", "expects": "..."},
    {"question": "How long does it take to walk the town of Brightwater?", "expects": "It takes aproximately 35 minutes to walk the town from end-to-end."},
    {"question": "If I need to get basic items; what time should I got shopping in Elder Ness?", "expects": "You should go shopping in Elder Ness during the morning hours, between 9 AM and 12 PM."},
    {"question": "When is the best time to book a hotel in Marchwood if I am on a low budget?", "expects": "The best time to book a hotel in Marchwood on a low budget is during the off-season, which is typically in the fall and winter months."},
    {"question": "What is there to see in Pellew Sands?", "expects": "There are several attractions in Pellew Sands, including the historic lighthouse, the scenic beachfront, and the local art gallery."},
    {"question": "What is a central location for my friends to meetup that want shops and amenities close by in Kestrelford?", "expects": "The central location for your friends to meetup in Kestrelford is the town square, which has several shops and amenities within walking distance."},
]

# Questions from a different world entirely. Your gate should refuse all five.
#
# There are five of these because criterion 3 in criteria.md names a target of
# "at least 4 of 5" — you need five things to try before you can report 4 of 5.
# `run_eval.py` runs these through retrieval and the gate on every eval and
# records what happened, so criterion 3 has evidence in the run log alongside
# the others. They cost no model calls: a refusal never reaches the model.
OUT_OF_SCOPE = [
    "What is the capital of Mongolia?",
    "How do I change the oil in a diesel engine?",
    "Who won the 1994 World Cup?",
    "What is the recommended dosage of ibuprofen for a headache?",
    "How do I write a for loop in Rust?",
]


def answered() -> list[dict]:
    """The questions you've actually filled in."""
    return [q for q in QUESTIONS if q.get("question", "").strip()]
