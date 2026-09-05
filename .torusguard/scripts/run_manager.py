#!/usr/bin/env python3
"""
TorusGuard Run Folder Lifecycle Manager (v1.0.0)
Creates isolated run folders, tracks manifest.json state, enumerates execution history,
and bridges completed run findings to the persistent security memory engine.
"""

import sys
import json
import datetime
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional


def create_run(base_dir: Path, command: str, target_name: str = "project") -> Path:
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    run_id = f"run-{timestamp}-{command}"
    run_folder = base_dir / run_id
    run_folder.mkdir(parents=True, exist_ok=True)

    manifest = {
        "run_id": run_id,
        "command": command,
        "target_name": target_name,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "status": "in_progress",
        "torusguard_version": "1.0.0",
        "findings_count": 0,
        "confirmed_fixed_count": 0,
        "regressed_count": 0
    }

    manifest_path = run_folder / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return run_folder


def list_runs(base_dir: Path) -> List[Dict[str, Any]]:
    runs = []
    if not base_dir.is_dir():
        return runs

    for d in sorted(base_dir.iterdir(), reverse=True):
        if d.is_dir() and d.name.startswith("run-"):
            manifest_file = d / "manifest.json"
            if manifest_file.is_file():
                try:
                    with open(manifest_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    runs.append(data)
                except Exception:
                    runs.append({"run_id": d.name, "status": "corrupted"})
            else:
                runs.append({"run_id": d.name, "status": "unmanifested"})
    return runs


def sync_run_to_memory(run_folder: Path, findings: Optional[List[Dict[str, Any]]] = None) -> int:
    """
    Sync findings from a completed run into the .torusguard/memory/ engine.
    Records events based on command type (audit -> audit_finding, apply -> fix_applied, recheck -> fix_verified).
    """
    manifest_file = run_folder / "manifest.json"
    if not manifest_file.is_file():
        return 0

    try:
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception:
        return 0

    command = manifest.get("command", "audit")

    # If findings not explicitly provided, try reading findings.json in run_folder
    actual_findings = findings
    if actual_findings is None:
        findings_file = run_folder / "findings.json"
        if findings_file.is_file():
            try:
                with open(findings_file, "r", encoding="utf-8") as f:
                    actual_findings = json.load(f)
            except Exception:
                actual_findings = []

    if not actual_findings or not isinstance(actual_findings, list):
        return 0

    # Import memory_engine in-process
    try:
        scripts_dir = Path(__file__).resolve().parent
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        import memory_engine

        recorded_count = 0
        for f in actual_findings:
            rule_id = f.get("rule_id") or f.get("id")
            if not rule_id:
                continue

            event_type = "audit_finding"
            if command in ("harden", "apply"):
                event_type = "fix_applied"
            elif command in ("recheck", "verify"):
                event_type = "fix_verified"

            data = {
                "rule_id": rule_id,
                "file_path": f.get("file_path") or f.get("file"),
                "line_number": f.get("line_number") or f.get("line"),
                "severity": (f.get("severity") or "medium").lower(),
                "confidence_score": f.get("confidence_score") or f.get("confidence", 70),
                "code_hash": f.get("code_hash"),
                "fix_strategy": f.get("fix_strategy") or f.get("strategy"),
                "verification_result": f.get("verification_result") or f.get("result", "fixed"),
                "suppression_reason": f.get("suppression_reason")
            }
            memory_engine.record_event(event_type, data)
            recorded_count += 1

        if recorded_count > 0:
            memory_engine.distill_patterns()

        return recorded_count
    except Exception as e:
        # Non-blocking: memory failure should never crash a run
        return 0


def main():
    parser = argparse.ArgumentParser(description="TorusGuard Run Manager")
    subparsers = parser.add_subparsers(dest="subcommand")

    create_p = subparsers.add_parser("create")
    create_p.add_argument("--command", "-c", default="audit", help="TorusGuard command (audit, web-validate, harden, etc.)")
    create_p.add_argument("--target", "-t", default="project", help="Target project name")
    create_p.add_argument("--dir", "-d", default=".torusguard/runs", help="Base runs directory")

    list_p = subparsers.add_parser("list")
    list_p.add_argument("--dir", "-d", default=".torusguard/runs", help="Base runs directory")
    list_p.add_argument("--json", action="store_true", help="Output JSON")

    sync_p = subparsers.add_parser("sync-memory")
    sync_p.add_argument("--run-folder", "-r", required=True, help="Path to run folder")

    args = parser.parse_args()

    if args.subcommand == "create":
        folder = create_run(Path(args.dir), args.command, args.target)
        print(f"Created run folder: {folder}")
    elif args.subcommand == "list":
        runs = list_runs(Path(args.dir))
        if args.json:
            print(json.dumps(runs, indent=2))
        else:
            print(f"Total Runs Found: {len(runs)}")
            for r in runs:
                print(f"  - {r.get('run_id')}: command={r.get('command')}, status={r.get('status')}")
    elif args.subcommand == "sync-memory":
        count = sync_run_to_memory(Path(args.run_folder))
        print(f"Synced {count} findings from run to memory.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
