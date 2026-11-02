# Escalation & Recovery Playbook

This playbook outlines systematic diagnostic procedures, failure recovery steps, loop mitigation rules, and escalation protocols when a subagent fails or performs poorly.

---

## 1. Diagnostic Triage: Root-Cause Classification

When a subagent returns an inadequate result, do not blindly escalate to a higher model tier. First classify the failure:

```
Subagent Failure Observed
            │
            ├─► Case A: Prompt Ambiguity / Missing Constraints
            │     Diagnosis: Subagent misunderstood user intent or edited wrong files.
            │     Remedy: Refine instructions with explicit file paths and acceptance criteria.
            │             Keep the SAME model tier.
            │
            ├─► Case B: Shallow Inference / Missed Edge Cases
            │     Diagnosis: Subagent attempted the fix but missed non-obvious branch conditions.
            │     Remedy: Increase reasoning effort (e.g., low → medium → high).
            │             Keep the SAME model tier before upgrading.
            │
            ├─► Case C: Capability Ceiling / Structural Complexity
            │     Diagnosis: Subagent produced invalid architecture, hallucinations, or couldn't parse AST.
            │     Remedy: Upgrade to next model tier (e.g., Tier 1 → Tier 2, or Tier 2 → Tier 3).
            │
            ├─► Case D: Context Window Overflow
            │     Diagnosis: Task fed massive files or unbounded command logs exceeding effective attention.
            │     Remedy: Pre-filter context (use targeted grep/tokenade/subtrees) or switch to a high-capacity model (e.g., Gemini 1M/2M).
            │
            └─► Case E: Tool Syntax / Formatting Incoherence
                  Diagnosis: Subagent emitted malformed tool calls or broken JSON schemas repeatedly.
                  Remedy: Replace with a model known for rigorous tool calling compliance (e.g., Sonnet or GPT-4o).
```

---

## 2. Step-by-Step Escalation Protocol

Follow this strictly bounded sequence:

### Step 1: Instruction Refinement (Zero extra model cost)
- Add negative constraints ("Do NOT modify file X").
- Provide 1–2 concrete input/output examples.
- Narrow the scope to a single function or file.
- Re-run with the same model.

### Step 2: Reasoning Effort Escalation (Marginal cost increase)
- If the current model supports thinking/reasoning parameters (e.g., `effort: "high"` or `thinking.budget_tokens`):
- Elevate reasoning from `low` to `medium`, or `medium` to `high`.
- This enables multi-step planning without paying the full price of a higher model tier.

### Step 3: Tier Elevation (Direct model upgrade)
- If the subagent remains blocked after Step 2, upgrade one tier level:
  - `Tier 1 (Economy)` ➔ `Tier 2 (Balanced)`
  - `Tier 2 (Balanced)` ➔ `Tier 3 (Advanced / Reasoning)`
  - `Tier 3 (Advanced)` ➔ `Tier 4 (Premium / Flagship)`

### Step 4: Specialization Delegation
- If the problem involves niche knowledge (e.g., advanced cryptography, kernel eBPF, deep database locking):
- Delegate specifically to a domain-specialized agent or provide exact API documentation in the prompt context.

### Step 5: Premium Resolution & Orchestrator Handback
- For mission-critical tasks where lower tiers fail, deploy a Tier 4 flagship model with high reasoning effort.
- If the Tier 4 agent also fails or requests user clarification, **STOP**.
- Preserve the failure diagnostics and report the exact blocker to the user.

---

## 3. Anti-Looping & Termination Rules

Orchestrator agents must prevent runaway subagent executions:

1. **Maximum Retry Budget:**
   - Allow a maximum of **2 retries** per subagent task.
   - Never spawn the same subagent model with identical instructions twice.
2. **Context Growth Check:**
   - If a subagent conversation exceeds 10 turns without tangible progress (no file edits or test runs), terminate the child process.
3. **Loop Detection Checklist:**
   - Is the subagent re-reading files it already inspected?
   - Is it re-executing failing shell commands without changing arguments?
   - Is it alternating between two conflicting code changes?
   - If **YES** to any: Intervene immediately, cancel the subagent task, and re-assess.
4. **Clean Abort & Reporting:**
   - Summarize what was attempted, what failed, and why the model could not resolve it.
   - Present concrete alternatives to the user.
