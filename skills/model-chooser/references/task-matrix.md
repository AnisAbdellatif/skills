# Subagent Task Archetype Matrix

This matrix provides pre-evaluated task archetypes commonly delegated by orchestrator agents, mapping each to its default complexity, recommended tier, reasoning effort setting, and fallback model.

---

## Task Archetype Reference Table

| Subagent Archetype | Core Objective | Complexity Category | Recommended Tier | Recommended Effort | Typical Selection (Claude) | Fallback Model | Hard Capability Requirements |
|---|---|---|---|---|---|---|---|
| **Explorer / Grepper** | Sweeps files, greps symbols, filters directory trees | Trivial | Tier 1 (Economy) | Low | `haiku` | `sonnet` | Fast read tools, high throughput |
| **Formatter / Linter** | Formats code, fixes syntax/indentation, renames identifiers | Trivial | Tier 1 (Economy) | Low | `haiku` | `sonnet` | Exact text replacement (`Edit` tool) |
| **Docstring / Doc Writer** | Generates standard API docs, README updates, comments | Simple | Tier 1 (Economy) | Low | `haiku` | `sonnet` | Markdown proficiency |
| **Log Analyzer / Filter** | Parses large log files, isolates error stack traces | Simple | Tier 1 (Economy) | Low | `haiku` | `sonnet` | Large context or streaming |
| **Unit Test Writer** | Writes unit tests for existing, well-defined functions | Standard | Tier 2 (Balanced) | Low / Medium | `sonnet` | `haiku` (simple) / `opus` | Test framework proficiency, mock generation |
| **Feature Implementer** | Writes new endpoints, UI components, routine logic | Standard | Tier 2 (Balanced) | Medium | `sonnet` | `opus` | Multi-tool execution (`Edit`, `Write`, `Bash`) |
| **Isolated Bugfixer** | Fixes known, reproduced bugs with clear error logs | Standard | Tier 2 (Balanced) | Medium | `sonnet` | `opus` | Root-cause tracing, test validation |
| **Routine Code Reviewer** | Checks diffs for style, conventions, basic logic errors | Standard | Tier 2 (Balanced) | Medium | `sonnet` | `opus` | Git diff analysis |
| **Complex Refactorer** | Rewrites modules, updates interfaces across files | Complex | Tier 3 (Reasoning) | High | `sonnet` (high) / `opus` | `sonnet` | High reasoning, dependency graph awareness |
| **Heisenbug / Race Debugger** | Diagnoses intermittent, concurrency, or timing bugs | Complex | Tier 3 (Reasoning) | High | `sonnet` (high) / `opus` | `opus` | Hypothesis generation & verification |
| **Architecture Planner** | Decomposes major epics into implementation steps | Complex | Tier 3 (Reasoning) | High | `opus` / `sonnet` (high) | `sonnet` | Systems thinking, trade-off analysis |
| **Security Auditor** | Reviews auth, crypto, input sanitization, injection vectors | Critical | Tier 3 / 4 (Premium) | High / Max | `opus` | `sonnet` (high) | Adversarial validation, vulnerability discovery |
| **Incident Investigator** | Root-cause analysis of production outage or data breach | Critical | Tier 4 (Premium) | Max | `opus` | `sonnet` (high) | Multi-signal synthesis, rigorous hypothesis testing |
| **Deadlock Resolver** | Resolves task where multiple lower-tier attempts failed | Critical | Tier 4 (Premium) | High / Max | `opus` | `sonnet` (high) | Deep chain-of-thought, failure reflection |

---

## Detailed Archetype Profiles

### 1. The Explorer (Search & Reconnaissance)
- **Role:** Sweep a codebase to find where symbols are declared or used, read directory hierarchies, or locate config files.
- **Why Tier 1:** Explorer agents should not analyze business logic deeply; they simply locate relevant files and return lists or small summaries to the orchestrator.
- **Rule:** Never spawn a Tier 3/4 model for exploratory `ls` / `grep` / `find` routines.

### 2. The Implementation Coder
- **Role:** Modifies files, introduces new functions, writes tests, runs the build command to ensure zero compilation errors.
- **Why Tier 2:** Frontier balanced models (e.g., `claude-sonnet-5-5`, `gpt-4o`) possess near-state-of-the-art coding proficiency while running significantly faster and cheaper than flagship reasoning models.
- **Reasoning Effort:** Set to `medium` for everyday coding; increase to `high` if handling intricate logic (e.g., custom parsers, state machines).

### 3. The Code Reviewer & Verifier
- **Principle:** Reviewers must be at least as capable as the implementation author.
- **Guidelines:**
  - For standard changes: A Tier 2 reviewer (`sonnet`) is appropriate.
  - For critical/security changes: Escalate the reviewer to Tier 3 or Tier 4 (`opus` or `sonnet` with `high` effort), even if the implementation was written by a Tier 2 agent.
  - Adversarial verification requires independent scrutiny, not rubber-stamping.

### 4. The Security Auditor
- **Role:** Hunts for privilege escalation, token hijacking, SQL/command injections, SSRF, memory leaks, or race conditions.
- **Why Tier 3/4:** A mistake or hallucination in a security audit gives false confidence and leaves real vulnerabilities exposed.
- **Effort:** Always assign `high` or `max` reasoning effort so the model thoroughly evaluates attacker exploitability.

---

## Batch & Parallel Subagent Allocation

When an orchestrator partitions work across $N$ parallel subagents, use a tiered pyramid:

```
[Orchestrator: Tier 2 or 3]
       │
       ├──► Subagent 1 (Search / Recon): Tier 1 (Haiku)
       ├──► Subagent 2 (Search / Recon): Tier 1 (Haiku)
       ├──► Subagent 3 (Search / Recon): Tier 1 (Haiku)
       │
       ▼ [Synthesis & Plan]
       ├──► Subagent 4 (Implementation A): Tier 2 (Sonnet)
       ├──► Subagent 5 (Implementation B): Tier 2 (Sonnet)
       │
       ▼ [Final Review]
       └──► Subagent 6 (Adversarial Audit): Tier 3/4 (Opus / Sonnet High)
```

**Cost Impact:** By allocating Tier 1 to reconnaissance and Tier 2 to implementation, the orchestrator reserves 80%+ of its token budget for the final critical review step.
