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
        f = request.files.get("file")
        if not f:
            return "sem arquivo", 400

        path = os.path.join("uploads", f.filename)
        f.save(path)

        print("arquivo salvo:", path)

        r1 = subprocess.run(["lua5.3","lua2rbxmxv2.lua",path], capture_output=True, text=True)
        print("lua stdout:", r1.stdout)
        print("lua stderr:", r1.stderr)

        rbxmx = None
        for file in os.listdir():
            if file.endswith(".rbxmx"):
                rbxmx = file
                break

        print("rbxmx:", rbxmx)

        if not rbxmx:
            return "rbxmx não gerado", 500

        r2 = subprocess.run(["python","rbxm2anim.py",rbxmx], capture_output=True, text=True)
        print("py stdout:", r2.stdout)
        print("py stderr:", r2.stderr)

        anim = None
        for file in os.listdir():
            if file.endswith(".anim"):
                anim = file
                break

        print("anim:", anim)

        if not anim:
            return "anim não gerado", 500

        return send_file(anim, as_attachment=True)

    except Exception as e:
        print("ERRO:", e)
        return str(e), 500

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
