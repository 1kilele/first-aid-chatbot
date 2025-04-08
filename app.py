
import json
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

# Setup
nltk.download("punkt")
stemmer = PorterStemmer()

# Load intents
with open("intents.json", "r", encoding="utf-8") as file:
    intents = json.load(file)

# Flask app
app = Flask(__name__)
CORS(app)

# Preprocess function
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stemmed = [stemmer.stem(word) for word in tokens]
    return stemmed

# Response function
def get_response(user_input):
    user_tokens = preprocess_text(user_input)
    best_match = None
    best_score = 0.0

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            pattern_tokens = preprocess_text(pattern)
            common_words = set(user_tokens).intersection(pattern_tokens)
            score = len(common_words) / len(pattern_tokens)

            if score > best_score:
                best_score = score
                best_match = intent

    if best_match and best_score >= 0.3:
        return random.choice(best_match["responses"])

    return "I'm not sure how to respond to that. Can you rephrase?"

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Chat endpoint
@app.route("/send", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Invalid request"}), 400
        response = get_response(data["message"])
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
