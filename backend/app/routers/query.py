from fastapi import APIRouter
from app.models.document import QueryRequest, QueryResponse, ChunkResult
from app.services.embedding_service import embed_texts
from app.services.chroma_service import query_collection

router = APIRouter()


@router.post("/sessions/{session_id}/query", response_model=QueryResponse)
def query_session(session_id: str, request: QueryRequest):
    """Retrieve the most relevant chunks for a question, across the session (or a filtered subset of documents)."""

    question_embedding = embed_texts([request.question])[0]

    raw_results = query_collection(
        session_id=session_id,
        query_embedding=question_embedding,
        top_k=5,
        document_ids=request.document_ids
    )

    chunks = []
    documents = raw_results["documents"][0]
    metadatas = raw_results["metadatas"][0]
    distances = raw_results["distances"][0]

    for text, metadata, distance in zip(documents, metadatas, distances):
        chunks.append(ChunkResult(
            text=text,
            filename=metadata["filename"],
            page=metadata["page"],
            chunk_index=metadata["chunk_index"],
            distance=distance
        ))

    return QueryResponse(
        session_id=session_id,
        question=request.question,
        results=chunks
    )