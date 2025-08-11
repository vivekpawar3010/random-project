from flask import Flask, request, send_file, render_template
import yt_dlp
import os
import uuid
import tempfile

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download_video():
    url = request.form.get("url")
    if not url:
        return "No URL provided", 400

    try:
        # Create a temporary directory for the download
        temp_dir = tempfile.mkdtemp()
        unique_id = str(uuid.uuid4())[:8]  # short unique filename
        output_template = os.path.join(temp_dir, f"video_{unique_id}.%(ext)s")

        ydl_opts = {
            'format': 'best',
            'outtmpl': output_template,
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Send the file and remove it after sending
        response = send_file(filename, as_attachment=True)
        @response.call_on_close
        def cleanup():
            try:
                os.remove(filename)
                os.rmdir(temp_dir)
            except:
                pass
        return response

    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == "__main__":
    # For production, set debug=False
    app.run(host="0.0.0.0", port=5000, debug=True)
