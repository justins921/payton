import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from transcript import get_transcript
from optimizer import optimize_transcript
from notion_client import save_to_notion

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    youtube_url = request.form.get("youtube_url", "").strip()
    if not youtube_url:
        return jsonify({"error": "Please provide a YouTube URL."}), 400

    openai_key = os.environ.get("OPENAI_API_KEY")
    notion_token = os.environ.get("NOTION_TOKEN")
    notion_page_id = os.environ.get("NOTION_PAGE_ID")

    if not openai_key:
        return jsonify({"error": "OPENAI_API_KEY not set in .env file."}), 500
    if not notion_token or not notion_page_id:
        return jsonify({"error": "NOTION_TOKEN or NOTION_PAGE_ID not set in .env file."}), 500

    try:
        # Step 1: Get transcript
        original = get_transcript(youtube_url)

        # Step 2: Optimize with AI
        optimized = optimize_transcript(original, openai_key)

        # Step 3: Save to Notion
        page_title = f"Transcript: {youtube_url}"
        notion_url = save_to_notion(
            notion_token, notion_page_id, page_title, original, optimized
        )

        return jsonify({
            "original": original,
            "optimized": optimized,
            "notion_url": notion_url,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
