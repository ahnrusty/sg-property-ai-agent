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

## Worked example

> @sg-property-agent compute BSD on $1.2M and ABSD if it's the 2nd property for an SPR.

Cursor will:
1. Activate the rule
2. Call the MCP `calculate_bsd(1_200_000)` tool
3. Call the MCP `calculate_absd(1_200_000, "SPR", 2)` tool
4. Format the response with breakdowns and IRAS verification reminder

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
