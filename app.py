 
import json
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Flask setup
app = Flask(__name__, template_folder='templates')
CORS(app)

# Download the punkt data for NLTK (only if not already available)
try:
    nltk.download('punkt')
except Exception as e:
    logging.error(f"Error downloading 'punkt': {e}")

# Load intents
try:
    with open("intents.json", "r", encoding="utf-8") as file:
        intents = json.load(file)
except Exception as e:
    logging.error(f"Error loading intents: {e}")
    intents = {}

stemmer = PorterStemmer()

def preprocess_text(text):
    try:
        tokens = word_tokenize(text.lower())
        stemmed = [stemmer.stem(word) for word in tokens]
        return stemmed
    except Exception as e:
        logging.error(f"Error preprocessing text: {e}")
        return []

def get_response(user_input):
    try:
        user_tokens = preprocess_text(user_input)
        best_match = None
        best_score = 0.0

        for intent in intents.get("intents", []):
            for pattern in intent.get("patterns", []):
                pattern_tokens = preprocess_text(pattern)
                common = set(user_tokens).intersection(pattern_tokens)
                score = len(common) / len(pattern_tokens)

                if score > best_score:
                    best_score = score
                    best_match = intent

        if best_match and best_score >= 0.3:
            return random.choice(best_match["responses"])

        return "I'm not sure how to respond to that. Can you rephrase?"
    except Exception as e:
        logging.error(f"Error getting response: {e}")
        return "Sorry, I encountered an error while processing your message."

# Route to serve the HTML page
@app.route("/")
def home():
    return render_template("index.html")

# Endpoint to receive chat messages
@app.route("/send", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Invalid request"}), 400

        user_input = data["message"]
        response = get_response(user_input)
        return jsonify({"response": response})
    except Exception as e:
        logging.error(f"Error in /send endpoint: {e}")
        return jsonify({"response": "Sorry, I'm having trouble responding right now."})

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)