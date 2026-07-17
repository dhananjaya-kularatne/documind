import os
from pymongo import MongoClient
from datetime import datetime

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
        "uploaded_at": datetime.utcnow()
    }
    documents_collection.insert_one(record)
    return record