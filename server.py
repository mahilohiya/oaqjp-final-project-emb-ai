from flask import Flask, request, jsonify
from emotion_detection import emotion_detector
import pylint.lint

app = Flask(__name__)

@app.route("/emotionDetector", methods=["POST"])
def detect_emotion():
    data = request.get_json()
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "Invalid input! Text cannot be empty."}), 400

    result = emotion_detector(text)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

# Static code analysis
def run_pylint():
    pylint.lint.Run(["server.py"])