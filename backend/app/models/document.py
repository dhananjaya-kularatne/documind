from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    """Returned after a successfull pdf upload"""
    document_id: str
    session_id: str
    filename: str
    page_count: int
    chunk_count: int
    status: str
    uploaded_at: datetime

class QueryRequest(BaseModel):
    """A question asked about documents in a session."""
    session_id: str
    question: str
    document_ids: list[str] | None = None

class ChunkResult(BaseModel):
    """A single retrieved chunk."""
    text: str
    filename: str
    page: int
    chunk_index: int
    distance: float

class QueryResponse(BaseModel):
    """Raw retrieval results for a question."""
    session_id: str
    question: str
    results: list[ChunkResult]

class AskRequest(BaseModel):
    """A question asked about documents inn a session, expecting a generated answer"""
    session_id: str
    question: str
    document_ids: list[str] | None = None

class SourceChunk(BaseModel):
    """A cunk cited as a source for the answer"""
    filename: str
    page: int
    text: str

class AskResponse(BaseModel):
    """A generated, grounded answer with citations"""
    session_id: str 
    question:str
    answer: str
    sources: list[SourceChunk]