import json
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from flask import Flask, request, jsonify
from flask_cors import CORS

# Use local NLTK data
nltk.data.path.append(r"C:\Users\oukoa\AppData\Roaming\nltk_data")

# Ensure necessary NLTK data is available
nltk.download("punkt")

app = Flask(__name__)
CORS(app)

# Load intents.json
with open("intents.json", "r", encoding="utf-8") as file:
    intents = json.load(file)

stemmer = PorterStemmer()

def preprocess_text(text):
    """Tokenize and stem input text to improve response matching."""
    tokens = word_tokenize(text.lower())
    stemmed_tokens = [stemmer.stem(word) for word in tokens]
    return stemmed_tokens

def get_response(user_input):
    """Finds the best response based on word similarity."""
    user_tokens = preprocess_text(user_input)

    best_match = None
    best_score = 0.0

    print("\nDEBUGGING INPUT:", user_input)
    print("User Tokens:", user_tokens)

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            pattern_tokens = preprocess_text(pattern)
            common_words = set(user_tokens).intersection(pattern_tokens)
            match_score = len(common_words) / len(pattern_tokens)

            print(f"Checking: {pattern}")
            print(f"Pattern Tokens: {pattern_tokens}")
            print(f"Match Score: {match_score}\n")

            if match_score > best_score:
                best_score = match_score
                best_match = intent

    if best_match and best_score >= 0.3:
        return random.choice(best_match["responses"])

    return "I'm not sure how to respond to that. Can you rephrase?"

@app.route("/")
def home():
    return "First Aid Chatbot is running! Use the /send endpoint to chat."

@app.route("/send", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Invalid request, please send a message field"}), 400

    user_input = data.get("message", "")
    response = get_response(user_input)

    return jsonify({"response": response})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

