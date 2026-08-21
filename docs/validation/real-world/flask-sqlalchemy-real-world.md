# Real-World Validation Record: Flask + SQLAlchemy Application

- **Repository:** Anonymized Flask Internal Document Processing Portal
- **Authorization:** Maintainer-permitted code review evaluation
- **Repository Version / Commit SHA:** `3c9a5e1f72b8d04a6e9c1f2a5b7d8e4c6f2a4b90`
- **Stack Detected:** Python 3.11, Flask 3.0, Flask-WTF, Flask-SQLAlchemy, SQLite/PostgreSQL, `requirements.txt`
- **TorusGuard Version:** v0.4.0
- **Date Tested:** 2026-08-21

---

## 🔍 Findings

| Rule ID | Classification | Evidence | Maintainer Outcome |
|---|---|---|---|
| `TG-INPUT-004` | **Confirmed** | Document upload handler saved files using raw `file.filename` directly to disk | **Confirmed & Remediated:** Integrated `werkzeug.utils.secure_filename()` and extension allowlist validation. |
| `TG-CSRF-001` | **Confirmed** | State-changing file deletion endpoint accepted POST requests without CSRF validation token | **Confirmed & Remediated:** Initialized `flask_wtf.CSRFProtect(app)` and added token fields. |
| `TG-INPUT-003` | **Likely** | Search query constructed using `db.session.execute(text(f"SELECT * FROM docs WHERE query LIKE '%{q}%'"))` | **Confirmed & Remediated:** Replaced with bound parameter `text("SELECT * FROM docs WHERE query LIKE :q")` with `{"q": f"%{q}%"}`. |

---

## 📊 Results Summary

- **Confirmed Findings:** 2 (Unsafe file upload, Missing CSRF defense)
- **Likely Findings:** 1 (Raw SQL string interpolation with `text()`)
- **False Positives:** 0
- **Documentation Improvements:** Added explicit like-query parameterization example to [guides/python/sqlalchemy.md](../../guides/python/sqlalchemy.md).
