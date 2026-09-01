import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import pypdf  # pyright: ignore[reportMissingImports]
from langchain_core.documents import Document  # pyright: ignore[reportMissingImports]

from utils.helpers import load_config

def load_pdf(file_path: str) -> list[Document]:
    """ 
    Load a PDF file and convert it to a list of Lanchain Document objects
    """

    try:
        reader = pypdf.PdfReader(file_path)
        documents = []

        # Loop through pages and convert them to Lanchain Document objects
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            metadata = {"source": file_path, "page": i + 1}
            documents.append(Document(page_content=text, metadata=metadata))
        
        return documents
    
    except Exception as e:
        print(f"Error loading PDF file: {e}")
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
    print(load_pdf(str(pdf_path)))