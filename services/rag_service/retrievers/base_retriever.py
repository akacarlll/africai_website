from services.rag_service.models import RetrieverConfig, SearchResult
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseRetriever(ABC):
    """Abstract base class for all retrievers"""
    
    def __init__(self, config: RetrieverConfig):
        self.config = config
        self.vector_client = None 
    
    @abstractmethod
    def search(self, query: str, max_results: int, filters: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """Perform search using this retriever"""
        pass
    
    @abstractmethod
    def initialize_connection(self):
        """Initialize connection to vector database"""
        pass
