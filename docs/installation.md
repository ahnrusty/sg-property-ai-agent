# Installation

## Requirements

- Python 3.10 or higher
- `uv` (recommended) or `pip`
- Git

## Install

### From source

```bash
git clone https://github.com/ahnrusty/sg-property-ai-agent.git
cd sg-property-ai-agent

# Create venv
uv venv
source .venv/bin/activate

# Install
uv pip install -e .
```

### From PyPI (when published)

```bash
uv pip install sg-property-ai-agent
```

## Verify

```bash
# Run the test suite
PYTHONPATH=mcp_server python -m pytest mcp_server/tests/ -v

# Start the MCP server (it will wait for stdio MCP requests)
python -m sg_property_mcp
# or
sg-property-mcp
```

The server logs to stderr and accepts MCP protocol over stdin/stdout. It is meant to be launched by an MCP-compatible client (Claude Desktop, Cursor, etc.) — not run directly in a normal shell.

## Tools provided

11 tools across 4 categories:

**Stamp duty**
- `calculate_bsd(consideration, property_type)`
- `calculate_absd(consideration, profile, property_count_after_purchase)`
- `calculate_ssd(consideration, holding_period_months)`

**Affordability**
- `estimate_mortgage(principal, annual_rate, tenure_years)`
- `estimate_max_loan(gross_monthly_income, existing_monthly_debt, stress_rate, tenure_years, ratio, msr_applicable)`
- `check_tdsr_msr(proposed_monthly_payment, gross_monthly_income, existing_monthly_debt, msr_applicable)`

**Lease and CPF**
- `lease_decay_value(freehold_equivalent_value, years_remaining)`
- `cpf_usage_limit(valuation_limit, years_remaining, youngest_buyer_age)`

**Listings**
- `score_listing(listing, criteria)`
- `compare_listings(listings, criteria)`
- `psf_calc(price, sqft, psf, sqm)`

## Next

- [Use with Claude Desktop](using-with-claude-desktop.md)
- [Use with Cursor](using-with-cursor.md)
- [Use with ChatGPT (prompts only, no MCP)](using-with-chatgpt.md)
