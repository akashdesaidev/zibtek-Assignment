from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict
import logging
import uuid

from app.core.config import settings

logger = logging.getLogger(__name__)


class QdrantService:
    """Service for interacting with Qdrant vector database"""
    
    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME
    
    def collection_exists(self) -> bool:
        """Check if collection exists"""
        try:
            collections = self.client.get_collections().collections
            return any(col.name == self.collection_name for col in collections)
        except Exception as e:
            logger.error(f"Error checking collection: {e}")
            return False
    
    def create_collection(self, vector_size: int = 1536):
        """
        Create a new collection
        
        Args:
            vector_size: Size of embedding vectors (1536 for text-embedding-3-small/ada-002)
        """
        try:
            if not self.collection_exists():
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                logger.info(f"Collection already exists: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            raise
    
    def upsert_documents(self, chunks: List[Dict[str, str]], embeddings: List[List[float]]):
        """
        Upsert document chunks with embeddings to Qdrant
        
        Args:
            chunks: List of document chunks with metadata
            embeddings: List of embedding vectors
        """
        try:
            points = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        'content': chunk['content'],
                        'url': chunk['metadata']['url'],
                        'title': chunk['metadata']['title'],
                        'chunk_index': chunk['metadata']['chunk_index']
                    }
                )
                points.append(point)
            
            # Upsert in batches
            batch_size = 100
            for i in range(0, len(points), batch_size):
                batch = points[i:i + batch_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )
            
            logger.info(f"Upserted {len(points)} points to Qdrant")
        except Exception as e:
            logger.error(f"Error upserting documents: {e}")
            raise
    
    def search(self, query_vector: List[float], limit: int = 5) -> List[Dict]:
        """
        Search for similar documents
        
        Args:
            query_vector: Query embedding vector
            limit: Number of results to return
            
        Returns:
            List of search results with content and metadata
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )
            
            return [
                {
                    'content': result.payload['content'],
                    'url': result.payload['url'],
                    'title': result.payload['title'],
                    'score': result.score
                }
                for result in results
            ]
        except Exception as e:
            logger.error(f"Error searching Qdrant: {e}")
            raise
    
    def delete_collection(self):
        """Delete the collection"""
        try:
            if self.collection_exists():
                self.client.delete_collection(collection_name=self.collection_name)
                logger.info(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise


# Global instance
qdrant_service = QdrantService()


