from openai import OpenAI

SYSTEM_PROMPT = """You are an expert course content writer and script optimizer.
Your job is to rewrite video scripts so they are better: more engaging, with updated
info, new ideas, and as helpful as possible to students.

Keep the same overall structure and teaching points, but improve:
- Clarity and flow
- Engagement and energy
- Actionable advice and examples
- Modern, up-to-date information
- Professional but conversational tone

Return ONLY the rewritten script with no preamble or commentary."""

USER_PROMPT_TEMPLATE = """I am redoing a new and improved version of my course Web Designer Sales Mastery.
Below is the original script for one of the videos. Please rewrite it so it is better — more engaging,
updated info, new ideas, and as helpful as possible to my students.

ORIGINAL SCRIPT:
{transcript}"""


def optimize_transcript(transcript: str, api_key: str) -> str:
    """Use OpenAI to rewrite/optimize the transcript."""
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(transcript=transcript)},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content
