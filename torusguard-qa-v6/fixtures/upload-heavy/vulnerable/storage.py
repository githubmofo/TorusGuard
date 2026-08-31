import os

UPLOAD_DIR = "/data/files"

def save_user_file(file_obj, raw_filename):
    dest = os.path.join(UPLOAD_DIR, raw_filename)
    with open(dest, "wb") as out:
        out.write(file_obj.read())
    return dest
