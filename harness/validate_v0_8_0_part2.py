"""
Validation Harness for TorusGuard v0.8.0 - Part 2 (Agents, Workflows & Templates)
Verifies:
1. All 5 specialist agent definitions in .torusguard/agents/
2. All 11 workflow files in .torusguard/workflows/
3. All 4 output templates in .torusguard/templates/
"""

import sys
from pathlib import Path

def test_part2_agents_workflows_templates():
    root = Path(__file__).resolve().parent.parent
    torusguard_dir = root / ".torusguard"
    
    print("=== TorusGuard v0.8.0 Part 2 Validation ===")
    
    # 1. Check Agents (5 files)
    agents_dir = torusguard_dir / "agents"
    assert agents_dir.is_dir(), "Missing .torusguard/agents directory"
    expected_agents = ["profiler", "auditor", "validator", "remediator", "reviewer"]
    for agent_name in expected_agents:
        agent_file = agents_dir / f"{agent_name}.md"
        assert agent_file.is_file(), f"Missing agent definition: {agent_file}"
        content = agent_file.read_text(encoding="utf-8")
        assert content.startswith("---"), f"Agent {agent_name}.md missing frontmatter"
        assert f"name: {agent_name}" in content, f"Agent {agent_name}.md frontmatter name mismatch"
        assert "Responsibilities" in content, f"Agent {agent_name}.md missing Responsibilities"
        assert "Safety Constraints" in content, f"Agent {agent_name}.md missing Safety Constraints"
        print(f"  [PASS] Agent verified: {agent_name}.md")

    # 2. Check Workflows (11 files)
    workflows_dir = torusguard_dir / "workflows"
    assert workflows_dir.is_dir(), "Missing .torusguard/workflows directory"
    expected_workflows = [
        "init",
        "authorize",
        "audit",
        "verify",
        "web-validate",
        "exploit-check",
        "harden",
        "apply",
        "recheck",
        "report",
        "status"
    ]
    for wf in expected_workflows:
        wf_file = workflows_dir / f"{wf}.md"
        assert wf_file.is_file(), f"Missing workflow: {wf_file}"
        content = wf_file.read_text(encoding="utf-8")
        assert len(content.splitlines()) >= 15, f"Workflow {wf}.md too short"
        assert "Objective" in content, f"Workflow {wf}.md missing Objective"
        assert "Execution Steps" in content or "Steps" in content, f"Workflow {wf}.md missing Steps"
        print(f"  [PASS] Workflow verified: {wf}.md")

    # 3. Check Templates (4 files)
    templates_dir = torusguard_dir / "templates"
    assert templates_dir.is_dir(), "Missing .torusguard/templates directory"
    expected_templates = [
        "authorization.template.md",
        "audit-report.template.md",
        "remediation-bundle.template.md",
        "finding-card.template.md"
    ]
    for tmpl in expected_templates:
        tmpl_file = templates_dir / tmpl
        assert tmpl_file.is_file(), f"Missing template: {tmpl_file}"
        content = tmpl_file.read_text(encoding="utf-8")
        assert "{{" in content and "}}" in content, f"Template {tmpl} missing variable placeholders"
        print(f"  [PASS] Template verified: {tmpl}")

    print("\n>>> ALL TORUSGUARD v0.8.0 PART 2 CHECKS PASSED (100%) <<<\n")

if __name__ == "__main__":
    try:
        test_part2_agents_workflows_templates()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected exception: {e}")
        sys.exit(2)
