import sys
import os
import logging
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup

# Add sibling folder to path (Jupyter notebook fix)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.env_loader import load_env, get_env_var
from utils.text_utils import split_text, safe_parse_json
from utils.llm_utils import create_llm, generate_flashcards
from utils.pinecone_utils import (
    init_pinecone, ensure_index, create_embeddings, upsert_flashcards
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DummyFlashcardGenerator:
    def __init__(self):
        """Initialize the flashcard generator with required configurations."""
        self.setup_environment()
        self.setup_components()
    
    def setup_environment(self) -> None:
        """Load environment variables and validate required keys."""
        try:
            load_env()
            self.openai_api_key = get_env_var("OPENAI_API_KEY")
            self.pinecone_api_key = get_env_var("PINECONE_API_KEY")
            logger.info("Environment variables loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load environment variables: {e}")
            raise
    
    def setup_components(self) -> None:
        """Initialize LLM, Pinecone, and embeddings."""
        try:
            self.llm = create_llm(self.openai_api_key)
            self.pc = init_pinecone(self.pinecone_api_key)
            self.index = ensure_index(self.pc)
            self.embedder = create_embeddings(self.openai_api_key)
            logger.info("Components initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            raise
    
    def fetch_web_content(self, url: str) -> str:
        """
        Fetch and clean web content from a given URL.
        
        Args:
            url: The URL to fetch content from
            
        Returns:
            Cleaned text content
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Remove unwanted tags
            unwanted_tags = ["script", "style", "head", "meta", "noscript", "footer", "nav"]
            for tag in soup(unwanted_tags):
                tag.decompose()
            
            # Get clean text
            main_content = soup.get_text(separator="\n", strip=True)
            logger.info(f"Successfully fetched content from {url}, length: {len(main_content)}")
            return main_content
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch content from {url}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while processing {url}: {e}")
            raise
    
    def process_content(self, content: str) -> List[Dict[str, Any]]:
        """
        Process content and generate flashcards.
        
        Args:
            content: Text content to process
            
        Returns:
            List of generated flashcards
        """
        try:
            chunks = split_text(content)
            
            # Skip header 
            chunks = chunks[1:]
            
            all_flashcards = []
            
            for i, chunk in enumerate(chunks):
                logger.info(f"Processing chunk {i+1}/{len(chunks)}")
                
                try:
                    chunk_output = generate_flashcards(self.llm, [chunk])
                    chunk_flashcards = safe_parse_json(chunk_output)
                    
                    if chunk_flashcards:
                        all_flashcards.extend(chunk_flashcards)
                        logger.info(f"Generated {len(chunk_flashcards)} flashcards from chunk {i+1}")
                    else:
                        logger.warning(f"No flashcards generated from chunk {i+1}")
                        
                except Exception as e:
                    logger.error(f"Failed to process chunk {i+1}: {e}")
                    continue
            
            logger.info(f"Total flashcards generated: {len(all_flashcards)}")
            return all_flashcards
            
        except Exception as e:
            logger.error(f"Failed to process content: {e}")
            raise
    
    
    def generate_flashcards_from_urls(self, urls: List[str]) -> None:
        """
        Main method to generate flashcards from a list of URLs.
        
        Args:
            urls: List of URLs to process
            clear_existing: Whether to clear existing Pinecone data
        """
        total_flashcards = 0
        
        for url in urls:
            logger.info(f"Processing URL: {url}")
            
            try:
                # Fetch and process content
                content = self.fetch_web_content(url)
                flashcards = self.process_content(content)
                
                # Upsert to Pinecone
                if flashcards:
                    upsert_flashcards(self.index, self.embedder, flashcards)
                    total_flashcards += len(flashcards)
                    logger.info(f"Successfully upserted {len(flashcards)} flashcards from {url}")
                else:
                    logger.warning(f"No flashcards generated from {url}")
                    
            except Exception as e:
                logger.error(f"Failed to process URL {url}: {e}")
                continue
        
        logger.info(f"Processing complete. Total flashcards generated: {total_flashcards}")

def main():
    """Main execution function."""
    try:
        # Initialize the generator
        generator = DummyFlashcardGenerator()
        
        # Define URLs to process
        urls = [
            "https://stanford.edu/~shervine/teaching/cs-230/cheatsheet-convolutional-neural-networks",
            "https://stanford.edu/~shervine/teaching/cs-230/cheatsheet-recurrent-neural-networks",
            "https://stanford.edu/~shervine/teaching/cs-230/cheatsheet-deep-learning-tips-and-tricks"
        ]
        
        # Generate flashcards
        generator.generate_flashcards_from_urls(urls)
        
    except Exception as e:
        logger.error(f"Application failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()