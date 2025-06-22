import pandas as pd
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Optional: for consistent results
DetectorFactory.seed = 0

df = pd.read_csv("youtube_comments.csv")

def safe_detect(text):
    try:
        text = str(text).strip()
        if len(text) < 5:
            return "undetected"
        return detect(text)
    except LangDetectException:
        return "undetected"

df['language'] = df['text'].apply(safe_detect)
df.to_csv("youtube_comments_lang.csv", index=False)
print("✅ Language detection complete.")
