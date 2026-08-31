import os
from pathlib import Path
from werkzeug.utils import secure_filename

UPLOAD_DIR = Path("/data/files").resolve()

def save_user_file(file_obj, raw_filename):
    safe_name = secure_filename(raw_filename)
    dest = (UPLOAD_DIR / safe_name).resolve()
    if not str(dest).startswith(str(UPLOAD_DIR)):
        raise ValueError("Path traversal attempt detected")
    with open(dest, "wb") as out:
        out.write(file_obj.read())
    return str(dest)
