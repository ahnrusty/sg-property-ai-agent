# SG Property Agent CLI

Local command-line agent. Combines an Ollama model (any) with the Python calculators so you get deterministic stamp duty / affordability / path-analysis numbers + natural-language explanation, fully offline.

## Setup

1. Install Ollama and build the model:
   ```bash
   cd ../ollama
   ollama create sg-property -f Modelfile.gemma3-26b
   # or any other Modelfile
   ```

2. Install the Python package:
   ```bash
   cd ../
   uv pip install -e .
   ```

## Usage

### Single query
```bash
sg_property_cli.py "I'm SC, first home, $1.8M condo. Compute stamp duties."
```

### Pipe from stdin
```bash
echo "BSD on $2M residential" | sg_property_cli.py
```

### Interactive REPL
```bash
sg_property_cli.py --interactive
```

### Use a specific model
```bash
sg_property_cli.py --model sg-property-qwen "Upgrade HDB to $2M condo, SC couple"
```

### Show calculator pre-pass
```bash
sg_property_cli.py --verbose "BSD on $1.5M"
```

## How it works

1. CLI scans your query for keywords (BSD, ABSD, mortgage, upgrade, wait-out, etc.)
2. If matched, runs the relevant Python calculator(s) deterministically
3. Injects exact results into the prompt sent to Ollama
4. Ollama (small or large model) formats the natural-language response using the exact numbers — no hallucinated arithmetic

This pattern works for any local model from Llama 3.2 3B to Llama 3.3 70B and beyond.

## Examples

```bash
$ sg_property_cli.py "SC, first home, $1.2M condo. Compute stamp duty."
[Calculator output]
BSD on $1,200,000: $32,600
ABSD on $1,200,000 (SC property #1): $0

[Ollama response]
For your first home purchase at $1,200,000 as a Singapore Citizen:

- Buyer's Stamp Duty (BSD): $32,600
- Additional Buyer's Stamp Duty (ABSD): $0 (first property, SC rate)
- Total stamp duty: $32,600

Payable within 14 days of OTP signing. CPF OA can be used for BSD.

Verify on IRAS calculator before transacting:
https://www.iras.gov.sg/quick-links/calculators

Next steps:
1. Confirm down payment + cash + CPF position with bank
2. Get IPA before issuing OTP
3. Engage CEA-registered agent for viewing and OTP execution
4. Engage conveyancing lawyer (~$2,500-$3,500)
```

```bash
$ sg_property_cli.py "Couple 58 and 56, both SC, want to buy 4-room HDB. Sold our condo last year."

[Calculator output]
[15-month wait check: ages 58/56, 4-room target]
Applies: False; Wait: 0 months
Reason: Senior exemption: both spouses (or single buyer) 55+ buying 4-room
or smaller resale flat.

[Ollama response]
Good news — the senior exemption applies. You do NOT need to wait 15 months
because both of you are 55+ and buying a 4-room resale flat.

You can apply for HDB resale immediately. Steps:
1. Register Intent to Buy on HDB Resale Portal (free, 12 months validity)
2. Obtain HFE Letter or bank IPA
3. Search and view flats
4. Issue OTP, exercise within 21 days
5. Submit Resale Application; HDB processes ~8 weeks
6. Complete and collect keys

Income check: HDB loan eligibility cap $14k family income.

Consider Silver Housing Bonus ($30k cash bonus) if you qualify (income at
purchase eligible; check HDB).

Verify all on HDB Resale Portal.
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| "Cannot reach Ollama" | Run `ollama serve` |
| Model name not found | Run `ollama list` to see installed models; `ollama create sg-property -f Modelfile.gemma3-26b` to build |
| Slow response | Use smaller model (`gemma3:4b`); reduce `--num-ctx` |
| Wrong calculator triggered | Be more explicit in query (include keywords like "BSD", "stamp duty", "upgrade") |
| Calculator missed | Pass to verbose with `-v` to see; fall back to direct Python: `python -c "from sg_property_mcp.tools.stamp_duty import calculate_bsd; print(calculate_bsd(1_500_000))"` |

## Performance benchmarks (M5 Max MacBook)

| Model | Cold start | Warm response | Quality |
|-------|------------|---------------|---------|
| gemma3:4b | ~3s | ~1.5s | Good for quick triage |
| qwen3:8b | ~5s | ~2.5s | Very good general use |
| gemma3:27b | ~8s | ~5s | Best for complex paths |
| llama3.3:70b | ~15s | ~10s | Best reasoning, slowest |

For batch processing or scripted automation, gemma3:4b or qwen3:8b are optimal speed/quality tradeoff.
