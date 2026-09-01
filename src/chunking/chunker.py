from langchain_text_splitters import RecursiveCharacterTextSplitter  # pyright: ignore[reportMissingImports]
from langchain_core.documents import Document  # pyright: ignore[reportMissingImports]
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from ingestion.loader import load_pdf
from utils.helpers import load_config

def chunk_documents(documents: list[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> list[Document]:
    """ 
    Chunk a list of documents into smaller documents
    """

    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=["\n\n", "\n", " ", ""])
        return text_splitter.split_documents(documents)
    except Exception as e:
        print(f"Error chunking documents: {e}")
        return []

if __name__ == "__main__":
    from pathlib import Path

    # 1. Load configuration settings
    config = load_config()
    
    # 2. Dynamically build paths using config data
    project_root = Path(__file__).resolve().parent.parent.parent
    pdf_path = (
        project_root 
        / config["paths"]["source_folder"] 
        / config["paths"]["pdf_filename"]
    )
    documents = load_pdf(str(pdf_path))
    chunks = chunk_documents(documents)
    print(f"Chunks: {len(chunks)}")
    print(chunks[0].page_content)
    