# Regression Fixture: Unsafe File Upload in Flask

- **Framework:** Flask / Werkzeug
- **Target Rule:** `TG-INPUT-004`
- **Expected Classification:** `Confirmed`
- **Expected Rule IDs:** `TG-INPUT-004`
- **Reasoning:** File upload handler concatenates unvalidated client `file.filename` into server filesystem path, risking path traversal (`../../etc/passwd`).

## Sample Code
```python
import os
from flask import Flask, request

app = Flask(__name__)
UPLOAD_DIR = "/var/uploads"

@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files['file']
    # VULNERABLE: Raw filename concatenation without secure_filename()
    f.save(os.path.join(UPLOAD_DIR, f.filename))
    return "Saved"
```
