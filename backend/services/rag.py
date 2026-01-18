import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Configuration du modèle d'embedding
embeddings = OllamaEmbeddings(model="nomic-embed-text")
CHROMA_PATH = "db/chroma_db"

def ingest_pdf_to_vector_db(pdf_path: str, niveau: str):
    """Découpe un PDF et l'ajoute à la base vectorielle"""
    if not os.path.exists(pdf_path):
        return f"Erreur : Le fichier {pdf_path} n'existe pas."
        
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    
    # Découpage en morceaux (chunks) de 1000 caractères
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(docs)
    
    # Marquage du niveau pour filtrer les recherches plus tard
    for chunk in chunks:
        chunk.metadata["niveau"] = niveau

    # Stockage persistant
    vector_db = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=CHROMA_PATH
    )
    return f"Succès : {len(chunks)} extraits de {niveau} enregistrés."

def get_relevant_context(query: str, niveau: str):
    """Récupère les extraits les plus proches de la question"""
    if not os.path.exists(CHROMA_PATH):
        return ""
        
    vector_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
    # Recherche filtrée par niveau (ex: seulement le programme de 4ème)
    results = vector_db.similarity_search(query, k=3, filter={"niveau": niveau})
    
    return "\n\n".join([doc.page_content for doc in results])