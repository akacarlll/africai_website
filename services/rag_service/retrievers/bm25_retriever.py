from .base_retriever import BaseRetriever
from typing import Dict, List, Any, Optional
from services.rag_service.models import SearchResult, RetrieverConfig
import os
import pickle
from langchain_community.retrievers import BM25Retriever
class LocalBM25Retriever(BaseRetriever):
    """BM25 keyword-based retriever"""
    def __init__(self, config: RetrieverConfig):
        super().__init__(config)
    def initialize_connection(self):
        """Initialize BM25 search engine"""
        base_path = r"C:\Users\carlf\Documents\GitHub\AfricAI\vector_stores\bm25_stores"
        doc_types = self.config.document_types
        all_documents = []
        if len(doc_types) == 1:
            path = os.path.join(base_path, doc_types[0], "bm25_index.pkl") # type: ignore
            if os.path.exists(path):
                with open(path, "rb") as f:
                    docs = pickle.load(f)
                self.vector_client = BM25Retriever.from_documents(docs, k1=self.config.params.get("k1", 1.2), b=self.config.params.get("b", 0.75), epsilon=self.config.params.get("epsilon", 0.25))
            else:
                raise FileNotFoundError(f"No BM25 store found for document type: {doc_types[0]}")
        else :
            for doc_type in doc_types:
                path = os.path.join(base_path, doc_type, "bm25_index.pkl") # type: ignore
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        docs = pickle.load(f) 
                        all_documents.extend(docs)
                else:
                    raise FileNotFoundError(f"No BM25 store found for document type: {doc_type}")
            self.vector_client = BM25Retriever.from_documents(all_documents, k1=self.config.params.get("k1", 1.2), b=self.config.params.get("b", 0.75), epsilon=self.config.params.get("epsilon", 0.25))
    
    def search(self, query: str, max_results: int, filters: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """Search using BM25 and return structured search results."""
        if self.vector_client is None:
            raise RuntimeError("BM25 retriever not initialized. Call initialize_connection() first.")

        docs = self.vector_client.get_relevant_documents(query)

        results = []
        seen = set()  # Optional: to avoid duplicate documents
        for doc in docs:
            content = doc.page_content
            metadata = doc.metadata or {}

            if content in seen:
                continue
            seen.add(content)

            results.append(SearchResult(
                content=content,
                metadata=metadata,
                relevance_score=0,
                document_type=self.config.document_types[0], # type: ignore
                date=metadata.get("year", "2024"),
                citation=content[:20],
                document_title=metadata.get("page_title", "Acte Ohada")
            ))

            if len(results) >= max_results:
                break

        return results
