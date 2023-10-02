from config import app, db, api, bcrypt
from models import db, User, Course, VideoFavorite, Video
from flask import make_response, jsonify, request, session, send_file
from flask_restful import Resource
import openai
import os
import uuid
import requests

openai.api_key = ""

ELEVENLABS_API_KEY = ""

# Choose your favorite ElevenLabs voice
ELEVENLABS_VOICE_NAME = "Joanne"
ELEVENLABS_ALL_VOICES = []

def transcribe_audio(filename: str) -> str:
    # Transcribe audio to text.
    with open(filename, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript.text

def generate_reply(conversation: list) -> str:
    # Generate a ChatGPT response.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful python assistant. You should only respond to python related questions. For any other question you must answer 'I\'m not suitable for this type of tasks. I can help with anything related to python.'" + conversation},
        ]
    )
    return response["choices"][0]["message"]["content"]


def generate_audio(text: str, output_path: str = "") -> str:
    voices = ELEVENLABS_ALL_VOICES
    try:
        voice_id = next(filter(lambda v: v["name"] == ELEVENLABS_VOICE_NAME, voices))["voice_id"]
    except StopIteration:
        voice_id = voices[0]["voice_id"]
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "content-type": "application/json"
    }
    data = {
        "text": text,
    }
    response = requests.post(url, json=data, headers=headers)
    with open(output_path, "wb") as output:
        output.write(response.content)
    return output_path

def get_voices() -> list:
    # get a list of available ElevenLabs voices.
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()["voices"]

if ELEVENLABS_API_KEY:
    if not ELEVENLABS_ALL_VOICES:
        ELEVENLABS_ALL_VOICES = get_voices()
    if not ELEVENLABS_VOICE_NAME:
        ELEVENLABS_VOICE_NAME = ELEVENLABS_ALL_VOICES[0]["name"]

@app.route("/")
def Home():
    return "Home Route"

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
            return user.to_dict(), 200
        
        return {}, 401

class Signup( Resource ):
    
    def post( self ):

        try:
            email = request.get_json()[ 'email' ]
            password = request.get_json()[ 'password' ]
        except KeyError:
            return { "error": "Missing a required field in the form." }, 400
        
        user_exists = User.query.filter_by(email=email).first() is not None
        
        if user_exists:
            return jsonify({"error": "User already exists"}, 409)
        
        hashed_password = bcrypt.generate_password_hash(password.encode( 'utf-8' ))
        new_user = User(
            email = email,
            password = hashed_password
        )
        db.session.add( new_user )
        db.session.commit()

        session[ 'user_id' ] = new_user.id
        
        return new_user.to_dict(), 201

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
            return user.to_dict(), 200

        else:
            return { "error": "Members Only Content, Unauthorized Access!"}, 401

class Logout( Resource ):

    def delete( self ):
        session[ 'user_id' ] = None
        return {}, 204

class Courses(Resource):
    def get(self):
        #get the data of all available courses
        courses = Course.query.all()
        if request.method == "GET":
            courses_serialized = [course.to_dict() for course in courses]
            return courses_serialized, 200
        else:
            return make_response( "Course not found.", 404 )

class Videos(Resource):
    def get(self):
        #git all the data of all videos
        videos = Video.query.all()
        if request.method == "GET":
            videos_serialized = [video.to_dict(only=('id', 'title', 'url', 'description', 'duration', 'pic','course_id')) for video in videos]
            return videos_serialized, 200
        else:
            return make_response( "Videos not found.", 404 )

class VideosById(Resource):
    def get(self, id):
        #get data on videos using video id
        video = Video.query.filter( Video.id == id ).first()
        if request.method == "GET":
            return make_response( video.to_dict(only=('id', 'title', 'url', 'description', 'duration', 'pic','course_id')), 200 )
        else:
            return make_response( "Course not found.", 404 )
        
class CourseById(Resource):
    def get(self, id):
        #get data about course using course id
        course = Course.query.filter( Course.id == id ).first()
        if request.method == "GET":
            return make_response( course.to_dict(), 200 )
        else:
            return make_response( "Course not found.", 404 )
        
class userById(Resource):
    def delete(self, id):
        if session.get('user_id'):
            #allows deleting the user and related data
            user = User.query.filter( User.id == id ).first()
            VideoFavorite.query.filter_by( user_id = id ).delete()
            db.session.delete( user )
            db.session.commit()
            return make_response("", 204)
        else:
            return make_response( "User not found.", 404 )

    def patch(self, id):
        #only allow changing user email
        if session.get('user_id'):
            user = User.query.filter( User.id == id ).first()
            user_data = request.get_json()
            for attr in user_data:
                setattr(user, attr, user_data[attr])
            db.session.add(user)
            db.session.commit()
            return make_response( user.to_dict(), 200 )
        else:
            return make_response( "User not found.", 404 )
class Transcribe(Resource):
    def post(self):
        # turn the given audio to text using Whisper.
        if 'file' not in request.files:
            return 'No file found', 400
        file = request.files['file']
        recording_file = f"{uuid.uuid4()}-mo.wav"
        recording_path = f"uploads/{recording_file}"
        os.makedirs(os.path.dirname(recording_path), exist_ok=True)
        file.save(recording_path)
        transcription = transcribe_audio(recording_path)
        return make_response({'text': transcription})

class Ask(Resource):
    def post(self):
        # Generate a ChatGPT response from the given conversation
        conversation = request.get_json()['question']
        reply = generate_reply(conversation)
        reply_file = f"{uuid.uuid4()}.mp3"
        reply_path = f"outputs/{reply_file}"
        os.makedirs(os.path.dirname(reply_path), exist_ok=True)
        audio = generate_audio(reply, output_path=reply_path)
        return jsonify({'text': reply, 'audio': f"/listen/{reply_file}"})

class Listen(Resource):
    def get(self, filename):
        # Return the audio file located at the given filename.
        if not filename:
            return make_response("No audio found", 404)
        return send_file(f"outputs/{filename}", mimetype="audio/mp3", as_attachment=False)


api.add_resource( Signup, '/signup', endpoint = 'signup' )
api.add_resource( Login, '/login', endpoint='login' )
api.add_resource( Logout, '/logout', endpoint='logout' )
api.add_resource( CheckSession, '/check_session', endpoint='check_session' )
api.add_resource( Courses, '/courses', endpoint='courses' )
api.add_resource( Videos, '/videos', endpoint='videos' )
api.add_resource( VideosById, '/video/<int:id>', endpoint='video/<int:id>' )
api.add_resource( CourseById, '/course/<int:id>', endpoint='course/<int:id>' )
api.add_resource( userById, '/users/<int:id>', endpoint='users/<int:id>' )
api.add_resource( Transcribe, '/transcribe', endpoint='transcribe' )
api.add_resource( Ask, '/ask', endpoint='/ask' )
api.add_resource( Listen, '/listen/<filename>', endpoint='listen/<filename>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)