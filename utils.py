# utils.py

import re
from googleapiclient.discovery import build
import time
import pandas as pd
from config import API_KEY, MAX_COMMENTS

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

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
