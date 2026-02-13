from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Mukesh Universal Multi-Downloader API is Running!"

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    # yt-dlp कॉन्फ़िगरेशन
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # वीडियो की जानकारी निकालना
            info = ydl.extract_info(url, download=False)
            
            # वीडियो का डायरेक्ट लिंक और टाइटल ढूंढना
            video_url = info.get('url')
            title = info.get('title', 'Universal-Downloader')

            return jsonify({
                "download_url": video_url,
                "title": title,
                "thumbnail": info.get('thumbnail', '')
            })
            
    except Exception as e:
        return jsonify({"error": f"Link not supported or error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
