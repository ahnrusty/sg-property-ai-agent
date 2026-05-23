# SG Property AI Agent

A complete AI assistant kit for Singapore residential property research, comparison, and due diligence. Includes a master system prompt, modular skills, an MCP server with calculators, worked examples, and integration guides for Claude Desktop, Cursor, and ChatGPT.

This is a personal research assistant. It is **not** a licensed estate agent, lawyer, mortgage broker, or tax adviser. It does not replace CEA-registered professionals.

## Disclaimer

Unofficial personal tool. Not affiliated with any agency, developer, bank, or government body. Vibe coded with AI assistance. All policy figures (ABSD, BSD, SSD, TDSR, MSR, LTV, CPF, lease decay) are illustrative and were correct at time of writing. Tax, loan and policy rules change. Always re-verify against IRAS, HDB, URA, MAS, and CPF Board before signing anything.

## What is in this repo

```
sg-property-ai-agent/
├── prompts/                Master system prompt + reusable templates
│   └── minimal/            Token-budget-aware variants (tiny, compact, quick-ref, decision trees, few-shot)
├── skills/                 18 modular knowledge files the agent can load on demand
├── mcp_server/             FastMCP server with 19 calculators + insights search
├── rag/                    Local RAG over 31 curated 2025-2027 SG property insights
├── ollama/                 Modelfiles for running fully offline on Ollama
├── cli/                    Local CLI that pairs Ollama with Python calculators
├── examples/               9 worked end-to-end conversations
└── docs/                   Installation and integration guides
```

## Quick start — pick the option that fits your context

### Option 1: Full prompt + frontier model (best quality)

Copy `prompts/system-prompt.md` into a Claude / GPT / Gemini chat. Paste listings, ask away. Best when you have a large context window and want maximum accuracy.

### Option 2: Tiny / compact prompt (token-constrained)

Use `prompts/minimal/system-prompt-tiny.md` (~800 tokens) or `prompts/minimal/system-prompt-compact.md` (~2,000 tokens) when context is limited. Add `prompts/minimal/quick-reference-card.md` for the lookup tables and `prompts/minimal/few-shot-examples.md` to show the model the exact output format.

### Option 3: Skills as context

When discussing a specific situation (HDB eligibility, ABSD on second property, decoupling), paste the matching file from `skills/` so the assistant has full reference text without guessing.

### Option 4: MCP server (deterministic calculators)

Run the MCP server locally and connect it to Claude Desktop, Cursor, or any MCP-compatible client. The assistant invokes 17 deterministic calculators for stamp duty, affordability, mortgage, lease decay, upgrade-path analysis, decoupling math, and listing scorecards instead of doing the maths in its head.

```bash
cd mcp_server
uv pip install -e .
python -m sg_property_mcp
```

See `docs/installation.md`, `docs/using-with-claude-desktop.md`, `docs/using-with-cursor.md`.

### Option 5: Local RAG over 2025-2027 insights

Quick local retrieval over 31 curated insight chunks (URA, HDB, IRAS, MAS, agency commentary). Zero-dependency BM25 by default; optional Ollama embeddings.

```bash
python -m rag.cli "2026 private property outlook"
python -m rag.cli --year 2027 --segment hdb "BTO supply"
python -m rag.cli --tag absd "remission rules"
python -m rag.cli --list   # see all 31 topics
```

See `rag/README.md`.

### Option 6: Fully offline with Ollama

Run the agent on a local model (Gemma 3 4B / 27B, Qwen 3 8B, Llama 3.3 70B). Zero per-query cost, full privacy, works offline.

```bash
ollama pull gemma3:27b
cd ollama
ollama create sg-property -f Modelfile.gemma3-26b
ollama run sg-property
```

See `ollama/README.md`. Pair with the CLI for Ollama + Python calculator hybrid:

```bash
cli/sg_property_cli.py "SC first home $1.8M, compute stamp duty"
cli/sg_property_cli.py --interactive
```

See `cli/README.md`.

## Loading strategy by context budget

| Context budget | Recommended setup |
|----------------|-------------------|
| ≥ 100k tokens (Claude Sonnet, Opus, GPT-5) | Full system prompt + all relevant skills + MCP server |
| 8-32k tokens (Gemma 3 27B, Qwen 3 8B, GPT-4-class) | Compact prompt + quick reference + few-shot examples + targeted skills |
| 4-8k tokens (Gemma 3 4B, Llama 3.2 3B) | Tiny prompt + 1-2 most relevant few-shot examples |
| Offline / cost-sensitive | CLI with Ollama backend + Python calculators |

## Tools provided by the MCP server

### Stamp duty
| Tool | Purpose |
|------|---------|
| `calculate_bsd` | Buyer's Stamp Duty for residential or non-residential |
| `calculate_absd` | Additional Buyer's Stamp Duty by buyer profile and property count |
| `calculate_ssd` | Seller's Stamp Duty by holding period |

### Affordability
| Tool | Purpose |
|------|---------|
| `check_tdsr_msr` | Total / Mortgage Servicing Ratio check |
| `estimate_mortgage` | Monthly payment, total interest, amortisation summary |
| `estimate_max_loan` | Maximum loan quantum given TDSR/MSR headroom |

### Lease and CPF
| Tool | Purpose |
|------|---------|
| `lease_decay_value` | Indicative value impact for remaining lease using Bala's Curve |
| `cpf_usage_limit` | CPF OA usage cap given remaining lease and youngest buyer age |
| `estimate_cpf_refund_at_sale` | CPF refund (principal + accrued interest) on property sale |

### Upgrade and downgrade paths
| Tool | Purpose |
|------|---------|
| `analyze_upgrade_path` | Full strategy analysis for HDB↔Condo, Condo↔Landed, Condo→HDB, etc. |
| `check_15_month_wait_out` | Private→HDB wait-out check with senior exemption logic |
| `estimate_decoupling_cost` | Cash cost of decoupling a joint private property |
| `compare_decoupling_vs_absd` | Decoupling cost vs paying ABSD comparison |
| `estimate_transition_cash_flow` | End-to-end cashflow model for sell + buy |

### Listings
| Tool | Purpose |
|------|---------|
| `score_listing` | Score a listing against user-defined criteria |
| `compare_listings` | Side-by-side comparison of 2+ listings |
| `psf_calc` | $/psf and $/sqm conversions |

### Insights RAG (local)
| Tool | Purpose |
|------|---------|
| `search_insights` | Search curated 2025-2027 SG property insights corpus (BM25 default, optional Ollama embeddings); filter by year, segment, tag |
| `list_insight_topics` | List all topics in the corpus |

## Skills (modular knowledge)

| File | Covers |
|------|--------|
| `skills/hdb-eligibility.md` | BTO, SBF, resale, ethnic quota, income ceiling, MOP, grants |
| `skills/condo-due-diligence.md` | MCST, sinking fund, en-bloc, rental caps, by-laws |
| `skills/landed-property.md` | Detached, semi-D, terrace, strata landed, foreign ownership |
| `skills/executive-condo.md` | EC eligibility, MOP, privatisation timeline |
| `skills/stamp-duties.md` | BSD, ABSD, SSD with current rates and remissions |
| `skills/tdsr-msr-loan-rules.md` | TDSR 55, MSR 30, stress-test floors, LTV ladder |
| `skills/cpf-housing-usage.md` | OA usage, accrued interest, lease coverage |
| `skills/lease-decay.md` | Bala's Curve, CPF impact, resale liquidity |
| `skills/new-launch-buying.md` | Showflat, OTP, progressive payment, DLP |
| `skills/resale-buying.md` | OTP, exercise, valuation, COV, completion |
| `skills/rental-tenancy.md` | Standard lease terms, diplomatic clause, deposit |
| `skills/selling-process.md` | Pricing, valuation, marketing, OTP, completion |
| `skills/market-outlook-2026-2027.md` | URA / HDB / SORA / supply pipeline snapshot |
| `skills/neighbourhood-scoring.md` | Commute, schools, future plans, noise, MRT lines |
| `skills/red-flags-checklist.md` | Listing and contract warning signs |
| `skills/upgrade-downgrade-paths.md` | All home transition paths (HDB↔Condo, Condo↔Landed, Condo→HDB) with strategy matrix |
| `skills/decoupling-strategy.md` | Decoupling mechanics, IRAS scrutiny, decision framework |
| `skills/sell-first-vs-buy-first.md` | Sequencing playbook with 6-month ABSD remission rules |

## License

MIT. See `LICENSE`.

## Contributing

Issues and PRs welcome for: updated policy figures, more accurate calculators, additional skills, and better worked examples. Please cite official sources (URA, HDB, IRAS, MAS, CPF Board) for any rule changes.
