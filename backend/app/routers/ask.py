from fastapi import APIRouter
from app.models.document import AskRequest, AskResponse, SourceChunk
from app.services.embedding_service import embed_texts
from app.services.chroma_service import query_collection
from app.services.groq_service import generate_answer
from app.services.mongo_service import save_conversation

router = APIRouter()


@router.post("/sessions/{session_id}/ask", response_model=AskResponse)
def ask_session(session_id: str, request: AskRequest):
    """Retrieve relevant chunks across the session and generate a grounded answer with citations."""

    question_embedding = embed_texts([request.question])[0]

    raw_results = query_collection(
        session_id=session_id,
        query_embedding=question_embedding,
        top_k=5,
        document_ids=request.document_ids
    )

    documents = raw_results["documents"][0]
    metadatas = raw_results["metadatas"][0]

    chunks = [
        {"text": text, "page": metadata["page"], "filename": metadata["filename"]}
        for text, metadata in zip(documents, metadatas)
    ]

    answer = generate_answer(request.question, chunks)

    save_conversation(
        session_id=session_id,
        question=request.question,
        answer=answer,
        source_chunks=chunks
    )

    sources = [SourceChunk(filename=c["filename"], page=c["page"], text=c["text"]) for c in chunks]

    return AskResponse(
        session_id=session_id,
        question=request.question,
        answer=answer,
        sources=sources
    )