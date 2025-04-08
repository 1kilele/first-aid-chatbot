import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

# Load the saved model
model = tf.keras.models.load_model("imdb_model.h5")

# Prepare text for prediction
def preprocess_text(text, max_features=10000, maxlen=200):
    word_index = imdb.get_word_index()
    words = text.lower().split()
    sequences = [word_index.get(word, 2) for word in words]  # 2 is the index for "unknown"
    return pad_sequences([sequences], maxlen=maxlen)

# Predict sentiment
def predict_sentiment(text):
    processed_text = preprocess_text(text)
    prediction = model.predict(processed_text)[0][0]
    sentiment = "Positive" if prediction > 0.5 else "Negative"
    print(f"Sentiment: {sentiment} (Confidence: {prediction:.2f})")

# Example
if __name__ == "__main__":
    text_input = "This movie was amazing! I loved it."
    predict_sentiment(text_input)
s