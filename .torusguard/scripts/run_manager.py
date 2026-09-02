#!/usr/bin/env python3
"""
TorusGuard Run Folder Lifecycle Manager
Creates isolated run folders, tracks manifest.json state, and enumerates execution history.
"""

import sys
import json
import datetime
import argparse
from pathlib import Path
from typing import Dict, Any, List

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
        "torusguard_version": "0.8.0",
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
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
