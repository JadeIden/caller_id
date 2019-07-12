import datetime
import io
from dataclasses import dataclass

from flask import Flask, request, send_file, render_template
from google.cloud import texttospeech
from flask_sqlalchemy import SQLAlchemy

from names import name_to_audio

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cache.db'
db = SQLAlchemy(app)


@dataclass
class TTSData:
    client: texttospeech.TextToSpeechClient = None
    voice: texttospeech.types.VoiceSelectionParams = None
    audio_config: texttospeech.types.AudioConfig = None


tts_info = TTSData()


def init_tts(tts):
    tts.client = texttospeech.TextToSpeechClient()
    tts.voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL
    )
    tts.audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3
    )


@app.route('/hello')
def hello_world():
    return 'Hello World!'


def load_audio(tts, text):
    from model import Name
    existing: Name = Name.query.filter_by(text=text).first()
    if existing:
        existing.last_access = datetime.datetime.utcnow()
        return existing.data
    audio = text_to_speech(tts, text)
    new_row = Name(text=text, data=audio)
    db.session.add(new_row)
    db.session.commit()
    return audio


def text_to_speech(tts, text):
    speech = texttospeech.types.SynthesisInput(text=text)
    binary = tts.client.synthesize_speech(speech, tts.voice, tts.audio_config)
    return binary.audio_content


@app.route('/audio')
def get_audio():
    global tts_info
    number = request.args.get('number', None)
    name = request.args.get('name', None)
    try:
        to_audio = name_to_audio(name, number)
    except ValueError as ex:
        return render_template('error.html', error=ex.message)
    audio = load_audio(tts_info, to_audio)
    return send_file(io.BytesIO(audio),
                     attachment_filename='audio.mp3',
                     mimetype='audio/mpeg')


with app.app_context():
    init_tts(tts_info)


if __name__ == '__main__':
    app.run()
