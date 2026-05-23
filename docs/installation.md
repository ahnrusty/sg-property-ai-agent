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

17 tools across 5 categories:

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
- `estimate_cpf_refund_at_sale(cpf_principal_used, years_held, accrued_rate)`

**Upgrade and downgrade paths**
- `analyze_upgrade_path(current_property, target_property, new_price, profile, marital_status, properties_after_new_buy, keep_existing, youngest_buyer_age, spouse_ages, hdb_flat_type_rooms)`
- `check_15_month_wait_out(target_hdb_rooms, youngest_buyer_age, spouse_ages, target_is_new_bto, has_otp_before_sep_2022)`
- `estimate_decoupling_cost(current_property_value, share_being_transferred)`
- `compare_decoupling_vs_absd(current_joint_property_value, new_property_price, profile, properties_after_new_buy)`
- `estimate_transition_cash_flow(sell_price, sell_outstanding_loan, sell_cpf_refund_estimate, sell_agent_commission_rate, new_price, new_ltv_cap, new_min_cash_pct, new_bsd, new_absd_upfront, interim_months, interim_rental_monthly)`

**Listings**
- `score_listing(listing, criteria)`
- `compare_listings(listings, criteria)`
- `psf_calc(price, sqft, psf, sqm)`

## Next

- [Use with Claude Desktop](using-with-claude-desktop.md)
- [Use with Cursor](using-with-cursor.md)
- [Use with ChatGPT (prompts only, no MCP)](using-with-chatgpt.md)
