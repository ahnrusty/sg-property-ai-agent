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

You should see something like:
- calculate_bsd
- calculate_absd
- calculate_ssd
- estimate_mortgage
- estimate_max_loan
- check_tdsr_msr
- lease_decay_value
- cpf_usage_limit
- score_listing
- compare_listings
- psf_calc

## Worked example

> User: "I'm a Singapore Citizen buying my first home at $1.8M. Compute my BSD."

Claude will call `calculate_bsd(1800000)` and return the breakdown ($54,600 in this case), with notes referring you to IRAS for verification.

> User: "Now compute ABSD if it were my second property."

Claude will call `calculate_absd(1800000, "SC", 2)` and return $360,000 (20% ABSD).

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
