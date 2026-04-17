from flask import Flask, request, jsonify
from emotion_detection import emotion_detector
import pylint.lint

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Emotion detector is running. Use POST /emotionDetector with JSON body: {'text': 'your text'}"
    })

@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detect():
    if request.method == "GET":
        return "Method not allowed for direct browser call. Use POST with form data: text=your sentence."

    text = request.form["text"]

    if not text.strip():
        return "Invalid input! Please enter some text."

    result = emotion_detector(text)
    
    if result["dominant_emotion"] is None:
        return "Invalid input! Please try again."

    return result

if __name__ == "__main__":
    app.run(debug=True)

# Static code analysis
def run_pylint():
    pylint.lint.Run(["server.py"])