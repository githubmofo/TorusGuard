#!/usr/bin/env python3
"""
TorusGuard v0.9.0 Granular Skills Validation Harness
Verifies all 13 skill folders, frontmatter contracts, required sections,
context budget discipline (<= 300 lines), router integrity, and script bindings.
"""

import os
import sys
import glob
import re
import argparse

EXPECTED_SKILLS = [
    "torusguard",
    "torusguard-init",
    "torusguard-authorize",
    "torusguard-audit",
    "torusguard-verify",
    "torusguard-web-validate",
    "torusguard-exploit-check",
    "torusguard-harden",
    "torusguard-apply",
    "torusguard-recheck",
    "torusguard-report",
    "torusguard-status",
    "torusguard-full",
]

PART1_SKILLS = [
    "torusguard-init",
    "torusguard-authorize",
    "torusguard-audit",
    "torusguard-verify",
    "torusguard-harden",
    "torusguard-apply",
]

PART2_SKILLS = [
    "torusguard-web-validate",
    "torusguard-exploit-check",
    "torusguard-recheck",
    "torusguard-report",
    "torusguard-status",
]

PART3_SKILLS = [
    "torusguard-full",
    "torusguard",
]

REQUIRED_SECTIONS = {
    "torusguard-init": ["Objective", "Pre-Flight Check", "Execution Steps", "Safety Constraints", "Output Format"],
    "torusguard-authorize": ["Objective", "Execution Steps", "Safety Constraints", "Output Format"],
    "torusguard-audit": ["Objective", "Execution Steps", "Confidence Scoring Rubric", "Finding Card Format", "Safety Constraints", "Output Format"],
    "torusguard-verify": ["Objective", "Execution Steps", "Evidence Sufficiency", "Safety Constraints", "Output Format"],
    "torusguard-web-validate": ["Objective", "Authorization Gate Check", "Safety Gate", "Execution Steps", "Credential Redaction", "Safety Constraints", "Output Format"],
    "torusguard-exploit-check": ["Objective", "Authorization Gate Check", "Bounded Probe Strategies", "Execution Steps", "Safety Constraints", "Output Format"],
    "torusguard-harden": ["Objective", "Execution Steps", "Ponytail Protocol", "Bundle Directory Structure", "Safety Constraints", "Output Format"],
    "torusguard-apply": ["Objective", "Execution Steps", "Governance & Safety Rules", "Output Format"],
    "torusguard-recheck": ["Objective", "Execution Steps", "State Transition Rules", "Safety Constraints", "Output Format"],
    "torusguard-report": ["Objective", "Execution Steps", "SARIF v2.1.0 Output Specification", "Safety Constraints", "Output Format"],
    "torusguard-status": ["Objective", "Execution Steps", "Safety Constraints", "Output Format"],
    "torusguard-full": ["Objective", "7-Stage Security Pipeline", "Specialist Skill Routing", "Pipeline Execution Instructions", "Confidence Scoring Rubric", "Safety & Governance", "Output Format"],
}


def parse_frontmatter(content):
    """Extract YAML frontmatter key-value pairs."""
    match = re.match(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
    if not match:
        return None
    raw = match.group(1)
    meta = {}
    for line in raw.split("\n"):
        line = line.strip()
        if ":" in line and not line.startswith("-"):
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip().strip("\"'")
    return meta


def validate_skills(target_skills):
    errors = []
    passed = 0

    print("================================================================================")
    print("TORUSGUARD v0.9.0 GRANULAR SKILLS VALIDATION SUITE")
    print("================================================================================")

    # 1. Existence & Structure
    print("\n1. Checking Skill File Existence & Structure...")
    for skill_name in target_skills:
        skill_dir = os.path.join("skills", skill_name)
        skill_file = os.path.join(skill_dir, "SKILL.md")
        if not os.path.isdir(skill_dir):
            errors.append(f"Directory missing: {skill_dir}")
            continue
        if not os.path.isfile(skill_file):
            errors.append(f"File missing: {skill_file}")
            continue
        print(f"  [PASS] Found {skill_file}")
        passed += 1

    # 2. YAML Frontmatter & Naming
    print("\n2. Checking Frontmatter Integrity & Versioning (0.9.0)...")
    for skill_name in target_skills:
        skill_file = os.path.join("skills", skill_name, "SKILL.md")
        if not os.path.isfile(skill_file):
            continue
        with open(skill_file, "r", encoding="utf-8") as fh:
            content = fh.read()
        meta = parse_frontmatter(content)
        if not meta:
            errors.append(f"Invalid or missing YAML frontmatter in {skill_file}")
            continue
        if meta.get("name") != skill_name:
            errors.append(f"Name mismatch in {skill_file}: expected '{skill_name}', got '{meta.get('name')}'")
            continue
        ver = meta.get("version", "")
        if not (ver.startswith("0.9.") or ver >= "0.9.0"):
            errors.append(f"Version mismatch in {skill_file}: expected '>=0.9.0', got '{ver}'")
            continue
        print(f"  [PASS] {skill_name}: name and version {ver} verified")
        passed += 1

    # 3. Context Budget Discipline (<= 300 lines)
    print("\n3. Checking Context Budget Discipline (<= 300 lines)...")
    for skill_name in target_skills:
        skill_file = os.path.join("skills", skill_name, "SKILL.md")
        if not os.path.isfile(skill_file):
            continue
        with open(skill_file, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
        count = len(lines)
        if count > 300:
            errors.append(f"Context budget exceeded in {skill_file}: {count} lines > 300")
            continue
        print(f"  [PASS] {skill_name}: {count} lines (within budget)")
        passed += 1

    # 4. Required Content Sections
    print("\n4. Checking Required Content Sections...")
    for skill_name in target_skills:
        if skill_name not in REQUIRED_SECTIONS:
            continue
        skill_file = os.path.join("skills", skill_name, "SKILL.md")
        if not os.path.isfile(skill_file):
            continue
        with open(skill_file, "r", encoding="utf-8") as fh:
            content = fh.read()
        missing_sections = []
        for sec in REQUIRED_SECTIONS[skill_name]:
            if sec.lower() not in content.lower():
                missing_sections.append(sec)
        if missing_sections:
            errors.append(f"{skill_name} missing required sections: {missing_sections}")
            continue
        print(f"  [PASS] {skill_name}: all required sections present")
        passed += 1

    # 5. Router Integrity (if router in target)
    if "torusguard" in target_skills:
        print("\n5. Checking Router Routing Table Integrity...")
        router_file = os.path.join("skills", "torusguard", "SKILL.md")
        with open(router_file, "r", encoding="utf-8") as fh:
            router_content = fh.read()
        router_missing = []
        for s in EXPECTED_SKILLS:
            if s == "torusguard":
                continue
            if s not in router_content:
                router_missing.append(s)
        if router_missing:
            errors.append(f"Router missing references to specialist skills: {router_missing}")
        else:
            print(f"  [PASS] Router references all 12 specialist skills cleanly")
            passed += 1

    # 6. Script Bindings Integrity
    print("\n6. Checking Script Binding Targets...")
    for skill_name in target_skills:
        skill_file = os.path.join("skills", skill_name, "SKILL.md")
        if not os.path.isfile(skill_file):
            continue
        with open(skill_file, "r", encoding="utf-8") as fh:
            content = fh.read()
        script_matches = re.findall(r"\.torusguard/scripts/([a-zA-Z0-9_\.]+\.py)", content)
        for s in set(script_matches):
            target_script = os.path.join(".torusguard", "scripts", s)
            if not os.path.isfile(target_script):
                errors.append(f"Referenced script does not exist: {target_script} (in {skill_name})")
    print("  [PASS] All referenced Python scripts exist in .torusguard/scripts/")
    passed += 1

    print("\n--------------------------------------------------------------------------------")
    print(f"RESULTS: {passed} Checks Passed | {len(errors)} Errors")
    if errors:
        print("\nERRORS DETECTED:")
        for e in errors:
            print(f"  [FAIL] {e}")
        print("================================================================================")
        return False
    print("================================================================================")
    print("ALL GRANULAR SKILLS VALIDATED CLEANLY!")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TorusGuard v0.9.0 Skills Validation Harness")
    parser.add_argument("--part", type=int, choices=[1, 2, 3], help="Validate specific execution part")
    args = parser.parse_args()

    if args.part == 1:
        target = PART1_SKILLS
    elif args.part == 2:
        target = PART2_SKILLS
    elif args.part == 3:
        target = EXPECTED_SKILLS
    else:
        target = EXPECTED_SKILLS

    success = validate_skills(target)
    sys.exit(0 if success else 1)
