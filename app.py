import os
import nltk
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from nltk.tokenize import word_tokenize

# Ensure that the necessary NLTK data is available (punkt)
nltk.download('punkt')

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

@app.route("/")
def home():
    return render_template("index.html")  # This will render the HTML page

@app.route("/send", methods=["POST"])
def chat():
    try:
        # Extract the message from the POST request
        user_input = request.json.get("message")
        
        if not user_input:
            return jsonify({"response": "Please provide a valid message."}), 400
        
        # Get the response based on the user input
        response = get_response(user_input)
        
        # Send back the response
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"response": f"Sorry, I'm having trouble responding right now. Error: {str(e)}"}), 500

def preprocess_text(text):
    # Tokenize the text to process it
    tokens = word_tokenize(text.lower())  # Converting text to lowercase
    return tokens

def get_response(user_input):
    # Tokenize the input text
    user_tokens = preprocess_text(user_input)

    # Basic response logic based on keywords in the user input
    if "cut" in user_tokens:
        return "To treat a cut, clean the wound with water, apply pressure to stop bleeding, and cover it with a clean bandage."
    elif "burn" in user_tokens:
        return "For burns, cool the area with cold water for at least 10 minutes and cover with a sterile bandage."
    else:
        return "Sorry, I didn't understand that. Can you give me more details?"

if __name__ == "__main__":
    # Running the Flask app
    app.run(host="0.0.0.0", port=8080, debug=True)

