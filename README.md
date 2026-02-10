# YouTube Transcript to Notion

A web app that extracts YouTube video transcripts, optimizes them with AI, and saves both versions to a Notion page.

## Prerequisites

### 1. Set up Notion

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations) and create a new integration
2. Copy the **Internal Integration Token** (starts with `ntn_`)
3. In Notion, open the page where you want transcripts saved
4. Click `...` > **Connections** > **Connect to** > select your integration
5. Copy the **page ID** from the URL — it's the 32-character string after the page name:
   ```
   https://notion.so/My-Page-abc123def456...  ← this part is the page ID
   ```

### 2. Set up OpenAI

1. Get an API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

## Deploy to Render (recommended)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) and sign up / log in
3. Click **New** > **Web Service**
4. Connect your GitHub repo
5. Render will auto-detect the `render.yaml` config. If not, set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Add these **Environment Variables** in the Render dashboard:
   - `OPENAI_API_KEY` — your OpenAI key
   - `NOTION_TOKEN` — your Notion integration token
   - `NOTION_PAGE_ID` — your Notion page ID
7. Click **Deploy** — Render will give you a public URL like `https://your-app.onrender.com`

## Run locally (optional)

```bash
pip install -r requirements.txt
cp .env.example .env
# fill in your keys in .env
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

## How it works

1. Paste a YouTube URL into the form
2. The app extracts the video's transcript using `youtube-transcript-api`
3. OpenAI (GPT-4o) rewrites the transcript to be more engaging and helpful
4. Both the original and optimized transcripts are saved as a new child page in Notion
5. You get a link to the Notion page and can preview both versions in the browser
