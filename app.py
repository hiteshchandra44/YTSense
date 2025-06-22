# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from langdetect import detect, DetectorFactory
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

from utils import extract_video_id, get_comments

DetectorFactory.seed = 0
nltk.download("vader_lexicon")

# Page layout
st.set_page_config(page_title="YouTube Sentiment Analyzer", layout="wide")
st.title("🎬 YouTube Comment Sentiment Analyzer")
st.markdown("Enter a YouTube video URL to fetch and analyze viewer sentiment.")

# Input
video_url = st.text_input("🔗 Paste YouTube video URL")

def detect_language(text):
    try:
        text = str(text).strip()
        if len(text) < 5:
            return "undetected"
        return detect(text)
    except:
        return "undetected"

def analyze_sentiment(df):
    sia = SentimentIntensityAnalyzer()
    df['language'] = df['text'].apply(detect_language)
    df['score'] = df['text'].apply(lambda x: sia.polarity_scores(str(x))['compound'])
    df['sentiment'] = df['score'].apply(
        lambda x: 'positive' if x >= 0.05 else 'negative' if x <= -0.05 else 'neutral'
    )
    return df

if video_url:
    video_id = extract_video_id(video_url)
    if video_id:
        try:
            with st.spinner("Fetching comments..."):
                df = get_comments(video_id)
                if df.empty:
                    st.warning("No comments found.")
                else:
                    df = analyze_sentiment(df)

                    st.success(f"{len(df)} comments analyzed.")
                    st.subheader("📋 Sample Comments")
                    st.dataframe(df[['text', 'language', 'sentiment', 'score']].head(15))

                    st.subheader("📊 Sentiment Breakdown")
                    sentiment_counts = df['sentiment'].value_counts()
                    fig, ax = plt.subplots()
                    sentiment_counts.plot(kind='bar', color=['green', 'gray', 'red'], ax=ax)
                    st.pyplot(fig)

                    st.subheader("✅ Most Positive Comments")
                    st.table(df.sort_values('score', ascending=False).head(5)[['text', 'score']])

                    st.subheader("❌ Most Negative Comments")
                    st.table(df.sort_values('score').head(5)[['text', 'score']])
        except Exception as e:
            st.error(str(e))
    else:
        st.error("Invalid YouTube URL.")
