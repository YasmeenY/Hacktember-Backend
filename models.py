from sqlalchemy.ext.associationproxy import association_proxy
from config import db, bcrypt
from flask import abort
from sqlalchemy_serializer import SerializerMixin

class User( db.Model, SerializerMixin ):
    __tablename__ = 'users'
    serialize_rules = ('-courses.users', '-courses-enrolled.user')

    id = db.Column( db.Integer, primary_key=True )
    first_name = db.Column( db.String )
    last_name = db.Column( db.String )
    email = db.Column( db.String, unique = True )
    password = db.Column( db.Text )

    courses_enrolled = db.relationship( 'CoursesEnrolled', back_populates = 'user', cascade='all, delete-orphan' )
    courses = association_proxy( 'coursesenrolled', 'course' )

    def authenticate( self, password ):
        return bcrypt.check_password_hash(
            self.password, password.encode( 'utf-8' )
        )

class Course( db.Model , SerializerMixin):
    __tablename__ = 'courses'
    serialize_rules = ( '-courses-enrolled.users', '-courses-enrolled.user' )

    id = db.Column( db.Integer, primary_key=True )
    name = db.Column( db.String )
    description = db.Column( db.String )

class CoursesEnrolled( db.Model , SerializerMixin):
    __tablename__ = 'courses-enrolled'
    serialize_rules = ( '-user.courses-enrolled', '-course.courses-enrolled' )

    id = db.Column( db.Integer, primary_key=True )
    created_at = db.Column( db.DateTime, server_default = db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate = db.func.now() )
    user_id = db.Column( db.Integer, db.ForeignKey( 'users.id' ) )
    course_id = db.Column( db.Integer, db.ForeignKey( 'courses.id' ) )
