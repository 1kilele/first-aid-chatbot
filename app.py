import json
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

# Download required NLTK data
nltk.download("punkt")

# Flask setup
app = Flask(__name__, template_folder='templates')
CORS(app)

# Load intents file
with open("intents.json", "r", encoding="utf-8") as file:
    intents = json.load(file)

stemmer = PorterStemmer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    return [stemmer.stem(word) for word in tokens]

def get_response(user_input):
    user_tokens = preprocess_text(user_input)
    best_match = None
    best_score = 0

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

# Route for the main page
@app.route("/")
def home():
    return render_template("index.html")

# Route to handle chat POST requests
@app.route("/send", methods=["POST"])
def send():
    try:
        data = request.get_json(force=True)
        message = data.get("message", "")
        if not message:
            return jsonify({"response": "Please type something!"})
        
        reply = get_response(message)
        return jsonify({"response": reply})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Sorry, I'm having trouble responding right now."}), 500

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

