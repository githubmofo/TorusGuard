from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route("/greet")
def greet():
    name = request.args.get("name", "Guest")
    return render_template("greet.html", name=name)

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    safe_name = secure_filename(f.filename)
    f.save(os.path.join("/var/uploads", safe_name))
    return "Saved"
