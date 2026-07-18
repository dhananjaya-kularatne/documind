from fastapi import APIRouter
from app.models.document import AskRequest, AskResponse, SourceChunk
from app.services.embedding_service import embed_texts
from app.services.chroma_service import query_collection
from app.services.groq_service import generate_answer
from app.services.mongo_service import save_conversation

router = APIRouter()


@router.post("/documents/{document_id}/ask", response_model=AskResponse)
def ask_document(document_id: str, request: AskRequest):
    """Retrieve relevant chunks and generate a grounded answer with citations."""

    question_embedding = embed_texts([request.question])[0]

    raw_results = query_collection(
        session_id=request.session_id,
        document_id=document_id,
        query_embedding=question_embedding,
        top_k=5
    )

    documents = raw_results["documents"][0]
    metadatas = raw_results["metadatas"][0]

    chunks = [
        {"text": text, "page": metadata["page"]}
        for text, metadata in zip(documents, metadatas)
    ]

    answer = generate_answer(request.question, chunks)

    save_conversation(
        document_id=document_id,
        question=request.question,
        answer=answer,
        source_chunks=chunks
    )

    sources = [SourceChunk(page=c["page"], text=c["text"]) for c in chunks]

    return AskResponse(
        document_id=document_id,
        question=request.question,
        answer=answer,
        sources=sources
    )