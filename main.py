from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)


app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route("/process-video", methods=["POST"])
def process_video():
    # get a file url
    file_url = request.form.get("file_url")
    if not file_url:
        return jsonify({"error": "Missing file_url parameter"}), 400
    
    output_path = "output.mp4"

    # Example FFmpeg command to convert video to a different format
    command = [
        "ffmpeg",
        "-i",
        file_url,
        "-bsf:a",
        "aac_adtstoasc",
        "-nostdin",
        # make it faster
        "-preset",
        "ultrafast",
        "-y",
        "-c",
        "copy",
        output_path,
    ]

    try:
        subprocess.run(command, check=True)
        return jsonify(
            {"message": "Video processed successfully", "output": output_path}
        )
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"FFmpeg error: {str(e)}"}), 500
    finally:
        # Clean up temporary files
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
