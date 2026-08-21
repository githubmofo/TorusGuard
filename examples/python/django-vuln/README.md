# Intentionally Vulnerable Example
> **WARNING:** This project exists only to test and demonstrate TorusGuard guidance. Do not deploy it, expose it to the internet, reuse its security patterns, or add real credentials. All secrets, users, payment values, and tokens are fake and nonfunctional.

---

## 🎯 Educational Purpose
This is a minimal Django reference application demonstrating common vulnerability patterns:
1. **`TG-SEC-001`**: Hardcoded dummy `SECRET_KEY` in `settings.py`.
2. **`TG-PLATFORM-003`**: Production-like configuration running with `DEBUG = True`.
3. **`TG-AUTH-007`**: Direct object lookup by ID without user ownership validation (IDOR) in `accounts/views.py`.
4. **`TG-AUTH-006`**: Mass assignment vulnerability in `accounts/forms.py` using `fields = '__all__'`.
5. **`TG-CACHE-001`**: Sensitive profile view missing `@never_cache` headers.

---

## 🚀 Running Locally (For Educational Testing Only)
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

See [fixes.md](fixes.md) and [../django-hardened/](../django-hardened/) for the safe counterpart.
