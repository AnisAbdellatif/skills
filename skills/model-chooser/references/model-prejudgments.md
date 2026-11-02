# Public Model Prejudgments & Tier Calibration

This reference document contains the pre-calibrated evaluation database of publicly available AI models.

When selecting a model for a subagent:
1. First obtain the list of **available models at that instance**.
2. Lookup each available model in this catalog (or apply the heuristic rules) to determine its tier, strengths, and operational parameters.
3. Select the best match from the available pool.

---

## 1. Anthropic Claude Family

Anthropic models are the primary engine for Claude Code and the Claude Agent SDK.

| Model Identifiers & Aliases | Prejudged Tier | Primary Strengths | Reasoning Profile | Typical Subagent Role |
|---|---|---|---|---|
| `claude-3-5-haiku-20241022`<br>`claude-haiku-4-5-20251001`<br>`claude-haiku-5-5`<br>*(alias: `haiku`)* | **Tier 1 (Economy)** | Ultra-fast latency, lowest token cost, precise JSON/schema outputs, concise text editing. | Standard inference (no extended thinking on older versions; low effort on 5.5). | Codebase search filtering, regex extraction, lint fixes, single-function docstrings. |
| `claude-3-7-sonnet-20250219`<br>`claude-sonnet-4-5-20250929`<br>`claude-sonnet-4-6`<br>`claude-sonnet-5`<br>`claude-sonnet-5-5`<br>*(alias: `sonnet`)* | **Tier 2 (Balanced)** *(Default workhorse)* | Exceptional coding proficiency, tool-calling reliability, multi-file awareness, clean diff generation. | Configurable reasoning effort (`low`, `medium`, `high`, `xhigh`). Can flex into Tier 3 when set to `high`. | Routine feature implementation, isolated bug fixing, unit test generation, PR reviews. |
| `claude-opus-4-6`<br>`claude-opus-4-7`<br>`claude-opus-4-8`<br>`claude-opus-5`<br>`claude-opus-5-5`<br>*(alias: `opus`)* | **Tier 3 / 4 (Advanced to Premium)** | Deep systems synthesis, high nuance, complex root-cause diagnosis, edge-case anticipation. | Deep extended thinking (`medium` to `max` effort). | Complex refactoring, architecture planning, security auditing, multi-signal incident investigation. |
| `claude-fable-5`<br>`claude-fable-5-1`<br>*(alias: `fable`)* | **Tier 4 (Premium / Maximum)** | Frontier problem solving, exceptional multi-step reasoning under heavy ambiguity. | Configurable thinking (`high` to `max` effort). | Critical deadlock resolution, high-impact architectural decisions, exhaustive cryptographic reviews. |

---

## 2. OpenAI Family

Used in multi-provider platforms (e.g. T3 Code, LangChain, custom gateways).

| Model Identifier | Prejudged Tier | Primary Strengths | Reasoning Profile | Typical Subagent Role |
|---|---|---|---|---|
| `gpt-4o-mini` | **Tier 1 (Economy)** | High speed, very low cost, structured output compliance. | Standard autoregressive. | Data transformation, log filtering, simple syntax fixes. |
| `gpt-4o` | **Tier 2 (Balanced)** | Broad multi-domain knowledge, strong coding, multimodal. | Standard autoregressive. | General software engineering, feature builds, standard debugging. |
| `o3-mini`, `o1-mini` | **Tier 3 (Reasoning)** | High performance on algorithmic, mathematical, and logical code puzzles. | Native test-time reasoning (`low`, `medium`, `high`). | Algorithm optimization, complex query generation, constraint satisfaction. |
| `o1`, `o1-pro` | **Tier 4 (Premium)** | Deep deliberation, thorough step-by-step verification, self-correction. | Extended native reasoning. | High-stakes security analysis, mission-critical architectural validation. |

---

## 3. Google Gemini Family

Used in Google Cloud, Vertex AI, and multi-provider agent gateways.

| Model Identifier | Prejudged Tier | Primary Strengths | Context Capacity | Typical Subagent Role |
|---|---|---|---|---|
| `gemini-2.5-flash-lite`<br>`gemini-3.1-flash-lite`<br>`gemini-3.5-flash-lite` | **Tier 1 (Economy)** | Sub-second latency, massive token throughput, dirt cheap. | 1M tokens | Bulk document scanning, full-repo grep aggregation. |
| `gemini-2.5-flash`<br>`gemini-3-flash`<br>`gemini-3.8-flash` | **Tier 2 (Balanced)** | Fast multimodal ingestion, good coding, strong context following. | 1M tokens | Standard development, UI component generation, test updates. |
| `gemini-2.5-pro`<br>`gemini-3.8-flash-high` | **Tier 3 (Reasoning)** | Deep reasoning across massive context (whole codebases or extensive docs). | 2M tokens | Large-scale codebase comprehension, cross-system dependency mapping. |
| `gemini-4-argon` | **Tier 4 (Premium)** | Maximum frontier reasoning and cross-modal synthesis. | 2M tokens | Mission-critical architecture and deep incident analysis. |

---

## 4. DeepSeek & Open-Weights Family

Used in self-hosted, private, or local runner environments.

| Model Identifier | Prejudged Tier | Strengths & Characteristics | Typical Subagent Role |
|---|---|---|---|
| `llama-3.2-1b/3b`, `qwen-2.5-coder-7b` | **Tier 1 (Economy)** | Fast local execution, zero API token cost. | Simple edits, documentation, linting. |
| `deepseek-v3`, `llama-3.3-70b`, `qwen-2.5-coder-32b`, `mistral-large` | **Tier 2 (Balanced)** | High coding benchmark performance, reliable syntax generation. | Everyday coding, routine tests and reviews. |
| `deepseek-r1`, `qwen-2.5-max` | **Tier 3 (Reasoning)** | Deep native chain-of-thought, strong math and logic derivation. | Complex logic debugging, algorithmic tasks. |

---

## 5. Heuristic Rules for Uncatalogued or Custom Models

When an available model at an instance is not explicitly listed in the tables above, apply these token-matching rules:

```
Available Model String
          │
          ├─► Contains: "mini", "lite", "flash-lite", "nano", "small", "7b", "8b"
          │     ➔ Prejudged: Tier 1 (Economy)
          │
          ├─► Contains: "flash", "turbo", "standard", "base", "14b", "32b", "70b"
          │     ➔ Prejudged: Tier 2 (Balanced)
          │
          ├─► Contains: "pro", "plus", "r1", "o3", "high", "coder-32b+", "reasoner"
          │     ➔ Prejudged: Tier 3 (Advanced / Reasoning)
          │
          ├─► Contains: "opus", "fable", "ultra", "max", "argon", "o1", "405b"
          │     ➔ Prejudged: Tier 4 (Premium / Maximum)
          │
          └─► No clear token matches:
                ➔ Prejudged: Tier 2 (Balanced default)
                ➔ Note in Rationale: "Model capabilities unverified in public database; calibrated to Tier 2 baseline."
```

---

## 6. Instance Discrepancy & Tier Gap Handling

Because you **must only choose from available models at that instance**, you may encounter instances where the ideal tier is missing:

| Desired Tier | Missing in Instance | Available Alternatives | Recommended Action & Rationale |
|---|---|---|---|
| **Tier 1 (Economy)** | No Tier 1 models available | Only Tier 2 available | Choose the Tier 2 model with `effort: low`. Note in Rationale: "No Tier 1 economy models available at this instance; using Tier 2 with Low reasoning effort to minimize latency and token consumption." |
| **Tier 3 (Reasoning)** | No Tier 3 models available | Tier 2 available | Choose the Tier 2 model with `effort: high` or `effort: max`. Note in Rationale: "No native Tier 3 reasoning model available; maximizing reasoning effort on Tier 2 workhorse to handle complex logic." |
| **Tier 4 (Premium)** | No Tier 4 models available | Tier 2 or 3 available | Choose the strongest available model (Tier 3 or Tier 2) with `effort: max`. Note in Rationale: "No Tier 4 model present at this instance; deploying highest available model with maximum thinking budget." |
