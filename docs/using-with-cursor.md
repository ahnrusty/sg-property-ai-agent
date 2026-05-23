# Using with Cursor

## Add the MCP server

In Cursor, open Settings → MCP, then add:

```json
{
  "sg-property": {
    "command": "/absolute/path/to/your/venv/bin/python",
    "args": ["-m", "sg_property_mcp"],
    "env": {
      "PYTHONPATH": "/absolute/path/to/sg-property-ai-agent/mcp_server"
    }
  }
}
```

Or add manually via Cursor settings UI. Restart Cursor.

## Load as a Cursor Rule (for persistent context)

Cursor rules live in `.cursor/rules/` per workspace, or `~/.cursor/rules/` user-wide.

Create `~/.cursor/rules/sg-property-agent.mdc`:

```markdown
---
description: Personal Singapore property research assistant. Buy / sell / rent / invest. Uses sg-property MCP for calculators.
alwaysApply: false
---

# SG Property Agent

You are an AI assistant for Singapore residential property research. Not a licensed estate agent, lawyer, or tax adviser.

See the master system prompt at /absolute/path/to/sg-property-ai-agent/prompts/system-prompt.md
See modular skills in /absolute/path/to/sg-property-ai-agent/skills/

Always use the `sg-property` MCP tools for arithmetic (BSD, ABSD, SSD, TDSR/MSR, mortgage, lease decay, scorecard).

Never fabricate transacted prices, lease years, or building facts. Cite sources for policy figures and recommend the user verify with IRAS, HDB, URA, MAS, CPF Board.

No em dashes in user-facing drafts.
```

Activate the rule with `@sg-property-agent` in chat.

## Worked examples

### Stamp duty quick check

> @sg-property-agent compute BSD on $1.2M and ABSD if it's the 2nd property for an SPR.

Cursor will:
1. Activate the rule
2. Call `calculate_bsd(1_200_000)` and `calculate_absd(1_200_000, "SPR", 2)`
3. Return formatted breakdown with IRAS verification reminder

### Upgrade path

> @sg-property-agent I'm SC, married, own $1.8M condo, want to buy $4M landed and keep the condo for rental. What's my best play?

Cursor will call `analyze_upgrade_path("CONDO", "LANDED", 4_000_000, "SC", "MARRIED_SC_SC", 2, keep_existing=True)` and surface the decoupling strategy as the high-leverage option, with cost-vs-savings math.

### Downgrade to HDB

> @sg-property-agent I'm 48, spouse 46, selling our $1.6M condo to buy a 5-room HDB. What's the timeline?

Cursor will call `check_15_month_wait_out(target_hdb_rooms=5, spouse_ages=[48, 46])` and flag the 15-month wait-out, recommend interim housing, and walk through the standard path from `skills/upgrade-downgrade-paths.md`.

## Skills as @-mentions

If you keep the repo open in a Cursor workspace, you can `@`-mention specific skill files:

> Help me decide between Plus and Standard BTO. @skills/hdb-eligibility.md @skills/cpf-housing-usage.md

Cursor will load those files as additional context.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| MCP not connecting | Settings → MCP → check status; check stderr in Cursor logs |
| Tools not visible | Restart Cursor; verify JSON config |
| Rule not activating | Verify `description` and `alwaysApply: false`; explicitly `@`-mention |
| Wrong Python path | Use absolute path; `which python` after activating venv |
