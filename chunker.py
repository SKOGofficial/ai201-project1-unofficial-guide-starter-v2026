"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _split_long(text: str, size: int, overlap: int) -> list[str]:
    """
    Cut one over-long paragraph into windows, preferring sentence ends.

    Only paragraphs above CHUNK_SIZE ever reach here — on city_guides that is
    1 of 115. The overlap exists for exactly this case: when a paragraph has to
    come apart, neighbouring pieces share CHUNK_OVERLAP characters, so a
    sentence straddling the cut still appears whole in one of them.
    """
    pieces: list[str] = []
    start = 0

    while start < len(text):
        window = text[start : start + size]

        # Prefer to end on a sentence boundary — but not by giving up more than
        # half the window to find one.
        if start + size < len(text):
            cut = max(window.rfind(". "), window.rfind("! "), window.rfind("? "))
            if cut > size // 2:
                window = window[: cut + 1]

        piece = window.strip()
        if piece:
            pieces.append(piece)

        step = len(window) - overlap
        start += step if step > 0 else len(window)

    return pieces


def _headings_only(block: str) -> bool:
    """True if every line is a markdown heading, so the block has no content."""
    return all(line.startswith("#") for line in block.splitlines() if line.strip())


def _blocks(text: str) -> list[str]:
    """
    One document into paragraph-sized blocks.

    A markdown heading is not a thought on its own: "## Getting there" is 16
    characters and answers nothing. Because it falls under CHUNK_MIN it gets
    carried forward onto the paragraph beneath it, which is how each chunk ends
    up naming the topic it belongs to.
    """
    blocks: list[str] = []
    carry = ""

    for raw in re.split(r"\n\s*\n", text):
        block = raw.strip()
        if not block:
            continue

        if carry:
            block = f"{carry}\n{block}"

        # Too small to stand alone, or all heading and no content — either way
        # it waits and joins the paragraph beneath it. Length alone is not
        # enough: a document title stacked on a section heading clears
        # CHUNK_MIN between them and still says nothing.
        if len(block) < config.CHUNK_MIN or _headings_only(block):
            carry = block
            continue

        carry = ""
        blocks.append(block)

    # A short tail with nothing following it joins the previous block rather
    # than becoming a fragment. This is where the starter's 2-character chunk
    # on advice_threads came from.
    if carry:
        if blocks:
            blocks[-1] = f"{blocks[-1]}\n{carry}"
        else:
            blocks.append(carry)

    return blocks


def _doc_title(text: str) -> str:
    """
    The document's level-1 heading line, or "" if it has none.

    Unit 2 change. Every guide names its town exactly once, in this line, and
    the section split throws it away for every chunk but the first. See
    `_with_title`.
    """
    for line in text.splitlines():
        if line.startswith("# "):
            return line.strip()
    return ""


def _with_title(piece: str, title: str) -> str:
    """
    Put the document's title line back on top of a section chunk.

    Why this exists. `_blocks` splits on `##` section headings, which is what
    criterion 4 asked for and which works. It also severs each section from the
    `# Town Name` line at the top of the file — and these guides name their
    town in that line and almost nowhere else. Before this change, 61 of the 72
    place-guide chunks did not contain the name of the place they described, so
    "how long to walk the town of Brightwater" was matched against a chunk
    reading "The town is walkable end to end in about 35 minutes" with nothing
    in it to say which town. It ranked 15th of 117.

    The title is restored verbatim rather than paraphrased: it is the
    document's own words put back where the split removed them, not new text.
    Applied to every document uniformly, including the regional guides whose
    titles ("Walking in the region") strengthen chunks that currently outrank
    the right answer. Prefixing only the town guides would be tuning the
    chunker to the question it is meant to fix.

    Chunks that already open with the title -- chunk 0 of each document, where
    `_blocks` carries the heading forward -- are left alone rather than
    repeating it.
    """
    if not title or piece.startswith(title):
        return piece
    return f"{title}\n{piece}"


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents on paragraph boundaries rather than character counts.

    The strategy, and why it is this one and not the starter's fixed window:

      - One paragraph is one chunk. In city_guides the median body paragraph is
        243 characters and each is a single idea — bus frequencies, or opening
        hours, or where to park. Cutting every 800 characters ignored those
        boundaries and produced chunks spanning three sections at once.
      - CHUNK_SIZE (400) is a ceiling, not a target width. Only 1 of 115
        paragraphs exceeds it, so almost nothing gets split; the one that does
        goes through `_split_long` with CHUNK_OVERLAP (100) shared characters.
      - CHUNK_MIN (50) keeps fragments out. Nothing below it survives as its
        own chunk — it merges into a neighbour instead.
      - Unit 2: each chunk is prefixed with its document's `# Title` line, so
        a section chunk carries the name of the place it is about. The size
        ceiling is applied to the body before the title goes on, so a chunk may
        exceed CHUNK_SIZE by the length of its title. See `_with_title`.
    """
    chunks: list[Chunk] = []

    for doc in documents:
        index = 0
        title = _doc_title(doc.text)
        for block in _blocks(doc.text):
            if len(block) <= config.CHUNK_SIZE:
                pieces = [block]
            else:
                pieces = _split_long(block, config.CHUNK_SIZE, config.CHUNK_OVERLAP)

            for piece in pieces:
                chunks.append(
                    Chunk(
                        text=_with_title(piece, title),
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                index += 1

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
