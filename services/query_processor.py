import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from services.rag_service.rag_service import get_rag_service

def process_query(query: str, doc_types: list, retriever_type: str, retriever_params: dict,
                  start_year: int, end_year: int, max_results: int) -> str:
    rag_service = get_rag_service()
    results = rag_service.search_documents(query, retriever_type, retriever_params, 
                                         doc_types, start_year, end_year, max_results)
    sources_formatted = "\n\n".join([
        f"***Chunk {i+1}:*** \n **Doc Title**:{source.metadata['metadata']} \n{source.content} \n The Chunk was founded in page {source.metadata.get('page_label', 'Unknown')}" 
        for i, source in enumerate(results.sources)
    ])
    
    return f"""**Response Based on Retrieved Context:**

    {results.answer}

    **Retrieved Chunks:**

    {sources_formatted}
    """
