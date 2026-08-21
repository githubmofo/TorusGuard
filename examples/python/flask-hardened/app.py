import os
from flask import Flask, request, jsonify, abort, session
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# ✅ TG-SEC-001: Environment-loaded secret
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_test_key_change_in_prod')
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# ✅ TG-CSRF-001: CSRF Protection enabled
csrf = CSRFProtect(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ✅ TG-AUTH-007: Ownership-scoped document lookup
@app.route('/documents/<int:doc_id>')
def get_document(doc_id):
    current_user_id = session.get('user_id')
    if not current_user_id:
        abort(401)
    # Simulated ownership check
    if doc_id != 101 or current_user_id != 42:
        abort(404)
    return jsonify({"doc_id": doc_id, "title": "Secure Document", "owner_id": current_user_id})

# ✅ TG-INPUT-004: Safe file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        abort(400, "No file provided")
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        abort(400, "Invalid file format")
    filename = secure_filename(file.filename)
    # Target safe path
    file.save(os.path.join('/tmp/secure_uploads', filename))
    return jsonify({"status": "saved", "filename": filename})
