"""This module contains helper functions and constants for the services."""

from langchain.embeddings import HuggingFaceEmbeddings
from services.retriever_service import FaissRetriever, LocalBM25Retriever, HybridRetriever, ChromaRetriever
from typing import Any
from functools import partial

DOC_TYPES_DICT : dict[str, str]= {"Code":"code", "Arrétés":"arrete", "Loi":"loi", "Circulaire":"circulaire", "Autres":"autres", "Décret":"decret", "Arrets":"arret"}
EMBEDDINGS = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

RETRIEVER_REGISTRY: dict[str, Any] = {
    "chroma": partial(ChromaRetriever, embeddings=EMBEDDINGS),
    "bm25": LocalBM25Retriever,
    "hybrid": HybridRetriever,
    "faiss_retriever": partial(FaissRetriever, embeddings=EMBEDDINGS),
}