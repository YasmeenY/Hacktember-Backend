from models import db, Course, Video, VideoFavorite
from faker import Faker
from app import app

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!

        print( "Deleting data..." )
        # User.query.delete()
        VideoFavorite.query.delete()
        Course.query.delete()
        Video.query.delete()


        print( "Creating Courses..." )
        res1 = Course( title = "Pappy's STL BBQ")
        res2 = Course( title = "Hopdoddy Burger Bar")
        res3 = Course( title = "Adrianna's")
        res4 = Course( title = "Oyster House")
        res5 = Course( title = "Sugarfire") 
        Courses = [ res1, res2, res3, res4, res5 ]

        print( "Creating videos..." )
        re1 = Video( title = "Pappy", description = fake.paragraph(nb_sentences=5), course_id = 1)
        re2 = Video( title = "Hopdoddy", description = fake.paragraph(nb_sentences=5), course_id = 1)
        re3 = Video( title = "Adria", description = fake.paragraph(nb_sentences=5), course_id = 1)
        re4 = Video( title = "Oyster",  description = fake.paragraph(nb_sentences=5), course_id = 3)
        re5 = Video( title = "Sugar", description = fake.paragraph(nb_sentences=5), course_id = 2) 
        videos = [ re1, re2, re3, re4, re5 ]

        print( "Creating VideoFavorite..." )
        r1 = VideoFavorite( user_id = 1, video_id = 1 )
        r2 = VideoFavorite( user_id = 1, video_id = 2 )
        r3 = VideoFavorite( user_id = 2, video_id = 3 )

        Videofavorite = [ r1, r2, r3]
        
        db.session.add_all( Videofavorite )
        db.session.add_all( Courses )
        db.session.add_all( videos )
        db.session.commit()

        print( "Seeding complete!" )