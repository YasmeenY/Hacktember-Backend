import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import isodate



load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")

if api_key is None:
    raise ValueError("No YouTube API key found in the environment variables.")

youtube = build('youtube', 'v3', developerKey=api_key)


Django_request = youtube.videos().list(
    part="snippet,contentDetails,statistics",
    id="UmljXZIypDc,a48xeeo5Vnk,qDwdMDQ8oX4,1PkNiYlkkjo,aHC3uTkT9r8"
)
response1 = Django_request.execute()

Flask_request = youtube.videos().list(
    part="snippet,contentDetails,statistics",
    id="MwZwr5Tvyxo,QnDWIZuWYW0,UIJKdCIEXUQ,cYWiDiIUxQc,44PvX0Yv368"
)
response2 = Flask_request.execute()

Pandas_request = youtube.videos().list(
    part="snippet,contentDetails,statistics",
    id="ZyhVh-qRZPA,zmdjNSmRXF4,W9XjRYFkkyw,Lw2rlcxScZY,DCDe29sIKcE"
)
response3 = Pandas_request.execute()

Insta_clone_request = youtube.videos().list(
    part="snippet,contentDetails,statistics",
    id="qw5ZEvylQBA,Drmowe4P_5Y,ag1KUIpgdpI,EBea7dwjjOg,uAazuxknPPw"
)
response4 = Insta_clone_request.execute()



titles = []
viedo_urls = [ 'https://www.youtube.com/watch?v=UmljXZIypDc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p', 'https://www.youtube.com/watch?v=a48xeeo5Vnk&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=3', 'https://www.youtube.com/watch?v=qDwdMDQ8oX4&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=3', 'https://www.youtube.com/watch?v=1PkNiYlkkjo&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=4', 'https://www.youtube.com/watch?v=aHC3uTkT9r8&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=5', 'https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=1', 'https://www.youtube.com/watch?v=QnDWIZuWYW0&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=2', 'https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3', 'https://www.youtube.com/watch?v=cYWiDiIUxQc&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=4', 'https://www.youtube.com/watch?v=44PvX0Yv368&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=5', 'https://www.youtube.com/watch?v=ZyhVh-qRZPA&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&index=1', 'https://www.youtube.com/watch?v=zmdjNSmRXF4&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&index=2', 'https://www.youtube.com/watch?v=W9XjRYFkkyw&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&index=3', 'https://www.youtube.com/watch?v=Lw2rlcxScZY&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&index=4', 'https://www.youtube.com/watch?v=DCDe29sIKcE&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&index=5', 'https://www.youtube.com/watch?v=qw5ZEvylQBA&list=PL_KegS2ON4s7aVgtk-UI6jaXazt6KyntZ', 'https://www.youtube.com/watch?v=Drmowe4P_5Y&list=PL_KegS2ON4s7aVgtk-UI6jaXazt6KyntZ&index=2', 'https://www.youtube.com/watch?v=ag1KUIpgdpI&list=PL_KegS2ON4s7aVgtk-UI6jaXazt6KyntZ&index=3', 'https://www.youtube.com/watch?v=EBea7dwjjOg&list=PL_KegS2ON4s7aVgtk-UI6jaXazt6KyntZ&index=4', 'https://www.youtube.com/watch?v=uAazuxknPPw&list=PL_KegS2ON4s7aVgtk-UI6jaXazt6KyntZ&index=5']
descriptions = []
images_urls = []
durations = []
difficulty = ['Beginner', 'Intermediate', 'Expert' ]
course_image = []
creator = []
course_titles = ['Python Django Tutorial', 'Python Flask Tutorial', "Python Pandas tutorial", "Python Instagram Clone"]




for i in range(5):
    title = response1['items'][i]['snippet']['title']
    titles.append(title)
    images = response1['items'][i]['snippet']['thumbnails']['standard']['url']
    images_urls.append(images)
    description = response1['items'][i]['snippet']['description']
    descriptions.append(description)
    duration = response1['items'][i]['contentDetails']['duration']
    dur = isodate.parse_duration(duration)
    durations.append(str(dur)[2:])
    

for i in range(5):
    title = response2['items'][i]['snippet']['title']
    titles.append(title)
    images = response2['items'][i]['snippet']['thumbnails']['standard']['url']
    images_urls.append(images)
    description = response2['items'][i]['snippet']['description']
    descriptions.append(description)
    duration = response2['items'][i]['contentDetails']['duration']
    dur = isodate.parse_duration(duration)
    durations.append(str(dur)[2:])


for i in range(5):
    title = response3['items'][i]['snippet']['title']
    titles.append(title)
    images = response3['items'][i]['snippet']['thumbnails']['standard']['url']
    images_urls.append(images)
    description = response3['items'][i]['snippet']['description']
    descriptions.append(description)
    duration = response3['items'][i]['contentDetails']['duration']
    dur = isodate.parse_duration(duration)
    durations.append(str(dur)[2:])

for i in range(5):
    title = response4['items'][i]['snippet']['title']
    titles.append(title)
    images = response4['items'][i]['snippet']['thumbnails']['standard']['url']
    images_urls.append(images)
    description = response4['items'][i]['snippet']['description']
    descriptions.append(description)
    duration = response4['items'][i]['contentDetails']['duration']
    dur = isodate.parse_duration(duration)
    durations.append(str(dur)[2:])


course_image.append(response1['items'][0]['snippet']['thumbnails']['standard']['url'])
course_image.append(response2['items'][0]['snippet']['thumbnails']['standard']['url'])
course_image.append(response3['items'][0]['snippet']['thumbnails']['standard']['url'])
course_image.append(response4['items'][0]['snippet']['thumbnails']['standard']['url'])

creator.append(response1['items'][0]['snippet']['channelTitle'])
creator.append(response2['items'][0]['snippet']['channelTitle'])
creator.append(response3['items'][0]['snippet']['channelTitle'])
creator.append(response4['items'][0]['snippet']['channelTitle'])

print(creator)












# python django urls videos:[ 'https://www.youtube.com/watch?v=UmljXZIypDc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p, https://www.youtube.com/watch?v=a48xeeo5Vnk&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=3, https://www.youtube.com/watch?v=qDwdMDQ8oX4&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=3, https://www.youtube.com/watch?v=1PkNiYlkkjo&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=4, https://www.youtube.com/watch?v=aHC3uTkT9r8&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=5']
# video youtube id list: [UmljXZIypDc, a48xeeo5Vnk, qDwdMDQ8oX4, 1PkNiYlkkjo, aHC3uTkT9r8]



# python flask tutorials: ['https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=1, https://www.youtube.com/watch?v=QnDWIZuWYW0&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=2, https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3, https://www.youtube.com/watch?v=cYWiDiIUxQc&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=4, https://www.youtube.com/watch?v=44PvX0Yv368&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=5.
# ']
# video youtube id list: [MwZwr5Tvyxo, QnDWIZuWYW0, UIJKdCIEXUQ, cYWiDiIUxQc, 44PvX0Yv368]



# Python Pandas tutorial: ['https://www.youtube.com/watch?v=ZyhVh-qRZPA&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&index=1,   https://www.youtube.com/watch?v=zmdjNSmRXF4&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&index=2, https://www.youtube.com/watch?v=W9XjRYFkkyw&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&index=3, https://www.youtube.com/watch?v=Lw2rlcxScZY&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&index=4, https://www.youtube.com/watch?v=DCDe29sIKcE&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS&index=5'] 
# video youtube id list: [ZyhVh-qRZPA, zmdjNSmRXF4, W9XjRYFkkyw, Lw2rlcxScZY, DCDe29sIKcE]



# python django instagram clone: [' https://www.youtube.com/watch?v=qw5ZEvylQBA&list=PL_KegS2ON4s7aVgtk-UI6jaXazt6KyntZ,    https://www.youtube.com/watch?v=Drmowe4P_5Y&list=PL_KegS2ON4s7aVgtk-UI6jaXazt6KyntZ&index=2, https://www.youtube.com/watch?v=ag1KUIpgdpI&list=PL_KegS2ON4s7aVgtk-UI6jaXazt6KyntZ&index=3, https://www.youtube.com/watch?v=EBea7dwjjOg&list=PL_KegS2ON4s7aVgtk-UI6jaXazt6KyntZ&index=4, https://www.youtube.com/watch?v=uAazuxknPPw&list=PL_KegS2ON4s7aVgtk-UI6jaXazt6KyntZ&index=5']
# video youtube id list:[qw5ZEvylQBA, Drmowe4P_5Y, ag1KUIpgdpI, EBea7dwjjOg, uAazuxknPPw]