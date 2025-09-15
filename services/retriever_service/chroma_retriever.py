"""This module contains the Chroma retriever implementation."""
from typing import Dict, Any, List, Optional
from abc import ABC
from langchain.vectorstores import Chroma
from langchain.embeddings.base import Embeddings
from dataclasses import dataclass
from .base_retriever import BaseRetriever
from services.rag_service.models import RetrieverConfig, SearchResult
from utils.helpers import DOC_TYPES_DICT

class ChromaRetriever(BaseRetriever):
    """
    Chroma retriever using LangChain's Chroma wrapper.
    """
    def __init__(self, config: RetrieverConfig, embeddings: Embeddings):
        super().__init__(config)
        self.embeddings = embeddings
        self.vector_client = None

    def initialize_connection(self):
        """Load Chroma vector store from disk."""
        base_path = "data/vector_stores/chroma_stores"
        doc_types = self.config.document_types

        if len(doc_types) == 1:
            path = f"{base_path}/{DOC_TYPES_DICT[doc_types[0]]}"
            self.vector_client = Chroma(persist_directory=path, embedding_function=self.embeddings)
            print("chroma initialized")
        else:
            first_path = f"{base_path}/{DOC_TYPES_DICT[doc_types[0]]}"
            merged_chroma = Chroma(persist_directory=first_path, embedding_function=self.embeddings)

            for doc_type in doc_types[1:]:
                path = f"{base_path}/{DOC_TYPES_DICT[doc_type]}"
                next_chroma = Chroma(persist_directory=path, embedding_function=self.embeddings)
                
                next_data = next_chroma._collection.get()
                
                if next_data['ids']:
                    merged_chroma._collection.add(
                        embeddings=next_data['embeddings'],
                        documents=next_data['documents'],
                        metadatas=next_data['metadatas'],
                        ids=next_data['ids']
                    )

            self.vector_client = merged_chroma

    def search(self, query: str, max_results: int, filters: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """Search using LangChain Chroma and return scored results."""
        if self.vector_client is None:
            raise RuntimeError("Chroma vector store not initialized. Call initialize_connection() first.")

        docs_with_scores = self.vector_client.similarity_search_with_score(query, k=max_results)
        print(len(docs_with_scores))
        results = []

        for doc, score in docs_with_scores:
            results.append(SearchResult(
                content=doc.page_content,
                metadata=doc.metadata if doc.metadata else {},
                relevance_score=score,
                document_type=self.config.document_types,
            ))
        return results
    
