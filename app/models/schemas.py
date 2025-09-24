from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StreamChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1000
    stream: bool = True

class StreamChatChunk(BaseModel):
    content: str
    is_complete: bool = False
    session_id: Optional[str] = None
    message_id: Optional[str] = None

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str
    database: bool
    redis: bool
