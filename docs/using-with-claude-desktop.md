# Using with Claude Desktop

## Add the MCP server

Open `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows).

Add the server under `mcpServers`:

```json
{
  "mcpServers": {
    "sg-property": {
      "command": "/absolute/path/to/your/venv/bin/python",
      "args": ["-m", "sg_property_mcp"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/sg-property-ai-agent/mcp_server"
      }
    }
  }
}
```

Restart Claude Desktop. The `sg-property` server should appear in the MCP tools panel.

## Load the system prompt

Two options:

### Option 1: Project knowledge (Claude Pro / Team)

Create a Claude project. Upload the contents of `prompts/system-prompt.md` and the relevant files from `skills/` as project knowledge. Claude will pull from these for every conversation in that project.

### Option 2: One-off chat

Paste the contents of `prompts/system-prompt.md` as the first message in any new chat. For specific situations, also paste the matching skill file (e.g. `skills/hdb-eligibility.md` for HDB questions).

## Verify tools are available

In Claude Desktop, send: "List the SG property tools you have access to."

You should see 17 tools:

**Stamp duty**: `calculate_bsd`, `calculate_absd`, `calculate_ssd`
**Affordability**: `estimate_mortgage`, `estimate_max_loan`, `check_tdsr_msr`
**Lease and CPF**: `lease_decay_value`, `cpf_usage_limit`, `estimate_cpf_refund_at_sale`
**Upgrade and downgrade paths**: `analyze_upgrade_path`, `check_15_month_wait_out`, `estimate_decoupling_cost`, `compare_decoupling_vs_absd`, `estimate_transition_cash_flow`
**Listings**: `score_listing`, `compare_listings`, `psf_calc`

## Worked examples

### Basic stamp duty

> User: "I'm a Singapore Citizen buying my first home at $1.8M. Compute my BSD."

Claude will call `calculate_bsd(1800000)` and return the breakdown ($54,600 in this case), with notes referring you to IRAS for verification.

> User: "Now compute ABSD if it were my second property."

Claude will call `calculate_absd(1800000, "SC", 2)` and return $360,000 (20% ABSD).

### Upgrade path analysis

> User: "I'm an SC couple selling my $720k HDB to buy a $1.8M condo. What are my options?"

Claude will call `analyze_upgrade_path("HDB", "CONDO", 1_800_000, "SC", "MARRIED_SC_SC", 1)` and return both viable strategies: Sell First (zero ABSD, 75% LTV, 2-3 months bridging) vs Buy First with 6-month remission (continuity but $360k ABSD float, 45% LTV).

### Decoupling math

> User: "We jointly own a $2M condo and want to buy a $2.5M investment property. Should we decouple?"

Claude will call `compare_decoupling_vs_absd(2_000_000, 2_500_000, "SC", 2)` and show: ABSD without decoupling = $500k; ABSD with decoupling = $0; decoupling cost ~$30k; net benefit ~$470k. Recommend decoupling.

### Wait-out check

> User: "I'm 56, my spouse is 58. We want to sell our condo and buy a 4-room HDB. Do we need to wait 15 months?"

Claude will call `check_15_month_wait_out(target_hdb_rooms=4, spouse_ages=[56, 58])` and return: senior exemption applies, no wait-out, direct transition possible.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Server doesn't appear | Check JSON syntax, restart Claude Desktop fully |
| "command not found" | Use absolute path to your venv's Python |
| Tools timeout | Check Python version (3.10+), reinstall fastmcp |
| ImportError on launch | Verify PYTHONPATH points to the `mcp_server` directory containing `sg_property_mcp/` |

## Update the server

```bash
cd sg-property-ai-agent
git pull
uv pip install -e . --upgrade
```

Restart Claude Desktop.
