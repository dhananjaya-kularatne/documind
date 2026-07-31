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
    distances = raw_results["distances"][0]

    # Only keep chunks that are genuinely relevant — Chroma always returns
    # up to top_k results regardless of how weak the match is, so without this
    # filter, unrelated chunks get shown as citations just to fill out the count.
    # Lower distance = more similar.
    DISTANCE_THRESHOLD = 1.3

    chunks = [
        {"text": text, "page": metadata["page"], "filename": metadata["filename"]}
        for text, metadata, distance in zip(documents, metadatas, distances)
        if distance < DISTANCE_THRESHOLD
    ]

    # If filtering removed everything, fall back to the single best match rather than giving the LLM zero context to work with.
    if not chunks and documents:
        chunks = [{"text": documents[0], "page": metadatas[0]["page"], "filename": metadatas[0]["filename"]}]

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