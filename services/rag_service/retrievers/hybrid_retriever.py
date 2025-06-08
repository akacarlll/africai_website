from services.rag_service.models import RetrieverConfig, SearchResult, RetrieverType
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .base_retriever import BaseRetriever
from .bm25_retriever import BM25Retriever
from .chroma_retriever import VectorSimilarityRetriever
class HybridRetriever(BaseRetriever):
    """Hybrid retriever combining vector and keyword search"""
    
    def __init__(self, config: RetrieverConfig):
        super().__init__(config)
        vector_config = RetrieverConfig(RetrieverType.VECTOR_SIMILARITY, config.params, config.document_types)
        bm25_config = RetrieverConfig(RetrieverType.BM25, config.params, config.document_types)
        
        self.vector_retriever = VectorSimilarityRetriever(vector_config)
        self.bm25_retriever = BM25Retriever(bm25_config)
    
    def initialize_connection(self):
        """Initialize both retrievers"""
        self.vector_retriever.initialize_connection()
        self.bm25_retriever.initialize_connection()
    
    def search(self, query: str, filters: Dict[str, Any], max_results: int) -> List[SearchResult]:
        """Perform hybrid search"""
        vector_weight = self.config.params.get("vector_weight", 0.7)
        keyword_weight = self.config.params.get("keyword_weight", 0.3)
        
        vector_results = self.vector_retriever.search(query, filters, max_results)
        bm25_results = self.bm25_retriever.search(query, filters, max_results)
        
        combined_results = self._combine_results(vector_results, bm25_results, vector_weight, keyword_weight)
        
        return combined_results[:max_results]
    
    def _combine_results(self, vector_results: List[SearchResult], bm25_results: List[SearchResult], 
                        vector_weight: float, keyword_weight: float) -> List[SearchResult]:
        """Combine and rerank results from both retrievers"""
        # TODO: Implement proper result fusion (e.g., RRF, score combination)
        all_results = {}
        
        for result in vector_results:
            result.relevance_score *= vector_weight
            all_results[result.document_title] = result
        
        for result in bm25_results:
            result.relevance_score *= keyword_weight
            if result.document_title in all_results:
                all_results[result.document_title].relevance_score += result.relevance_score
            else:
                all_results[result.document_title] = result
 
        return sorted(all_results.values(), key=lambda x: x.relevance_score, reverse=True)
