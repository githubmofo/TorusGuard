# TorusGuard Skill Reference: Python Security Overview

> **Loaded When:** Any Python project is detected (`requirements.txt`, `pyproject.toml`, `Pipfile`, `.py` source files).

---

## 🐍 Python Platform Security Principles

1. **Explicit Boundaries Over Dynamic Magic:** Avoid unpacking arbitrary user dictionaries directly into database ORM models or data structures (`**req.dict()`, `**request.json`).
2. **Server-Side Authorization First:** Route decorators (`@login_required`) verify identity, but database queries must verify resource ownership (`user_id == current_user.id`).
3. **Outbound Request Bounding (SSRF):** Always validate scheme, resolve DNS, and block private CIDR blocks before calling `requests.get()` or `httpx.get()`.
4. **Deterministic Environments:** Always maintain virtual environment isolation and commit cryptographically verifiable lockfiles (`poetry.lock`, `uv.lock`, `requirements.lock`).
