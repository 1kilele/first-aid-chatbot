import spacy

# Load spaCy's small English model
nlp = spacy.load("en_core_web_sm")

def determine_intent(message):
    """
    Determines the intent of a message using spaCy.
    Returns:
      - 'greeting' if message is a greeting,
      - 'farewell' if message is a farewell,
      - 'question' if the message is a question,
      - 'unknown' otherwise.
    """
    doc = nlp(message.lower())
    for token in doc:
        if token.lemma_ in ["hello", "hi", "hey"]:
            return "greeting"
        if token.lemma_ in ["bye", "goodbye"]:
            return "farewell"
    if "?" in message:
        return "question"
    return "unknown"
