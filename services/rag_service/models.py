from enum import Enum
from typing import Dict, Any, List
from dataclasses import dataclass

class DocumentType(Enum):
    """Supported document types"""
    CONTRACT = "contracts"
    STATUTE = "statutes" 
    CASE_LAW = "case_law"
    REGULATION = "regulations"
    LEGAL_MEMO = "legal_memos"
    COURT_FILING = "court_filings"
    CODE = "code"

class   RetrieverType(Enum):
    """Supported retriever types"""
    ENSEMBLE = "ensemble_retriever"
    BM25 = "bm25"
    HYBRID = "hybrid"
    DENSE_PASSAGE = "dense_passage"
    FAISS = "faiss_retriever"
    QDRANT = "qdrant_retriever"
    CHROMA = "chroma_retriever"

@dataclass
class SearchResult:
    """Structure for search results"""
    content: str
    relevance_score: float
    document_type: list[str]
    metadata: Dict[str, Any]

@dataclass
class RAGResponse:
    """Structure for RAG response"""
    answer: str
    sources: List[SearchResult]
    confidence_score: float
    query: str
    retriever_used: str
    processing_time: float


@dataclass
class RetrieverConfig:
    """Configuration for retriever"""
    type: RetrieverType
    params: Dict[str, Any]
    document_types: List[str]
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "RetrieverConfig":
        return RetrieverConfig(
            type=data["type"],
            params={k: v for k, v in data.items() if k not in {"retriever_type", "doc_type"}},
            document_types=data.get("doc_type", [])
        )
