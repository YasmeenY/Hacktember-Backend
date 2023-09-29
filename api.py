import os
from googleapiclient.discovery import build
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")

if api_key is None:
    raise ValueError("No YouTube API key found in the environment variables.")

youtube = build('youtube', 'v3', developerKey=api_key)


# request = youtube.videos().list(
#         part="snippet,contentDetails,statistics",
#         id="Ks-_Mh1QhMc"
#     )

# response  = request.execute()

# request = youtube.playlists().list(
#         part="snippet,contentDetails",
#         channelId="UCCezIgC97PvUuR4_gbFUs5g",
#         maxResults=5
#     )

request = youtube.videos().list(
    part="snippet,contentDetails,statistics",
    id="Ks-_Mh1QhMc,c0KYU2j0TM4,eIho2S0ZahI"
)
response = request.execute()

print(response)
print(response.status_code)