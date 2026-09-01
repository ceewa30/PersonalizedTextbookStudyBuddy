from langchain_openai import OpenAIEmbeddings # pyright: ignore[reportMissingImports]
from langchain_core.documents import Document  # pyright: ignore[reportMissingImports]
from langchain_chroma import Chroma # pyright: ignore[reportMissingImports]
import chromadb  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv
import sys
import os
from pathlib import Path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from ingestion.loader import load_pdf
from chunking.chunker import chunk_documents
from embeddings.embedder import embed_documents
from dotenv import load_dotenv
from utils.helpers import load_config

load_dotenv(override=True)
config = load_config()

project_root = Path(__file__).resolve().parent.parent.parent
db_storage_path = project_root / config["paths"]["chroma_db_dir"]

def vector_db_store(chunks: list[Document], embedding_model: OpenAIEmbeddings, persist_dir: Path) -> Chroma:
    """Initialize Chroma DB and save the document chunks to disk. """

    try:
        print(f"Storing {len(chunks)} chunks in ChromaDB at {persist_dir} ...")

        persistent_client = chromadb.PersistentClient(path=str(persist_dir))

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            client=persistent_client,
            collection_name=config["vector_store"]["collection_name"]
        )
        print("Database build and successfully saved to disk.")
        return vector_store

    except Exception as e:
        print(f"Error saving to vector database: {e}")
        raise e



if __name__ == "__main__":
    pdf_path = (
        project_root 
        / config["paths"]["source_folder"] 
        / config["paths"]["pdf_filename"]
    )
    documents = load_pdf(str(pdf_path))
    chunks = chunk_documents(documents)
    embedding_model = OpenAIEmbeddings(model=config["models"]["embedding"])
    
    # 4. Store your chunks into the persistent local Chroma DB
    vector_store = vector_db_store(
        chunks=chunks, 
        embedding_model=embedding_model, 
        persist_dir=db_storage_path
    )
