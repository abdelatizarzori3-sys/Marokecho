import os

from flask import Flask, jsonify, request, send_from_directory

from components import check_api_key, process_message

# Serve frontend files
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_BASE_DIR)


app = Flask(__name__, static_folder=_PARENT_DIR, static_url_path="")


@app.route("/")
def index():
    return send_from_directory(_PARENT_DIR, "index.html")


@app.route("/api/status")
def status():
    ok, msg = check_api_key()
    return jsonify(
        {
            "status": "online" if ok else "offline",
            "gemini": "connected" if ok else "disconnected",
            "message": msg,
            "version": "4.0",
        }
    )


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    msg = data.get("message", "")
    if not msg:
        return jsonify({"reply": "Empty message"}), 400
    reply = process_message(msg)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
