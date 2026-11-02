#!/usr/bin/env python3
"""
Model Chooser CLI & Helper Utility

Selects the most appropriate model for a subagent task EXCLUSIVELY from the models
available at that specific runtime instance.

Uses a rich prejudgment database and heuristic rules to evaluate whatever models
are available in the current environment.
"""

import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Prejudgments for publicly known models:
# Maps substring or regex to (prejudged_tier, default_effort, capability_notes)
KNOWN_MODEL_PREJUDGMENTS = [
    # Claude family
    (r"haiku", 1, "low", "Fast, economical, precise extraction and formatting"),
    (r"sonnet", 2, "medium", "Frontier coding, robust tool calling, balanced performance"),
    (r"opus", 4, "high", "Deep systems reasoning, multi-file synthesis, security analysis"),
    (r"fable", 4, "high", "Flagship capability, multi-step problem solving under ambiguity"),

    # OpenAI family
    (r"gpt-4o-mini", 1, "none", "Inexpensive, fast, reliable JSON formatting"),
    (r"gpt-4o", 2, "medium", "Multimodal, strong general coding and development"),
    (r"o3-mini", 3, "high", "Test-time reasoning for algorithms and math"),
    (r"o1-mini", 3, "high", "Reasoning for logical and coding constraints"),
    (r"o1-pro", 4, "max", "Exhaustive deliberative reasoning"),
    (r"o1", 4, "high", "Deep multi-step reasoning flagship"),

    # Google Gemini family
    (r"flash-lite", 1, "none", "Extreme throughput, ultra-low cost, large context"),
    (r"flash-high", 3, "high", "Fast inference with enhanced reasoning capability"),
    (r"flash", 2, "low", "Fast multimodal coding and broad context processing"),
    (r"pro", 3, "high", "Deep context reasoning and cross-document synthesis"),
    (r"argon", 4, "high", "Maximum capability multimodal frontier reasoning"),

    # DeepSeek & Open weights
    (r"deepseek-reasoner|r1", 3, "high", "Deep native chain-of-thought and math/code reasoning"),
    (r"deepseek-chat|deepseek-v3", 2, "medium", "Strong coding proficiency and standard development"),
    (r"qwen.*coder-7b", 1, "none", "Lightweight local code assistant"),
    (r"qwen.*coder-32b", 2, "medium", "Solid local coding and tool calling"),
    (r"qwen.*max", 3, "high", "Frontier reasoning in open family"),
    (r"llama.*-8b|llama.*-3b|llama.*-1b", 1, "none", "Lightweight edge/local execution"),
    (r"llama.*-70b", 2, "medium", "Robust open-weight development model"),
    (r"llama.*-405b", 4, "high", "Massive parameter open weights flagship"),
]

# Heuristic rules for uncatalogued or custom model names
NAME_HEURISTIC_TIERS = [
    (r"mini|lite|flash-lite|nano|small|7b|8b", 1, "low"),
    (r"flash|turbo|standard|base|14b|32b|70b", 2, "medium"),
    (r"pro|plus|r1|o3|high|reasoner", 3, "high"),
    (r"opus|fable|ultra|max|argon|o1|405b", 4, "max"),
]

COMPLEXITY_TIERS = {
    "trivial": 1,
    "simple": 1,
    "standard": 2,
    "complex": 3,
    "critical": 4,
}

COMPLEXITY_KEYWORDS = {
    "critical": [
        "security", "vulnerability", "audit", "exploit", "cve", "auth", "cryptograph",
        "permission", "privilege", "production outage", "incident", "deadlock", "race condition"
    ],
    "complex": [
        "architecture", "architectural", "refactor", "memory leak", "concurrency",
        "distributed", "migration", "redesign", "multi-file debugging"
    ],
    "standard": [
        "implement", "feature", "endpoint", "bugfix", "fix bug", "unit test",
        "component", "integration", "code review", "pr review"
    ],
    "simple": [
        "summarize", "summary", "explain", "classify", "docstring", "comment",
        "type error", "q&a", "readme", "log filter"
    ],
    "trivial": [
        "format", "lint", "rename", "regex", "extract regex", "sort", "indentation",
        "find file", "grep", "search codebase", "ls"
    ],
}


def discover_instance_models() -> List[str]:
    """
    Dynamically discover models available at this runtime instance.
    Inspects environment variables, local cache files, or standard subagent aliases.
    """
    # 1. Environment variable override
    env_models = os.environ.get("AVAILABLE_MODELS")
    if env_models:
        return [m.strip() for m in env_models.split(",") if m.strip()]

    discovered = []

    # 2. Inspect Claude cache model catalogs
    cache_catalog_dir = os.path.expanduser("~/.claude/cache/model-catalog")
    if os.path.isdir(cache_catalog_dir):
        json_files = sorted(glob.glob(os.path.join(cache_catalog_dir, "*.json")), key=os.path.getmtime, reverse=True)
        if json_files:
            try:
                with open(json_files[0], "r", encoding="utf-8") as f:
                    data = json.load(f)
                    models = data.get("catalog", {}).get("config", {}).get("models", [])
                    for m in models:
                        mid = m.get("id")
                        if mid and mid not in discovered:
                            discovered.append(mid)
            except Exception:
                pass

    # 3. Inspect gateway-models.json
    if not discovered:
        gateway_file = os.path.expanduser("~/.claude/cache/gateway-models.json")
        if os.path.isfile(gateway_file):
            try:
                with open(gateway_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    models = data.get("models", [])
                    for m in models:
                        mid = m.get("id")
                        if mid and mid not in discovered:
                            discovered.append(mid)
            except Exception:
                pass

    # 4. Fallback to standard Claude Code subagent tool aliases if no cache catalog was readable
    if not discovered:
        discovered = ["haiku", "sonnet", "opus", "fable"]

    return discovered


def prejudge_model(model_name: str) -> Tuple[int, str, str]:
    """
    Apply pre-calibrated evaluation knowledge to determine a model's tier,
    recommended reasoning effort, and rationale notes.
    """
    model_lower = model_name.lower()

    # Exact or substring match in known public catalog
    for pattern, tier, effort, notes in KNOWN_MODEL_PREJUDGMENTS:
        if re.search(pattern, model_lower):
            return tier, effort, notes

    # Heuristic match for uncatalogued models
    for pattern, tier, effort in NAME_HEURISTIC_TIERS:
        if re.search(pattern, model_lower):
            return tier, effort, f"Inferred Tier {tier} from model naming token '{pattern}'"

    # Default baseline for completely unknown models
    return 2, "medium", "Calibrated to Tier 2 baseline (balanced workhorse)"


def match_requested_model(requested: str, available_models: List[str]) -> Optional[str]:
    """
    Match a user/prompt-requested model string or alias against the instance's available models.
    Checks exact match first, then substring/family match.
    """
    req_lower = requested.strip().lower()
    if not req_lower:
        return None

    # 1. Exact case-insensitive match
    for m in available_models:
        if m.lower() == req_lower:
            return m

    # 2. Substring/alias match (e.g. "opus" -> "claude-opus-5-5", "haiku" -> "claude-haiku-5-5")
    for m in available_models:
        if req_lower in m.lower():
            return m

    return None


def detect_explicit_model_in_prompt(task: str, available_models: List[str]) -> Optional[str]:
    """
    Detect if the task prompt explicitly instructs using a specific model.
    Examples: "use claude-opus-5-5 to...", "spawn a haiku subagent", "with gpt-4o"
    """
    task_lower = task.lower()

    # Check if any available model ID is explicitly named in the prompt
    # Sort by length descending so more specific IDs match before shorter substrings
    for m in sorted(available_models, key=len, reverse=True):
        m_lower = m.lower()
        if re.search(rf"\b{re.escape(m_lower)}\b", task_lower):
            return m

    # Check common explicit directive phrases with model family aliases
    directive_pattern = re.compile(
        r"\b(?:use|using|with|spawn|run\s+on|select|pick|choose|via)\s+(?:a\s+|an\s+|the\s+|model\s+)?"
        r"([a-z0-9][a-z0-9._-]+)"
    )
    known_tokens = [
        "haiku", "sonnet", "opus", "fable",
        "gpt-4o-mini", "gpt-4o", "o3-mini", "o1-mini", "o1-pro", "o1",
        "flash-lite", "flash-high", "flash", "argon",
        "deepseek-r1", "deepseek-v3", "r1",
    ]
    for match in directive_pattern.finditer(task_lower):
        token = match.group(1).strip(".,:;!?")
        if token in known_tokens:
            resolved = match_requested_model(token, available_models)
            if resolved:
                return resolved

    return None


def infer_complexity(task: str) -> str:
    """Heuristically infer task complexity from description."""
    task_lower = task.lower()
    for level, keywords in COMPLEXITY_KEYWORDS.items():
        if any(re.search(rf"\b{re.escape(kw)}\b", task_lower) for kw in keywords):
            return level
    return "standard"


def choose_model_from_available(
    task: str,
    available_models: List[str],
    complexity: Optional[str] = None,
    user_model: Optional[str] = None,
    is_escalation: bool = False,
    is_reviewer: bool = False,
) -> Dict[str, Any]:
    """
    Selects the optimal model EXCLUSIVELY from the available models at this instance.
    If the prompt or user explicitly specifies a model, uses that model unconditionally
    no matter what the best model for the task would otherwise be.
    """
    if not available_models:
        raise ValueError("No available models found or specified for this instance.")

    # Deduplicate while preserving order
    unique_available = []
    for m in available_models:
        clean = m.strip()
        if clean and clean not in unique_available:
            unique_available.append(clean)

    # Step 1 & 2: Determine complexity & target tier
    if not complexity:
        complexity = infer_complexity(task)
    complexity = complexity.lower()
    if complexity not in COMPLEXITY_TIERS:
        complexity = "standard"

    target_tier = COMPLEXITY_TIERS[complexity]

    if is_reviewer and target_tier in (2, 3):
        target_tier = min(4, target_tier + 1)

    if is_escalation:
        target_tier = min(4, target_tier + 1)

    # Step 3: Evaluate all available models using prejudgments
    evaluated_models = []
    tier_map: Dict[int, List[Dict[str, Any]]] = {1: [], 2: [], 3: [], 4: []}

    for model_id in unique_available:
        tier, effort, notes = prejudge_model(model_id)
        entry = {
            "id": model_id,
            "tier": tier,
            "default_effort": effort,
            "notes": notes,
        }
        evaluated_models.append(entry)
        tier_map[tier].append(entry)

    # Step 0 / Step 4: Unconditional Explicit Model Override (from CLI flag OR prompt text)
    explicit_request = user_model or detect_explicit_model_in_prompt(task, unique_available)
    if explicit_request:
        matched_model = match_requested_model(explicit_request, unique_available)
        if matched_model:
            tier, effort, _ = prejudge_model(matched_model)
            # Determine what the optimal model would have been for fallback/context
            optimal_candidates = tier_map.get(target_tier) or evaluated_models
            optimal_model = optimal_candidates[0]["id"]
            fallback_candidates = [m["id"] for m in evaluated_models if m["id"] != matched_model]
            if optimal_model != matched_model and optimal_model in fallback_candidates:
                fb = optimal_model
            else:
                fb = fallback_candidates[0] if fallback_candidates else "None available"

            if optimal_model != matched_model:
                rationale = (
                    f"Although this {complexity.capitalize()} task would normally target Tier {target_tier} "
                    f"(e.g. {optimal_model}), the prompt explicitly instructed using '{matched_model}'. "
                    f"Explicit model instructions override optimal model selection unconditionally."
                )
            else:
                rationale = (
                    f"The prompt explicitly instructed using '{matched_model}', which is confirmed available "
                    f"at this instance and also matches the optimal Tier {target_tier} for this {complexity.capitalize()} task."
                )

            return {
                "task": task,
                "complexity": complexity.capitalize(),
                "available_models": unique_available,
                "selected_model": matched_model,
                "reasoning_effort": effort.capitalize() if effort != "none" else "Not supported / Default",
                "fallback": fb,
                "rationale": rationale,
                "tier": tier,
            }
        else:
            user_warning = (
                f"Explicitly requested model '{explicit_request}' is not available at this instance; "
                f"falling back to best available model. "
            )
    else:
        user_warning = ""

    # Step 5: Select best candidate from available models matching target tier
    selected_entry = None
    rationale_note = ""

    if tier_map[target_tier]:
        # Exact tier match found
        selected_entry = tier_map[target_tier][0]
        rationale_note = f"Selected from available Tier {target_tier} models ({selected_entry['notes']})."
    else:
        # Tier gap handling: Find closest available tier
        available_tiers = [t for t in sorted(tier_map.keys()) if tier_map[t]]
        if target_tier > max(available_tiers):
            # Wanted higher tier, only lower available: pick highest available and elevate reasoning effort
            closest_tier = max(available_tiers)
            selected_entry = tier_map[closest_tier][0]
            selected_entry["default_effort"] = "max"
            rationale_note = (
                f"Target Tier {target_tier} is not available at this instance. "
                f"Selected highest available tier (Tier {closest_tier}) and maximized reasoning effort."
            )
        else:
            # Wanted lower tier, only higher available: pick lowest available and lower reasoning effort
            closest_tier = min(available_tiers)
            selected_entry = tier_map[closest_tier][0]
            selected_entry["default_effort"] = "low"
            rationale_note = (
                f"Target Tier {target_tier} is not available at this instance. "
                f"Selected lowest available tier (Tier {closest_tier}) with Low reasoning effort to minimize token cost."
            )

    selected_model = selected_entry["id"]
    effort = selected_entry["default_effort"]

    # Select fallback from remaining available models
    fallbacks = [m["id"] for m in evaluated_models if m["id"] != selected_model]
    fallback_model = fallbacks[0] if fallbacks else "None available"

    effort_display = effort.capitalize() if effort != "none" else "Not supported / Default"

    full_rationale = (
        f"{user_warning}"
        f"Task is classified as {complexity.capitalize()} (target Tier {target_tier}). "
        f"{rationale_note}"
    )

    return {
        "task": task,
        "complexity": complexity.capitalize(),
        "available_models": unique_available,
        "selected_model": selected_model,
        "reasoning_effort": effort_display,
        "fallback": fallback_model,
        "rationale": full_rationale,
        "tier": selected_entry["tier"],
    }


def format_output_contract(decision: Dict[str, Any]) -> str:
    """Format decision strictly according to the Output Contract."""
    avail_str = ", ".join(decision["available_models"])
    return (
        f"Task: {decision['task']}\n"
        f"Complexity: {decision['complexity']}\n"
        f"Available models: {avail_str}\n"
        f"Selected model: {decision['selected_model']}\n"
        f"Reasoning effort: {decision['reasoning_effort']}\n"
        f"Fallback: {decision['fallback']}\n"
        f"Rationale: {decision['rationale']}"
    )


def main():
    parser = argparse.ArgumentParser(description="Model Chooser for Subagent Tasks (Instance-Bounded)")
    parser.add_argument("--task", "-t", required=True, help="Task description")
    parser.add_argument(
        "--available-models", "-a",
        help="Comma-separated list or JSON array of models available at this instance"
    )
    parser.add_argument(
        "--complexity", "-c",
        choices=["trivial", "simple", "standard", "complex", "critical"],
        help="Explicit complexity category"
    )
    parser.add_argument("--user-model", "-m", help="User specified model preference")
    parser.add_argument("--escalate", action="store_true", help="Escalate by one tier")
    parser.add_argument("--reviewer", action="store_true", help="Select model for a reviewer subagent")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Discover or parse available models
    if args.available_models:
        raw = args.available_models.strip()
        if raw.startswith("[") and raw.endswith("]"):
            available = json.loads(raw)
        else:
            available = [x.strip() for x in raw.split(",") if x.strip()]
    else:
        available = discover_instance_models()

    decision = choose_model_from_available(
        task=args.task,
        available_models=available,
        complexity=args.complexity,
        user_model=args.user_model,
        is_escalation=args.escalate,
        is_reviewer=args.reviewer,
    )

    if args.json:
        print(json.dumps(decision, indent=2))
    else:
        print(format_output_contract(decision))


if __name__ == "__main__":
    main()
