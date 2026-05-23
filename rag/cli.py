#!/usr/bin/env python3
"""Standalone CLI for the local SG property insights RAG.

Usage:
    python -m rag.cli "What is the 2026 private property outlook?"
    python -m rag.cli --year 2027 "BTO supply"
    python -m rag.cli --segment hdb "wait-out rule"
    python -m rag.cli --tag absd "remission"
    python -m rag.cli --list

Outputs ranked passages with source URLs for grounded responses.
"""

from __future__ import annotations

import argparse
import json
import sys

from rag.search import list_topics, search_insights


def format_result(r: dict) -> str:
    lines = [
        f"\n[{r['score']}] {r['title']}",
        f"  Year: {r['year']}/{r['quarter']} | Segment: {r['segment']} | "
        f"Tags: {', '.join(r['tags'][:5])}",
        f"  Source: {r['source_org']} ({r['date']})",
        f"  URL: {r['source_url']}",
        f"  {r['content']}",
    ]
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(
        description="Local RAG over 2025-2027 SG property insights."
    )
    p.add_argument("query", nargs="?", help="Query string")
    p.add_argument("--top-k", type=int, default=5)
    p.add_argument(
        "--backend",
        choices=["bm25", "embeddings"],
        default="bm25",
        help="Retrieval backend (default bm25; embeddings requires Ollama)",
    )
    p.add_argument("--year", type=int, help="Filter to a specific year (2024-2027)")
    p.add_argument(
        "--segment",
        choices=["private", "hdb", "ec", "landed", "rental", "all"],
        help="Filter by segment",
    )
    p.add_argument("--tag", help="Filter by tag (e.g. 'absd', 'gls', 'mop')")
    p.add_argument("--list", action="store_true", help="List all topics in the corpus")
    p.add_argument("--json", action="store_true", help="Output raw JSON")
    args = p.parse_args()

    if args.list:
        topics = list_topics()
        if args.json:
            print(json.dumps(topics, indent=2))
            return
        print(f"\nCorpus contains {topics['total']} topics:\n")
        for t in topics["topics"]:
            tag_str = ", ".join(t["tags"][:4])
            print(f"  [{t['year']}] {t['id']}: {t['title']}")
            print(f"         tags: {tag_str}")
        return

    if not args.query:
        p.error("Provide a query or use --list")

    result = search_insights(
        query=args.query,
        top_k=args.top_k,
        backend=args.backend,
        year_filter=args.year,
        segment_filter=args.segment,
        tag_filter=args.tag,
    )

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print(f"\nQuery: {result['query']}")
    print(f"Backend: {result['backend']}")
    print(f"Filters: {result['filters']}")
    print(f"Results: {len(result['results'])}")

    if not result["results"]:
        print("\nNo results. Try a different query or relax filters.")
        for n in result["notes"]:
            print(f"  - {n}")
        return

    for r in result["results"]:
        print(format_result(r))

    print("\nNotes:")
    for n in result["notes"]:
        print(f"  - {n}")


if __name__ == "__main__":
    main()
