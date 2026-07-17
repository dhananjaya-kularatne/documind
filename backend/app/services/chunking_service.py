CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def chunk_pages(pages: list[dict]) -> list[dict]:
    """
    Split page text into overlapping chunks.
    Input:  [{"page": 1, "text": "..."}, ...]
    Output: [{"page": 1, "chunk_index": 0, "text": "..."}, ...]
    """
    chunks = []
    chunk_index = 0

    for page in pages:
        text = page["text"]
        start = 0

        while start < len(text):
            end = start + CHUNK_SIZE
            chunk_text = text[start:end]

            chunks.append({
                "page": page["page"],
                "chunk_index": chunk_index,
                "text": chunk_text
            })

            chunk_index += 1
            start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks