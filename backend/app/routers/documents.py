import os
import uuid
import tempfile
from fastapi import APIRouter, UploadFile, Form
from datetime import datetime

from app.models.document import DocumentResponse
from app.services.pdf_service import extract_text_by_page
from app.services.chunking_service import chunk_pages
from app.services.embedding_service import embed_texts
from app.services.chroma_service import store_chunks, get_collection_name
from app.services.mongo_service import create_document_record

router = APIRouter()


@router.post("/documents", response_model=DocumentResponse)
async def upload_document(file: UploadFile, session_id: str | None = Form(None)):
    """Upload a PDF, extract text, chunk it, embed it, and store it."""

    if session_id is None:
        session_id = str(uuid.uuid4())

    document_id = str(uuid.uuid4())

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    pages = extract_text_by_page(tmp_path)
    os.remove(tmp_path)

    chunks = chunk_pages(pages)
    chunk_texts = [c["text"] for c in chunks]
    embeddings = embed_texts(chunk_texts)

    collection_name = get_collection_name(session_id, document_id)
    store_chunks(session_id, document_id, chunks, embeddings)

    create_document_record(
        document_id=document_id,
        session_id=session_id,
        filename=file.filename,
        page_count=len(pages),
        chunk_count=len(chunks),
        chroma_collection=collection_name
    )

    return DocumentResponse(
        document_id=document_id,
        session_id=session_id,
        filename=file.filename,
        page_count=len(pages),
        chunk_count=len(chunks),
        status="processed",
        uploaded_at=datetime.utcnow()
    )