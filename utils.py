# utils.py

import re
import time
import pandas as pd
from config import API_KEY, MAX_COMMENTS
from googleapiclient.discovery import build
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from functools import lru_cache

@lru_cache(maxsize=1)
def load_bert_pipeline():
    model_name = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Extract video ID from YouTube URL
def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

# Fetch comments using YouTube Data API
def get_comments(video_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    comments = []
    next_page_token = None

    try:
        while len(comments) < MAX_COMMENTS:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=100,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'text': comment['textDisplay'],
                    'author': comment['authorDisplayName'],
                    'published': comment['publishedAt']
                })

                if len(comments) >= MAX_COMMENTS:
                    break

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

            time.sleep(1)
    except Exception as e:
        raise RuntimeError(f"API error: {e}")

    return pd.DataFrame(comments)

# Load BERT pipeline (Hugging Face)
def load_bert_pipeline():
    model_name = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Apply BERT sentiment to DataFrame
def apply_bert_sentiment(df, text_column='text'):
    bert = load_bert_pipeline()
    label_map = {"LABEL_0": "negative", "LABEL_1": "neutral", "LABEL_2": "positive"}

    def safe_predict(x):
        if pd.isna(x) or not isinstance(x, str) or x.strip() == "":
            return "neutral"  # fallback label
        try:
            return label_map[bert(x[:512])[0]['label']]
        except:
            return "neutral"

    df['bert_sentiment'] = df[text_column].apply(safe_predict)
    return df


