# Flask Security Guide (TorusGuard v0.4.0)

> **Scope:** Security standards and hardening guidance for Flask web applications. Covers application factory configuration, session cookie security, route authorization, CSRF defense, Jinja2 template safety, and secure file handling.

---

## 🔍 Scope and Detection
TorusGuard detects Flask applications when `from flask import Flask`, `Flask(__name__)`, or `flask` in dependency files is present.

---

## ⚙️ 1. Application Factory & Session Security

Flask relies on developer-configured extensions and settings for baseline security.

### Safe Application Factory Pattern
```python
import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    # 1. Secret Key from Environment (TG-SEC-001)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
    if not app.config['SECRET_KEY'] and not app.debug:
        raise RuntimeError("FLASK_SECRET_KEY must be set in production.")

    # 2. Session Cookie Security Flags
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

    # 3. Maximum Payload Size for Uploads (TG-RATE-003)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

    # 4. Enable CSRF Protection (TG-CSRF-001)
    csrf.init_app(app)

    return app
```

---

## 🛡️ 2. CSRF Protection for Cookie-Based Flows (`TG-CSRF-001`)

Always enable `Flask-WTF`'s `CSRFProtect` globally for session-cookie authenticated applications.

```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
```

In Jinja templates:
```html
<form method="post">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
    <!-- form fields -->
</form>
```

---

## 👤 3. Route Authorization & Object Ownership (`TG-AUTH-007`)

### ❌ Unsafe Pattern (IDOR)
```python
# VULNERABLE: Any user can access invoice by changing the URL parameter
@app.route("/invoices/<int:invoice_id>")
@login_required
def get_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return render_template("invoice.html", invoice=invoice)
```

### ✅ Safe Pattern
```python
# SAFE: Scope query to authenticated session user
@app.route("/invoices/<int:invoice_id>")
@login_required
def get_invoice(invoice_id):
    invoice = Invoice.query.filter_by(id=invoice_id, user_id=current_user.id).first_or_404()
    return render_template("invoice.html", invoice=invoice)
```

---

## 🎨 4. Jinja2 Template Safety (`TG-INPUT-002`)

* Jinja2 autoescapes variables by default in `.html`, `.xml`, and `.xhtml` templates.
* **Avoid** using the `| safe` filter or `Markup()` on user-supplied input unless it has been explicitly sanitized by an allowlist HTML sanitizer (like `bleach` or `nh3`).

---

## 📂 5. File Upload Safety (`TG-INPUT-004`)

Always sanitize client-supplied filenames using `werkzeug.utils.secure_filename` and validate extensions.

```python
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    file = request.files.get('file')
    if not file or not allowed_file(file.filename):
        abort(400, "Invalid file type")
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return {"status": "uploaded"}
```

---

## 📋 Manual Review Checklist for Flask

- [ ] `app.config['SECRET_KEY']` is loaded from a secure environment variable.
- [ ] `SESSION_COOKIE_SECURE`, `HTTPONLY`, and `SAMESITE` flags are set.
- [ ] `CSRFProtect` is initialized for cookie-authenticated forms and APIs.
- [ ] Database lookups by ID enforce `user_id = current_user.id`.
- [ ] File uploads use `secure_filename()` and enforce size caps (`MAX_CONTENT_LENGTH`).
- [ ] Debug mode is disabled (`app.run(debug=False)`) in production.
