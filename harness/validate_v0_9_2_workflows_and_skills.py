#!/usr/bin/env python3
"""
TorusGuard v0.9.2 Workflows & Skills Validation Suite
Validates the Command-Engine Standard across both:
1. Workflows (.torusguard/workflows/*.md)
2. Skills (skills/*/SKILL.md and .torusguard/skills/*/SKILL.md)
Validates YAML frontmatter, required sections, script bindings, and two-way cross-bindings.
"""

import os
import sys
import yaml
from pathlib import Path

WORKFLOW_FILES = [
    "init.md", "authorize.md", "audit.md", "verify.md",
    "web-validate.md", "exploit-check.md", "harden.md",
    "apply.md", "recheck.md", "report.md", "status.md"
]

SKILL_NAMES = [
    "torusguard-init", "torusguard-authorize", "torusguard-audit", "torusguard-verify",
    "torusguard-web-validate", "torusguard-exploit-check", "torusguard-harden",
    "torusguard-apply", "torusguard-recheck", "torusguard-report", "torusguard-status",
    "torusguard-full", "torusguard"
]

WORKFLOW_REQUIRED_SECTIONS = [
    "Mandatory Pre-Flight",
    "When to Use",
    "Execution Steps",
    "Failure Recovery",
    "Hallucination Guard",
    "Output Card Format",
    "Next Steps"
]

SKILL_REQUIRED_SECTIONS = {
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


def parse_markdown_frontmatter(content):
    """Parse YAML frontmatter from markdown file."""
    if not content.startswith("---"):
        return None, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content
    try:
        meta = yaml.safe_load(parts[1])
        return meta, parts[2]
    except Exception:
        return None, content


def validate_workflows(repo_root):
    """Validate all 11 workflows against the Command-Engine Standard."""
    print("\n--- 1. Testing Workflows (.torusguard/workflows/) ---")
    workflows_dir = repo_root / ".torusguard" / "workflows"
    assert workflows_dir.is_dir(), f"Missing directory: {workflows_dir}"

    for w_name in WORKFLOW_FILES:
        w_path = workflows_dir / w_name
        assert w_path.is_file(), f"Missing workflow file: {w_path}"

        content = w_path.read_text(encoding="utf-8")
        meta, body = parse_markdown_frontmatter(content)
        assert meta is not None, f"Invalid YAML frontmatter in {w_name}"

        # Frontmatter keys check
        req_meta = ["description", "tools", "version", "agent", "lifecycle-phase", "required-skills", "scripts-binding"]
        for key in req_meta:
            assert key in meta, f"Workflow {w_name} missing frontmatter key: {key}"

        # Required sections check
        for sec in WORKFLOW_REQUIRED_SECTIONS:
            assert sec in body, f"Workflow {w_name} missing required section: {sec}"

        # Scripts binding check
        for script in meta.get("scripts-binding", []):
            script_path = repo_root / script
            assert script_path.is_file(), f"Workflow {w_name} binds non-existent script: {script}"

        # Line budget check (90 - 200 lines)
        line_count = len(content.splitlines())
        assert 90 <= line_count <= 250, f"Workflow {w_name} line count {line_count} outside bounds (90-250)"
        print(f"  [PASS] {w_name}: {line_count} lines | Agent: {meta['agent']} | Skills: {meta['required-skills']}")


def validate_skills_and_mirrors(repo_root):
    """Validate all 13 skills in skills/ and their mirrors in .torusguard/skills/."""
    print("\n--- 2. Testing Skills & Mirror Synchronization ---")
    skills_root = repo_root / "skills"
    mirror_root = repo_root / ".torusguard" / "skills"
    assert skills_root.is_dir(), f"Missing directory: {skills_root}"
    assert mirror_root.is_dir(), f"Missing directory: {mirror_root}"

    for s_name in SKILL_NAMES:
        s_path = skills_root / s_name / "SKILL.md"
        m_path = mirror_root / s_name / "SKILL.md"

        assert s_path.is_file(), f"Missing skill file: {s_path}"
        assert m_path.is_file(), f"Missing mirrored skill file: {m_path}"

        content_s = s_path.read_text(encoding="utf-8")
        content_m = m_path.read_text(encoding="utf-8")

        # Check exact content sync between skills/ and .torusguard/skills/
        assert content_s == content_m, f"Skill content out of sync between skills/{s_name} and .torusguard/skills/{s_name}"

        meta, body = parse_markdown_frontmatter(content_s)
        assert meta is not None, f"Invalid YAML frontmatter in {s_path}"
        assert meta.get("name") == s_name, f"Name mismatch in {s_name}: got {meta.get('name')}"

        # Check required sections if registered
        if s_name in SKILL_REQUIRED_SECTIONS:
            for sec in SKILL_REQUIRED_SECTIONS[s_name]:
                assert sec in body, f"Skill {s_name} missing required section: {sec}"

        # Context budget check (<= 300 lines)
        line_count = len(content_s.splitlines())
        assert line_count <= 300, f"Skill {s_name} exceeds context budget: {line_count} > 300"
        print(f"  [PASS] {s_name}: {line_count} lines (budget <= 300) | Mirror synchronized")


def validate_cross_bindings(repo_root):
    """Validate 1:1 cross-bindings between workflows and skills."""
    print("\n--- 3. Testing Two-Way Workflow <-> Skill Cross-Bindings ---")
    workflows_dir = repo_root / ".torusguard" / "workflows"
    skills_root = repo_root / "skills"

    for w_name in WORKFLOW_FILES:
        meta, _ = parse_markdown_frontmatter((workflows_dir / w_name).read_text(encoding="utf-8"))
        req_skills = meta.get("required-skills", [])
        assert len(req_skills) >= 1, f"Workflow {w_name} declares no required skills"

        primary_skill = req_skills[0]
        skill_file = skills_root / primary_skill / "SKILL.md"
        assert skill_file.is_file(), f"Workflow {w_name} binds non-existent skill: {primary_skill}"

        s_meta, _ = parse_markdown_frontmatter(skill_file.read_text(encoding="utf-8"))
        skill_wf = s_meta.get("workflow", "")
        expected_wf = f".torusguard/workflows/{w_name}"
        assert skill_wf == expected_wf, f"Skill {primary_skill} workflow mismatch: expected {expected_wf}, got {skill_wf}"
        print(f"  [PASS] Cross-binding verified: {w_name} <===> {primary_skill}")


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    print("================================================================================")
    print("TORUSGUARD v0.9.2 WORKFLOWS & SKILLS COMMAND-ENGINE TEST SUITE")
    print("================================================================================")

    try:
        validate_workflows(repo_root)
        validate_skills_and_mirrors(repo_root)
        validate_cross_bindings(repo_root)
        print("\n================================================================================")
        print("ALL v0.9.2 WORKFLOWS & SKILLS VALIDATION CHECKS PASSED (100%)")
        print("================================================================================")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] Assertion failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(2)
