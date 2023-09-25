from models import db, User, Course, CoursesEnrolled
from faker import Faker
from app import app

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!

        print( "Deleting data..." )
        # User.query.delete()
        CoursesEnrolled.query.delete()
        Course.query.delete()


        print( "Creating Courses..." )
        res1 = Course( name = "Pappy's STL BBQ", description = fake.paragraph(nb_sentences=5))
        res2 = Course( name = "Hopdoddy Burger Bar", description = fake.paragraph(nb_sentences=5))
        res3 = Course( name = "Adrianna's", description = fake.paragraph(nb_sentences=5))
        res4 = Course( name = "Oyster House",  description = fake.paragraph(nb_sentences=5))
        res5 = Course( name = "Sugarfire", description = fake.paragraph(nb_sentences=5)) 
        Courses = [ res1, res2, res3, res4, res5 ]

        print( "Creating CoursesEnrolled..." )
        r1 = CoursesEnrolled( user_id = 1, course_id = 1 )
        r2 = CoursesEnrolled( user_id = 1, course_id = 2 )
        r3 = CoursesEnrolled( user_id = 2, course_id = 3 )

        coursesenrolled = [ r1, r2, r3]
        
        db.session.add_all( coursesenrolled )
        db.session.add_all( Courses )
        db.session.commit()

        print( "Seeding complete!" )