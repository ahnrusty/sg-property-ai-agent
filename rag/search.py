"""Local RAG search over the curated 2025-2027 SG property insights corpus.

Two retrieval backends:
1. BM25 (default, zero-dependency, pure Python)
2. Ollama embeddings (optional, uses nomic-embed-text or any embedding model)

Both return ranked passages with metadata for grounded responses.
"""

from __future__ import annotations

import json
import math
import re
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

CORPUS_PATH = Path(__file__).parent / "corpus" / "insights.jsonl"
OLLAMA_URL = "http://localhost:11434/api/embeddings"
DEFAULT_EMBED_MODEL = "nomic-embed-text"

# Stopwords for BM25 tokenisation
_STOP = frozenset(
    "a an and are as at be by for from has have in is it its of on or that the "
    "to was were will with this these those i you he she we they our us my your".split()
)

_TOKEN_RE = re.compile(r"[a-z0-9$%][\w\-$%]*", re.IGNORECASE)


# -------------- Corpus loading --------------


def load_corpus(path: Path | str = CORPUS_PATH) -> list[dict[str, Any]]:
    """Load JSONL corpus into a list of dicts."""
    docs: list[dict[str, Any]] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            docs.append(json.loads(line))
    return docs


def doc_text(doc: dict[str, Any]) -> str:
    """Concatenate searchable fields of a doc."""
    parts = [
        doc.get("title", ""),
        " ".join(doc.get("tags", [])),
        str(doc.get("year", "")),
        doc.get("quarter", ""),
        doc.get("segment", ""),
        doc.get("region", ""),
        doc.get("content", ""),
    ]
    return " ".join(str(p) for p in parts if p)


# -------------- BM25 --------------


def tokenize(text: str) -> list[str]:
    """Lowercase + split + drop stopwords."""
    return [
        t.lower()
        for t in _TOKEN_RE.findall(text)
        if t.lower() not in _STOP and len(t) > 1
    ]


class BM25:
    """Minimal BM25 implementation, pure Python stdlib."""

    def __init__(
        self,
        corpus: list[dict[str, Any]],
        k1: float = 1.5,
        b: float = 0.75,
    ) -> None:
        self.corpus = corpus
        self.k1 = k1
        self.b = b
        self.docs_tokens = [tokenize(doc_text(d)) for d in corpus]
        self.doc_lens = [len(d) for d in self.docs_tokens]
        self.avg_dl = sum(self.doc_lens) / len(self.doc_lens) if self.doc_lens else 0.0

        # Document frequency
        self.df: Counter[str] = Counter()
        for d in self.docs_tokens:
            for term in set(d):
                self.df[term] += 1

        self.n = len(self.docs_tokens)
        self.idf: dict[str, float] = {
            term: math.log(1 + (self.n - df + 0.5) / (df + 0.5))
            for term, df in self.df.items()
        }

    def score(self, query_tokens: list[str], doc_idx: int) -> float:
        """Compute BM25 score for query against a single doc."""
        doc = self.docs_tokens[doc_idx]
        if not doc:
            return 0.0
        tf = Counter(doc)
        dl = self.doc_lens[doc_idx]
        score = 0.0
        for term in query_tokens:
            if term not in self.idf:
                continue
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self.idf[term]
            denom = f + self.k1 * (1 - self.b + self.b * dl / self.avg_dl)
            score += idf * (f * (self.k1 + 1)) / denom
        return score

    def search(self, query: str, top_k: int = 5) -> list[tuple[int, float]]:
        """Return [(doc_idx, score), ...] for the top-k results."""
        query_tokens = tokenize(query)
        if not query_tokens:
            return []
        scored = [(i, self.score(query_tokens, i)) for i in range(self.n)]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s in scored[:top_k] if s[1] > 0]


# -------------- Optional Ollama embeddings --------------


def ollama_embed(text: str, model: str = DEFAULT_EMBED_MODEL) -> list[float] | None:
    """Get an embedding from Ollama. Returns None if unavailable."""
    body = json.dumps({"model": model, "prompt": text}).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return data.get("embedding")
    except (urllib.error.URLError, TimeoutError, ConnectionError):
        return None


def _cosine(a: list[float], b: list[float]) -> float:
    """Cosine similarity, pure stdlib."""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


class EmbeddingIndex:
    """Optional embedding index using Ollama."""

    def __init__(
        self,
        corpus: list[dict[str, Any]],
        model: str = DEFAULT_EMBED_MODEL,
    ) -> None:
        self.corpus = corpus
        self.model = model
        self.embeddings: list[list[float]] = []
        self._build()

    def _build(self) -> None:
        for doc in self.corpus:
            emb = ollama_embed(doc_text(doc), self.model)
            if emb is None:
                # Fall back: zero vector (will rank last via cosine)
                emb = []
            self.embeddings.append(emb)

    def search(self, query: str, top_k: int = 5) -> list[tuple[int, float]]:
        q_emb = ollama_embed(query, self.model)
        if q_emb is None:
            return []
        scored = []
        for i, doc_emb in enumerate(self.embeddings):
            if not doc_emb:
                continue
            scored.append((i, _cosine(q_emb, doc_emb)))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s in scored[:top_k] if s[1] > 0]


# -------------- High-level API --------------


def search_insights(
    query: str,
    top_k: int = 5,
    backend: str = "bm25",
    corpus_path: Path | str = CORPUS_PATH,
    year_filter: int | None = None,
    segment_filter: str | None = None,
    tag_filter: str | None = None,
) -> dict[str, Any]:
    """Search the SG property insights corpus.

    Args:
        query: Free-text query.
        top_k: Number of results to return.
        backend: "bm25" (default, zero-dependency) or "embeddings" (requires Ollama).
        corpus_path: Path to JSONL corpus.
        year_filter: If set, only return docs matching this year.
        segment_filter: If set, only return docs matching this segment
            ("private", "hdb", "ec", "landed", "rental", "all").
        tag_filter: If set, only return docs whose tags list contains this tag.

    Returns:
        dict with query, backend, results (list of doc + score + snippet), notes.
    """
    corpus = load_corpus(corpus_path)

    # Pre-filter
    filtered_indices: list[int] = []
    for i, doc in enumerate(corpus):
        if year_filter is not None and doc.get("year") != year_filter:
            continue
        if segment_filter and doc.get("segment") not in (segment_filter, "all"):
            continue
        if tag_filter and tag_filter not in doc.get("tags", []):
            continue
        filtered_indices.append(i)

    if not filtered_indices:
        return {
            "query": query,
            "backend": backend,
            "results": [],
            "notes": [
                "No documents matched the filters. "
                "Try removing year/segment/tag filters."
            ],
        }

    filtered_corpus = [corpus[i] for i in filtered_indices]

    if backend == "embeddings":
        index = EmbeddingIndex(filtered_corpus)
        ranked = index.search(query, top_k=top_k)
        if not ranked:
            # Fall back to BM25 if Ollama unavailable
            backend = "bm25 (embeddings unavailable)"
            ranked = BM25(filtered_corpus).search(query, top_k=top_k)
    else:
        ranked = BM25(filtered_corpus).search(query, top_k=top_k)

    results = []
    for doc_idx, score in ranked:
        doc = filtered_corpus[doc_idx]
        results.append(
            {
                "id": doc.get("id"),
                "title": doc.get("title"),
                "year": doc.get("year"),
                "quarter": doc.get("quarter"),
                "segment": doc.get("segment"),
                "tags": doc.get("tags", []),
                "source_org": doc.get("source_org"),
                "source_url": doc.get("source_url"),
                "date": doc.get("date"),
                "content": doc.get("content"),
                "score": round(score, 4),
            }
        )

    return {
        "query": query,
        "backend": backend,
        "filters": {
            "year": year_filter,
            "segment": segment_filter,
            "tag": tag_filter,
        },
        "results": results,
        "notes": [
            f"Returned {len(results)} of {len(filtered_corpus)} corpus docs.",
            "All policy figures are illustrative; verify with the source_url.",
            "Use the source_org and source_url for citations.",
        ],
    }


def list_topics() -> dict[str, Any]:
    """List all available topics in the corpus (id, title, tags)."""
    corpus = load_corpus()
    return {
        "total": len(corpus),
        "topics": [
            {
                "id": d.get("id"),
                "title": d.get("title"),
                "year": d.get("year"),
                "tags": d.get("tags", []),
            }
            for d in corpus
        ],
    }
