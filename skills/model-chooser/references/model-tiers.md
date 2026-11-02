# Model Tiers & Provider Reference Catalog

This reference maps common frontier and open models across the four operational tiers, detailing their relative token costs, context capacities, key strengths, and typical subagent assignments.

---

## Tier Summary Overview

| Tier | Category | Latency | Relative Cost | Primary Model Focus | Typical Use Case |
|---|---|---|---|---|---|
| **Tier 1** | Fast / Economy | Ultra-low (<1s to 2s) | 1x (Baseline) | High throughput, concise outputs | Formatting, simple transforms, data extraction, grep/search parsing |
| **Tier 2** | Balanced | Low to Moderate (2s–6s) | ~5x – 10x | Robust coding, tool calling, instruction following | Everyday implementation, unit tests, bug fixes, routine reviews |
| **Tier 3** | Advanced / Reasoning | Moderate to High (5s–20s) | ~15x – 30x | Deep reasoning, multi-file context, architecture | Complex debugging, refactoring, systems design, difficult research |
| **Tier 4** | Premium / Maximum Capability | High (variable thinking) | ~40x – 100x+ | Frontier reasoning, critical validation, safety | Security audits, mission-critical decisions, deadlock resolution |

---

## 1. Anthropic Claude Family

Anthropic models are the primary engine for Claude Code and the Claude Agent SDK.

### Model Catalog & Tier Assignments

| Tier | Model ID | Aliases / Shorthand | Context Window | Key Strengths & Subagent Role |
|---|---|---|---|---|
| **Tier 1** | `claude-3-5-haiku-20241022`<br>`claude-haiku-4-5-20251001`<br>`claude-haiku-5-5` | `haiku` | 200k tokens | Blazing fast, cheap, excellent instruction following. Ideal for search parsing, diff cleanup, lightweight file summaries. |
| **Tier 2** | `claude-3-7-sonnet-20250219`<br>`claude-sonnet-4-5-20250929`<br>`claude-sonnet-4-6`<br>`claude-sonnet-5`<br>`claude-sonnet-5-5` | `sonnet` | 200k tokens | Default workhorse. Superior coding proficiency, exceptional tool calling, balanced speed. Standard implementation subagents. |
| **Tier 3** | `claude-sonnet-5-5` *(thinking / high effort)*<br>`claude-opus-4-6`<br>`claude-opus-5` | `sonnet` (effort: high)<br>`opus` | 200k tokens | Extended thinking enables rigorous planning, complex multi-file bug hunting, and deep AST refactoring. |
| **Tier 4** | `claude-opus-5-5`<br>`claude-fable-5-1` | `opus` (effort: max)<br>`fable` | 200k tokens | Maximum intelligence, nuanced evaluation of security vectors, architectural trade-offs, highest-stakes decisions. |

### Configuration in Claude Code & Agent SDK
- **Native Claude Code Agent:** Accepts shorthand `model: "haiku" | "sonnet" | "opus" | "fable"`.
- **Reasoning Effort:** Configured via `effort: "low" | "medium" | "high" | "xhigh" | "max"`.
- **Decoupled Decision:** Setting `model: "sonnet", effort: "high"` achieves Tier 3 reasoning capabilities at a fraction of Tier 4 cost.

---

## 2. OpenAI Family

Used in multi-provider platforms (e.g., T3 Code, LangChain, custom orchestrators).

| Tier | Model Identifier | Context Window | Strengths & Subagent Role |
|---|---|---|---|
| **Tier 1** | `gpt-4o-mini` | 128k tokens | Fast, inexpensive, reliable JSON schema outputs. Great for data filtering and lint checks. |
| **Tier 2** | `gpt-4o`, `o4-mini` (low effort) | 128k tokens | Versatile, fast multimodal and coding capabilities. Ideal for general development tasks. |
| **Tier 3** | `o3-mini` (medium/high effort), `o1` | 128k – 200k tokens | Specialized reasoning models that think before responding. Excellent for algorithms and logic proofs. |
| **Tier 4** | `o1` (high effort), `o1-pro` | 200k tokens | Deep deliberation and validation for critical algorithmic or mathematical challenges. |

---

## 3. Google Gemini Family

Used in Google Cloud, Vertex AI, and multi-provider agent gateways.

| Tier | Model Identifier | Context Window | Strengths & Subagent Role |
|---|---|---|---|
| **Tier 1** | `gemini-2.5-flash-lite`<br>`gemini-3.1-flash-lite`<br>`gemini-3.5-flash-lite` | 1M tokens | Extremely economical, high-throughput, massive context ingestion for search and log scanning. |
| **Tier 2** | `gemini-2.5-flash`<br>`gemini-3-flash`<br>`gemini-3.8-flash` | 1M tokens | Fast, multimodal, strong reasoning-to-cost ratio. Handles extensive codebases in-context. |
| **Tier 3** | `gemini-2.5-pro`<br>`gemini-3.8-flash-high` | 2M tokens | Deep context understanding, complex synthesis across hundreds of documentation pages or repositories. |
| **Tier 4** | `gemini-4-argon` / Flagship Pro | 2M tokens | Mission-critical analysis with huge context windows. |

---

## 4. Open-Weights & DeepSeek Family

Common in self-hosted, local, or privacy-conscious enterprise environments.

| Tier | Model Identifier | Context Window | Strengths & Subagent Role |
|---|---|---|---|
| **Tier 1** | `llama-3.2-3b`, `qwen-2.5-coder-7b` | 32k – 128k tokens | Fast local execution, zero API token cost, basic edits and formatting. |
| **Tier 2** | `deepseek-v3`, `llama-3.3-70b`, `qwen-2.5-coder-32b` | 64k – 128k tokens | Strong coding benchmarks, robust standard development capabilities. |
| **Tier 3** | `deepseek-r1`, `qwen-2.5-max` | 64k – 128k tokens | Deep native reasoning, complex problem solving at open-weight price points. |
| **Tier 4** | Ensemble `deepseek-r1` / Flagship verified | 64k – 128k tokens | High-difficulty mathematical and algorithmic verification. |

---

## Selection Decision Matrix: Cost vs. Capability

When balancing cost and latency across subagents:

```
Token Cost
    ▲
    │                                          [Tier 4: Flagship / Opus]
    │                                          - Critical security
    │                                          - System architecture
    │                                          - Deadlock recovery
    │
    │                       [Tier 3: Reasoning / Sonnet-High / o3]
    │                       - Complex multi-file debugging
    │                       - Difficult refactoring
    │
    │          [Tier 2: Balanced / Sonnet / GPT-4o]  <-- DEFAULT
    │          - Everyday implementation
    │          - Unit testing
    │          - Routine code reviews
    │
    │ [Tier 1: Economy / Haiku / Flash-Lite]
    │ - Grep / file search filtering
    │ - Formatting / renaming
    │ - Trivial docstrings
    └─────────────────────────────────────────────────────────────► Task Complexity
```

### Golden Rule for Model Identifiers
Never guess or construct synthetic model identifiers. If an orchestrator provides a dynamic model catalog (such as `orchestrator_capabilities` or `gateway-models.json`), verify the exact string before returning the Output Contract.
