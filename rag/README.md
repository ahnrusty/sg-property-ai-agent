# Local RAG: SG Property Insights 2025-2027

Quick local retrieval-augmented generation over a curated corpus of Singapore property insights for 2025, 2026, and 2027. Zero-dependency by default (BM25). Optional Ollama embeddings for semantic search.

## What's in the corpus

30 curated insight chunks covering:

- **2025 retrospective**: full-year URA PPI, HDB resale, CCR/RCR/OCR breakdown, million-dollar HDB flats trend
- **2026 outlook**: URA Q1 2026 final, HDB resale Q1 dip, segment forecasts, new launch pipeline (down 30% YoY)
- **2027 outlook**: BTO supply (~15k+ flats), GLS reload from 2025-awarded sites, MOP wave (18,939 unlocks)
- **Policy framework**: ABSD rates (unchanged since Apr 2023), 6-month remission, 15-month wait-out, HDB Plus/Prime/Standard
- **Macro**: SORA forecast, Fed outlook impact, construction cost pressure, CPF retirement sums
- **Strategy**: decoupling mechanics, upgrader pipeline, rental yield compression, EC outlook
- **Workflow**: quarterly refresh checklist

Each chunk includes year, quarter, region, segment, tags, source organisation, source URL, and publication date.

## Usage

### Command-line

```bash
# Basic query
python -m rag.cli "What is the 2026 private property outlook?"

# Filter by year
python -m rag.cli --year 2027 "BTO supply"

# Filter by segment
python -m rag.cli --segment hdb "wait-out rule"

# Filter by tag
python -m rag.cli --tag absd "remission"

# List all topics
python -m rag.cli --list

# Raw JSON output for piping
python -m rag.cli --json "decoupling"

# Use Ollama embeddings (requires nomic-embed-text or similar)
python -m rag.cli --backend embeddings "what about CCR luxury"
```

### Python API

```python
from rag.search import search_insights, list_topics

# Search
result = search_insights(
    query="HDB MOP wave 2027",
    top_k=5,
    year_filter=2027,
)
for r in result["results"]:
    print(r["title"], r["score"])
    print(r["content"])
    print(r["source_url"])

# List all topics
topics = list_topics()
print(f"{topics['total']} insights in corpus")
```

### Use with Ollama embeddings (optional)

For semantic search instead of keyword:

```bash
ollama pull nomic-embed-text  # ~270MB
python -m rag.cli --backend embeddings "What are the HDB cooling measures?"
```

Falls back to BM25 automatically if Ollama is unavailable.

## Backends

| Backend | Dependencies | Quality | Speed | Best for |
|---------|--------------|---------|-------|----------|
| `bm25` (default) | None | Excellent for keyword matches | Instant | Direct queries, specific terms |
| `embeddings` | Ollama + embedding model | Better semantic matching | ~50ms per query | Paraphrased / conceptual queries |

BM25 is surprisingly strong for our short, well-tagged corpus. Embeddings help when the user's vocabulary differs from the corpus (e.g. "cooling measures" matches ABSD/SSD chunks).

## Filtering

| Filter | Values |
|--------|--------|
| `--year` | 2024, 2025, 2026, 2027 |
| `--segment` | private, hdb, ec, landed, rental, all |
| `--tag` | absd, hdb, mop, gls, ssd, sora, ppi, outlook, etc. (see `--list`) |

Combine filters: `python -m rag.cli --year 2026 --segment hdb "supply"`

## Integration with the agent

### Via MCP

Once registered as an MCP tool (see `mcp_server/sg_property_mcp/server.py`), the agent can call:

```
search_insights(query="2026 SORA forecast", top_k=3)
```

and get back grounded passages with source URLs to cite in responses.

### Via CLI wrapper

`cli/sg_property_cli.py` (Ollama agent CLI) auto-augments queries about market trends with relevant RAG results.

### Via pure prompt

For minimal-token / Ollama setups, paste the top-3 RAG results into the prompt before the user query:

```bash
python -m rag.cli "2027 BTO supply" --json | jq -r '.results[].content' | head -3 > /tmp/context.txt
echo "Context: $(cat /tmp/context.txt)\n\nUser query: ..." | ollama run sg-property
```

## Adding to the corpus

Append a JSON line to `corpus/insights.jsonl`:

```json
{"id": "unique_id", "title": "Title", "year": 2026, "quarter": "Q2", "region": "all", "segment": "private", "tags": ["..."], "source_org": "...", "source_url": "https://...", "date": "2026-05-01", "content": "..."}
```

Required fields: `id`, `title`, `year`, `segment`, `content`.
Optional but recommended: `quarter`, `region`, `tags`, `source_org`, `source_url`, `date`.

No reindexing step needed — BM25 rebuilds at each query (cheap for small corpus). For thousands of docs, switch to a persistent index.

## Refresh strategy

The corpus is a curated snapshot, not a live feed. Refresh quarterly when:

- URA / HDB release new statistics
- MAS / IRAS / MND / HDB publish policy changes
- Major analyst reports drop (OrangeTee, ERA, Huttons, PropNex, JLL)
- New launch take-up numbers post

See `skills/market-outlook-2026-2027.md` for the refresh checklist.

## Testing

```bash
PYTHONPATH=. python -m pytest tests/test_rag.py
```
