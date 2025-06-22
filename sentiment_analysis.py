import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')
df = pd.read_csv("youtube_comments_lang.csv")

vader = SentimentIntensityAnalyzer()
df['vader_score'] = df['text'].apply(lambda x: vader.polarity_scores(str(x))['compound'])
df['vader_sentiment'] = df['vader_score'].apply(
    lambda x: 'positive' if x >= 0.05 else 'negative' if x <= -0.05 else 'neutral'
)

df.to_csv("youtube_comments_with_sentiment.csv", index=False)
print("Sentiment analysis completed.")
