"""This module contains the Qdrant retriever implementation."""
from typing import Dict, Any, List, Optional
from abc import ABC
from langchain.vectorstores import Qdrant
from langchain.embeddings.base import Embeddings
from dataclasses import dataclass
from .base_retriever import BaseRetriever
from services.rag_service.models import RetrieverConfig, SearchResult
from utils.helpers import DOC_TYPES_DICT

class QdrantRetriever(BaseRetriever):
    """
    Qdrant retriever using LangChain's Qdrant wrapper.
    """
    def __init__(self, config: RetrieverConfig, embeddings: Embeddings):
        super().__init__(config)
        self.embeddings = embeddings
        self.vector_client = None

    def initialize_connection(self):
        """Initialize Qdrant vector store."""
        base_path = "data/vector_stores/qdrant_stores"
        doc_types = self.config.document_types

        if len(doc_types) == 1:
            path = f"{base_path}/{DOC_TYPES_DICT[doc_types[0]]}"
            self.vector_client = Qdrant.from_existing_collection(
                embedding=self.embeddings,
                path=path,
                collection_name=DOC_TYPES_DICT[doc_types[0]]
            )
        else:
            first_path = f"{base_path}/{DOC_TYPES_DICT[doc_types[0]]}"
            merged_qdrant = Qdrant.from_existing_collection(
                embedding=self.embeddings,
                path=first_path,
                collection_name=DOC_TYPES_DICT[doc_types[0]]
            )

            for doc_type in doc_types[1:]:
                path = f"{base_path}/{DOC_TYPES_DICT[doc_type]}"
                next_qdrant = Qdrant.from_existing_collection(
                    embedding=self.embeddings,
                    path=path,
                    collection_name=DOC_TYPES_DICT[doc_type]
                )
                merged_qdrant.collection.upsert(
                    points=next_qdrant.collection.get()['points']
                )

            self.vector_client = merged_qdrant

    def search(self, query: str, max_results: int, filters: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """Search using LangChain Qdrant and return scored results."""
        if self.vector_client is None:
            raise RuntimeError("Qdrant vector store not initialized. Call initialize_connection() first.")

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