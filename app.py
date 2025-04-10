import json
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

# Flask setup
app = Flask(__name__, template_folder='templates')
CORS(app)

# Download the punkt data for NLTK (only if not already available)
nltk.download('punkt')

# Load intents
with open("intents.json", "r", encoding="utf-8") as file:
    intents = json.load(file)

stemmer = PorterStemmer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stemmed = [stemmer.stem(word) for word in tokens]
    return stemmed

def get_response(user_input):
    user_tokens = preprocess_text(user_input)
    best_match = None
    best_score = 0.0

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            pattern_tokens = preprocess_text(pattern)
            common = set(user_tokens).intersection(pattern_tokens)
            score = len(common) / len(pattern_tokens)

            if score > best_score:
                best_score = score
                best_match = intent

    if best_match and best_score >= 0.3:
        return random.choice(best_match["responses"])
    
    return "I'm not sure how to respond to that. Can you rephrase?"

# Route to serve the HTML page
@app.route("/")
def home():
    return render_template("index.html")

# Endpoint to receive chat messages
@app.route("/send", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Invalid request"}), 400
    
    user_input = data["message"]
    response = get_response(user_input)
    return jsonify({"response": response})

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

