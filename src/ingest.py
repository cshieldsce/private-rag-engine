import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from src.config import settings


def ingest_documents():
    """
    Scan documents folder, load PDFs, split into chunks, and upsert to ChromaDB.
    """
    documents_path = Path(settings.documents_directory)
    
    if not documents_path.exists():
        print(f"Creating documents directory: {documents_path}")
        documents_path.mkdir(parents=True, exist_ok=True)
        print("Please add PDF files to the documents folder and run again.")
        return
    
    # Find all PDF files
    pdf_files = list(documents_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {documents_path}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    # Load all documents
    all_documents = []
    for pdf_file in pdf_files:
        print(f"Loading: {pdf_file.name}")
        loader = PyPDFLoader(str(pdf_file))
        documents = loader.load()
        all_documents.extend(documents)
    
    print(f"Loaded {len(all_documents)} pages")
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        length_function=len,
    )
    chunks = text_splitter.split_documents(all_documents)
    print(f"Split into {len(chunks)} chunks")
    
    # Initialize embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
    
    # Create or load ChromaDB and upsert chunks
    print("Upserting to ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=settings.chroma_persist_directory,
    )
    
    print(f"✓ Successfully ingested {len(chunks)} chunks into ChromaDB")
    print(f"✓ Persistent storage at: {settings.chroma_persist_directory}")


if __name__ == "__main__":
    # Verify API key exists
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    ingest_documents()
