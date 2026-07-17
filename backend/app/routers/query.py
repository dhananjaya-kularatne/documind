from fastapi import APIRouter
from app.models.document import QueryRequest, QueryResponse, ChunkResult
from app.services.embedding_service import embed_texts
from app.services.chroma_service import query_collection

router = APIRouter()


@router.post("/documents/{document_id}/query", response_model=QueryResponse)
def query_document(document_id: str, request: QueryRequest):
    """Retrieve the most relevant chunks for a question, scoped to one document."""

    question_embedding = embed_texts([request.question])[0]

    raw_results = query_collection(
        session_id=request.session_id,
        document_id=document_id,
        query_embedding=question_embedding,
        top_k=5
    )

    chunks = []
    documents = raw_results["documents"][0]
    metadatas = raw_results["metadatas"][0]
    distances = raw_results["distances"][0]

    for text, metadata, distance in zip(documents, metadatas, distances):
        chunks.append(ChunkResult(
            text=text,
            page=metadata["page"],
            chunk_index=metadata["chunk_index"],
            distance=distance
        ))

    return QueryResponse(
        document_id=document_id,
        question=request.question,
        results=chunks
    )