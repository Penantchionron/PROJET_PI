import os
from services.rag import ingest_pdf_to_vector_db

DATA_PATH = "data"

def run_ingestion():
    # Parcourt les dossiers 6eme, 5eme, 4eme, 3eme
    for niveau in ["6eme", "5eme", "4eme", "3eme"]:
        dir_path = os.path.join(DATA_PATH, niveau)
        if os.path.exists(dir_path):
            for filename in os.listdir(dir_path):
                if filename.endswith(".pdf"):
                    print(f"Lecture de {filename}...")
                    ingest_pdf_to_vector_db(os.path.join(dir_path, filename), niveau)
    print("Base de connaissances prête !")

if __name__ == "__main__":
    run_ingestion()