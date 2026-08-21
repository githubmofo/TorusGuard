import os
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# ❌ TG-SEC-001: Hardcoded secret key
app.config['SECRET_KEY'] = 'hardcoded_insecure_development_key'

# ❌ TG-AUTH-007: IDOR in document view
@app.route('/documents/<int:doc_id>')
def get_document(doc_id):
    # Simulated DB lookup without user verification
    return jsonify({"doc_id": doc_id, "title": "Confidential Report", "owner_id": 99})

# ❌ TG-INPUT-004: Unsafe file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    # Saves raw filename directly to disk
    file.save(os.path.join('/tmp/uploads', file.filename))
    return jsonify({"status": "saved"})
