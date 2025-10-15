import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Set, Dict
import time
import logging
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class WebScraper:
    """Web scraper for extracting content from websites"""
    
    def __init__(self, base_url: str, max_pages: int = 100, cache_file: str = None):
        self.base_url = base_url
        self.max_pages = max_pages
        self.visited_urls: Set[str] = set()
        self.documents: List[Dict[str, str]] = []
        self.cache_file = cache_file or f"scraped_content_{urlparse(base_url).netloc.replace('.', '_')}.json"
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL belongs to the base domain"""
        parsed_base = urlparse(self.base_url)
        parsed_url = urlparse(url)
        return parsed_base.netloc == parsed_url.netloc
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text.strip()
    
    def extract_content(self, url: str) -> Dict[str, str]:
        """Extract content from a single page"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get page title
            title = soup.find('title')
            title_text = title.get_text() if title else url
            
            # Extract main content
            # Try to find main content areas
            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            
            if main_content:
                text = main_content.get_text(separator=' ', strip=True)
                text = self.clean_text(text)
                
                return {
                    'url': url,
                    'title': title_text,
                    'content': text
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {e}")
            return None
    
    def get_links(self, url: str, soup: BeautifulSoup) -> List[str]:
        """Extract all valid links from a page"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            
            # Only include URLs from the same domain
            if self.is_valid_url(full_url) and full_url not in self.visited_urls:
                # Remove fragments
                full_url = full_url.split('#')[0]
                links.append(full_url)
        
        return links
    
    def save_to_file(self, documents: List[Dict[str, str]]) -> None:
        """Save scraped documents to a JSON file"""
        try:
            # Create data directory if it doesn't exist
            os.makedirs("data", exist_ok=True)
            
            cache_data = {
                "base_url": self.base_url,
                "scraped_at": datetime.now().isoformat(),
                "total_documents": len(documents),
                "documents": documents
            }
            
            file_path = os.path.join("data", self.cache_file)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(documents)} documents to {file_path}")
            
        except Exception as e:
            logger.error(f"Error saving documents to file: {e}")
            raise
    
    def load_from_file(self) -> List[Dict[str, str]]:
        """Load scraped documents from a JSON file"""
        try:
            file_path = os.path.join("data", self.cache_file)
            
            if not os.path.exists(file_path):
                logger.info(f"Cache file {file_path} does not exist")
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            documents = cache_data.get("documents", [])
            scraped_at = cache_data.get("scraped_at", "Unknown")
            
            logger.info(f"Loaded {len(documents)} documents from cache (scraped at: {scraped_at})")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading documents from file: {e}")
            return []
    
    def crawl(self) -> List[Dict[str, str]]:
        """Crawl the website and extract content"""
        to_visit = [self.base_url]
        
        while to_visit and len(self.visited_urls) < self.max_pages:
            url = to_visit.pop(0)
            
            if url in self.visited_urls:
                continue
            
            logger.info(f"Crawling: {url}")
            self.visited_urls.add(url)
            
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract content
                doc = self.extract_content(url)
                if doc and len(doc['content']) > 100:  # Only include pages with substantial content
                    self.documents.append(doc)
                    logger.info(f"Extracted content from: {url}")
                
                # Get new links to visit
                new_links = self.get_links(url, soup)
                to_visit.extend(new_links)
                
                # Be respectful - add delay
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error crawling {url}: {e}")
        
        logger.info(f"Crawled {len(self.visited_urls)} pages, extracted {len(self.documents)} documents")
        
        # Save to file for future use
        if self.documents:
            self.save_to_file(self.documents)
        
        return self.documents
    
    def crawl_or_load(self, force_refresh: bool = False) -> List[Dict[str, str]]:
        """
        Crawl website or load from cache
        
        Args:
            force_refresh: If True, always crawl fresh. If False, try to load from cache first.
            
        Returns:
            List of documents
        """
        if not force_refresh:
            # Try to load from cache first
            cached_documents = self.load_from_file()
            if cached_documents:
                logger.info("Using cached content. Set force_refresh=True to crawl fresh.")
                return cached_documents
        
        # Cache miss or force refresh - crawl fresh
        logger.info("Crawling fresh content...")
        return self.crawl()


def scrape_website(base_url: str, max_pages: int = 50, force_refresh: bool = False) -> List[Dict[str, str]]:
    """
    Scrape a website and return documents (with caching)
    
    Args:
        base_url: The base URL to start crawling from
        max_pages: Maximum number of pages to crawl
        force_refresh: If True, always crawl fresh. If False, try to load from cache first.
        
    Returns:
        List of documents with url, title, and content
    """
    scraper = WebScraper(base_url, max_pages)
    return scraper.crawl_or_load(force_refresh=force_refresh)


