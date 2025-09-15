"""
RAG Service - Main orchestration for Retrieval-Augmented Generation
"""
from langchain.prompts import PromptTemplate
from typing import List, Dict, Any, Optional
from ..rag_service.models import RetrieverConfig, RAGResponse, RetrieverType, SearchResult
from services.retriever_service import FaissRetriever, LocalBM25Retriever, HybridRetriever, ChromaRetriever, BaseRetriever
from services.llm_service.rag.rag_llm_service import RagLLMService
from services.document_service import DocumentFinder
from utils.helpers import EMBEDDINGS

class RAGService:
    """Main RAG orchestration service"""
    
    def __init__(self):
        """Initialize RAG service with vector DB and LLM connections"""
        self.llm = RagLLMService()

    def _get_retriever(self, retriever_type: str, params: Dict[str, Any], doc_types: List[str]) -> BaseRetriever:
        """Get and configure the appropriate retriever"""
        
        # Convert document types
        # document_types = [DocumentType(dt.lower().replace(" ", "_")) for dt in doc_types or []]
        

        config = RetrieverConfig(
            type=RetrieverType(retriever_type),
            params=params,
            document_types=doc_types # type: ignore
        )
        if retriever_type == "chroma":
            retriever = ChromaRetriever(config, embeddings=EMBEDDINGS)
        elif retriever_type == "bm25":
            retriever = LocalBM25Retriever(config)
        elif retriever_type == "hybrid":
            retriever = HybridRetriever(config)
        elif retriever_type == "faiss_retriever":
            retriever = FaissRetriever(config, embeddings=EMBEDDINGS)
        else:
            # Default to vector similarity
            retriever = ChromaRetriever(config, embeddings=EMBEDDINGS)
        

        retriever.initialize_connection()
        return retriever
    
    def search_documents(
        self, 
        query: str, 
        retriever_type: str,
        params: dict[str, Any],
        doc_types: List[str],
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        max_results: int = 10
    ) -> RAGResponse:
        """
        Main RAG pipeline: search + generate
        
        Args:
            query: User's legal question
            doc_types: Filter by document types
            start_year: Filter by start year
            end_year: Filter by end year
            max_results: Maximum number of results
            
        Returns:
            RAGResponse with answer and sources
        """

        retriever = self._get_retriever(retriever_type, params, doc_types)

        search_results = self._vector_search(
            query, retriever, doc_types, start_year, end_year, max_results
        )
        search_results = self._add_binary(search_results, doc_types)
        
        answer = self._generate_answer(query, search_results)
        
        confidence = self._calculate_confidence(search_results)
        
        return RAGResponse(
            answer=answer,
            sources=search_results,
            confidence_score=confidence,
            query=query,
            retriever_used=retriever_type,
            processing_time=0
        )
       
    def _build_filters(self, doc_types: List[str], start_year: int, end_year: int) -> Dict[str, Any]:
        """Build filters for search"""
        filters = {}
        
        if doc_types:
            filters["document_type"] = {"$in": doc_types}
        
        if start_year and end_year:
            filters["year"] = {"$gte": start_year, "$lte": end_year}
        
        return filters
    def _vector_search(
        self, 
        query: str, 
        retriever: BaseRetriever, 
        doc_types: Optional[List[str]] = None,
        start_year: Optional[int] = None, # 
        end_year: Optional[int] = None,
        max_results: int = 10
    ) -> List[SearchResult]:
        """
        Search your existing vector index
        TODO: Replace with actual vector database integration
        """
        return retriever.search(query, max_results)

    
    def _generate_answer(self, query: str, search_results: List[SearchResult]) -> str:
        """
        Generate answer using LLM based on retrieved documents
        TODO: Replace with actual LLM integration
        """
        context = "\n\n".join([result.content for result in search_results])
        prompt = self._build_prompt(query, context)
        return self.llm.generate(prompt)
        
        
    def _calculate_confidence(self, search_results: List[SearchResult]) -> float:
        """Calculate confidence score based on search results"""
        if not search_results:
            return 0.0
        
        # Simple confidence calculation based on top result relevance
        # You can make this more sophisticated
        top_score = max(result.relevance_score for result in search_results)
        return min(top_score, 1.0)
    
    def _build_prompt(self, query: str, context: str) -> str:
        """Build prompt for LLM with query and context as arguments"""
 
        template = """You are a helpful AI assistant. Use the following context to answer the question accurately and comprehensively.
 
        Context:
        {context}

        Question: {question}

        Instructions:
        - Base your answer strictly on the provided context
        - If the context doesn't contain enough information, say so
        - Be precise and cite relevant information from the context
        - Provide a structured and clear response

        Answer:"""
        return template.format(context=context, question=query)  
    def _add_binary(self, search_result:list[SearchResult], doc_types:list) -> list[SearchResult]:
        if doc_types != ["Code"]:
            print("doc has other type Code")
            return search_result # TODO Change the input data so CSV have a source too, then change DocumentFinder class to add csv.
        finder = DocumentFinder(search_result, num_of_docs=3)
        return finder.enrich_search_result()   
    
# Singleton instance
_rag_service = None

def get_rag_service() -> RAGService:
    """Get singleton RAG service instance"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service

