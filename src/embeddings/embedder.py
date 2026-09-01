from langchain_openai import OpenAIEmbeddings # pyright: ignore[reportMissingImports]
from langchain_core.documents import Document  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv
import sys
import os
from pathlib import Path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from ingestion.loader import load_pdf
from chunking.chunker import chunk_documents
from utils.helpers import load_config

config = load_config()

project_root = Path(__file__).resolve().parent.parent.parent

load_dotenv(override=True)

def embed_documents(documents: list[Document]) -> list[list[float]]:
    """ 
    Embed a list of documents using text-embedding-3-small
    """

    try:
        embeddings = OpenAIEmbeddings(model=config["models"]["embedding"])
        texts = [doc.page_content for doc in documents]
        return embeddings.embed_documents(texts)
    except Exception as e:
        print(f"Error embedding documents: {e}")
        return []   

if __name__ == "__main__":
    
    pdf_path = (
        project_root 
        / config["paths"]["source_folder"] 
        / config["paths"]["pdf_filename"]
    )
    documents = load_pdf(str(pdf_path))
    chunks = chunk_documents(documents)
    embeddings = embed_documents(chunks)
    print(embeddings)