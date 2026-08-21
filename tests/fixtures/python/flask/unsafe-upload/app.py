import os

def save_uploaded_file(upload_dir, file_obj):
    # VULNERABLE: Direct filename access without secure_filename()
    destination = os.path.join(upload_dir, file_obj.filename)
    return destination
