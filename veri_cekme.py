import os
import csv
from googleapiclient.discovery import build 

API_KEY = ''
VIDEO_IDS = ['NWOtDJZ2cRg', 'QUp1nVyBEic', '9QZEuMu2eC0'] 
#1.id matematik, 2. id yapay sinir ağları,3. id yatırım
output_dir = os.path.join(os.path.expanduser('~'), 'Desktop', 'ai')
os.makedirs(output_dir, exist_ok=True)
youtube = build('youtube', 'v3', developerKey=API_KEY)

def fetch_youtube_comments(video_id, max_comments=50):
    comments = []   
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_comments,
        textFormat="plainText"
    )
    response = request.execute()

    while request is not None:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'author': comment['authorDisplayName'],
                'text': comment['textDisplay'],
                'published_at': comment['publishedAt'],
                'like_count': comment['likeCount'],
                'reply_count': item['snippet']['totalReplyCount']
            })
        if 'nextPageToken' in response:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=response['nextPageToken'],
                maxResults=max_comments,
                textFormat="plainText"
            )
            response = request.execute()
        else:
            request = None
    return comments

def save_comments_to_csv(video_id, comments, index):
    output_csv_path = os.path.join(output_dir, f'youtube_yorumlari_ve_meta_verileri_{index}.csv')
    with open(output_csv_path, mode='w', newline='', encoding='utf-16') as file:
        writer = csv.DictWriter(file, fieldnames=['author', 'text', 'published_at', 'like_count', 'reply_count'])
        writer.writeheader()
        for comment in comments:
            writer.writerow(comment) 
 
for index, video_id in enumerate(VIDEO_IDS):
    comments = fetch_youtube_comments(video_id)
    save_comments_to_csv(video_id, comments, index)