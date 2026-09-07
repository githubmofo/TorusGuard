#!/usr/bin/env python3
"""
TorusGuard Content-Aware Diff Line Scanner (v1.0.0)
Evaluates unified diff patches against security invariants before harden or apply,
including regression watch checks against persistent memory patterns.
Pure Python 3.10+ standard library (zero external dependencies).
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

BYPASS_PATTERNS = [
    (re.compile(r'(?:#|//|/\*)\s*(?:TODO\s*:?\s*)?(?:bypass|skip|disable)[_\s]*(?:auth|security|check|guard|filter|csrf|tenant)', re.IGNORECASE), "Suspicious authentication or security check bypass comment"),
    # TLS / Certificate validation bypasses across Python, Go, Node, Java, C#, PHP, Rust
    (re.compile(r'\bverify\s*=\s*False\b'), "Disabled TLS certificate verification (verify=False)"),
    (re.compile(r'\bInsecureSkipVerify\s*:\s*true\b'), "Disabled Go TLS certificate verification (InsecureSkipVerify: true)"),
    (re.compile(r'\bNODE_TLS_REJECT_UNAUTHORIZED\s*=\s*[\'"]?0[\'"]?'), "Disabled Node.js TLS verification (NODE_TLS_REJECT_UNAUTHORIZED=0)"),
    (re.compile(r'\brejectUnauthorized\s*:\s*false\b'), "Disabled Node.js TLS rejectUnauthorized"),
    (re.compile(r'\b(?:TrustAllStrategy|NoopHostnameVerifier|DangerousAcceptAnyServerCertificateValidator)\b'), "Disabled Java / C# TLS certificate validation"),
    (re.compile(r'\bServerCertificateCustomValidationCallback\s*=\s*(?:\([^)]*\)\s*=>\s*true|HttpClientHandler\.DangerousAcceptAnyServerCertificateValidator)'), "Disabled C# TLS certificate callback"),
    (re.compile(r'\bCURLOPT_SSL_VERIFYPEER\s*(?:=>|,)\s*(?:false|0)\b', re.IGNORECASE), "Disabled PHP curl SSL verification (CURLOPT_SSL_VERIFYPEER => false)"),
    (re.compile(r'\bdanger_accept_invalid_certs\s*\(\s*true\s*\)'), "Disabled Rust reqwest TLS certificate validation"),
    # Auth & CSRF bypasses
    (re.compile(r'\b(?:skip_auth|bypass_auth|disable_auth|allow_all|permit_all)\s*=\s*True\b', re.IGNORECASE), "Explicit security bypass flag enabled"),
    (re.compile(r'@(?:csrf_exempt|allow_anonymous|disable_token_check)\b'), "Decorator disabling route-level security or CSRF protection"),
    (re.compile(r'\[(?:AllowAnonymous|Authorize\s*\(\s*Roles\s*=\s*"\*"\s*\))\]'), "Attribute disabling ASP.NET authentication or authorization"),
    (re.compile(r'\.csrf\(\)\.disable\(\)|\.csrf\([^)]*AbstractHttpConfigurer::disable\)'), "Spring Security CSRF protection explicitly disabled"),
    # CORS wildcard with credentials
    (re.compile(r'\bCORS_ALLOW_ALL_ORIGINS\s*=\s*True\b'), "Wildcard CORS origin enabled in patch"),
    (re.compile(r'@CrossOrigin\s*\(\s*(?:origins\s*=\s*)?["\']\*["\']'), "Wildcard CORS origin annotation in Java/Spring"),
    # Native dangerous constructs
    (re.compile(r'\bextract\s*\(\s*\$_(?:POST|GET|REQUEST)\s*\)'), "Dangerous PHP extract() on untrusted user input"),
    (re.compile(r'\bunsafe\s*\{'), "Unvetted Rust unsafe block introduced in patch"),
    # Polyglot additional security bypasses (Python, Ruby, Java, Kotlin, Elixir, Dart, C++)
    (re.compile(r'\bSESSION_COOKIE_SECURE\s*=\s*False\b'), "Session cookie secure flag disabled"),
    (re.compile(r'\bparams\.permit!'), "Rails strong parameters mass assignment bypass (params.permit!)"),
    (re.compile(r'\b(?:csrf(?:\(\))?\.disable\(\)|\.csrf\(\)\.disable\(\)|\.csrf\([^)]*AbstractHttpConfigurer::disable\))'), "CSRF protection explicitly disabled"),
    (re.compile(r'\b(?:verify_peer\s*:\s*false|verify\s*:\s*:verify_none)\b'), "Disabled Elixir TLS certificate verification"),
    (re.compile(r'\bbadCertificateCallback\s*='), "Disabled Dart/Flutter badCertificateCallback validation"),
    (re.compile(r'\bSSL_VERIFY_NONE\b'), "Disabled C/C++ OpenSSL certificate verification (SSL_VERIFY_NONE)"),
    (re.compile(r'\bpermitAll\(\)'), "Unrestricted access granted via permitAll()"),
    (re.compile(r'\bverify\s*(?:=>|=)\s*false\b', re.IGNORECASE), "Disabled TLS/HTTP client verification (verify => false)"),
    # Linters and scanners suppressions
    (re.compile(r'(?:#|//|/\*)\s*nosec\b', re.IGNORECASE), "Suppression comment (nosec) hiding potential vulnerability"),
    (re.compile(r'@SuppressWarnings\s*\(\s*["\'](?:security|all)["\']\s*\)'), "Java security suppression annotation")
]

SECRET_PATTERNS = [
    (re.compile(r'\b(?:sk_live|ak_live)_[0-9a-zA-Z]{20,}\b'), "Live payment or cloud API secret key"),
    (re.compile(r'\bgh[pousr]_[0-9a-zA-Z]{36}\b'), "GitHub personal access token"),
    (re.compile(r'\beyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]+\b'), "Hardcoded JSON Web Token (JWT) string"),
    (re.compile(r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----'), "Hardcoded private key block"),
    (re.compile(r'(?:password|secret|api_key|access_token)\s*=\s*["\'][A-Za-z0-9@#$%^&+=_\-]{8,}["\']', re.IGNORECASE), "Hardcoded credential or API secret string")
]

TENANT_FILTER_PATTERNS = [
    re.compile(r'\.filter\([^)]*\btenant\s*='),
    re.compile(r'\.filter_by\([^)]*\btenant\s*='),
    re.compile(r'\bwhere\s+tenant_id\s*='),
    re.compile(r'\btenant_id\s*==?'),
    re.compile(r'\btenantId\s*:'),
    re.compile(r'\.Where\([^)]*(?:tenant_id|TenantId)'),
    re.compile(r'\bwhere\s*:\s*\{[^}]*tenant')
]


def check_memory_regressions(
    current_file: str,
    current_line: int,
    added_content: str,
    root_dir: Optional[Path] = None
) -> List[Dict[str, Any]]:
    """
    Check if the added line re-introduces a vulnerability in a file
    that is tracked under active Regression Watch in .torusguard/memory/patterns.json.
    """
    violations = []
    base = Path(root_dir or Path.cwd()).resolve()
    torusguard_dir = base / ".torusguard"
    if not torusguard_dir.exists():
        for parent in base.parents:
            if (parent / ".torusguard").exists():
                torusguard_dir = parent / ".torusguard"
                break

    patterns_file = torusguard_dir / "memory" / "patterns.json"
    if not patterns_file.exists():
        return violations

    try:
        with open(patterns_file, "r", encoding="utf-8") as f:
            patterns = json.load(f)
    except Exception:
        return violations

    clean_file = current_file.replace("\\", "/")
    for pat in patterns:
        if pat.get("pattern_type") == "regression_watch":
            affected = [f.replace("\\", "/") for f in pat.get("affected_files", [])]
            if clean_file in affected or any(clean_file.endswith(a) for a in affected):
                rule_id = pat.get("rule_id", "TG-REG")
                desc = pat.get("description", "Regression watch violation")
                violations.append({
                    "rule_id": "TG-DIFF-004",
                    "category": "Regression Watch",
                    "severity": "HIGH",
                    "file": current_file,
                    "line": current_line,
                    "content": added_content.strip(),
                    "description": f"File {current_file} matches active Regression Watch for {rule_id}: {desc}"
                })
    return violations


def audit_diff(
    diff_content: str,
    check_memory: bool = False,
    root_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Parses a unified diff and returns detected violations.
    Optionally checks against active regression watch patterns in memory.
    """
    lines = diff_content.splitlines()
    violations: List[Dict[str, Any]] = []

    current_file = "unknown"
    current_line = 0

    additions: List[tuple[int, str]] = []
    deletions: List[tuple[int, str]] = []

    for line_idx, line in enumerate(lines, 1):
        if line.startswith('+++ b/'):
            current_file = line[6:].strip()
            continue
        elif line.startswith('--- a/'):
            continue
        elif line.startswith('@@'):
            # Parse line number e.g. @@ -10,5 +12,6 @@
            match = re.search(r'\+(\d+)', line)
            if match:
                current_line = int(match.group(1)) - 1
            continue

        if line.startswith('+') and not line.startswith('+++'):
            current_line += 1
            added_content = line[1:]
            additions.append((current_line, added_content))

            # Check bypass patterns
            for pat, desc in BYPASS_PATTERNS:
                if pat.search(added_content):
                    violations.append({
                        "rule_id": "TG-DIFF-001",
                        "category": "Bypass Sink",
                        "severity": "CRITICAL",
                        "file": current_file,
                        "line": current_line,
                        "content": added_content.strip(),
                        "description": desc
                    })

            # Check secret ingestion
            for pat, desc in SECRET_PATTERNS:
                if pat.search(added_content):
                    violations.append({
                        "rule_id": "TG-DIFF-002",
                        "category": "Secret Ingestion",
                        "severity": "CRITICAL",
                        "file": current_file,
                        "line": current_line,
                        "content": "[REDACTED_POTENTIAL_SECRET]",
                        "description": desc
                    })

            # Check memory regression watch if requested
            if check_memory:
                reg_violations = check_memory_regressions(current_file, current_line, added_content, root_dir=root_dir)
                violations.extend(reg_violations)

        elif line.startswith('-') and not line.startswith('---'):
            deleted_content = line[1:]
            deletions.append((line_idx, deleted_content))

    # Check for tenant filter deletion without replacement
    for del_idx, del_line in deletions:
        for t_pat in TENANT_FILTER_PATTERNS:
            if t_pat.search(del_line):
                # Verify if an equivalent tenant filter exists in additions
                replaced = any(t_pat.search(add_line) for _, add_line in additions)
                if not replaced:
                    violations.append({
                        "rule_id": "TG-DIFF-003",
                        "category": "Tenant Filter Removal",
                        "severity": "HIGH",
                        "file": current_file,
                        "line": del_idx,
                        "content": del_line.strip(),
                        "description": "Tenant isolation filter was removed without being restored in additions"
                    })

    status = "PASSED" if not violations else "BLOCKED"
    return {
        "status": status,
        "files_inspected": list(set(v["file"] for v in violations)) if violations else [current_file],
        "additions_count": len(additions),
        "deletions_count": len(deletions),
        "total_violations": len(violations),
        "violations": violations
    }


def audit_diff_file(file_path: str, check_memory: bool = False, root_dir: Optional[Path] = None) -> Dict[str, Any]:
    path = Path(file_path)
    if not path.is_file():
        return {
            "status": "ERROR",
            "error": f"File not found: {file_path}",
            "violations": []
        }
    content = path.read_text(encoding="utf-8", errors="replace")
    return audit_diff(content, check_memory=check_memory, root_dir=root_dir)


def check_diff_content(diff_content: str, file_path: str = "") -> List[Dict[str, Any]]:
    """Convenience helper to audit diff string directly and return list of violations."""
    res = audit_diff(diff_content)
    return res.get("violations", [])


def install_pre_commit_hook(root_dir: Optional[Path] = None) -> bool:
    """Install TorusGuard pre-commit security hook into .git/hooks/pre-commit."""
    base = Path(root_dir or Path.cwd()).resolve()
    git_dir = base / ".git"
    if not git_dir.exists():
        for parent in base.parents:
            if (parent / ".git").exists():
                git_dir = parent / ".git"
                break
    if not git_dir.exists():
        print("[ERROR] Diff Guard: Not a git repository (no .git directory found).", file=sys.stderr)
        return False

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_file = hooks_dir / "pre-commit"

    hook_script = """#!/usr/bin/env sh
# TorusGuard Pre-Commit Security Diff Guard
# Automatically blocks commits containing security bypasses, secret leaks, or tenant stripping.
python .torusguard/scripts/diff_guard.py --pre-commit
"""
    try:
        hook_file.write_text(hook_script, encoding="utf-8")
        if os.name != "nt":
            import stat
            os.chmod(hook_file, hook_file.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print(f"[SUCCESS] Installed TorusGuard pre-commit hook at: {hook_file}")
        return True
    except Exception as e:
        print(f"[ERROR] Diff Guard: Failed to install pre-commit hook: {e}", file=sys.stderr)
        return False


def uninstall_pre_commit_hook(root_dir: Optional[Path] = None) -> bool:
    """Uninstall TorusGuard pre-commit hook from .git/hooks/pre-commit."""
    base = Path(root_dir or Path.cwd()).resolve()
    git_dir = base / ".git"
    if not git_dir.exists():
        for parent in base.parents:
            if (parent / ".git").exists():
                git_dir = parent / ".git"
                break
    if not git_dir.exists():
        print("[WARN] Diff Guard: No .git directory found.", file=sys.stderr)
        return False

    hook_file = git_dir / "hooks" / "pre-commit"
    if hook_file.exists():
        try:
            hook_file.unlink()
            print("[SUCCESS] Uninstalled TorusGuard pre-commit hook.")
            return True
        except Exception as e:
            print(f"[ERROR] Diff Guard: Failed to delete hook file: {e}", file=sys.stderr)
            return False
    else:
        print("[INFO] Diff Guard: No pre-commit hook currently installed.")
        return True


def main():
    parser = argparse.ArgumentParser(description="TorusGuard Unified Diff Security Scanner")
    parser.add_argument("diff_path", nargs="?", help="Path to unified diff file (or read stdin if omitted)")
    parser.add_argument("--check-memory", action="store_true", help="Check additions against persistent memory regression watch patterns")
    parser.add_argument("--pre-commit", action="store_true", help="Audit git staged diff (--cached) for pre-commit hook")
    parser.add_argument("--install-hook", action="store_true", help="Install TorusGuard pre-commit hook into .git/hooks/pre-commit")
    parser.add_argument("--uninstall-hook", action="store_true", help="Uninstall TorusGuard pre-commit hook")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    if args.install_hook:
        sys.exit(0 if install_pre_commit_hook() else 1)

    if args.uninstall_hook:
        sys.exit(0 if uninstall_pre_commit_hook() else 1)

    if args.pre_commit:
        import subprocess
        try:
            res_git = subprocess.run(
                ["git", "diff", "--cached"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            diff_text = res_git.stdout
        except Exception as e:
            print(f"[ERROR] Diff Guard: Could not read git staged diff: {e}", file=sys.stderr)
            sys.exit(1)

        if not diff_text.strip():
            print("[PASS] Diff Guard (pre-commit): No staged changes detected.")
            sys.exit(0)

        res = audit_diff(diff_text, check_memory=True)
    elif args.diff_path:
        res = audit_diff_file(args.diff_path, check_memory=args.check_memory)
    else:
        if sys.stdin.isatty():
            parser.print_help()
            sys.exit(1)
        diff_text = sys.stdin.read()
        res = audit_diff(diff_text, check_memory=args.check_memory)

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        if res.get("status") == "PASSED":
            print(f"[PASS] Diff Guard: Clean patch (+{res['additions_count']}/-{res['deletions_count']}). Zero security bypasses.")
            sys.exit(0)
        else:
            print(f"[BLOCKED] Diff Guard: Found {res.get('total_violations', 0)} security invariant violation(s):")
            for v in res.get("violations", []):
                print(f"  - [{v['severity']}] {v['rule_id']} at {v['file']}:{v['line']} -> {v['description']}")
            sys.exit(1)


if __name__ == "__main__":
    main()

