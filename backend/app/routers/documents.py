import os
import tempfile
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, File, Form, UploadFile

from app.models.document import DocumentResponse
from app.services.chroma_service import get_collection_name, store_chunks
from app.services.chunking_service import chunk_pages
from app.services.embedding_service import embed_texts
from app.services.mongo_service import create_document_record
from app.services.pdf_service import extract_text_by_page

router = APIRouter()


@router.post("/documents", response_model=list[DocumentResponse])
async def upload_documents(files: list[UploadFile] = File(...), session_id: str | None = Form(None)):
    """Upload one or more PDFs into a session, extract, chunk, embed, and store each."""

    if session_id is None:
        session_id = str(uuid.uuid4())

    results = []

    for file in files:
        document_id = str(uuid.uuid4())

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        pages = extract_text_by_page(tmp_path)
        os.remove(tmp_path)

        chunks = chunk_pages(pages)

        if not chunks:
            create_document_record(
                document_id=document_id,
                session_id=session_id,
                filename=file.filename,
                page_count=len(pages),
                chunk_count=0,
                chroma_collection=""
            )
            results.append(DocumentResponse(
                document_id=document_id,
                session_id=session_id,
                filename=file.filename,
                page_count=len(pages),
                chunk_count=0,
                status="no_extractable_text",
                uploaded_at=datetime.now(timezone.utc)
            ))
            continue

        chunk_texts = [c["text"] for c in chunks]
        embeddings = embed_texts(chunk_texts)

        collection_name = get_collection_name(session_id)
        store_chunks(session_id, document_id, file.filename, chunks, embeddings)

        create_document_record(
            document_id=document_id,
            session_id=session_id,
            filename=file.filename,
            page_count=len(pages),
            chunk_count=len(chunks),
            chroma_collection=collection_name
        )

        results.append(DocumentResponse(
            document_id=document_id,
            session_id=session_id,
            filename=file.filename,
            page_count=len(pages),
            chunk_count=len(chunks),
            status="processed",
            uploaded_at=datetime.now(timezone.utc)
        ))

    return results