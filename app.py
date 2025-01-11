from flask import Flask, request, jsonify
import os
from pydub import AudioSegment
import speech_recognition as sr

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

r = sr.Recognizer()

@app.route("/")
def main():
  return "To transcribe send a form data post request with a audio file to the /transcribe endpoint"

@app.route("/transcribe", methods=["POST"])
def transcribe():
  if 'file' not in request.files:
    return jsonify({'error': 'No audio file provided'}), 400

  audio_file = request.files['file']

  file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
  audio_file.save(file_path)

  wav_path = os.path.join(app.config['UPLOAD_FOLDER'], "audio.wav")
  audio = AudioSegment.from_mp3(file_path)
  audio.export(wav_path, format="wav")

  os.remove(file_path)

  with sr.AudioFile(wav_path) as source:
    sound = r.record(source)
    result = "idk what happend but its not handled so gl"

    try:
      result = r.recognize_google(sound)
      os.remove(wav_path)
    except sr.UnknownValueError:
      result = "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
      result = "Could not request results from Google Speech Recognition service"
    finally:
      return jsonify({'transcription': result})
  
if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8080)
