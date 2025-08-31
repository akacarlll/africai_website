from typing import Dict, Any, List, Optional
from abc import ABC
from langchain.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from dataclasses import dataclass
import numpy as np
from .base_retriever import BaseRetriever
from services.rag_service.models import RetrieverConfig, SearchResult
from utils.helpers import DOC_TYPES_DICT
class FaissRetriever(BaseRetriever):
    """
    FAISS retriever using LangChain's FAISS wrapper.
    """
    def __init__(self, config: RetrieverConfig, embeddings: Embeddings):
        super().__init__(config)
        self.embeddings = embeddings
        self.vector_client = None  

    def initialize_connection(self):
        """Load FAISS vector store from disk."""
        base_path = "data/vector_stores/faiss_stores"
        doc_types = self.config.document_types

        if len(doc_types) == 1:
            path = f"{base_path}/{DOC_TYPES_DICT[doc_types[0]]}"
            self.vector_client = FAISS.load_local(path, embeddings=self.embeddings, allow_dangerous_deserialization=True)
        else:
            first_path = f"{base_path}/{DOC_TYPES_DICT[doc_types[0]]}"
            merged_faiss = FAISS.load_local(first_path, embeddings=self.embeddings, allow_dangerous_deserialization=True)

            for doc_type in doc_types[1:]:
                path = f"{base_path}/{DOC_TYPES_DICT[doc_type]}"
                next_faiss = FAISS.load_local(path, embeddings=self.embeddings, allow_dangerous_deserialization=True)
                merged_faiss.merge_from(next_faiss)

            self.vector_client = merged_faiss

    def search(self, query: str, max_results: int, filters: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """Search using LangChain FAISS and return scored results."""
        if self.vector_client is None:
            raise RuntimeError("FAISS vector store not initialized. Call initialize_connection() first.")

        docs = self.vector_client.similarity_search(query, k=max_results)
        results = []

        for doc in docs:
            results.append(SearchResult(
                content=doc.page_content,
                metadata=doc.metadata if doc.metadata else {},
                relevance_score=0,
                document_type=self.config.document_types,
            ))
        return results