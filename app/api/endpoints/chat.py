import uuid
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.deps import get_database_session
from app.models.schemas import StreamChatRequest, StreamChatChunk, HealthCheck
from app.models.database import ChatMessage
from app.agents.langgraph_workflow import chat_workflow
from app.core.config import settings
from app.core.rate_limiter import limiter

router = APIRouter()

@router.post("/stream")
@limiter.limit(f"{settings.rate_limit_requests}/minute")
async def stream_chat(request: Request, chat_request: StreamChatRequest, db: Session = Depends(get_database_session)):
    session_id = chat_request.session_id or str(uuid.uuid4())
    
    # Save user message
    user_message = ChatMessage(
        session_id=session_id,
        message_id=str(uuid.uuid4()),
        role="user",
        content=chat_request.message
    )
    db.add(user_message)
    db.commit()
    
    async def generate_stream():
        ai_message_id = str(uuid.uuid4())
        full_response = ""
        
        async for chunk in chat_workflow.process_message_stream(
            chat_request.message, 
            chat_request.temperature, 
            chat_request.max_tokens
        ):
            full_response += chunk
            chunk_data = StreamChatChunk(
                content=chunk,
                session_id=session_id,
                message_id=ai_message_id
            )
            yield f"data: {chunk_data.model_dump_json()}\n\n"
        
        # Save AI response
        ai_message = ChatMessage(
            session_id=session_id,
            message_id=ai_message_id,
            role="assistant",
            content=full_response
        )
        db.add(ai_message)
        db.commit()
        
        # Final chunk
        final_chunk = StreamChatChunk(content="", is_complete=True, session_id=session_id, message_id=ai_message_id)
        yield f"data: {final_chunk.model_dump_json()}\n\n"
    
    return StreamingResponse(generate_stream(), media_type="text/event-stream")

@router.get("/health", response_model=HealthCheck)
async def health_check():
    try:
        from app.core.database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = True
    except:
        db_status = False
    
    return HealthCheck(
        status="healthy" if db_status else "unhealthy",
        timestamp=datetime.utcnow(),
        version=settings.app_version,
        database=db_status,
        redis=True
    )
