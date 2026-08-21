# Regression Fixture: CSRF Defense Enabled in Flask

- **Framework:** Flask / Flask-WTF
- **Target Rule:** `TG-CSRF-001`
- **Expected Classification:** Safe (No findings)
- **Expected Rule IDs:** None / Safe
- **Reasoning:** Application instantiates `CSRFProtect(app)` globally, protecting all state-changing POST/PUT/DELETE requests.

## Sample Code
```python
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some-secret'
csrf = CSRFProtect(app)
```
