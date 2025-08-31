import streamlit as st
from typing import Dict, Any


def get_retriever_sidebar_params(retriever_type: str):
    """Generate retriever-specific parameters in sidebar and return them explicitly"""

    params: Dict[str, Any] = {"retriever_type": retriever_type}
    
    st.subheader("Retriever Parameters")
    
    if retriever_type == "ensemble_retriever":
        st.markdown("**Ensemble Retriever Parameters:**")
        params["retrievers"] = st.multiselect(
            "Select Retrievers to Combine",
            ["faiss", "bm25", "chroma", "qdrant"],
            default=["faiss", "bm25"],
            help="Choose which retrievers to combine in the ensemble"
        )
        params["weights"] = {}
        for retriever in params["retrievers"]:
            params["weights"][retriever] = st.slider(
                f"{retriever.upper()} Weight",
                0.0, 1.0, 1.0 / len(params["retrievers"]), 0.05,
                help=f"Weight for {retriever} results in final ranking"
            )
        params["rerank"] = st.checkbox(
            "Enable Reranking",
            value=True,
            help="Apply cross-encoder reranking to final results"
        )
        
    elif retriever_type == "faiss_retriever":
        st.markdown("**Faiss Retriever Parameters:**")
        params["index_type"] = st.selectbox(
            "Index Type",
            ["IndexFlatIP", "IndexIVFFlat", "IndexHNSW"],
            help="Faiss index type - Flat for accuracy, IVF for speed, HNSW for balance"
        )
        params["similarity_threshold"] = st.slider(
            "Similarity Threshold", 
            0.0, 1.0, 0.7, 0.05,
            help="Minimum similarity score for relevant documents"
        )
        params["nprobe"] = st.slider(
            "Search Probes (for IVF)",
            1, 100, 10, 1,
            help="Number of clusters to search (only for IVF indexes)"
        )
        
    elif retriever_type == "chroma_retriever":
        st.markdown("**Chroma Retriever Parameters:**")
        params["collection_name"] = st.text_input(
            "Collection Name",
            value="legal_documents",
            help="Name of the Chroma collection to search"
        )
        params["similarity_threshold"] = st.slider(
            "Similarity Threshold", 
            0.0, 1.0, 0.7, 0.05,
            help="Minimum similarity score for relevant documents"
        )
        params["enable_metadata_filter"] = st.checkbox(
            "Enable Metadata Filtering",
            value=True,
            help="Use document metadata for additional filtering"
        )
        
    elif retriever_type == "qdrant_retriever":
        st.markdown("**Qdrant Retriever Parameters:**")
        params["collection_name"] = st.text_input(
            "Collection Name",
            value="legal_docs",
            help="Name of the Qdrant collection to search"
        )
        params["similarity_threshold"] = st.slider(
            "Similarity Threshold", 
            0.0, 1.0, 0.7, 0.05,
            help="Minimum similarity score for relevant documents"
        )
        params["search_params"] = {
            "hnsw_ef": st.slider(
                "HNSW Search Effort",
                16, 512, 128, 16,
                help="Higher values = more accurate but slower search"
            ),
            "exact": st.checkbox(
                "Exact Search",
                value=False,
                help="Use exact search instead of approximate (slower but more accurate)"
            )
        }
        
    elif retriever_type == "bm25":
        st.markdown("**BM25 Parameters:**")
        params["k1"] = st.slider(
            "BM25 k1 parameter", 
            0.1, 3.0, 1.2, 0.1,
            help="Controls term frequency scaling - higher values give more weight to term frequency"
        )
        params["b"] = st.slider(
            "BM25 b parameter", 
            0.0, 1.0, 0.75, 0.05,
            help="Controls document length normalization - 0 means no normalization, 1 means full normalization"
        )
        params["epsilon"] = st.slider(
            "BM25 epsilon",
            0.0, 1.0, 0.25, 0.05,
            help="Floor value for IDF calculation to avoid negative scores"
        )
        
    with st.expander("Current Parameters", expanded=False):
        st.json(params)
    
    return params

def sidebar_config():
    st.header("🔍 Search Options")
    doc_types = st.multiselect(
        "Document Types",
        ["Code", "Arrétés", "Loi", "Circulaire", "Autres", "Décret", "Arrets"],
        default=["Code", "Loi"]
    )

    retriever_options = {
        "ensemble_retriever": "Ensemble Retriever - Combines multiple retrieval methods for optimal results",
        "faiss_retriever": "Faiss as Retriever - High-performance vector similarity search using Meta's Faiss",
        "chroma_retriever": "Chroma as Retriever - Open-source embedding database with built-in filtering",
        "qdrant_retriever": "Qdrant as Retriever - Vector search engine with advanced filtering and scalability",
        "bm25": "BM25 - Traditional keyword-based search with term frequency scoring",
    }

    retriever_display = st.selectbox(
        "Retriever Type",
        options=list(retriever_options.keys()),
        format_func=lambda x: retriever_options[x],
        index=1,
        help="Choose the retrieval method that best fits your search needs"
    )

    retriever_explanations = {
        "ensemble_retriever": """
        **Ensemble Retriever:**
        - Combines multiple retrieval algorithms (e.g., vector + BM25 + reranking)
        - Best for: Maximum accuracy and comprehensive legal research
        - Strengths: Leverages benefits of different approaches, reduces blind spots
        - Use when: Quality is more important than speed, complex legal queries
        """,
        "faiss_retriever": """
        **Faiss as Retriever:**
        - Meta's high-performance vector similarity search library
        - Best for: Large-scale legal document collections, fast semantic search
        - Strengths: Extremely fast vector search, handles millions of documents
        - Use when: You have large document volumes and need speed with semantic understanding
        """,
        "chroma_retriever": """
        **Chroma as Retriever:**
        - Open-source embedding database with built-in metadata filtering
        - Best for: Structured legal research with document categorization
        - Strengths: Easy filtering by document type, date, jurisdiction, etc.
        - Use when: You need semantic search with strong filtering capabilities
        """,
        "qdrant_retriever": """
        **Qdrant as Retriever:**
        - Production-ready vector search engine with advanced features
        - Best for: Enterprise legal applications requiring scalability
        - Strengths: Advanced filtering, payload support, clustering, high availability
        - Use when: Building production legal systems with complex requirements
        """,
        "bm25": """
        **BM25 (Best Matching 25):**
        - Traditional probabilistic keyword-based search
        - Best for: Exact term matching, specific legal citations
        - Strengths: Fast, precise for known terms and phrases
        - Use when: Searching for specific statutes, case names, or legal terms
        """,
    }

    with st.expander(f"ℹ️ About {retriever_options[retriever_display]}", expanded=False):
        st.markdown(retriever_explanations[retriever_display])
    
    retriever_type = retriever_display
    retriever_params = get_retriever_sidebar_params(retriever_type) 
    retriever_params["doc_type"] = doc_types
    st.subheader("Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_year = st.number_input("From Year", value=2020, min_value=1970, max_value=2025)
    with col2:
        end_year = st.number_input("To Year", value=2024, min_value=1970, max_value=2025)

    max_results = st.slider("Max Results", min_value=1, max_value=50, value=10)
    return {
        "doc_types": doc_types, 
        "retriever_type": retriever_type,
        "retriever_params": retriever_params,
        "start_year": start_year,
        "end_year": end_year,
        "max_results": max_results
        }   