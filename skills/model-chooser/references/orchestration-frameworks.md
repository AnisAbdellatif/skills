# Orchestration Frameworks & Runtime Integration

This reference describes how to dynamically discover models available at a specific runtime instance, and how to pass selected models and reasoning effort settings across different agent orchestration frameworks.

---

## 1. Runtime Model Discovery Methods

Before selecting a model, an orchestrator must identify the set of models actually available at that instance.

### Method A: Claude Code CLI Tool Declaration
In Claude Code, subagent capabilities are defined in the runtime system prompt. Inspect the `Agent` tool definition:
```json
"model": {
  "description": "Optional model override for this agent...",
  "enum": ["sonnet", "opus", "haiku", "fable"]
}
```
Available aliases at this instance: `["haiku", "sonnet", "opus", "fable"]`.
In addition, check `<system-reminder>` or `<runtime_info>` blocks for exact version IDs (e.g. `claude-sonnet-5-5`, `claude-opus-5-5`, `claude-haiku-5-5`, `claude-fable-5-1`).

### Method B: Claude Code Local Cache Catalogs
When running with host filesystem access, inspect cached model catalogs directly:
- `~/.claude/cache/model-catalog/*.json`
- `~/.claude/cache/gateway-models.json`
These files list the exact active models, display names, context limits, and supported reasoning effort levels.

### Method C: T3 Code Orchestrator Capabilities
When operating in T3 Code or multi-provider orchestration:
```text
orchestrator_capabilities()
```
Returns active providers and their available models. Never guess model identifiers outside this returned listing.

### Method D: Environment Variables & Caller Inputs
In scripted pipelines or custom agents, inspect:
- `AVAILABLE_MODELS` (comma-separated string or JSON array)
- CLI argument `--available-models`

---

## 2. Claude Code CLI Runtime

In Claude Code, subagents are launched primarily using the native `Agent` tool or forked sessions.

### Tool Call Signature
```json
{
  "description": "Short 3-5 word task description",
  "prompt": "Detailed subagent instructions...",
  "subagent_type": "coder | general-purpose | Explore | Plan | claude",
  "model": "haiku | sonnet | opus | fable",
  "effort": "low | medium | high | xhigh | max",
  "run_in_background": false
}
```

### Parameter Mapping Rules
- **Model:**
  - `haiku`: Maps to the latest Tier 1 economy model (`claude-haiku-5-5` or configured haiku).
  - `sonnet`: Maps to the balanced workhorse (`claude-sonnet-5-5`). Default for general development.
  - `opus`: Maps to the high-intelligence reasoning flagship (`claude-opus-5-5`).
  - `fable`: Specialized or experimental frontier agent when configured.
- **Effort:**
  - Controls thinking / chain-of-thought token allocation.
  - `low`: Quick, straightforward tasks.
  - `medium`: Default for balanced programming.
  - `high` / `xhigh`: Deep multi-step debugging or planning.
  - `max`: Exhaustive reasoning for mission-critical tasks (use sparingly).
- **Subagent Type:**
  - `"fork"`: Inherits full conversation context and parent model; ignores `model` override.
  - `"Explore"`: Read-only search agent; best paired with `model: "haiku"`.
  - `"coder"`: Implementation agent; best paired with `model: "sonnet"`.
  - `"Plan"`: Software architect; best paired with `model: "sonnet"` (effort: high) or `model: "opus"`.

---

## 3. T3 Code Orchestration Runtime

T3 Code provides cross-provider multi-agent delegation with persistent threads and cloud sandboxes.

### Delegation Call
```json
{
  "task": "Implement module XYZ...",
  "brief": "Context and constraints...",
  "target": {
    "provider": "anthropic | openai | google | deepseek",
    "model": "exact-catalog-model-id",
    "options": {
      "reasoning_effort": "low | medium | high"
    }
  },
  "workspaceStrategy": "worktree | isolate"
}
```

### Native vs. Delegated Rule
- **Use Native `Agent`:** When the child subagent runs on the same provider as the orchestrator, finishes in the current turn, and needs no external worktree.
- **Use `delegate_task`:** When delegating to another provider (e.g., Gemini or OpenAI), running long background jobs, or requiring an isolated git worktree (`workspaceStrategy: "worktree"`).

---

## 4. Claude Agent SDK / Anthropic Messages API

When configuring custom agentic loops with the Anthropic Python or TypeScript SDK:

```python
import anthropic

client = anthropic.Anthropic()

# Configure model and thinking budget based on Tier selection
def create_subagent_params(tier: int, task_prompt: str, available_models: list[str]):
    # Select strictly from available_models
    ...
```

---

## 5. LangGraph / CrewAI / AutoGen Frameworks

In graph-based or role-based multi-agent frameworks:

1. **Dynamic Model Router Node:**
   - Implement a model chooser node at graph branching points to inspect runtime available models and route tasks to worker agents configured with the appropriate tier.
2. **Fallback Handlers:**
   - If a provider rate-limits or removes a model, route dynamically to the designated fallback model.
