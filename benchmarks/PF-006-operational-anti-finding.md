# PF-006: Operational Tasks — Conversation, Git, Cron, Memory, Web, Inter-Agent
**Date:** 2026-03-21 ~01:38 ET
**Conditions:** A (Haiku raw), B (Haiku scaffolded), C (Sonnet raw)
**Tasks:** 9 operational tasks covering untested categories

## Critical Finding: Scaffolding Broke Haiku on Operational Tasks

**Condition B (scaffolded Haiku) scored 0/9 — total execution failure.**

The per-task constraint blocks (## CONSTRAINTS before each task) caused Haiku to treat the entire prompt as a set of meta-instructions. It acknowledged the constraints, mapped them, and then said "Standing by for actual task assignment" — never executing any of the 9 tasks.

This is the "guards not curricula" principle taken to its logical extreme: when the guard text is MORE prominent than the task text, the model guards instead of working.

## Scores

| Task | A (Haiku raw) | B (Haiku scaffolded) | C (Sonnet) |
|---|:---:|:---:|:---:|
| Context switch (2 threads) | 8 | 0 | 8 |
| Garbled input interpretation | 7 | 0 | 9 |
| Git commit + push | 8 | 0 | 8 |
| Git non-fast-forward | 8 | 0 | 8 |
| Timezone-aware cron | 6 | 0 | 9 |
| Memory recall | 8 | 0 | 8 |
| Daily log writing | 7 | 0 | 8 |
| HN search strategy | 6 | 0 | 9 |
| Inter-agent verification | 9 | 0 | 8 |
| **Average** | **7.4** | **0** | **8.3** |

## Task-Level Analysis

### Where Haiku raw matched Sonnet:
- **Context switching** (conv_01): Both tracked both threads, acknowledged explicitly
- **Git operations** (git_01, git_02): Both gave exact commands, recommended rebase
- **Memory recall** (memory_01): Both cited date, spoke naturally

### Where Sonnet was notably better:
- **Garbled input** (conv_02): Sonnet referenced an existing skill (task-complexity-router) — domain awareness
- **Cron** (cron_01): Sonnet used wrapper script approach (cleaner than inline condition)
- **Web search** (web_01): Sonnet gave exact API URL with Unix timestamp — immediately executable

### Where Haiku raw was notably better:
- **Inter-agent** (agent_01): Haiku was MORE cautious — full verification checklist, explicit "DO NOT send immediately." Sonnet was quicker to act ("act on it directly"). For security-sensitive tasks, Haiku's caution is actually better.

## New Findings

### Finding PF-006-F1: Scaffold Failure Mode — Preamble Confusion
When scaffolding is structured as per-task constraint blocks before each task in a batch, Haiku processes the constraints as the primary content and never reaches the tasks. This is a STRUCTURAL failure, not a quality issue — the model literally doesn't execute.

**Fix:** For multi-task prompts, either:
1. One scaffold block at the top (tested and works in PF-001/002)
2. No scaffold at all for operational tasks (these don't need it)
3. Scaffold inline within each task prompt in SINGLE-task spawns (untested but likely works)

### Finding PF-006-F2: Haiku's Natural Caution on Security Tasks
Raw Haiku was more cautious than Sonnet on inter-agent communication (agent_01). Haiku built a verification checklist and explicitly said "DO NOT send immediately." Sonnet verified the sender but then acted immediately.

For security-sensitive operational tasks, raw Haiku's default caution may be preferable to Sonnet's efficiency.

### Finding PF-006-F3: Operational Tasks Don't Need Scaffolding
7.4/10 raw vs 0/10 scaffolded. The gap to Sonnet (8.3) is only 0.9 points. These tasks are "capability" tasks where Haiku's default behavior is already good enough. Scaffolding adds risk without benefit.

## Routing Recommendation

| Category | Model | Scaffold | Why |
|---|---|---|---|
| Conversation/context switching | Haiku raw | None | 8/10, adequate |
| Git operations | Haiku raw | None | 8/10, matches Sonnet |
| Cron/scheduling | Sonnet | None | Cleaner timezone handling |
| Memory recall | Haiku raw | None | 8/10, natural delivery |
| Memory writing | Haiku raw | None | 7/10, adequate structure |
| Web search strategy | Sonnet | None | Specific APIs, executable |
| Inter-agent comms | Haiku raw | None | 9/10, better caution |
