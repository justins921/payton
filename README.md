# YouTube Transcript to Notion

A web app that extracts YouTube video transcripts, optimizes them with AI, and saves both versions to a Notion page.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Notion

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations) and create a new integration
2. Copy the **Internal Integration Token** (starts with `ntn_`)
3. In Notion, open the page where you want transcripts saved
4. Click `...` > **Connections** > **Connect to** > select your integration
5. Copy the **page ID** from the URL — it's the 32-character string after the page name:
   ```
   https://notion.so/My-Page-abc123def456...  ← this part is the page ID
   ```

### 3. Set up OpenAI

1. Get an API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### 4. Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your keys:

```
OPENAI_API_KEY=sk-your-key-here
NOTION_TOKEN=ntn_your-token-here
NOTION_PAGE_ID=your-page-id-here
```

### 5. Run

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

## How it works

1. Paste a YouTube URL into the form
2. The app extracts the video's transcript using `youtube-transcript-api`
3. OpenAI (GPT-4o) rewrites the transcript to be more engaging and helpful
4. Both the original and optimized transcripts are saved as a new child page in Notion
5. You get a link to the Notion page and can preview both versions in the browser
