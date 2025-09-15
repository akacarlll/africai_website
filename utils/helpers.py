from langchain.embeddings import HuggingFaceEmbeddings

DOC_TYPES_DICT : dict[str, str]= {"Code":"code", "Arrétés":"arrete", "Loi":"loi", "Circulaire":"circulaire", "Autres":"autres", "Décret":"decret", "Arrets":"arret"}
EMBEDDINGS = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
