from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

from app.core.config import settings
from app.core.database import init_db
from app.api.routes import chat, conversations
from app.models.schemas import HealthCheck

# Initialize LangSmith tracing if configured
if settings.LANGSMITH_TRACING and settings.LANGSMITH_TRACING.lower() == "true":
    try:
        from langsmith import Client
        from langchain_core.tracers import LangChainTracer
        
        # Set LangSmith environment variables
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        if settings.LANGSMITH_ENDPOINT:
            os.environ["LANGCHAIN_ENDPOINT"] = settings.LANGSMITH_ENDPOINT
        if settings.LANGSMITH_API_KEY:
            os.environ["LANGCHAIN_API_KEY"] = settings.LANGSMITH_API_KEY
        if settings.LANGSMITH_PROJECT:
            os.environ["LANGCHAIN_PROJECT"] = settings.LANGSMITH_PROJECT
        
        logging.info("LangSmith tracing enabled")
    except ImportError:
        logging.warning("LangSmith not installed. Install with: pip install langsmith")
else:
    logging.info("LangSmith tracing disabled")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI Chatbot for Zibtek using RAG and LangChain"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
app.include_router(conversations.router, prefix=f"{settings.API_V1_STR}/chat", tags=["conversations"])


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Starting up application...")
    init_db()
    logger.info("Database initialized")


@app.get("/", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck(
        status="healthy",
        message=f"{settings.PROJECT_NAME} is running"
    )


@app.get("/health", response_model=HealthCheck)
async def health():
    """Health check endpoint"""
    return HealthCheck(
        status="healthy",
        message="Service is healthy"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


