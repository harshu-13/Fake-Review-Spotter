import os
import joblib

# ==========================================
# Load the trained model
# ==========================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "trained_model")

model = joblib.load(os.path.join(MODEL_DIR, "review_model_v2.pkl"))
vectorizer = joblib.load(os.path.join(MODEL_DIR, "tfidf_vectorizer_v2.pkl"))
encoder = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))


# ==========================================
# Predict Review
# ==========================================

def predict_review(review_text):
    """
    Predict whether a review is Fake or Genuine.
    """

    # Convert review into TF-IDF features
    review_vector = vectorizer.transform([review_text])

    # Predict
    prediction = model.predict(review_vector)[0]

    # Convert numeric label back to text
    label = encoder.inverse_transform([prediction])[0]

    # Approximate confidence using decision score
    decision_score = abs(model.decision_function(review_vector)[0])

    confidence = min(99, round(60 + decision_score * 10))

    return {
        "review": review_text,
        "prediction": label,
        "confidence": confidence
    }