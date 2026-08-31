from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

@app.route("/greet")
def greet():
    name = request.args.get("name", "Guest")
    # SSTI: Unescaped string formatting in template
    return render_template_string(f"Hello {name}")

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    # Path Traversal in filename
    f.save(os.path.join("/var/uploads", f.filename))
    return "Saved"
