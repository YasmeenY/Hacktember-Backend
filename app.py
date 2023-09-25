from config import app, db, api, bcrypt
from models import db, User, Course, CoursesEnrolled
from flask import make_response, jsonify, request, session
from flask_restful import Resource

@app.route("/")
def Home():
    return "Home Route"

def user_to_dict( user ):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }
def courses_to_dict( user ):
    return {
        "id": user.id,
        "course_id": user.course_id,
    }

class ClearSession( Resource ):
    
    def delete( self ):

        session[ 'page_views' ] = None
        session[ 'user_id' ] = None

        return {}, 204

class CheckSession(Resource):

    def get(self):
        
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return user_to_dict( user ), 200
        
        return {}, 401

class Signup( Resource ):
    
    def post( self ):

        try:
            first_name = request.get_json()[ 'first_name' ]
            last_name = request.get_json()[ 'last_name' ]
            email = request.get_json()[ 'email' ]
            password = request.get_json()[ 'password' ]
        except KeyError:
            return { "error": "Missing a required field in the form." }, 400
        
        user_exists = User.query.filter_by(email=email).first() is not None
        
        if user_exists:
            return jsonify({"error": "User already exists"}, 409)
        
        hashed_password = bcrypt.generate_password_hash(password.encode( 'utf-8' ))
        new_user = User(
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = hashed_password
        )
        db.session.add( new_user )
        db.session.commit()

        session[ 'user_id' ] = new_user.id
        
        return user_to_dict( new_user ), 201

class Login( Resource ):

    def post( self ):
        try:
            email = request.get_json()[ 'email' ]
            password = request.get_json()[ 'password' ]
        except TypeError:
            return { "error": "Missing 'email' or 'password'." }, 400
        
        user = User.query.filter( User.email == email ).first()

        if not user:
            return {"error": "user doesn't exist"}, 404

        if user.authenticate( password ):
            session[ 'user_id' ] = user.id
            return user_to_dict( user ), 200

        else:
            return { "error": "Members Only Content, Unauthorized Access!"}, 401

class Logout( Resource ):

    def delete( self ):
        session[ 'user_id' ] = None
        return {}, 204

api.add_resource( Signup, '/signup', endpoint = 'signup' )
api.add_resource( Login, '/login', endpoint='login' )
api.add_resource( Logout, '/logout', endpoint='logout' )
api.add_resource( CheckSession, '/check_session', endpoint='check_session' )

@app.route( '/users/<int:id>', methods=[ "GET", "DELETE", "PATCH" ] )
def user( id ):
    user = User.query.filter( User.id == id ).first()
    user_courses = CoursesEnrolled.query.filter( CoursesEnrolled.user_id == id ).all()
    if user:
        if request.method == "GET":
            user_dict =  user_to_dict( user)
            user_dict["courses_enrolled"] = [courses_to_dict(r) for r in user_courses]
            return make_response( jsonify( user_dict ), 200 )
        
        elif request.method == "DELETE":
            CoursesEnrolled.query.filter_by( user_id = id ).delete()
            db.session.delete( user )
            db.session.commit()
            return make_response("", 204)

        elif request.method == "PATCH":
            user_data = request.get_json()
            for attr in user_data:
                setattr(user, attr, user_data[attr])
            db.session.add(user)
            db.session.commit()
            user_dict =  user_to_dict( user)
            user_dict["courses_enrolled"] = [courses_to_dict(r) for r in user.courses_enrolled]
            return make_response( jsonify( user_dict ), 200 )
    else:
        return make_response( "User not found.", 404 )

if __name__ == '__main__':
    app.run(port=5555, debug=True)