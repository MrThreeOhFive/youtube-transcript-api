from flask import Flask, request, jsonify
from flask_cors import CORS

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("❌ Failed to import youtube_transcript_api. Is it in requirements.txt?")
    raise

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return '✅ YouTube Transcript API is live.'

@app.route('/get_transcripts', methods=['POST'])
def get_transcripts():
    try:
        data = request.get_json(force=True)
        if not data or 'video_ids' not in data:
            return jsonify({"error": "Missing video_ids"}), 400

        video_ids = data['video_ids']
        results = []

        for vid in video_ids:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(vid)
                transcript_text = " ".join([entry['text'] for entry in transcript])
            except Exception as e:
                transcript_text = f"Error: {str(e)}"
            results.append({"video_id": vid, "transcript": transcript_text})

        return jsonify(results), 200

    except Exception as e:
        print(f"❌ Error in /get_transcripts: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(host='0.0.0.0', port=3000)
