"""
Reranker service for improving context relevance
Uses BGE-Reranker (BAAI/bge-reranker-large) from HuggingFace
Fast, local, no API calls needed!
"""
import logging
from typing import List, Dict, Optional
from sentence_transformers import CrossEncoder
import torch

from app.core.config import settings

logger = logging.getLogger(__name__)


class RerankerService:
    """Service for reranking retrieved documents using BGE-Reranker"""
    
    def __init__(self):
        """Initialize BGE reranker model"""
        self.model = None
        self.enabled = settings.USE_RERANKER
        
        if self.enabled:
            try:
                logger.info(f"Loading reranker model: {settings.RERANK_MODEL}")
                
                # Determine device
                device = "cuda" if torch.cuda.is_available() else "cpu"
                logger.info(f"Using device: {device}")
                
                # Load BGE reranker model
                self.model = CrossEncoder(
                    settings.RERANK_MODEL,
                    max_length=512,
                    device=device
                )
                
                logger.info(f"Reranker initialized successfully with {settings.RERANK_MODEL}")
                
            except Exception as e:
                logger.error(f"Failed to initialize BGE reranker: {e}")
                logger.info("Reranker will be disabled")
                self.enabled = False
        else:
            logger.info("Reranker disabled in settings")
    
    def rerank_documents(
        self,
        query: str,
        documents: List[Dict[str, any]],
        top_n: Optional[int] = None,
        threshold: Optional[float] = None
    ) -> List[Dict[str, any]]:
        """
        Rerank documents based on relevance to query using BGE model
        
        Args:
            query: User query
            documents: List of document dicts with 'content', 'url', 'score' keys
            top_n: Number of top results to return (default: from settings)
            threshold: Minimum relevance score 0-1 (default: from settings)
            
        Returns:
            Reranked and filtered list of documents with updated scores
        """
        if not self.enabled or not documents:
            logger.info("Reranker not enabled or no documents to rerank")
            return documents
        
        if not self.model:
            logger.warning("Reranker model not initialized")
            return documents
        
        try:
            # Use settings defaults if not provided
            top_n = top_n or settings.RERANK_TOP_N
            threshold = threshold or settings.RERANK_THRESHOLD
            
            logger.info(f"Reranking {len(documents)} documents with top_n={top_n}, threshold={threshold}")
            
            # Prepare query-document pairs for the model
            pairs = [[query, doc['content'][:512]] for doc in documents]
            
            # Get relevance scores from BGE model
            # BGE outputs logits, we'll normalize them to 0-1 range using sigmoid
            scores = self.model.predict(pairs, batch_size=settings.RERANK_BATCH_SIZE)
            
            # Apply sigmoid to convert logits to probabilities (0-1 range)
            import numpy as np
            scores = 1 / (1 + np.exp(-scores))  # Sigmoid function
            
            # Create reranked document list with scores
            scored_docs = []
            for idx, (doc, score) in enumerate(zip(documents, scores)):
                scored_doc = {
                    'content': doc['content'],
                    'url': doc['url'],
                    'original_score': doc['score'],  # Vector similarity score
                    'rerank_score': float(score),    # BGE relevance score
                    'score': float(score)            # Use rerank score as primary
                }
                scored_docs.append(scored_doc)
                
                logger.debug(
                    f"Doc {idx}: original_score={doc['score']:.3f}, "
                    f"rerank_score={float(score):.3f}"
                )
            
            # Sort by rerank score (descending)
            scored_docs.sort(key=lambda x: x['rerank_score'], reverse=True)
            
            # Log rerank score distribution
            rerank_scores = [doc['rerank_score'] for doc in scored_docs]
            logger.info(f"Rerank score distribution - Min: {min(rerank_scores):.3f}, Max: {max(rerank_scores):.3f}, Avg: {sum(rerank_scores)/len(rerank_scores):.3f}")
            
            # Filter by threshold first, then limit to top_n
            reranked_docs = []
            filtered_out_count = 0
            
            # First, filter by threshold
            for i, doc in enumerate(scored_docs):
                if doc['rerank_score'] >= threshold:
                    reranked_docs.append(doc)
                    logger.debug(f"Doc {i+1}: rerank_score={doc['rerank_score']:.3f} ✅ (above threshold {threshold})")
                else:
                    filtered_out_count += 1
                    logger.info(f"Doc {i+1}: rerank_score={doc['rerank_score']:.3f} ❌ (below threshold {threshold})")
            
            # Then limit to top_n
            if len(reranked_docs) > top_n:
                logger.info(f"Limiting {len(reranked_docs)} threshold-passing docs to top {top_n}")
                reranked_docs = reranked_docs[:top_n]
            
            logger.info(f"Reranking filter results: {len(reranked_docs)} final docs (from {len(scored_docs)} total, {filtered_out_count} filtered out by threshold)")
            
            logger.info(
                f"Reranking complete: {len(documents)} → {len(reranked_docs)} documents "
                f"(filtered by threshold {threshold})"
            )
            
            return reranked_docs
            
        except Exception as e:
            logger.error(f"Error during reranking: {e}")
            logger.info("Falling back to original document order")
            return documents
    
    def is_enabled(self) -> bool:
        """Check if reranker is enabled and available"""
        return self.enabled and self.model is not None


# Global instance
reranker_service = RerankerService()
