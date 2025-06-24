# streamlit_app.py
import os
os.environ["STREAMLIT_WATCHER_IGNORE"] = "none"

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import extract_video_id, get_comments, apply_bert_sentiment

# Streamlit setup
st.set_page_config(page_title="YouTube Sentiment Analyzer", layout="wide")
st.title("🎬 YouTube Comment Sentiment Analyzer (BERT-powered)")
st.markdown("Paste any YouTube video URL below to see a real-time sentiment breakdown using BERT.")

# Input
video_url = st.text_input("🔗 YouTube Video URL")

# Main workflow
if video_url:
    video_id = extract_video_id(video_url)

    if video_id:
        try:
            with st.spinner("🔍 Fetching comments..."):
                df = get_comments(video_id)

            if df.empty:
                st.warning("⚠️ No comments found for this video.")
            else:
                st.success(f"✅ {len(df)} comments fetched successfully!")

                with st.spinner("💡 Analyzing sentiment with BERT..."):
                    df = apply_bert_sentiment(df)

                # Show sample
                st.subheader("🧪 Sample Comments with Sentiment")
                st.dataframe(df[['text', 'bert_sentiment']].head(15))

                # Distribution chart
                st.subheader("📊 Sentiment Distribution")
                sentiment_counts = df['bert_sentiment'].value_counts()
                fig, ax = plt.subplots()
                sentiment_counts.plot(kind='bar', color=['green', 'gray', 'red'], ax=ax)
                plt.title("Sentiment Overview")
                st.pyplot(fig)

                # Top Positive & Negative Comments
                st.subheader("👍 Most Positive Comments")
                st.write(df[df['bert_sentiment'] == 'positive'][['text']].head(5))

                st.subheader("👎 Most Negative Comments")
                st.write(df[df['bert_sentiment'] == 'negative'][['text']].head(5))
        except Exception as e:
            st.error(f"🚫 Error: {str(e)}")
    else:
        st.error("❗ Could not extract video ID. Please check the URL format.")
