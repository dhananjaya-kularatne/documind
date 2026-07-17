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
    
    