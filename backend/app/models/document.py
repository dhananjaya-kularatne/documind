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
    """A question asked about a specific document"""
    session_id: str
    question: str

class ChunkResult(BaseModel):
    """A single retrieved chunk."""
    text: str
    page: int
    chunk_index: int
    distance: float

class QueryResponse(BaseModel):
    """Raw retrieval results for a question."""
    document_id: str
    question: str
    results: list[ChunkResult]

class AskRequest(BaseModel):
    """A question asked about a document, expecting a generated answer"""
    session_id: str
    question: str

class SourceChunk(BaseModel):
    """A cunk cited as a source for the answer"""
    page: int
    text: str

class AskResponse(BaseModel):
    """A generated, grounded answer with citations"""
    document_id: str 
    question:str
    answer: str
    sources: list[SourceChunk]