import os
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from src.config import settings, get_openai_client


app = FastAPI(title="PrivateDoc AI", version="1.0.0")


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


def check_api_key():
    """Check if OPENAI_API_KEY exists in environment."""
    if not os.environ.get("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="OPENAI_API_KEY not found in environment variables"
        )


def get_vectorstore():
    """Initialize and return ChromaDB vectorstore."""
    embeddings = OpenAIEmbeddings(model=settings.openai_embedding_model)
    vectorstore = Chroma(
        persist_directory=settings.chroma_persist_directory,
        embedding_function=embeddings
    )
    return vectorstore


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    RAG endpoint: retrieves relevant chunks and generates answer using GPT-4o-mini.
    """
    check_api_key()
    
    try:
        vectorstore = get_vectorstore()
        
        llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0
        )
        
        template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Answer:"""

        PROMPT = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": settings.retrieval_top_k}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        result = qa_chain({"query": request.query})
        
        sources = [doc.metadata.get("source", "unknown") for doc in result["source_documents"]]
        
        return ChatResponse(
            answer=result["result"],
            sources=sources
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
