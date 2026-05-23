"""Tests for the local RAG search."""

from __future__ import annotations

import sys
from pathlib import Path

# Add repo root to path so we can import rag/
_repo_root = Path(__file__).resolve().parents[2]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

import pytest

from rag.search import (  # noqa: E402
    BM25,
    list_topics,
    load_corpus,
    search_insights,
    tokenize,
)


class TestTokenize:
    def test_basic(self) -> None:
        tokens = tokenize("ABSD remission for SC married couples")
        assert "absd" in tokens
        assert "remission" in tokens
        assert "sc" in tokens
        assert "married" in tokens
        assert "couples" in tokens
        # Stopwords filtered
        assert "for" not in tokens

    def test_filters_short(self) -> None:
        tokens = tokenize("a b c d the")
        assert tokens == []  # all filtered (stopwords or too short)

    def test_dollar_signs_kept(self) -> None:
        tokens = tokenize("$1.8M condo at 75% LTV")
        assert any("$" in t or "1.8m" in t.lower() for t in tokens)


class TestCorpus:
    def test_loads_at_least_20_docs(self) -> None:
        docs = load_corpus()
        assert len(docs) >= 20

    def test_all_have_required_fields(self) -> None:
        for doc in load_corpus():
            assert "id" in doc, f"Missing id: {doc}"
            assert "title" in doc, f"Missing title: {doc}"
            assert "year" in doc, f"Missing year: {doc}"
            assert "content" in doc, f"Missing content: {doc}"

    def test_years_in_expected_range(self) -> None:
        for doc in load_corpus():
            assert 2024 <= doc["year"] <= 2028, f"Year out of range: {doc['id']}"


class TestBM25Search:
    def test_finds_absd_doc(self) -> None:
        result = search_insights("ABSD rates")
        assert len(result["results"]) > 0
        # Top result should mention ABSD
        top_content = result["results"][0]["content"].lower()
        assert "absd" in top_content

    def test_finds_2027_outlook(self) -> None:
        result = search_insights("2027 BTO supply")
        assert len(result["results"]) > 0
        # Should rank a 2027-tagged doc highly
        top_titles = [r["title"] for r in result["results"][:3]]
        assert any("2027" in t for t in top_titles)

    def test_finds_decoupling(self) -> None:
        result = search_insights("decoupling for upgraders")
        assert len(result["results"]) > 0
        top = result["results"][0]
        assert "decoupling" in top["content"].lower()

    def test_year_filter(self) -> None:
        result = search_insights("supply", year_filter=2027)
        for r in result["results"]:
            assert r["year"] == 2027

    def test_segment_filter(self) -> None:
        result = search_insights("forecast", segment_filter="hdb")
        for r in result["results"]:
            assert r["segment"] in ("hdb", "all")

    def test_tag_filter(self) -> None:
        result = search_insights("rule", tag_filter="absd")
        for r in result["results"]:
            assert "absd" in r["tags"]

    def test_no_match_returns_empty(self) -> None:
        result = search_insights("xyzqqquuuu nonexistent terms")
        assert result["results"] == []

    def test_returns_metadata(self) -> None:
        result = search_insights("HDB MOP wave")
        r = result["results"][0]
        assert r["id"]
        assert r["title"]
        assert r["year"]
        assert r["source_url"]
        assert r["score"] > 0


class TestListTopics:
    def test_returns_all(self) -> None:
        topics = list_topics()
        assert topics["total"] >= 20
        assert len(topics["topics"]) == topics["total"]

    def test_each_topic_has_metadata(self) -> None:
        topics = list_topics()
        for t in topics["topics"]:
            assert t["id"]
            assert t["title"]
            assert "year" in t
            assert isinstance(t["tags"], list)


class TestBM25Class:
    def test_score_higher_for_match(self) -> None:
        corpus = load_corpus()
        bm = BM25(corpus)
        query_tokens = tokenize("ABSD remission")
        results = bm.search("ABSD remission", top_k=3)
        assert len(results) > 0
        # Score should be > 0 for the top result
        assert results[0][1] > 0
