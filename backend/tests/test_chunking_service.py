from app.services.chunking_service import chunk_pages


def test_chunking_produces_chunks():
    """A page with text should produce at least one chunk."""
    pages = [{"page": 1, "text": "a" * 600}]
    chunks = chunk_pages(pages)

    assert len(chunks) > 0
    assert chunks[0]["page"] == 1


def test_chunking_respects_chunk_size():
    """No chunk should exceed the configured CHUNK_SIZE."""
    pages = [{"page": 1, "text": "a" * 1200}]
    chunks = chunk_pages(pages)

    for chunk in chunks:
        assert len(chunk["text"]) <= 500