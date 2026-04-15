# Benchmarks

Blind evaluation results from Claude scaffold routing experiments. All judging by Claude Opus, blind evaluation.

| File | What it tests | Key finding |
|------|--------------|-------------|
| [PF-001](PF-001-haiku-vs-sonnet.md) | Scaffolded Haiku vs raw Haiku vs raw Sonnet (18 tasks) | Scaffolded Haiku MAE 1.0 vs Sonnet 1.2 on eval |
| [PF-002](PF-002-content-routing.md) | Expanded task coverage: content, status, config, social (13 tasks) | Scaffolded Haiku wins 4/5 on content drafting |
| [PF-006](PF-006-operational-anti-finding.md) | Scaffolds on operational tasks (9 tasks) | Scaffolding broke Haiku: 0/9 execution failure |
| [L2-002](L2-002-sonnet-vs-opus.md) | Scaffolded Sonnet vs raw Opus (10 tasks, n=4, 140 API calls) | Scaffolded Sonnet composite 8.49 vs Opus 7.45 |
