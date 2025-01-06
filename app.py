from flask import Flask, request, jsonify
import os
import whisper

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = whisper.load_model("tiny.en")

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

  result = model.transcribe(file_path, language="en")
  transcription = result["text"]

  os.remove(file_path)

  return jsonify({'transcription': transcription})

if __name__ == '__main__':
  app.run()