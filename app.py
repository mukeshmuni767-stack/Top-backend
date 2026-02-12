from flask import Flask, request, jsonify
from flask_cors import CORS
import instaloader

app = Flask(__name__)
CORS(app)  # यह आपकी वेबसाइट को सर्वर से जुड़ने की अनुमति देगा

L = instaloader.Instaloader()

@app.route('/')
def home():
    return "Mukesh API is Running!"

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # रील का शॉर्टकोड निकालना
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        return jsonify({
            "download_url": post.video_url,
            "title": post.caption[:50] if post.caption else "Mukesh-Downloader"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
