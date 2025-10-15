from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    PROJECT_NAME: str = "Zibtek AI Chatbot"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-5"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-ada-002"
    
    # GPT-5 Specific Settings
    GPT5_REASONING_EFFORT: str = "medium"  # minimal, low, medium, high
    GPT5_VERBOSITY: str = "medium"  # low, medium, high
    
    # Qdrant
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION_NAME: str = "zibtek_docs"
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/chatbot.db"
    
    # Scraping
    TARGET_WEBSITE: str = "https://www.zibtek.com"
    
    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RESULTS: int = 20  # Initial retrieval from vector DB (before reranking)
    SIMILARITY_THRESHOLD: float = 0.1  # Lowered from 0.7 to allow more results for reranking
    
    # Reranker Settings (BGE-Reranker from HuggingFace)
    USE_RERANKER: bool = True
    RERANK_MODEL: str = "BAAI/bge-reranker-v2-m3"  # BGE reranker model (removed trailing comma)
    RERANK_TOP_N: int = 10  # Final number of results to keep after reranking
    RERANK_THRESHOLD: float = 0.3  # Minimum relevance score (0-1) - lowered to allow more results
    RERANK_BATCH_SIZE: int = 16  # Batch size for reranking
    
    # LangSmith Tracing (Optional)
    LANGSMITH_TRACING: Optional[str] = None
    LANGSMITH_ENDPOINT: Optional[str] = None
    LANGSMITH_API_KEY: Optional[str] = None
    LANGSMITH_PROJECT: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields instead of raising error


settings = Settings()


