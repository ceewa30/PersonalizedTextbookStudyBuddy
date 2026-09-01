import sys
import os
from pathlib import Path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from dotenv import load_dotenv
from langchain_chroma import Chroma  # pyright: ignore[reportMissingImports]
from langchain_openai import OpenAIEmbeddings  # pyright: ignore[reportMissingImports]
from langchain_core.documents import Document  # pyright: ignore[reportMissingImports]
from utils.helpers import load_config



load_dotenv(override=True)
config = load_config()

project_root = Path(__file__).resolve().parent.parent.parent
db_storage_path = project_root / config["paths"]["chroma_db_dir"]


def query_vector_db(query: str, k: int = 4) -> list[Document]:
    """ 
    Connects to the persistent local Chroma DB and retrieves
    the top 'k' most relevant textbook chunks.
    """

    try:
        embedding_model = OpenAIEmbeddings(model=config["models"]["embedding"])

        vector_store = Chroma(
            persist_directory=str(db_storage_path),
            embedding_function=embedding_model,
            collection_name=config["vector_store"]["collection_name"]
        )

        print(f"Searching for matches for: '{query}' ...")
        results = vector_store.similarity_search(query, k=k)
        return results
    
    except Exception as e:
        print(f"Error querying vector database: {e}")
        return []

if __name__ == "__main__":
    # Test question from a beginner reading the Python textbook
    test_query = "What is a list comprehension and how do you use it?"
    
    matched_docs = query_vector_db(query=test_query, k=3)
    
    print(f"\nFound {len(matched_docs)} matching textbook sections:")
    for i, doc in enumerate(matched_docs, 1):
        print(f"\n--- Result {i} (Source: {doc.metadata.get('source')}, Page: {doc.metadata.get('page')}) ---")
        print(doc.page_content.strip()[:300] + "...") 