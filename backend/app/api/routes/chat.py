from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.database import get_db, Message
from app.models.schemas import MessageRequest, ChatResponse
from app.services.langchain_rag import rag_service
from app.core.security import prompt_injection_detector
from app.utils.logger import log_query

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/debug/rag-test")
async def test_rag_pipeline():
    """
    Debug endpoint to test RAG pipeline functionality
    """
    try:
        test_query = "What services does Zibtek offer?"
        logger.info(f"Testing RAG pipeline with query: {test_query}")
        
        # Test context retrieval
        context, sources = rag_service.retrieve_context(test_query)
        
        return {
            "query": test_query,
            "context_found": bool(context),
            "context_length": len(context),
            "sources_count": len(sources),
            "sources": sources,
            "context_preview": context[:500] + "..." if len(context) > 500 else context
        }
    except Exception as e:
        logger.error(f"Error in RAG test: {e}")
        raise HTTPException(status_code=500, detail=f"RAG test failed: {str(e)}")


@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: MessageRequest,
    db: Session = Depends(get_db)
):
    """
    Send a message and get a response
    
    Args:
        request: Message request with conversation_id and message
        db: Database session
        
    Returns:
        Chat response with message and sources
    """
    try:
        # Check for prompt injection
        is_injection, injection_msg = prompt_injection_detector.detect(request.message)
        if is_injection:
            return ChatResponse(
                message=injection_msg,
                sources=[],
                conversation_id=request.conversation_id
            )
        
        # Sanitize input
        sanitized_message = prompt_injection_detector.sanitize(request.message)
        
        # Get chat history
        chat_history = db.query(Message).filter(
            Message.conversation_id == request.conversation_id
        ).order_by(Message.timestamp).all()
        
        # Format history for RAG
        history_list = [
            {"role": msg.role, "content": msg.content}
            for msg in chat_history
        ]
        
        # Generate response using RAG
        response_text, sources = rag_service.generate_response(
            query=sanitized_message,
            chat_history=history_list
        )
        
        # Save user message
        user_message = Message(
            conversation_id=request.conversation_id,
            role="user",
            content=request.message
        )
        db.add(user_message)
        
        # Save assistant response
        assistant_message = Message(
            conversation_id=request.conversation_id,
            role="assistant",
            content=response_text
        )
        db.add(assistant_message)
        db.commit()
        
        # Log the query and response
        log_query(
            db=db,
            conversation_id=request.conversation_id,
            user_query=request.message,
            bot_response=response_text,
            sources=sources
        )
        
        return ChatResponse(
            message=response_text,
            sources=sources,
            conversation_id=request.conversation_id
        )
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error processing message")


