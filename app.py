from config import app, db, api, bcrypt
from models import db, User, Course, VideoFavorite
from flask import make_response, jsonify, request, session, send_file, render_template
from flask_restful import Resource
import openai
import os
import requests
import uuid
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

openai.api_key = ""

def transcribe_audio(filename: str) -> str:
    """
        Transcribe audio to text.
    """
    with open(filename, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript.text

def generate_reply(conversation: list) -> str:
    """
        Generate a ChatGPT response.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful python assistant."},
        ] + conversation
    )
    return response["choices"][0]["message"]["content"]

def generate_audio(text):
    load_dotenv() 

    speech_key =  os.getenv('SPEECH_KEY')
    speech_reg = os.getenv('SPEECH_REGION')
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_reg)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='en-US-JennyNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

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

api.add_resource( Signup, '/signup', endpoint = 'signup' )
api.add_resource( Login, '/login', endpoint='login' )
api.add_resource( Logout, '/logout', endpoint='logout' )
api.add_resource( CheckSession, '/check_session', endpoint='check_session' )

@app.route( '/users/<int:id>', methods=[ "GET", "DELETE", "PATCH" ] )
def user( id ):
    user = User.query.filter( User.id == id ).first()
    # if request.method == "GET":
    #     return make_response( user.to_dict(), 200 )
    if user:
        
        if request.method == "DELETE":
            VideoFavorite.query.filter_by( user_id = id ).delete()
            db.session.delete( user )
            db.session.commit()
            return make_response("", 204)

        elif request.method == "PATCH":
            user_data = request.get_json()
            for attr in user_data:
                setattr(user, attr, user_data[attr])
            db.session.add(user)
            db.session.commit()
            return make_response( user.to_dict(), 200 )
    else:
        return make_response( "User not found.", 404 )

@app.route( '/course/<int:id>', methods=[ "GET" ] )
def course( id ):
    course = Course.query.filter( Course.id == id ).first()
    if request.method == "GET":
        return make_response( course.to_dict(), 200 )
    else:
        return make_response( "Course not found.", 404 )

# under here not tested yet
@app.route('/transcribe', methods=['POST'])
def transcribe():
    """
        turn the given audio to text using Whisper.
    """
    if 'file' not in request.files:
        return 'No file found', 400
    file = request.files['file']
    recording_file = f"{uuid.uuid4()}.wav"
    recording_path = f"uploads/{recording_file}"
    os.makedirs(os.path.dirname(recording_path), exist_ok=True)
    file.save(recording_path)
    transcription = transcribe_audio(recording_path)
    return jsonify({'text': transcription})

@app.route('/ask', methods=['POST'])
def ask():
    """
        Generate a ChatGPT response from the given conversation
    """
    conversation = request.get_json(force=True).get("conversation", "")
    reply = generate_reply(conversation)
    return jsonify({'text': reply})


@app.route('/listen', methods=['POST'])
def listen():
    text = request.get_json()[ 'text' ]
    audio = generate_audio(text)
    return jsonify({'text': reply})

if __name__ == '__main__':
    app.run(port=5555, debug=True)