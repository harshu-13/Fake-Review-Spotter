from flask import Flask, render_template, request, send_file
import os
import re
import string
import joblib
import pandas as pd
import plotly.express as px
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)

# ==========================================
# Folder Configuration
# ==========================================

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# ==========================================
# Load Model
# ==========================================

model = joblib.load("trained_model/review_model_v2.pkl")
vectorizer = joblib.load("trained_model/tfidf_vectorizer_v2.pkl")
encoder = joblib.load("trained_model/label_encoder.pkl")

# ==========================================
# NLP Setup
# ==========================================

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# ==========================================
# Text Cleaning
# ==========================================

def clean_text(text):

    text = str(text).lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"<.*?>", "", text)

    text = re.sub(r"\d+", "", text)

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    text = re.sub(r"\s+", " ", text).strip()

    words = text.split()

    words = [
        word
        for word in words
        if word not in stop_words
    ]

    words = [
        lemmatizer.lemmatize(word)
        for word in words
    ]

    return " ".join(words)

# ==========================================
# Home Page
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")

# ==========================================
# Single Review Page
# ==========================================

@app.route("/single-review")
def single_review():
    return render_template("single_review.html")

# ==========================================
# Predict Single Review
# ==========================================

@app.route("/predict_review", methods=["POST"])
def predict_review():

    review = request.form["review"].strip()

    if review == "":
        return render_template(
            "single_review.html",
            error="⚠️ Please enter a review before clicking Analyze."
    )

    clean_review = clean_text(review)

    review_vector = vectorizer.transform([clean_review])

    prediction = model.predict(review_vector)[0]

    prediction = encoder.inverse_transform([prediction])[0]

    print("=" * 50)
    print("Original :", review)
    print("Cleaned  :", clean_review)
    print("Prediction:", prediction)
    print("=" * 50)

    if prediction == "Fake":
        prediction = "❌ Fake Review"
    else:
        prediction = "✅ Genuine Review"

    return render_template(
        "result.html",
        review=review,
        prediction=prediction
    )

# ==========================================
# Upload CSV Page
# ==========================================

@app.route("/upload")
def upload():
    return render_template("upload.html")

# ==========================================
# Upload CSV and Analyze
# ==========================================

@app.route("/upload_file", methods=["POST"])
def upload_file():

    if "review_file" not in request.files:
        return "No file uploaded."

    file = request.files["review_file"]

    if file.filename == "":
        return "Please choose a CSV file."

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    df = pd.read_csv(filepath)

    possible_columns = [
        "review",
        "Review",
        "text",
        "text_",
        "review_text",
        "Review_Text"
    ]

    review_column = None

    for col in possible_columns:
        if col in df.columns:
            review_column = col
            break

    if review_column is None:
        return "No review column found in CSV."

    predictions = []

    for review in df[review_column]:

        clean_review = clean_text(review)

        review_vector = vectorizer.transform([clean_review])

        result = model.predict(review_vector)[0]

        result = encoder.inverse_transform([result])[0]

        print("----------------------------------------")
        print("Original :", review)
        print("Cleaned  :", clean_review)
        print("Prediction:", result)

        if result == "Fake":
            predictions.append("Fake Review")
        else:
            predictions.append("Genuine Review")

    df["Prediction"] = predictions

    # ==========================================
    # Statistics
    # ==========================================

    total_reviews = len(df)

    fake_reviews = predictions.count("Fake Review")

    genuine_reviews = predictions.count("Genuine Review")

    fake_percentage = round(
        (fake_reviews / total_reviews) * 100,
        2
    )

    genuine_percentage = round(
        (genuine_reviews / total_reviews) * 100,
        2
    )

    # ==========================================
    # Pie Chart
    # ==========================================

    fig = px.pie(
        names=["Fake Reviews", "Genuine Reviews"],
        values=[fake_reviews, genuine_reviews],
        title="Review Distribution"
    )

    chart = fig.to_html(full_html=False)

    # ==========================================
    # Save Report
    # ==========================================

    output_file = os.path.join(
        app.config["REPORT_FOLDER"],
        "analysis_results.csv"
    )

    df.to_csv(output_file, index=False)

    # ==========================================
    # Show Result
    # ==========================================

    return render_template(
        "bulk_result.html",
        total_reviews=total_reviews,
        fake_reviews=fake_reviews,
        genuine_reviews=genuine_reviews,
        fake_percentage=fake_percentage,
        genuine_percentage=genuine_percentage,
        chart=chart,
        tables=[
            df.head(10).to_html(
                classes="table table-striped",
                index=False,
                justify="center"
            )
        ]
    )

# ==========================================
# Download Report
# ==========================================

@app.route("/download_report")
def download_report():

    output_file = os.path.join(
        app.config["REPORT_FOLDER"],
        "analysis_results.csv"
    )

    return send_file(
        output_file,
        as_attachment=True,
        download_name="analysis_results.csv"
    )

# ==========================================
# Dashboard
# ==========================================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)