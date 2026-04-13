from flask import Flask, request, send_file
import subprocess, os

app = Flask(__name__)

os.makedirs("uploads", exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return open("index.html","r",encoding="utf-8").read()

@app.route("/convert", methods=["POST"])
def convert():
    f = request.files["file"]
    path = os.path.join("uploads", f.filename)
    f.save(path)

    subprocess.run(["lua","lua2rbxmxv2.lua",path])
    subprocess.run(["python","rbxm2anim.py","lua2rbxmx.rbxmx"])

    out = None
    for file in os.listdir():
        if file.endswith(".anim"):
            out = file
            break

    if not out:
        return "error", 500

    return send_file(out, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
