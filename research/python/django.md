# Python Security Research Notes (TorusGuard v0.4.0)

## Research Overview
This research explores framework-specific attack surfaces and native defensive patterns across the Python web ecosystem.

### Framework Findings
* **Django:** Strong built-in CSRF and ORM parameterization, but common risks arise in `settings.py` misconfigurations (`DEBUG=True`, wildcard `ALLOWED_HOSTS`) and ModelForm mass assignment when `fields = '__all__'` is used.
* **DRF:** Default `AllowAny` permissions on unconfigured ViewSets and writable serializer fields allow privilege escalation.
* **FastAPI:** Pydantic request models provide strong typing, but accept dynamic dicts if not configured with `extra="forbid"`. Outbound `httpx`/`requests` calls require explicit SSRF validation.
* **Flask:** Minimalist core requires manual integration of `Flask-WTF` for CSRF and explicit session cookie flags.
* **SQLAlchemy:** Automatic parameterization in ORM queries, but raw `text()` clauses risk SQL injection if strings are formatted or interpolated.
