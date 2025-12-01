import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from src.config import settings


def ingest_documents():
    """Load documents from directory and ingest into ChromaDB."""
    documents_path = Path(settings.documents_directory)
    
    if not documents_path.exists():
        print(f"Documents directory not found: {documents_path}")
        return
    
    # Find all PDF files
    pdf_files = list(documents_path.glob("**/*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {documents_path}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    # Load documents
    all_docs = []
    for pdf_file in pdf_files:
        print(f"Loading: {pdf_file}")
        loader = PyPDFLoader(str(pdf_file))
        docs = loader.load()
        all_docs.extend(docs)
    
    print(f"Loaded {len(all_docs)} document pages")
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap
    )
    splits = text_splitter.split_documents(all_docs)
    print(f"Split into {len(splits)} chunks")
    
    # Create embeddings and store in ChromaDB
    embeddings = OpenAIEmbeddings(model=settings.openai_embedding_model)
    
    print("Creating vector store...")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=settings.chroma_persist_directory
    )
    
    print(f"✓ Successfully ingested {len(splits)} chunks into ChromaDB")
    print(f"✓ Vector store persisted to: {settings.chroma_persist_directory}")


if __name__ == "__main__":
    ingest_documents()
