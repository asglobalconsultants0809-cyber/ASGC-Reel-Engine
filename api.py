from flask import Flask, jsonify, send_file
import subprocess
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ASGC Reel Engine API Running"})

@app.route("/render", methods=["POST"])
def render():

    try:
        result = subprocess.run(
            ["python", "main.py"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return jsonify({
                "success": False,
                "stdout": result.stdout,
                "stderr": result.stderr
            }), 500

        video_path = os.path.join(BASE_DIR, "output", "final_reel.mp4")

        return send_file(
            video_path,
            mimetype="video/mp4",
            as_attachment=False,
            download_name="final_reel.mp4"
        )

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)