import os
from googleapiclient.discovery import build
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")

if api_key is None:
    raise ValueError("No YouTube API key found in the environment variables.")

youtube = build('youtube', 'v3', developerKey=api_key)

# response  = request.execute()

# request = youtube.playlists().list(
#         part="snippet,contentDetails",
#         channelId="UCCezIgC97PvUuR4_gbFUs5g",
#         maxResults=5
#     )

request = youtube.videos().list(
    part="snippet,contentDetails,statistics",
    id="ZyhVh-qRZPA,zmdjNSmRXF4,W9XjRYFkkyw,Lw2rlcxScZY,DCDe29sIKcE"
)
response = request.execute()

print(response)
print(response.status_code)

# python django urls videos:[ 'https://www.youtube.com/watch?v=UmljXZIypDc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p, https://www.youtube.com/watch?v=a48xeeo5Vnk&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=3, https://www.youtube.com/watch?v=qDwdMDQ8oX4&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=3, https://www.youtube.com/watch?v=1PkNiYlkkjo&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=4, https://www.youtube.com/watch?v=aHC3uTkT9r8&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=5']
# video youtube id list: [UmljXZIypDc, a48xeeo5Vnk, qDwdMDQ8oX4, 1PkNiYlkkjo, aHC3uTkT9r8]



# python flask tutorials: ['https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=1, https://www.youtube.com/watch?v=QnDWIZuWYW0&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=2, https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3, https://www.youtube.com/watch?v=cYWiDiIUxQc&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=4, https://www.youtube.com/watch?v=44PvX0Yv368&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=5.
# ']
# video youtube id list: [MwZwr5Tvyxo, QnDWIZuWYW0, UIJKdCIEXUQ, cYWiDiIUxQc, 44PvX0Yv368]



# Python Pandas tutorial: ['https://www.youtube.com/watch?v=ZyhVh-qRZPA&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&index=1,   https://www.youtube.com/watch?v=zmdjNSmRXF4&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&index=2, https://www.youtube.com/watch?v=W9XjRYFkkyw&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&index=3, https://www.youtube.com/watch?v=Lw2rlcxScZY&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&index=4, https://www.youtube.com/watch?v=DCDe29sIKcE&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&index=5'] 
# video youtube id list: [ZyhVh-qRZPA, zmdjNSmRXF4, W9XjRYFkkyw, Lw2rlcxScZY, DCDe29sIKcE]



# python django instagram clone: [' https://www.youtube.com/watch?v=qw5ZEvylQBA&list=PL_KegS2ON4s7aVgtk-UI6jaXazt6KyntZ,    https://www.youtube.com/watch?v=Drmowe4P_5Y&list=PL_KegS2ON4s7aVgtk-UI6jaXazt6KyntZ&index=2, https://www.youtube.com/watch?v=ag1KUIpgdpI&list=PL_KegS2ON4s7aVgtk-UI6jaXazt6KyntZ&index=3, https://www.youtube.com/watch?v=EBea7dwjjOg&list=PL_KegS2ON4s7aVgtk-UI6jaXazt6KyntZ&index=4, https://www.youtube.com/watch?v=uAazuxknPPw&list=PL_KegS2ON4s7aVgtk-UI6jaXazt6KyntZ&index=5']
# video youtube id list:[qw5ZEvylQBA, Drmowe4P_5Y, ag1KUIpgdpI, EBea7dwjjOg, uAazuxknPPw]