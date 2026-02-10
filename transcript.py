import os
import re
import subprocess
import tempfile

from openai import OpenAI


def get_transcript(youtube_url: str, proxy_url: str | None = None, openai_key: str | None = None) -> str:
    """Fetch transcript for a YouTube video.

    1. Try yt-dlp to grab existing subtitles (fastest, free).
    2. Fall back to downloading audio + OpenAI Whisper transcription.
    """
    transcript = _get_subtitles(youtube_url, proxy_url)
    if transcript:
        return transcript

    if openai_key:
        return _whisper_transcribe(youtube_url, proxy_url, openai_key)

    raise ValueError(
        "No subtitles found for this video and no OpenAI key available for Whisper fallback."
    )


def _get_subtitles(youtube_url: str, proxy_url: str | None = None) -> str | None:
    """Use yt-dlp to download existing subtitles (manual or auto-generated)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_template = os.path.join(tmpdir, "%(id)s")
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-auto-sub",
            "--write-sub",
            "--sub-lang", "en",
            "--sub-format", "vtt",
            "--output", output_template,
            youtube_url,
        ]
        if proxy_url:
            cmd.extend(["--proxy", proxy_url])

        subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        # Find the VTT file
        for f in os.listdir(tmpdir):
            if f.endswith(".vtt"):
                return _parse_vtt(os.path.join(tmpdir, f))

    return None


def _parse_vtt(filepath: str) -> str:
    """Parse a VTT subtitle file into plain text."""
    with open(filepath) as f:
        content = f.read()

    lines = []
    for line in content.split("\n"):
        line = line.strip()
        # Skip VTT headers, timestamps, and blank lines
        if (
            not line
            or line.startswith("WEBVTT")
            or line.startswith("Kind:")
            or line.startswith("Language:")
            or line.startswith("NOTE")
            or re.match(r"^\d{2}:\d{2}", line)
            or re.match(r"^\d+$", line)
        ):
            continue
        # Remove inline tags like <c>, </c>, <00:00:01.234>
        line = re.sub(r"<[^>]+>", "", line)
        if line:
            lines.append(line)

    # Deduplicate consecutive identical lines (common in auto-subs)
    deduped = []
    for line in lines:
        if not deduped or line != deduped[-1]:
            deduped.append(line)

    return " ".join(deduped)


def _whisper_transcribe(youtube_url: str, proxy_url: str | None, openai_key: str) -> str:
    """Download audio with yt-dlp and transcribe with OpenAI Whisper."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "audio.mp3")
        cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "5",
            "--output", output_path,
            youtube_url,
        ]
        if proxy_url:
            cmd.extend(["--proxy", proxy_url])

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            raise ValueError(f"Failed to download audio: {result.stderr[:500]}")

        # Find the mp3 file (yt-dlp may add extension)
        audio_file = None
        for f in os.listdir(tmpdir):
            if f.endswith(".mp3"):
                audio_file = os.path.join(tmpdir, f)
                break

        if not audio_file:
            raise ValueError("Failed to download audio from YouTube.")

        client = OpenAI(api_key=openai_key)
        with open(audio_file, "rb") as f:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
            )

        return response.text
