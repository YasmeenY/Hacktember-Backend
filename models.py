from sqlalchemy.ext.associationproxy import association_proxy
from config import db, bcrypt
from flask import abort
from sqlalchemy_serializer import SerializerMixin

class User( db.Model, SerializerMixin ):
    __tablename__ = 'users'
    serialize_rules = ('-video_favorite.user',)

    id = db.Column( db.Integer, primary_key=True )
    email = db.Column( db.String, unique = True )
    password = db.Column( db.Text )

    video_favorite = db.relationship( 'VideoFavorite',cascade="all,delete", backref = 'user' )

    def authenticate( self, password ):
        return bcrypt.check_password_hash(
            self.password, password.encode( 'utf-8' )
        )

class Course( db.Model , SerializerMixin):
    __tablename__ = 'courses'
    serialize_rules = ( '-videos.course', )

    id = db.Column( db.Integer, primary_key=True )
    title = db.Column( db.String )
    creator = db.Column( db.String )
    course_image = db.Column( db.String )
    difficulty = db.Column( db.String )

    videos = db.relationship( 'Video',cascade="all,delete", backref = 'course' )

class Video( db.Model , SerializerMixin):
    __tablename__ = 'videos'
    serialize_rules = ( '-video_favorite.video', )

    id = db.Column( db.Integer, primary_key=True )
    title = db.Column( db.String )
    url = db.Column( db.String )
    description = db.Column( db.String )
    duration = db.Column( db.String )
    pic = db.Column( db.String )
    course_id = db.Column( db.Integer, db.ForeignKey( 'courses.id' ) )

    video_favorite = db.relationship('VideoFavorite', backref='video')

class VideoFavorite( db.Model , SerializerMixin):
    __tablename__ = 'video_favorite'
    serialize_rules = ( '-user.video_favorite', '-video.video_favorite', )

    id = db.Column( db.Integer, primary_key=True )
    liked_at = db.Column( db.DateTime, server_default = db.func.now() )
    user_id = db.Column( db.Integer, db.ForeignKey( 'users.id' ) )
    video_id = db.Column( db.Integer, db.ForeignKey( 'videos.id' ) )
