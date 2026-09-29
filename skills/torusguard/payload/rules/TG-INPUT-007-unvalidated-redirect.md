---
id: TG-INPUT-007
title: Unvalidated URL Redirection (Open Redirect)
category: input-validation
severity: Medium
confidence: High
frameworks:
  - django
  - flask
  - fastapi
  - express
  - nextjs
cwe: CWE-601
asvs_v4: V5.1.5
nist_ssdf: PW.5.1
---

# TG-INPUT-007: Unvalidated URL Redirection (Open Redirect)

## 🚨 Problem Statement
Passing unvalidated or untrusted user input directly into HTTP redirect responses (`redirect()`, `res.redirect()`, `header('Location: ...')`) enables Open Redirect vulnerabilities. Attackers use trusted domains to trick users into phishing sites or OAuth credential harvesting portals.

---

## 💥 Adversarial Threat & Exploitation
An attacker generates a legitimate-looking link:
```http
GET /login?next=https://evil-phishing.com/account HTTP/1.1
Host: secure-bank.com
```
If the server performs `return redirect(request.GET.get('next'))`, the user is seamlessly forwarded to the malicious domain after authentication.

---

## 🛠️ Framework-Native Remediations

### 🐍 Django / Flask
#### ❌ Unsafe Pattern
```python
return redirect(request.GET.get("next"))
```

#### ✅ Safe Remediation
```python
from urllib.parse import urlparse, urljoin
from django.utils.http import url_has_allowed_host_and_scheme

def safe_redirect(request):
    next_url = request.GET.get("next", "/")
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("/")
```
