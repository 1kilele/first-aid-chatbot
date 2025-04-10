import logging
import nltk
from flask import Flask, request, jsonify

# Download punkt tokenizer for NLTK if not already downloaded
try:
    nltk.download('punkt')  # Ensure we are downloading 'punkt' and not 'punkt_tab'
except Exception as e:
    logging.error(f"Error downloading 'punkt': {e}")

# Initialize Flask app
app = Flask(__name__)

# Example function to preprocess text
def preprocess_text(text):
    from nltk.tokenize import word_tokenize
    # Tokenize the input text
    tokens = word_tokenize(text.lower())
    return tokens

# Function to generate a response based on user input
def get_response(user_input):
    user_tokens = preprocess_text(user_input)
    # Example: Respond with tokenized input for now
    response = f"Tokens: {user_tokens}"
    return response

@app.route("/send", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message")
        if not user_input:
            return jsonify({"response": "Please send a message."}), 400

        # Get response based on user input
        response = get_response(user_input)
        return jsonify({"response": response})
    
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"response": "Sorry, I'm having trouble responding right now."}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)

