# 🤖 Fake Review Spotter

An AI-powered web application that detects whether customer reviews are **Fake** or **Genuine** using **Natural Language Processing (NLP)** and **Machine Learning**.

---

## 📌 Project Overview

Fake online reviews can mislead customers and influence purchasing decisions. This project aims to automatically classify customer reviews as **Fake** or **Genuine** using Natural Language Processing (NLP) and Machine Learning techniques.

## ✨ Features

- 🔍 Detect whether a customer review is Fake or Genuine
- 📂 Upload a CSV file for bulk review analysis
- 📊 Interactive dashboard displaying review statistics
- 📈 Pie chart visualization using Plotly
- 📥 Download prediction results as a CSV report
- 🧹 Text preprocessing using NLP techniques
- 🤖 Machine Learning-based review classification using Linear SVM
- 🎨 Responsive web interface built with Flask

## 🛠 Tech Stack

### Programming Language
- Python

### Machine Learning
- Scikit-learn
- Linear SVM
- TF-IDF Vectorizer

### Natural Language Processing
- NLTK
- Stopword Removal
- Lemmatization

### Backend
- Flask

### Frontend
- HTML
- CSS

### Data Processing
- Pandas
- NumPy

### Visualization
- Plotly

### Model Storage
- Joblib

## 📂 Dataset

The machine learning model was trained using two publicly available datasets:

- **Amazon Fake Review Dataset** – Contains customer reviews collected from Amazon products.
- **Deceptive Opinion Spam Dataset** – Contains truthful and deceptive hotel reviews for research purposes.

Both datasets were merged, cleaned, and preprocessed before training the model.

## ⚙️ Machine Learning Workflow

1. Load the datasets
2. Merge the datasets
3. Clean the review text
4. Remove stopwords
5. Perform lemmatization
6. Convert text into TF-IDF vectors
7. Split the data into training and testing sets
8. Train the Linear SVM classifier
9. Evaluate model performance
10. Save the trained model using Joblib
11. Deploy the model using Flask

## 📈 Model Performance

| Metric | Value |
|---------|-------|
| Machine Learning Algorithm | Linear Support Vector Machine (Linear SVM) |
| Feature Extraction | TF-IDF Vectorizer |
| Accuracy | ~90% |
| NLP Library | NLTK |

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/fake-review-spotter.git
```

### 2. Navigate to the project

```bash
cd fake-review-spotter
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask application

```bash
python app.py
```

### 5. Open your browser

```
http://127.0.0.1:5000
```

## 🔮 Future Enhancements

- Improve the model using transformer-based architectures such as BERT.
- Add user authentication and login functionality.
- Store prediction history in a database.
- Develop REST APIs for external integration.
- Provide explainable AI by highlighting suspicious words.
- Deploy using Docker and cloud platforms.


## 👩‍💻 Author

**Harsha Vardhini Selva Ganesh**

Computer Science Engineering Student

GitHub: *(Add your GitHub profile link after creating your repository.)*