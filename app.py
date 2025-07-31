from flask import Flask, render_template, request, send_file
from moviepy.editor import VideoFileClip
import os
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    video = request.files['video']
    if video.filename == '':
        return "No file selected", 400

    # Save video temporarily
    video_filename = f"{uuid.uuid4()}.mp4"
    video_path = os.path.join("static", video_filename)
    video.save(video_path)

    # MP3 output filename
    mp3_filename = video_filename.replace('.mp4', '.mp3')
    mp3_path = os.path.join("static", mp3_filename)

    # Convert using moviepy
    try:
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(mp3_path)
        clip.close()
    except Exception as e:
        return f"Error during conversion: {e}", 500
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)

    return send_file(mp3_path, as_attachment=True)

@app.route('/terms')
def terms():
    return render_template('terms.html')

if __name__ == '__main__':
    app.run(debug=True)