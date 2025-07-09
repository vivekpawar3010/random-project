from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Serve your HTML file
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "No URL provided", 400

    # Download options
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    # Send the file to the user
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)