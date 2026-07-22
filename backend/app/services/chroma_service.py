import chromadb

_client = chromadb.PersistentClient(path="./chroma_db")


def get_collection_name(session_id: str) -> str:
    return f"session_{session_id}"


def store_chunks(session_id: str, document_id: str, filename: str, chunks: list[dict], embeddings: list[list[float]]):
    """
    Store chunk text + embeddings in a Chroma collection scoped to this session and document.
    Each chunk is tagged with its document_id and filename for later filtering.
    """ 
    collection_name = get_collection_name(session_id)
    collection = _client.get_or_create_collection(name=collection_name)

    ids = [f"{document_id}_chunk_{c['chunk_index']}" for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [
        {
            "document_id": document_id,
            "filename": filename,
            "page": c["page"],
            "chunk_index": c["chunk_index"]
        }
        for c in chunks
    ]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )


def query_collection(session_id: str, query_embedding: list[float], top_k: int = 5, document_ids: list[str] | None = None):
    """
    Retrieve the top_k most relevant chunks for a query embedding, optionally filtered to specific document_ids.
    """
    collection_name = get_collection_name(session_id)
    collection = _client.get_collection(name=collection_name)

    where_filter = {"document_id": {"$in": document_ids}} if document_ids else None

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where_filter
    )
    return results