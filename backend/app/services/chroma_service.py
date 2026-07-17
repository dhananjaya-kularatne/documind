import chromadb

_client = chromadb.PersistentClient(path="./chroma_db")


def get_collection_name(session_id: str, document_id: str) -> str:
    return f"session_{session_id}_doc_{document_id}"


def store_chunks(session_id: str, document_id: str, chunks: list[dict], embeddings: list[list[float]]):
    """
    Store chunk text + embeddings in a Chroma collection scoped to this session and document.
    """ 
    collection_name = get_collection_name(session_id, document_id)
    collection = _client.get_or_create_collection(name=collection_name)

    ids = [f"chunk_{c['chunk_index']}" for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [{"page": c["page"], "chunk_index": c["chunk_index"]} for c in chunks]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )


def query_collection(session_id: str, document_id: str, query_embedding: list[float], top_k: int = 5):
    """
    Retrieve the top_k most relevant chunks for a query embedding.
    """
    collection_name = get_collection_name(session_id, document_id)
    collection = _client.get_collection(name=collection_name)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results