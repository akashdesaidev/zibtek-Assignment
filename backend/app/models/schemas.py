from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class MessageRequest(BaseModel):
    """Request model for sending a message"""
    conversation_id: str
    message: str


class MessageResponse(BaseModel):
    """Response model for a message"""
    role: str
    content: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    """Response model for chat"""
    message: str
    sources: List[str] = []
    conversation_id: str


class ConversationCreate(BaseModel):
    """Request model for creating a conversation"""
    title: Optional[str] = "New Chat"


class ConversationResponse(BaseModel):
    """Response model for a conversation"""
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ConversationWithMessages(BaseModel):
    """Response model for conversation with messages"""
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse]
    
    class Config:
        from_attributes = True


class ConversationList(BaseModel):
    """Response model for list of conversations"""
    conversations: List[ConversationResponse]


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    message: str


