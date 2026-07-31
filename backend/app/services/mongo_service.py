import os
from pymongo import MongoClient
from datetime import datetime, timezone

_client = MongoClient(os.getenv("MONGODB_URI"))
_db = _client[os.getenv("MONGODB_DB_NAME")]

documents_collection = _db["documents"]
conversations_collection = _db["conversations"]


def create_document_record(document_id: str, session_id: str, filename: str,
                             page_count: int, chunk_count: int, chroma_collection: str) -> dict:
    """
    Insert a new document record after successful upload + processing.
    """
    record = {
        "_id": document_id,
        "session_id": session_id,
        "filename": filename,
        "page_count": page_count,
        "chunk_count": chunk_count,
        "chroma_collection": chroma_collection,
        "status": "processed",
        "uploaded_at": datetime.now(timezone.utc)
    }
    documents_collection.insert_one(record)
    return record

def save_conversation(session_id: str, question: str, answer: str, source_chunks: list[dict]) -> dict:
    """
    Log a question/answer pair for a document.
    """
    record = {
        "session_id": session_id,
        "question": question, 
        "answer": answer, 
        "source_chunks": source_chunks,
        "created_at": datetime.now(timezone.utc)
    }

    conversations_collection.insert_one(record)
    return record

async def list_session_documents(session_id: str) -> list[dict]:
    """
    Return the true, authoritative list of documents for a session,
    read directly from MongoDB rather than trusted from frontend state.
    """
    cursor = documents_collection.find({"session_id": session_id})
    return list(cursor)


def delete_document_record(document_id: str) -> None:
    """Remove a document's metadata record from MongoDB."""
    documents_collection.delete_one({"_id": document_id})