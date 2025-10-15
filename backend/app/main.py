from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

from app.core.config import settings
from app.core.database import init_db
from app.api.routes import chat, conversations
from app.models.schemas import HealthCheck


# =========================================
# 1️⃣ Configure Logging FIRST
# =========================================
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),  # Console output
        # logging.FileHandler("app.log"),  # Optional file output
    ],
    force=True  # Override any existing logging setup (important for uvicorn)
)

# Create main logger
logger = logging.getLogger("zibtek")
logger.setLevel(logging.INFO)

# Align uvicorn log levels
logging.getLogger("uvicorn").setLevel(logging.INFO)
logging.getLogger("uvicorn.error").setLevel(logging.INFO)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("uvicorn.asgi").setLevel(logging.WARNING)


# =========================================
# 2️⃣ LangSmith Tracing Setup
# =========================================
if settings.LANGSMITH_TRACING and settings.LANGSMITH_TRACING.lower() == "true":
    try:
        from langsmith import Client
        from langchain_core.tracers import LangChainTracer

        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        if settings.LANGSMITH_ENDPOINT:
            os.environ["LANGCHAIN_ENDPOINT"] = settings.LANGSMITH_ENDPOINT
        if settings.LANGSMITH_API_KEY:
            os.environ["LANGCHAIN_API_KEY"] = settings.LANGSMITH_API_KEY
        if settings.LANGSMITH_PROJECT:
            os.environ["LANGCHAIN_PROJECT"] = settings.LANGSMITH_PROJECT

        logger.info("✅ LangSmith tracing enabled")
    except ImportError:
        logger.warning("⚠️ LangSmith not installed. Run: pip install langsmith")
else:
    logger.info("🚫 LangSmith tracing disabled")


# =========================================
# 3️⃣ FastAPI App Initialization
# =========================================
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI Chatbot for Zibtek using RAG and LangChain",
)

# =========================================
# 4️⃣ Middleware & Routes
# =========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
app.include_router(conversations.router, prefix=f"{settings.API_V1_STR}/chat", tags=["conversations"])


# =========================================
# 5️⃣ Events
# =========================================
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting up Zibtek AI Chatbot...")
    logger.info("📊 Initializing database...")
    init_db()
    logger.info("✅ Database initialized successfully")
    logger.info("🎯 Application ready to serve requests!")


# =========================================
# 6️⃣ Health Endpoints
# =========================================
@app.get("/", response_model=HealthCheck)
async def health_check():
    logger.info("🏥 Health check accessed at '/'")
    return HealthCheck(
        status="healthy",
        message=f"{settings.PROJECT_NAME} is running",
    )


@app.get("/health", response_model=HealthCheck)
async def health():
    logger.info("🏥 Health check accessed at '/health'")
    return HealthCheck(
        status="healthy",
        message="Service is healthy",
    )


# =========================================
# 7️⃣ Run
# =========================================
if __name__ == "__main__":
    import uvicorn

    logger.info("🧩 Starting Uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
