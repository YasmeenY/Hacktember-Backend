from models import db, Course, Video, VideoFavorite
from app import app
import random
from api import titles, viedo_urls, descriptions, images_urls, durations, difficulty, course_image, creator, course_titles

# print(titles)
if __name__ == '__main__':
    with app.app_context():
        Course.query.delete()
        Video.query.delete()

        courses = []
        playlist1 = []
        playlist2 = []
        playlist3 = []
        playlist4 = []


        for i in range(4):
            course = Course(title = course_titles[i], creator = creator[i], course_image = course_image[i], difficulty = random.choice(difficulty))
            courses.append(course)

        for i in range(5):
            video = Video(course_id= 1, title = titles[i], url = viedo_urls[i], description = descriptions[i], duration = durations[i], pic = images_urls[i])
            playlist1.append(video)
        
        for i in range(5,10):
            video = Video(course_id= 2, title = titles[i], url = viedo_urls[i], description = descriptions[i], duration = durations[i], pic = images_urls[i])
            playlist2.append(video)
        
        for i in range(10,15):
            video = Video(course_id= 3, title = titles[i], url = viedo_urls[i], description = descriptions[i], duration = durations[i], pic = images_urls[i])
            playlist3.append(video)
        
        for i in range(15,20):
            video = Video(course_id= 4, title = titles[i], url = viedo_urls[i], description = descriptions[i], duration = durations[i], pic = images_urls[i])
            playlist4.append(video)




        db.session.add_all(courses)
        db.session.add_all(playlist1)
        db.session.add_all(playlist2)
        db.session.add_all(playlist3)
        db.session.add_all(playlist4)
        db.session.commit()
        