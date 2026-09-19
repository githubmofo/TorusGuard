---
id: TG-INPUT-005
title: Unsafe Template Rendering & Disabled Autoescaping
category: input-validation-encoding
severity: High
confidence: Confirmed
frameworks:
  - django
  - flask
  - fastapi
cwe: CWE-79
asvs_v4: V5.3.3
nist_ssdf: PW.5.1
---

# TG-INPUT-005: Unsafe Template Rendering & Disabled Autoescaping

## 🚨 Problem Statement
Rendering user-controlled input directly into templates without context-aware escaping (e.g., using `render_template_string` or explicitly disabling escaping with `|safe` or `mark_safe`) allows attackers to inject malicious HTML, JavaScript, or server-side template directives.

> **Tuning Guardrails (v0.5.6):**
> - **DISTINGUISH** direct unsafe rendering from framework-managed autoescaped template rendering (e.g., passing context variables to `render_template("foo.html", var=x)`).
> - **DO NOT flag** safe templating utilities or correctly escaped output paths.
> - **FLAG ONLY** when unsafe rendering, disabled escaping, `mark_safe`, `|safe`, or dynamic template execution is materially relevant.

---

## 💥 Adversarial Threat & Exploitation
1. **Server-Side Template Injection (Flask / Jinja2):**
   ```python
   # Unsafe Flask SSTI
   @app.route("/greet")
   def greet():
       name = request.args.get("name")
       template = f"<h1>Hello {name}</h1>"
       return render_template_string(template)  # RCE via {{ 7*7 }} or {{ config.__class__... }}
   ```
2. **Cross-Site Scripting (Django / Jinja2):**
   ```python
   # Unsafe Django mark_safe
   from django.utils.safestring import mark_safe

   def comment_view(request):
       user_comment = request.POST.get("comment")
       # Bypasses HTML escaping
       html_output = mark_safe(f"<div class='comment'>{user_comment}</div>")
       return HttpResponse(html_output)
   ```

---

## 🛠️ Framework-Native Remediations

### 🐍 Flask / Jinja2 (Safe Parameter Passing)

#### ❌ Unsafe Pattern
```python
# Unsafe: Concatenating input into template string
return render_template_string(f"Hello {user_input}")
```

#### ✅ Safe Remediation
```python
# Safe: Pass input as context variable to autoescaped template file
from flask import render_template

@app.route("/greet")
def greet():
    name = request.args.get("name", "")
    return render_template("greet.html", name=name)  # Automatically HTML-escaped by Jinja2
```

---

### 🐍 Django (Template Context & `format_html`)

#### ❌ Unsafe Pattern
```python
# Unsafe: mark_safe on unescaped input string
return HttpResponse(mark_safe(f"<b>Welcome, {username}</b>"))
```

#### ✅ Safe Remediation
```python
# Safe: Use format_html for conditional safe markup with autoescaped arguments
from django.utils.html import format_html

def welcome_view(request):
    username = request.GET.get("username", "")
    # format_html escapes variables while preserving the fixed HTML wrapper
    safe_markup = format_html("<b>Welcome, {}</b>", username)
    return HttpResponse(safe_markup)
```

---

## 🧪 Verification & Reproduction
1. Submit XSS payload:
   ```bash
   curl "http://localhost:5000/greet?name=%3Cscript%3Ealert(1)%3C/script%3E"
   ```
2. **Assertion:** Response body must contain HTML entity encoded characters (`&lt;script&gt;alert(1)&lt;/script&gt;`) and must NOT execute raw tags.
