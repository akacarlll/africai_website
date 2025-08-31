""" Sends the documents binary"""
from .rag_service.models import SearchResult
import os
import logging
from typing import Any

class DocumentFinder:
    """
    Enrichit un SearchResult avec les PDF binaires des documents les plus pertinents.
    """
    def __init__(self, search_result: list[SearchResult], num_of_docs: int = 3):
        self.search_result = search_result
        self.num_of_docs = num_of_docs
        self.selected_docs = []
        self.cleaned_paths: list[dict[str, Any]] = []
        self.base_path : str = "data"

    def _extract_top_docs(self):
        """
        Extrait les `num_of_docs` premiers documents (nom + chemin) depuis les métadonnées.
        Doit trouver les documents à enrichir.
        """
        docs = []
        for result in self.search_result:
            doc_title = result.metadata.get("source", [])
            docs.append(doc_title)
        self.selected_docs = docs[:self.num_of_docs]  
        return self.selected_docs

    def _resolve_paths(self):
        """
        Ajoute les chemins absolus à chaque document sélectionné.
        """
        for full_path in self.selected_docs:

            normalized_path = full_path.replace("\\", "/")

            end_path = normalized_path.split("01_raw")[1].lstrip("/")
            corrected_path = os.path.join(self.base_path, end_path)

            if not os.path.exists(corrected_path):
                logging.warning(f"Fichier non trouvé : {corrected_path}")
                continue

            self.cleaned_paths.append({
                "file_name": os.path.basename(corrected_path),
                "resolved_path": corrected_path
            })

        return self.cleaned_paths

    def _add_pdf_binaries_to_metadata(self):
        """
        Lit les fichiers PDF et les ajoute dans le champ "pdf_binary".
        """
        for doc, result in zip(self.cleaned_paths, self.search_result):
            path = doc["resolved_path"]
            try:
                with open(path, "rb") as f:
                    doc["pdf_binary"] = f.read()
            except Exception as e:
                logging.error(f"Erreur lecture {path}: {e}")
                doc["pdf_binary"] = None

            result.binary = doc["pdf_binary"]
        return self.search_result
    def enrich_search_result(self) -> list[SearchResult]:
        """
        Full pipeline: extract top docs, resolve paths, read binaries, and update metadata.
        """
        self._extract_top_docs()
        self._resolve_paths()
        return self._add_pdf_binaries_to_metadata()