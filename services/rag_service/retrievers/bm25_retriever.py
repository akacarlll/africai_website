from .base_retriever import BaseRetriever
from typing import Dict, List, Any, Optional
from services.rag_service.models import SearchResult, RetrieverConfig
import os
import pickle
from langchain_community.retrievers import BM25Retriever
from utils.helpers import DOC_TYPES_DICT

class LocalBM25Retriever(BaseRetriever):
    """BM25 keyword-based retriever"""
    def __init__(self, config: RetrieverConfig):
        super().__init__(config)
    def initialize_connection(self):
        """Initialize BM25 search engine"""
        base_path = "data/vector_stores/bm25_stores"
        doc_types = self.config.document_types
        all_documents = []
        if len(doc_types) == 1:
            path = os.path.join(base_path, DOC_TYPES_DICT[doc_types[0]], "bm25_index.pkl") # type: ignore
            if os.path.exists(path):
                with open(path, "rb") as f:
                    retriever = pickle.load(f)
                self.vector_client = retriever
            else:
                raise FileNotFoundError(f"No BM25 store found for document type: {DOC_TYPES_DICT[doc_types[0]]}")
        else :
            for doc_type in doc_types:
                path = os.path.join(base_path, DOC_TYPES_DICT[doc_type], "bm25_index.pkl") # type: ignore
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        retriever = pickle.load(f) 
                        all_documents.extend(retriever.docs)
                else:
                    raise FileNotFoundError(f"No BM25 store found for document type: {doc_type}")
            self.vector_client = BM25Retriever.from_documents(all_documents)
    
    def search(self, query: str, max_results: int, filters: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """Search using BM25 and return structured search results."""
        if self.vector_client is None:
            raise RuntimeError("BM25 retriever not initialized. Call initialize_connection() first.")

        docs = self.vector_client.get_relevant_documents(query)
        results = []
        for doc in docs:
            results.append(SearchResult(
                content=doc.page_content,
                metadata=doc.metadata,
                relevance_score=0,
                document_type=self.config.document_types, 
            ))
        return results[:max_results]
