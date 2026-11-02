#!/usr/bin/env python3
"""
Model Selection Validator

Validates that a proposed model selection adheres to the Model Chooser rules:
- Has all required Output Contract fields (Task, Complexity, Available models, Selected model, Reasoning effort, Fallback, Rationale)
- Strictly verifies that Selected model and Fallback are members of Available models
- Uses valid complexity levels (Trivial, Simple, Standard, Complex, Critical)
- Flags rule violations (e.g., using Tier 4 for Trivial work without escalation)
"""

import re
import sys
from typing import Dict, Tuple, List

REQUIRED_FIELDS = [
    "Task",
    "Complexity",
    "Available models",
    "Selected model",
    "Reasoning effort",
    "Fallback",
    "Rationale",
]

VALID_COMPLEXITIES = {"trivial", "simple", "standard", "complex", "critical"}


def parse_contract(text: str) -> Dict[str, str]:
    data = {}
    for line in text.strip().splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if key in REQUIRED_FIELDS:
                data[key] = val
    return data


def validate_contract(data: Dict[str, str]) -> Tuple[bool, List[str]]:
    errors = []
    warnings = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in data or not data[field]:
            errors.append(f"Missing required field: '{field}'")

    if errors:
        return False, errors

    # Check complexity
    complexity = data.get("Complexity", "").lower()
    if complexity not in VALID_COMPLEXITIES:
        errors.append(
            f"Invalid complexity '{data.get('Complexity')}'. Must be one of: "
            f"{', '.join(sorted(VALID_COMPLEXITIES))}"
        )

    # Check Instance-Bounded Selection Rule:
    # Selected model MUST come from Available models
    avail_raw = data.get("Available models", "")
    available_list = [m.strip().lower() for m in avail_raw.split(",") if m.strip()]
    selected = data.get("Selected model", "").strip().lower()
    fallback = data.get("Fallback", "").strip().lower()

    if available_list:
        if selected not in available_list:
            errors.append(
                f"Principle Violation: Selected model '{data.get('Selected model')}' is NOT in the list of available models at this instance: {avail_raw}"
            )
        if fallback != "none available" and fallback not in available_list:
            errors.append(
                f"Principle Violation: Fallback model '{data.get('Fallback')}' is NOT in the list of available models at this instance: {avail_raw}"
            )

    # Check rule: Never spend premium-model resources on trivial work (unless explicitly requested)
    rationale = data.get("Rationale", "").lower()
    is_explicit_override = any(k in rationale for k in ["explicit", "requested", "instructed", "specified"])
    if (
        not is_explicit_override
        and complexity in ("trivial", "simple")
        and any(flagship in selected for flagship in ["opus", "o1", "argon"])
    ):
        # Check if only premium was available
        if len(available_list) > 1 and not all(any(flagship in m for flagship in ["opus", "o1", "argon"]) for m in available_list):
            warnings.append(
                f"Principle Warning: Selected model '{data.get('Selected model')}' appears to be a Tier 4 premium model for a '{complexity}' task while alternatives exist."
            )

    if errors:
        return False, errors
    return True, warnings


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print("Usage: python validate_selection.py [contract_file_or_string]")
        sys.exit(0)

    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = sys.stdin.read()

    data = parse_contract(text)
    valid, messages = validate_contract(data)

    if valid:
        print("✅ Contract is valid!")
        for w in messages:
            print(f"⚠️  {w}")
        sys.exit(0)
    else:
        print("❌ Contract validation failed:")
        for e in messages:
            print(f"  - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
