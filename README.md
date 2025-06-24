# 🎯 YTSense: YouTube Comment Sentiment Analyzer

**YTSense** is an interactive web application that analyzes the sentiment of YouTube video comments in real-time using BERT-based NLP models. Just enter a video URL, and Sentiview will fetch comments, detect language, and classify sentiment (Positive, Negative, Neutral) — all in a clean Streamlit dashboard.

---

## 🚀 Features

- 🔍 **Real-time comment extraction** from any YouTube video
- 🌍 **Language detection** for multilingual comments
- 🤖 **Sentiment classification** using fine-tuned BERT
- 📈 **Performance metrics**: Accuracy, F1-Score, Confusion Matrix
- 🧠 Evaluation on 18,000+ labeled YouTube comments

---

## 🧪 Sample Evaluation Results

Tested on the [YouTubeCommentsDataSet.csv](https://huggingface.co/datasets/) (100 sample rows):

📊 Classification Report:
precision recall f1-score support

nginx
Copy
Edit
negative       1.00      0.93      0.97        15
 neutral       0.74      0.92      0.82        25
positive       0.96      0.88      0.92        60

accuracy                           0.90       100
macro avg 0.90 0.91 0.90 100
weighted avg 0.91 0.90 0.90 100

✅ Accuracy: 90.00%
✅ Macro F1 Score: 0.9029
✅ Weighted F1 Score: 0.9032

yaml
Copy
Edit

---

## 📦 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, HuggingFace Transformers, pandas
- **Model**: `cardiffnlp/twitter-roberta-base-sentiment`
- **APIs**: YouTube Data API v3
- **NLP Tools**: `langdetect`, `transformers`, `nltk`

---

## 🔧 How It Works

1. Enter YouTube video URL into the app
2. Fetch top N comments using YouTube Data API
3. Detect comment language (skip if not supported)
4. Run BERT sentiment analysis on filtered comments
5. Display summary metrics and most positive/negative samples

---

## 🛠️ Installation

```bash
git clone https://github.com/your-username/sentiview.git
cd sentiview
pip install -r requirements.txt
Add your YouTube API Key in config.py:

python
Copy
Edit
API_KEY = "YOUR_YOUTUBE_API_KEY"
▶️ Run the App
bash
Copy
Edit
streamlit run app.py
📁 Project Structure
bash
Copy
Edit
├── app.py                  # Streamlit dashboard
├── fetch_comments.py       # YouTube comment fetcher
├── detect_language.py      # Language detection logic
├── utils.py                # Helper functions incl. BERT sentiment
├── evaluate.py             # Performance testing script
├── YoutubeCommentsDataSet.csv # Optional sample dataset
├── requirements.txt
└── README.md
