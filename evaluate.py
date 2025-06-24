import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, f1_score, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt
from utils import apply_bert_sentiment

# Load the first 100 rows from the CSV
df = pd.read_csv("YoutubeCommentsDataSet.csv", nrows=100)
df = df.rename(columns=lambda x: x.strip().lower())

# Adjust if your column names are different
df = df[['comment', 'sentiment']]
df.columns = ['text', 'label']

# Normalize labels (handle casing, whitespace, and 'Other')
label_map = {
    "Positive": "positive",
    "Negative": "negative",
    "Neutral": "neutral",
    "Other": "neutral"  # Grouping 'other' as neutral
}
df['label'] = df['label'].map(lambda x: label_map.get(str(x).strip().capitalize(), 'neutral'))

# Apply BERT-based sentiment prediction
df = apply_bert_sentiment(df)

# Print classification report
print("\n📊 Classification Report:")
print(classification_report(df['label'], df['bert_sentiment']))

# Accuracy
accuracy = accuracy_score(df['label'], df['bert_sentiment'])
print(f"\n✅ Accuracy: {accuracy:.4f}")

# F1 scores
macro_f1 = f1_score(df['label'], df['bert_sentiment'], average='macro')
weighted_f1 = f1_score(df['label'], df['bert_sentiment'], average='weighted')
print(f"✅ Macro F1 Score: {macro_f1:.4f}")
print(f"✅ Weighted F1 Score: {weighted_f1:.4f}")

# Confusion matrix
labels = ["positive", "neutral", "negative"]
cm = confusion_matrix(df['label'], df['bert_sentiment'], labels=labels)

# Plot confusion matrix
sns.heatmap(cm, annot=True, fmt='d', cmap="Blues", xticklabels=labels, yticklabels=labels)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()
