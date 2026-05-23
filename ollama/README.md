# Running SG Property Agent on Ollama (Local Models)

This directory contains [Ollama](https://ollama.com) Modelfiles for packaging the agent as a callable local model. Works fully offline once the base model is pulled.

## Why local?

- **Privacy**: queries stay on your machine; no API calls
- **Cost**: zero per-query cost after initial download
- **Latency**: sub-second on capable hardware
- **Offline**: works without internet (except for live URA / HDB lookups)

## Models supported

| Modelfile | Base model | RAM needed | Speed (M-series Mac) | Quality |
|-----------|-----------|------------|----------------------|---------|
| `Modelfile.gemma3-26b` | `gemma3:27b` | ~20 GB | ~80 tok/s on M5 Max | Best |
| `Modelfile.qwen3-8b` | `qwen3:8b` | ~6 GB | ~120 tok/s on M5 Max | Very good |
| `Modelfile.llama3.3-70b` | `llama3.3:70b` | ~48 GB | ~30 tok/s | Best (large) |
| `Modelfile.gemma3-4b` | `gemma3:4b` | ~3 GB | ~200 tok/s | Good for triage |

Pick the largest you can comfortably fit.

## Setup

### 1. Install Ollama

```bash
# macOS
brew install ollama
# or download from ollama.com

# Start the server (runs in background)
ollama serve &
```

### 2. Pull base model

```bash
ollama pull gemma3:27b   # ~16 GB download
# or
ollama pull qwen3:8b     # ~5 GB
# or
ollama pull llama3.3:70b # ~40 GB
# or
ollama pull gemma3:4b    # ~2.5 GB
```

### 3. Build the agent model

```bash
cd ollama/
ollama create sg-property -f Modelfile.gemma3-26b
# or any Modelfile of your choice
```

### 4. Run

```bash
ollama run sg-property
```

Now you have an offline Singapore property assistant.

## Pairing with MCP calculators

Ollama models cannot directly call MCP tools. Two workarounds:

**Option A: Two-stage with Python helper**

Use the included `sg-property-cli.py` (in `cli/` directory) which:
1. Sends user query to Ollama for understanding
2. Calls Python calculators directly for arithmetic
3. Returns to Ollama for final formatting

```bash
python ../cli/sg_property_cli.py "SC first home $1.8M, compute stamp duty"
```

**Option B: Embed calculators in prompt**

For simple cases, the system prompt's quick reference card includes the formulas inline. Capable models (Gemma 3 26B+, Qwen 3 8B+) can compute correctly with the rate tables in context.

For complex cases (decoupling vs ABSD, multi-strategy comparison), Option A is more reliable.

## Customising

Each Modelfile sets:
- `SYSTEM` — the system prompt (compact version embedded)
- `TEMPLATE` — chat template (model-specific)
- `PARAMETER` — temperature, top_p, num_ctx tuning

To use the tiny system prompt instead of compact:
1. Open the Modelfile
2. Replace the SYSTEM block with contents of `prompts/minimal/system-prompt-tiny.md`
3. Rebuild: `ollama create sg-property -f Modelfile.gemma3-26b`

## Performance notes

| Model | Context window | Speed (M-series) | Best for |
|-------|----------------|------------------|----------|
| gemma3:4b | 8k | very fast | Quick triage, simple calc |
| qwen3:8b | 32k | fast | General use; balance of speed and quality |
| gemma3:27b | 32k | medium | Most accurate for complex paths |
| llama3.3:70b | 8k | slower | Best reasoning; needs large RAM |

For decoupling math, multi-listing comparison, or 4-path upgrade analysis: use Gemma 3 26B+ or Qwen 3 8B.

## Updating

After the agent skills are updated upstream:

```bash
git pull
cd ollama/
ollama create sg-property -f Modelfile.gemma3-26b
# (rebuilds with latest system prompt)
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Model output garbled | Check `num_ctx`; reduce if RAM-constrained |
| Hallucinated prices | Re-emphasise "Never fabricate" in system prompt; cite sources |
| Forgets rules mid-conversation | Use Qwen 3 8B+ or Gemma 3 26B+; smaller models drift |
| Slow first response | Cold start; subsequent responses are fast |
| Out of memory | Use smaller model or reduce `num_ctx` |

## Sample one-liner usage

```bash
# Direct query
echo "Compute BSD on $1.5M residential" | ollama run sg-property

# Pipe a file
cat my_listing.txt | ollama run sg-property

# API call
curl http://localhost:11434/api/generate -d '{
  "model": "sg-property",
  "prompt": "SC married, upgrading HDB to $2M condo. Sell first or buy first?",
  "stream": false
}'
```
