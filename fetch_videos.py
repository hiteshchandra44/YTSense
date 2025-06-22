from googleapiclient.discovery import build
from config import API_KEY, MAX_RESULTS

def search_videos(query, region='IN'):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    res = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=MAX_RESULTS,
        regionCode=region
    ).execute()
    return [item['id']['videoId'] for item in res['items']]
