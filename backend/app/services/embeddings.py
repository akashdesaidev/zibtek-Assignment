from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from typing import List, Dict
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for creating text embeddings"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.OPENAI_EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def chunk_documents(self, documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Split documents into chunks
        
        Args:
            documents: List of documents with 'content', 'url', and 'title'
            
        Returns:
            List of chunks with metadata
        """
        chunks = []
        
        for doc in documents:
            # Split the content into chunks
            text_chunks = self.text_splitter.split_text(doc['content'])
            
            for i, chunk in enumerate(text_chunks):
                chunks.append({
                    'content': chunk,
                    'metadata': {
                        'url': doc['url'],
                        'title': doc['title'],
                        'chunk_index': i
                    }
                })
        
        logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
        return chunks
    
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for a list of texts
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.embeddings.embed_documents(texts)
            logger.info(f"Created {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"Error creating embeddings: {e}")
            raise


# Global instance
embedding_service = EmbeddingService()


