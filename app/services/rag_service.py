import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Define persistence paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
PERSIST_DIRECTORY = os.path.join(DATA_DIR, "chroma_db")

def get_embeddings():
    """Returns the configured embeddings model."""
    return OllamaEmbeddings(model="llama3", base_url="http://localhost:11434")

def ingest_document(file_path: str) -> int:
    """
    Ingests a PDF document into the vector store.
    1. Loads the PDF
    2. Splits into chunks
    3. Embeds and stores in ChromaDB
    
    Returns:
        int: Number of chunks created
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # 1. Load PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # 2. Split Text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)

    if not chunks:
        return 0

    # 3. Embed and Persist
    embeddings = get_embeddings()
    
    # Initialize Chroma and add documents (this automatically persists in recent versions)
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    
    return len(chunks)

def query_knowledge_base(query: str, k: int = 3):
    """
    Retrieves the top k relevant chunks for a given query.
    """
    embeddings = get_embeddings()
    
    # Initialize Chroma with the persist directory
    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )
    
    results = vectorstore.similarity_search(query, k=k)
    return results
