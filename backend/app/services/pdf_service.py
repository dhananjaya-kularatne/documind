import pdfplumber


def extract_text_by_page(file_path: str) -> list[dict]:
    """
    Extract text from a PDF, one entry per page.
    Returns a list like: [{"page": 1, "text": "..."}, {"page": 2, "text": "..."}]
    """
    pages = []

    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                pages.append({"page": page_number, "text": text})

    return pages