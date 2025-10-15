from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime
import logging
from pydantic import BaseModel

from app.core.database import get_db, Conversation, Message
from app.models.schemas import (
    ConversationCreate,
    ConversationResponse,
    ConversationWithMessages,
    ConversationList,
    MessageResponse
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/new", response_model=ConversationResponse)
async def create_conversation(
    request: ConversationCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new conversation
    
    Args:
        request: Conversation creation request
        db: Database session
        
    Returns:
        Created conversation
    """
    try:
        conversation = Conversation(
            id=str(uuid.uuid4()),
            title=request.title or "New Chat",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        logger.info(f"Created conversation: {conversation.id}")
        return conversation
        
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating conversation")


@router.get("/conversations", response_model=ConversationList)
async def get_conversations(db: Session = Depends(get_db)):
    """
    Get all conversations
    
    Args:
        db: Database session
        
    Returns:
        List of conversations
    """
    try:
        conversations = db.query(Conversation).order_by(
            Conversation.updated_at.desc()
        ).all()
        
        return ConversationList(conversations=conversations)
        
    except Exception as e:
        logger.error(f"Error getting conversations: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving conversations")


@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
async def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific conversation with messages
    
    Args:
        conversation_id: ID of the conversation
        db: Database session
        
    Returns:
        Conversation with messages
    """
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp).all()
        
        return ConversationWithMessages(
            id=conversation.id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=[MessageResponse.from_orm(msg) for msg in messages]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving conversation")


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a conversation
    
    Args:
        conversation_id: ID of the conversation
        db: Database session
        
    Returns:
        Success message
    """
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        db.delete(conversation)
        db.commit()
        
        logger.info(f"Deleted conversation: {conversation_id}")
        return {"message": "Conversation deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting conversation")


class TitleUpdate(BaseModel):
    """Request model for updating conversation title"""
    title: str


@router.put("/conversations/{conversation_id}/title")
async def update_conversation_title(
    conversation_id: str,
    request: TitleUpdate,
    db: Session = Depends(get_db)
):
    """
    Update conversation title
    
    Args:
        conversation_id: ID of the conversation
        request: Title update request
        db: Database session
        
    Returns:
        Updated conversation
    """
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        conversation.title = request.title
        conversation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(conversation)
        
        return conversation
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating conversation title: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating conversation")


