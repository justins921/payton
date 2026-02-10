from notion_client import Client


def _text_to_blocks(text: str, heading: str) -> list[dict]:
    """Convert a text string into Notion blocks with a heading.

    Notion API limits rich_text arrays to 100 items and each item to 2000 chars,
    so we chunk the text accordingly.
    """
    blocks = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": heading}}]
            },
        }
    ]

    # Split text into chunks of 2000 chars for Notion's limit
    chunk_size = 2000
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    # Notion allows max 100 rich_text items per block, so batch into paragraphs
    for i in range(0, len(chunks), 100):
        batch = chunks[i:i + 100]
        rich_text = [
            {"type": "text", "text": {"content": chunk}} for chunk in batch
        ]
        blocks.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": rich_text},
            }
        )

    return blocks


def save_to_notion(
    notion_token: str,
    parent_page_id: str,
    title: str,
    original_transcript: str,
    optimized_transcript: str,
) -> str:
    """Create a new child page under the given parent with both transcripts.

    Returns the URL of the created Notion page.
    """
    client = Client(auth=notion_token)

    # Build all content blocks
    blocks = []
    blocks.append({
        "object": "block",
        "type": "divider",
        "divider": {},
    })
    blocks.extend(_text_to_blocks(original_transcript, "Original Transcript"))
    blocks.append({
        "object": "block",
        "type": "divider",
        "divider": {},
    })
    blocks.extend(_text_to_blocks(optimized_transcript, "Optimized Transcript"))

    # Notion API allows max 100 blocks per request
    # We'll create the page with the first batch then append the rest
    first_batch = blocks[:100]
    remaining = blocks[100:]

    page = client.pages.create(
        parent={"page_id": parent_page_id},
        properties={
            "title": [{"text": {"content": title}}]
        },
        children=first_batch,
    )

    page_id = page["id"]

    # Append remaining blocks in batches of 100
    while remaining:
        batch = remaining[:100]
        remaining = remaining[100:]
        client.blocks.children.append(block_id=page_id, children=batch)

    return page["url"]
