---
name: model-chooser
description: Selects the most appropriate available AI model for each subagent task. Use whenever spawning, delegating to, or configuring a subagent that can use a different model. Optimizes task quality, cost, latency, context capacity, and reliability.
---

# Model Chooser

## Purpose

Choose the most appropriate model for every subagent based on the actual work it needs to perform.

The objective is not to always choose the strongest model. It is to choose the least expensive and fastest model that can reliably complete the assigned task to the required quality.

## Core principles

1. **Explicit prompt instruction overrides everything.** If the prompt explicitly tells you to use a specific model, use that model no matter what the "best" or most optimal model for the task would otherwise be (provided it is available at that instance).
2. **Instance-bounded selection.** Choose exclusively from models confirmed available at that specific runtime instance. Never select from an abstract or hardcoded list if the model is not present in the current environment.
3. **Public model prejudgment.** Apply deep, pre-calibrated evaluation knowledge of publicly available models (benchmarks, reasoning architectures, token costs, latency, tool proficiency) to classify whatever models are available at the instance.
4. **Task requirements determine model selection.** When no model is explicitly mandated by the prompt, the nature of the work dictates the model tier, not habit or convenience.
5. **Capability takes priority over cost.** Never sacrifice correctness or reliability on demanding tasks to save tokens.
6. **Never spend premium-model resources on trivial work** (unless explicitly instructed by the prompt). High-tier models must not be wasted on mechanical transformations or simple lookups.
7. **Never compromise critical work merely to save tokens** (unless a specific model is explicitly mandated by the prompt). Mission-critical analysis and security reviews require the highest competence available.
8. **Escalate when task complexity or observed performance requires it.** Upgrade tiers or reasoning effort dynamically when a subagent struggles or fails validation.
9. **Treat model selection and reasoning effort as separate decisions.** Increasing thinking/reasoning effort on a lower tier is often superior to switching tiers without reasoning.

---

## Model selection workflow

Before spawning, delegating to, or configuring a subagent, complete these steps:

### 0. Check for explicit model instruction in the prompt (Immediate Override)

Check if the user or orchestrator prompt explicitly tells you to use a specific model (e.g., *"use Opus"*, *"spawn a Haiku subagent"*, *"run this with gpt-4o"*):

- **If YES:** You **must** select that requested model **no matter what the best or most optimal model for the task would otherwise be**. Do not second-guess the prompt to save tokens on a trivial task, and do not upgrade it on a complex task. Verify that the requested model (or its alias) is available at this instance, and proceed directly to the Output Contract.
- **If NO:** Proceed to Step 1 to determine the optimal model.

### 1. Discover available models at this instance

Never guess or assume a model exists. Identify the exact candidate models available in the current environment:

- **Claude Code CLI / Subagent Tool:** Check the `Agent` tool parameter schema (e.g. `model: ["sonnet", "opus", "haiku", "fable"]`), system prompt announcements, or session model information.
- **Local Runtime / Cache:** Check available models in `~/.claude/cache/model-catalog/*.json` or `~/.claude/cache/gateway-models.json` if accessible.
- **T3 Code / Orchestration Tools:** Call `orchestrator_capabilities` or inspect provider target options.
- **Explicit Context / Parameters:** Check models supplied by the user, orchestrator prompt, or configuration flags.

> **Absolute Rule:** The selected model and fallback MUST be members of this discovered set. If only a single model is available at this instance, use it and optimize via reasoning effort instead.

### 2. Analyze the task

Evaluate the subagent's task across 9 key dimensions:

- **Complexity:** Is the task mechanical, straightforward, or intellectually demanding?
- **Reasoning:** Does it require simple single-step inference or multi-step, branchy reasoning?
- **Domain expertise:** Does it require niche specialized knowledge or general programming/language ability?
- **Context:** How much information must the model process (few lines vs. entire repository or massive logs)?
- **Accuracy:** What happens if the subagent makes a mistake (trivial re-run vs. silent bug in production or security breach)?
- **Autonomy:** Does it need to make open-ended architectural decisions or simply follow strict, prescribed instructions?
- **Tools:** Does it require coding, terminal commands, web search, browser automation, vision, or structured output?
- **Latency:** Does the orchestrator or user need an immediate response (e.g., interactive autocomplete vs. background batch job)?
- **Cost:** Is the task likely to consume substantial tokens across many iterative loops?

### 3. Classify task complexity & target tier

Map the task to one of five baseline complexity categories and target tiers:

| Category | Examples | Target Tier | Optimization Focus |
|---|---|---|---|
| **Trivial** | Formatting, linting, renaming, regex extraction, grep parsing | **Tier 1 (Fast / Economy)** | Speed & cost minimization |
| **Simple** | Summarization, log filtering, basic classification, simple Q&A | **Tier 1 (Fast / Economy)** | Speed & low latency |
| **Standard** | Routine feature coding, unit tests, isolated bug fixes, doc updates | **Tier 2 (Balanced)** *(Default)* | Balanced quality, code correctness, & speed |
| **Complex** | Multi-file debugging, architectural analysis, refactoring, race conditions | **Tier 3 (Advanced / Reasoning)** | Deep reasoning, multi-step synthesis |
| **Critical** | Security reviews, cryptographic audits, high-impact decisions, deadlocks | **Tier 4 (Premium / Maximum)** | Maximum intelligence, safety margins |

### 4. Evaluate available models using prejudgments

Filter the **discovered available models** into tiers using pre-calibrated model intelligence (see `references/model-prejudgments.md` for full public catalog):

- **Tier 1 Candidates (Economy):** Models optimized for fast, lightweight processing (e.g. models with identifiers containing `haiku`, `flash-lite`, `mini`, `7b`, `8b`).
- **Tier 2 Candidates (Balanced):** Default frontier workhorses (e.g. models containing `sonnet`, `gpt-4o`, `flash`, `32b`, `70b`).
- **Tier 3 Candidates (Advanced / Reasoning):** Models with extended thinking or specialized multi-step reasoning (e.g. `sonnet` with high reasoning effort, `opus`, `o3-mini`, `pro`, `r1`).
- **Tier 4 Candidates (Premium / Maximum):** Flagship reasoning models (e.g. `opus` with max reasoning effort, `fable`, `o1`, `argon`).
- **Unknown Models:** If an available model is not in the public prejudgment database, infer its tier from suffix heuristics (`-lite` ➔ Tier 1, `-pro` ➔ Tier 3) or mark its capabilities as unknown rather than making blind assumptions.

### 5. Select the best match from the available pool

1. Check hard capability requirements (context window, tool use, vision, structured output). A model lacking a hard requirement must be disqualified.
2. Select the candidate in the target tier that provides the best reliability, speed, and cost efficiency.
3. **Tier Gap Handling:** If the target tier contains no models in the current instance:
   - If targeting Tier 1 but only Tier 2 is available: Select the Tier 2 model with `effort: low` to minimize latency and token burn.
   - If targeting Tier 3/4 but only Tier 2 is available: Select the Tier 2 model and increase reasoning effort to `high` or `max`.
   - If targeting Tier 4 but only Tier 3 is available: Select the Tier 3 model with maximum reasoning effort.
4. Select a fallback model that is also present in the available pool. If the chosen model later proves unavailable or out of credits, first try the same model through another provider (see *Unavailable model or exhausted credits*).

---

## Escalation policy

Start with the lowest suitable tier available. Escalate when:
1. The subagent cannot solve the task or enters a loop.
2. The subagent output fails automated validation or test execution.
3. Unresolved contradictions or unexpected complexity emerge.
4. Context size exceeds the model's practical capacity.

### Escalation sequence
```
[Initial Attempt: Lowest Suitable Available Model]
          │ (Fails / Prompt ambiguity)
          ▼
1. Retry with improved instructions (zero model cost increase)
          │ (Fails / Needs deeper thought)
          ▼
2. Increase reasoning effort (e.g., low → medium → high) if supported
          │ (Fails / Model capability ceiling)
          ▼
3. Upgrade to the next higher tier available in the instance
          │ (Fails / Domain knowledge missing)
          ▼
4. Delegate to a specialized agent archetype (e.g., dedicated planner)
          │ (Fails / High-impact deadlock)
          ▼
5. Deploy the highest-tier available model with maximum reasoning effort
```

**Guardrail:** Enforce bounded retries (maximum 2 retries per subagent task). If still unresolved, stop and report the blocker directly to the user.

---

## Special rules

### Explicit model in prompt (Unconditional Override)
If the prompt explicitly tells you to use a specific model:
- **Use that model no matter what the best model is.** An explicit instruction in the prompt unconditionally overrides tier optimization, cost-saving rules, and task-complexity heuristics.
- Even if the task is Trivial and the prompt asks for a Tier 4 flagship model (e.g. Opus), or if the task is Critical and the prompt asks for a Tier 1 economy model (e.g. Haiku), obey the prompt's explicit model choice.
- Match the requested name or alias (e.g. `opus` ➔ `claude-opus-5-5`) against the instance's available models.
- Only if the requested model does not exist at all in the current instance, inform the user and select the closest available substitute.

### Unavailable model or exhausted credits (Cross-provider check first)
If the selected model (or an explicitly requested one) is unavailable, rate-limited, or its provider's credits are exhausted:
1. **Before moving to the next model in line**, check whether the *same* model is offered by another provider in this instance (e.g. `claude-sonnet-5-5` via Anthropic and via Antigravity; inspect `orchestrator_capabilities` provider targets / model catalogs).
2. If it is, route the task to that provider with the same model and reasoning effort.
3. Only if no provider can serve that model, fall back to the next model in line — and apply the same cross-provider check to that fallback before going further.
4. Report the provider switch in the output contract (`Rationale`).

### Parent model inheritance
Use the parent orchestrator's model when:
- No suitable alternative model exists in the instance's available models.
- Strict consistency in formatting or domain perspective is necessary.
- The task requires capabilities unique to the parent model.
- The framework does not expose subagent model selection.

### Parallel subagents
When spawning multiple subagents:
- Evaluate each task independently.
- Use economical Tier 1/2 models for parallel exploratory tasks (e.g. multi-directory grepping).
- Reserve stronger available models for synthesis and implementation.
- Monitor cumulative token burn and concurrency limits.

### Reviewer agents
- Reviewer subagents must be capable of independently evaluating implementation complexity.
- For critical or security reviews, choose an available model with equal or higher capability and higher reasoning effort than the implementation subagent.

---

## Output contract

When selecting a model, return:

```text
Task: <What the subagent will do>
Complexity: <Trivial | Simple | Standard | Complex | Critical>
Available models: <Comma-separated list of models available at this instance>
Selected model: <Exact model chosen from the available list>
Reasoning effort: <Low | Medium | High | XHigh | Max | Not supported>
Fallback: <Alternative model chosen from the available list>
Rationale: <Brief explanation linking the task needs to the selected available model>
```

### Example: Instance with Claude Models

```text
Task: Fix a straightforward TypeScript type error.
Complexity: Simple
Available models: claude-haiku-5-5, claude-sonnet-5-5, claude-opus-5-5
Selected model: claude-haiku-5-5
Reasoning effort: Low
Fallback: claude-sonnet-5-5
Rationale: The task is narrow and deterministic. Among the models available at this instance, Haiku reliably handles type fixes with the lowest latency and token cost.
```

### Example: Constrained Instance (Only Sonnet Available)

```text
Task: Audit session token validation logic for race conditions.
Complexity: Critical
Available models: claude-sonnet-5-5
Selected model: claude-sonnet-5-5
Reasoning effort: Max
Fallback: None available
Rationale: Security analysis requires maximum reasoning. Because only claude-sonnet-5-5 is available at this instance, we escalate reasoning effort to Max to achieve deep analytical deliberation within the available model constraints.
```

### Example: Explicit Model Override in Prompt

```text
Task: Use claude-opus-5-5 to format and sort this JSON configuration file.
Complexity: Trivial
Available models: claude-haiku-5-5, claude-sonnet-5-5, claude-opus-5-5
Selected model: claude-opus-5-5
Reasoning effort: Low
Fallback: claude-haiku-5-5
Rationale: Although JSON formatting is a Trivial task best suited for an economy model (claude-haiku-5-5), the prompt explicitly instructed using claude-opus-5-5. Explicit prompt instructions override optimal tier selection unconditionally.
```

---

## Final decision rule

Always apply this two-part rule:

1. **Explicit Override Check:** Did the prompt explicitly tell you to use a specific model? If yes, **choose that model immediately** (from the instance's available models), no matter what the best model would otherwise be.
2. **Optimization Check:** Otherwise, ask:
   > **"Among the models available at this instance, which model can reliably complete this specific subagent task with the lowest reasonable cost and latency?"**
   Choose that model.

---

## Where to look

| Need | Reference |
|---|---|
| Public model prejudgments (Claude, OpenAI, Gemini, DeepSeek, Llama), tier calibrations, and naming heuristics | `references/model-prejudgments.md` |
| Task matrix for common subagent archetypes (Explore, Coder, Reviewer, Security, Planner) | `references/task-matrix.md` |
| How to dynamically discover available models across runtime frameworks (Claude Code, T3, SDK) | `references/orchestration-frameworks.md` |
| Failure recovery, error diagnosis, loop mitigation, and escalation playbooks | `references/escalation-and-recovery.md` |
| CLI & programmatic model chooser utility with auto-discovery | `scripts/choose_model.py` |
