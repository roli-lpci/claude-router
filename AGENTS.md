# AGENTS.md

## Overview

**claude-router** routes Claude API calls to the cheapest model that works using embedding-based task classification + task-specific scaffolds. Single Python file, ~200 LOC, no build step. Blind-eval validated: 11x cost reduction with equal or better quality on eval, research, and content tasks.

## File Map

- `router.py` — The only code file. `ClaudeRouter` class with `.route()` and `.build_prompt()` methods. ~200 LOC.
- `scaffolds.json` — 5 scaffold templates: calibrated-scoring, insight-first, plan-first, substance-check, bug-hunt. Each includes task description, constraint text, evidence, and when_to_use/when_not_to_use.
- `data/centroids.json` — Pre-computed task classification embeddings (nomic-embed-text, 768-dim). One centroid per category. **Do not modify.**
- `data/routing_table.json` — Category -> (model + scaffold) lookup. Maps 12 task categories to Haiku/Sonnet/Opus + optional scaffold. **Do not modify structure.**
- `README.md` — Full documentation, benchmarks, cost math, anti-findings.
- `requirements.txt` — Dependencies: `requests`, `numpy`.
- `examples/basic_usage.py` — End-to-end example: classify, route, call Anthropic API.

## How It Works

1. Embed incoming prompt via Ollama (nomic-embed-text, ~5ms)
2. Cosine-similarity against centroids for all 12 categories
3. Look up routing table: best category -> model + scaffold key
4. If low confidence, fall back to Opus (safe default)
5. Return scaffold text (if applicable) to prepend to prompt

No LLM calls, no external APIs, ~10ms total latency.

## Testing Changes

```bash
# Requires Ollama running with nomic-embed-text
ollama pull nomic-embed-text

# Test classification on a single prompt
python router.py "Evaluate this research paper"

# Run test suite (8 default test prompts)
python router.py
```

Expected output: JSON with `{category, model, scaffold_key, confidence, ...}` or a table with routing decisions.

## What NOT to Change

- **centroids.json** — Pre-computed task classification embeddings. Do not modify.
- **routing_table.json structure** — The category->model mappings are validated. Adding/removing categories requires retraining centroids. Changing model assignments should only happen after blind evaluation.

## Common Tasks

### Add a new scaffold
1. Edit `scaffolds.json`: add a new key with `task`, `text`, `evidence`, `when_to_use`, `when_not_to_use`.
2. Do NOT add it to routing_table.json until tested.
3. Run blind eval on your task domain (10+ judgments) before committing.
4. Update README.md scaffold table if it becomes a default.

**Anti-finding**: Scaffolds break operational and coding tasks. The router already avoids scaffolding these. Do not scaffold categories marked `null` in routing_table.json.

### Change which model handles a category
1. Edit `routing_table.json`: update the `"model"` value (haiku/sonnet/opus).
2. Test against your task distribution with `python router.py`.
3. Run blind eval (10+ judgments) before merging.

### Debug classification mismatches
1. Run `python router.py "your prompt"` -- check the `confidence` field (margin between best and second-best category).
2. Low confidence (<0.02) -> prompt is ambiguous, falls back to Opus automatically.
3. Wrong category -> centroids trained on a different task distribution. Consider custom centroids via constructor.

### Use custom data files
```python
router = ClaudeRouter(
    centroids_path="my_centroids.json",
    routing_table_path="my_routing.json",
    scaffolds_path="my_scaffolds.json"
)
```

## Key Constraints

- Requires Ollama running locally with `nomic-embed-text`.
- Centroids trained on one user's workload -- may not match yours. Test before relying on routing decisions.
- Scaffolds validated through blind eval. Do not add scaffolds without testing.
- Scaffolds on operational/coding tasks make quality worse (anti-finding). Router handles this automatically.

## Error Handling

- `RuntimeError`: Ollama is down, timed out, or returned unexpected response format.
- `ValueError`: JSON files (centroids, routing table, scaffolds) are malformed, missing, or have mismatched keys (e.g., routing table references a scaffold that doesn't exist).

See README.md for benchmarks, cost analysis, and anti-findings.
