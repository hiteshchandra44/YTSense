import time
import pandas as pd
from googleapiclient.discovery import build
from config import API_KEY, TOPIC, REGIONS, MAX_COMMENTS
from fetch_videos import search_videos

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_comments(video_id, max_comments=100):
    comments = []
    next_page_token = None
    try:
        while len(comments) < max_comments:
            res = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                textFormat='plainText',
                maxResults=100,
                pageToken=next_page_token
            ).execute()

            for item in res['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'video_id': video_id,
                    'text': comment['textDisplay'],
                    'author': comment['authorDisplayName'],
                    'published': comment['publishedAt']
                })
                if len(comments) >= max_comments:
                    break

            next_page_token = res.get('nextPageToken')
            if not next_page_token:
                break
            time.sleep(1)
    except Exception as e:
        print(f"⚠️ Skipping video {video_id} — Error: {e}")
    return comments


if __name__ == "__main__":
    all_comments = []
    for region in REGIONS:
        video_ids = search_videos(TOPIC, region)
        for vid in video_ids:
            print(f"Fetching comments for {vid} in {region}")
            try:
                comments = get_comments(vid, MAX_COMMENTS)
                for c in comments:
                    c['region'] = region
                all_comments.extend(comments)
            except Exception as e:
                print(f"⚠️ Skipping video {vid} due to error: {e}")

    df = pd.DataFrame(all_comments)
    df.to_csv("youtube_comments.csv", index=False)
    print("✅ Saved comments to youtube_comments.csv")

