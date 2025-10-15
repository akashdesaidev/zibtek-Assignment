from sqlalchemy.orm import Session
from datetime import datetime
import json
import logging
from typing import List

from app.core.database import QueryLog

logger = logging.getLogger(__name__)


def log_query(
    db: Session,
    conversation_id: str,
    user_query: str,
    bot_response: str,
    sources: List[str]
):
    """
    Log a query and response to the database
    
    Args:
        db: Database session
        conversation_id: ID of the conversation
        user_query: User's query
        bot_response: Bot's response
        sources: List of source URLs
    """
    try:
        query_log = QueryLog(
            conversation_id=conversation_id,
            user_query=user_query,
            bot_response=bot_response,
            sources=json.dumps(sources),
            timestamp=datetime.utcnow()
        )
        db.add(query_log)
        db.commit()
        logger.info(f"Logged query for conversation {conversation_id}")
    except Exception as e:
        logger.error(f"Error logging query: {e}")
        db.rollback()


