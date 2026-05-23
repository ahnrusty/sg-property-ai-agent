# SG Property AI Agent

A complete AI assistant kit for Singapore residential property research, comparison, and due diligence. Includes a master system prompt, modular skills, an MCP server with calculators, worked examples, and integration guides for Claude Desktop, Cursor, and ChatGPT.

This is a personal research assistant. It is **not** a licensed estate agent, lawyer, mortgage broker, or tax adviser. It does not replace CEA-registered professionals.

## Disclaimer

Unofficial personal tool. Not affiliated with any agency, developer, bank, or government body. Vibe coded with AI assistance. All policy figures (ABSD, BSD, SSD, TDSR, MSR, LTV, CPF, lease decay) are illustrative and were correct at time of writing. Tax, loan and policy rules change. Always re-verify against IRAS, HDB, URA, MAS, and CPF Board before signing anything.

## What is in this repo

```
sg-property-ai-agent/
├── prompts/                Master system prompt + reusable templates
├── skills/                 Modular knowledge files the agent can load on demand
├── mcp_server/             FastMCP server with calculators (ABSD, BSD, SSD, TDSR/MSR, mortgage, lease decay, scorecard)
├── examples/               Worked end-to-end conversations
└── docs/                   Installation and integration guides
```

## Quick start

### Option 1: Plain prompt (any chat tool)

Copy `prompts/system-prompt.md` into the first message of a fresh chat. Paste listings, ask away.

### Option 2: Skills as context

When discussing a specific situation (e.g. HDB resale eligibility, ABSD on second property), additionally paste the matching file from `skills/` so the assistant has full reference text without guessing.

### Option 3: MCP server (calculators)

Run the MCP server locally and connect it to Claude Desktop, Cursor, or any MCP-compatible client. The assistant can then invoke deterministic calculators for stamp duty, affordability, mortgage payment, lease decay, and listing scorecards instead of doing the maths in its head.

```bash
cd mcp_server
uv pip install -e .
python -m sg_property_mcp
```

See `docs/installation.md` and `docs/using-with-claude-desktop.md`.

## Tools provided by the MCP server

| Tool | Purpose |
|------|---------|
| `calculate_bsd` | Buyer's Stamp Duty for residential or non-residential |
| `calculate_absd` | Additional Buyer's Stamp Duty by buyer profile and property count |
| `calculate_ssd` | Seller's Stamp Duty by holding period |
| `check_tdsr_msr` | Total / Mortgage Servicing Ratio check given income and debts |
| `estimate_mortgage` | Monthly payment, total interest, amortisation summary |
| `estimate_max_loan` | Maximum loan quantum given TDSR/MSR headroom |
| `lease_decay_value` | Indicative value impact for remaining lease using Bala's Curve |
| `cpf_usage_limit` | CPF OA usage cap given remaining lease and youngest buyer age |
| `score_listing` | Score a listing against user-defined criteria |
| `compare_listings` | Side-by-side comparison of 2+ listings |
| `psf_calc` | $/psf and $/sqm conversions |

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

## License

MIT. See `LICENSE`.

## Contributing

Issues and PRs welcome for: updated policy figures, more accurate calculators, additional skills, and better worked examples. Please cite official sources (URA, HDB, IRAS, MAS, CPF Board) for any rule changes.
