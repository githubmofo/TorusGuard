"""
TorusGuard v0.7.0 Authorization & Scope Enforcement Engine
Enforces explicit target authorization and scope boundaries before any runtime validation.
No runtime HTTP or browser interaction is permitted without valid, non-expired authorization.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from urllib.parse import urlparse


class AuthorizationError(PermissionError):
    """Raised when runtime validation is attempted without valid authorization or outside approved scope."""
    pass


@dataclass
class TargetScope:
    target_hosts: List[str]
    allowed_path_prefixes: List[str]
    forbidden_paths: List[str]
    valid_from: str
    valid_until: str
    max_depth: int = 3
    max_requests: int = 100
    allow_state_changing_methods: bool = False
    allowed_issue_classes: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TargetScope":
        return cls(
            target_hosts=data.get("target_hosts", []),
            allowed_path_prefixes=data.get("allowed_path_prefixes", ["/"]),
            forbidden_paths=data.get("forbidden_paths", ["/admin/delete", "/system/shutdown"]),
            valid_from=data.get("valid_from", ""),
            valid_until=data.get("valid_until", ""),
            max_depth=data.get("max_depth", 3),
            max_requests=data.get("max_requests", 100),
            allow_state_changing_methods=data.get("allow_state_changing_methods", False),
            allowed_issue_classes=data.get("allowed_issue_classes", [
                "auth_bypass",
                "tenant_isolation",
                "header_trust",
                "path_traversal",
                "debug_exposure"
            ])
        )


@dataclass
class AuthorizationRecord:
    authorization_id: str
    target_name: str
    authorized_by: str
    authorization_type: str  # "target_owner", "written_authorization", "ci_sandboxed_test"
    scope: TargetScope
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["scope"] = self.scope.to_dict()
        return d


class AuthorizationManager:
    """
    Validates, manages, and stores target authorizations in isolated run folders.
    """

    @staticmethod
    def is_scope_active(scope: TargetScope) -> Tuple[bool, str]:
        now = datetime.now(timezone.utc)
        if scope.valid_from:
            try:
                v_from = datetime.fromisoformat(scope.valid_from.replace("Z", "+00:00"))
                if now < v_from:
                    return False, f"Authorization not yet active (starts {scope.valid_from})"
            except Exception:
                pass
        if scope.valid_until:
            try:
                v_until = datetime.fromisoformat(scope.valid_until.replace("Z", "+00:00"))
                if now > v_until:
                    return False, f"Authorization expired at {scope.valid_until}"
            except Exception:
                pass
        return True, "Authorization active"

    @classmethod
    def validate_url(cls, url: str, scope: TargetScope) -> Tuple[bool, str]:
        """
        Ensures target URL is strictly inside approved hosts, allowed path prefixes,
        and not in forbidden paths.
        """
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        if not host:
            return False, f"Invalid URL (missing host): {url}"

        # Match approved host (supports exact host:port or hostname)
        host_matched = False
        for approved in scope.target_hosts:
            approved_lower = approved.lower()
            if host == approved_lower or host.startswith(approved_lower + ":") or approved_lower.startswith(host + ":"):
                host_matched = True
                break

        if not host_matched:
            return False, f"Host '{host}' is NOT in approved target_hosts: {scope.target_hosts}"

        # Check forbidden paths
        path = parsed.path or "/"
        for forbidden in scope.forbidden_paths:
            if path.startswith(forbidden):
                return False, f"Path '{path}' matches forbidden path '{forbidden}'"

        # Check allowed path prefixes
        prefix_matched = False
        for prefix in scope.allowed_path_prefixes:
            if path.startswith(prefix):
                prefix_matched = True
                break

        if not prefix_matched:
            return False, f"Path '{path}' does NOT match any allowed_path_prefixes: {scope.allowed_path_prefixes}"

        # Check TTL
        active, reason = cls.is_scope_active(scope)
        if not active:
            return False, reason

        return True, "URL within authorized scope"

    @classmethod
    def check_authorized_or_raise(cls, url: str, auth: Optional[AuthorizationRecord], method: str = "GET") -> None:
        """
        Hard security gate: raises AuthorizationError if auth is missing, expired,
        or URL violates scope boundaries.
        """
        if not auth:
            raise AuthorizationError("Runtime validation blocked: No authorization record provided.")

        # Method check
        if method.upper() in ["POST", "PUT", "DELETE", "PATCH"] and not auth.scope.allow_state_changing_methods:
            raise AuthorizationError(f"State-changing method '{method}' is forbidden under current scope.")

        valid, reason = cls.validate_url(url, auth.scope)
        if not valid:
            raise AuthorizationError(f"Runtime validation blocked: {reason}")

    @classmethod
    def write_artifacts(cls, run_dir: Path, auth: AuthorizationRecord) -> Tuple[Path, Path]:
        """
        Emits standard scope.json and authorization.md into the run folder.
        """
        run_dir.mkdir(parents=True, exist_ok=True)
        scope_file = run_dir / "scope.json"
        auth_file = run_dir / "authorization.md"

        # 1. Write scope.json
        with open(scope_file, "w", encoding="utf-8") as f:
            json.dump(auth.to_dict(), f, indent=2)

        # 2. Write authorization.md
        md_content = f"""# TorusGuard v0.7.0 Runtime Authorization Document

**Authorization ID:** `{auth.authorization_id}`  
**Target Application:** `{auth.target_name}`  
**Authorized By:** `{auth.authorized_by}`  
**Authorization Type:** `{auth.authorization_type}`  
**Created At:** `{auth.created_at}`  

---

## 🔒 Scope Boundaries & Permitted Constraints

| Parameter | Allowed Value |
|---|---|
| **Target Hosts** | `{", ".join(auth.scope.target_hosts)}` |
| **Allowed Path Prefixes** | `{", ".join(auth.scope.allowed_path_prefixes)}` |
| **Forbidden Paths** | `{", ".join(auth.scope.forbidden_paths)}` |
| **Active Window** | `{auth.scope.valid_from}` ➔ `{auth.scope.valid_until}` |
| **Max Navigation Depth** | `{auth.scope.max_depth}` levels |
| **Max Request Budget** | `{auth.scope.max_requests}` requests |
| **State-Changing Methods** | `{"Allowed" if auth.scope.allow_state_changing_methods else "Forbidden (Read-only GET/HEAD only)"}` |
| **Approved Issue Classes** | `{", ".join(auth.scope.allowed_issue_classes or [])}` |

---

## ⚖️ Legal & Governance Statement
This authorization represents verifiable consent by `{auth.authorized_by}` to perform non-destructive, bounded runtime validation against the specified target hosts. Destructive testing, denial of service, memory corruption, and automated credential stuffing are strictly prohibited.
"""
        with open(auth_file, "w", encoding="utf-8") as f:
            f.write(md_content)

        return scope_file, auth_file
