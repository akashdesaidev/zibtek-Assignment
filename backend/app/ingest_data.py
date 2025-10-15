"""
Data ingestion script to scrape website and populate Qdrant
"""
import logging
from app.core.config import settings
from app.services.scraper import scrape_website
from app.services.embeddings import embedding_service
from app.services.qdrant_service import qdrant_service

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def ingest_data():
    """Main data ingestion function"""
    try:
        logger.info("Starting data ingestion...")
        
        # Check if collection already exists
        if qdrant_service.collection_exists():
            logger.info("Collection already exists. Skipping ingestion.")
            logger.info("To re-ingest, delete the collection first.")
            return
        
        # Step 1: Scrape website
        logger.info(f"Scraping website: {settings.TARGET_WEBSITE}")
        documents = scrape_website(settings.TARGET_WEBSITE, max_pages=50)
        
        if not documents:
            logger.error("No documents scraped. Exiting.")
            return
        
        logger.info(f"Scraped {len(documents)} documents")
        
        # Step 2: Chunk documents
        logger.info("Chunking documents...")
        chunks = embedding_service.chunk_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")
        
        # Step 3: Create embeddings
        logger.info("Creating embeddings...")
        texts = [chunk['content'] for chunk in chunks]
        embeddings = embedding_service.create_embeddings(texts)
        logger.info(f"Created {len(embeddings)} embeddings")
        
        # Step 4: Create Qdrant collection
        logger.info("Creating Qdrant collection...")
        qdrant_service.create_collection(vector_size=len(embeddings[0]))
        
        # Step 5: Upload to Qdrant
        logger.info("Uploading to Qdrant...")
        qdrant_service.upsert_documents(chunks, embeddings)
        
        logger.info("Data ingestion completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during data ingestion: {e}")
        raise


if __name__ == "__main__":
    ingest_data()


