# Using with ChatGPT (Prompts Only)

ChatGPT does not yet support local MCP servers in the same way Claude Desktop and Cursor do. You can still use the system prompt and skills as Custom Instructions or paste them into a new chat.

## Option 1: Custom GPT

Create a new Custom GPT in ChatGPT:

1. **Name**: SG Property Agent
2. **Description**: Personal AI research assistant for Singapore residential property
3. **Instructions**: Paste the entire contents of `prompts/system-prompt.md`
4. **Knowledge**: Upload all files from `skills/` and `prompts/`
5. **Capabilities**: enable Web Browsing (for live URA / HDB / IRAS lookups), Code Interpreter (for arithmetic that would otherwise go to MCP)

Code Interpreter can run the Python calculators if you upload the `mcp_server/sg_property_mcp/tools/` files. The Custom GPT can then execute `calculate_bsd()`, `calculate_absd()` etc. in a sandbox.

## Option 2: One-off chat

For users without a Custom GPT, paste `prompts/system-prompt.md` as the first message of a new chat.

For specific tasks, also paste:
- HDB question → `skills/hdb-eligibility.md`
- Affordability → `skills/tdsr-msr-loan-rules.md`
- Stamp duty maths → `skills/stamp-duties.md`
- CPF question → `skills/cpf-housing-usage.md`
- Older leasehold → `skills/lease-decay.md`
- Market timing → `skills/market-outlook-2026-2027.md`
- Moving home (HDB↔Condo, Condo↔Landed, etc.) → `skills/upgrade-downgrade-paths.md`
- Keeping current property while buying second → `skills/decoupling-strategy.md`
- Sequencing the sale and purchase → `skills/sell-first-vs-buy-first.md`

ChatGPT will hold these as context for the session.

## Option 3: Python calculators standalone

If you just want the calculators (no MCP), you can use the Python modules directly:

```python
from sg_property_mcp.tools.stamp_duty import calculate_bsd, calculate_absd
from sg_property_mcp.tools.upgrade_paths import (
    analyze_upgrade_path,
    check_15_month_wait_out,
    compare_decoupling_vs_absd,
)

bsd = calculate_bsd(1_800_000)
print(f"BSD: {bsd.total}")  # 54600.0

absd = calculate_absd(1_800_000, "SC", 2)
print(f"ABSD: {absd.total}")  # 360000.0

# HDB → Condo upgrade analysis
result = analyze_upgrade_path(
    current_property="HDB",
    target_property="CONDO",
    new_price=1_800_000,
    profile="SC",
    marital_status="MARRIED_SC_SC",
    properties_after_new_buy=1,
)
for strategy in result["strategies"]:
    print(strategy["strategy"], strategy["absd_net"])

# Decoupling cost vs ABSD
comparison = compare_decoupling_vs_absd(
    current_joint_property_value=2_000_000,
    new_property_price=2_500_000,
    profile="SC",
    properties_after_new_buy=2,
)
print(f"Net benefit: {comparison['net_benefit']}")
```

Useful for spreadsheets, Streamlit apps, or your own UI on top.

## Limitations vs Claude Desktop / Cursor

| Feature | ChatGPT | Claude / Cursor |
|---------|---------|------------------|
| System prompt | Custom Instructions or paste | First message or rule |
| Skills as context | Custom GPT Knowledge | `@`-mention or paste |
| Live calculators | Code Interpreter (workaround) | MCP server (native) |
| Web browsing | Built-in | Some clients support |
| Persistence | Per-chat (or Custom GPT) | Per-project / per-chat |

ChatGPT is fine for casual research. For repeated, accurate computation, prefer Claude Desktop or Cursor with the MCP server attached.
