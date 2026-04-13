from flask import Flask, request, send_file
import subprocess, os

app = Flask(__name__)

os.makedirs("uploads", exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return open("index.html","r",encoding="utf-8").read()

@app.route("/convert", methods=["POST"])
def convert():
    try:
        f = request.files["file"]
        path = os.path.join("uploads", f.filename)
        f.save(path)

        r1 = subprocess.run(["lua","lua2rbxmxv2.lua",path], capture_output=True, text=True)
        print("LUA:", r1.stdout, r1.stderr)

        r2 = subprocess.run(["python","rbxm2anim.py","lua2rbxmx.rbxmx"], capture_output=True, text=True)
        print("PY:", r2.stdout, r2.stderr)

        out = None
        for file in os.listdir():
            if file.endswith(".anim"):
                out = file
                break

        if not out:
            return "erro: anim não gerado", 500

        return send_file(out, as_attachment=True)

    except Exception as e:
        return str(e), 500

    return send_file(out, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
