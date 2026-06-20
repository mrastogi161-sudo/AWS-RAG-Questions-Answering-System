from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import os

from src.rag_pipeline import RAGPipeline
from src.schemas import AskRequest, AskResponse, Source, AnalyticsResponse
from database import Database
from src.config import Config
from src.pdf_loader import PDFLoader
from src.chunker import DocumentChunker
from src.vector_store import VectorStoreManager

app = FastAPI(title="AWS Agreement RAG System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGPipeline()
db = Database()

@app.post("/ingest")
async def ingest_document():
    try:
        if not os.path.exists(Config.PDF_PATH):
            raise HTTPException(
                status_code=404, 
                detail=f"PDF not found at {Config.PDF_PATH}"
            )
        
        
        documents = PDFLoader.load_pdf(Config.PDF_PATH)
        
        
        chunker = DocumentChunker()
        chunks = chunker.split_documents(documents)
      
        vector_manager = VectorStoreManager()
        vector_manager.create_vectorstore(chunks)
        
        return {
            "status": "success", 
            "message": f"Document ingested and indexed with {len(chunks)} chunks"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(request: AskRequest):
    """Process a query through the RAG pipeline."""
    if not request.query or request.query.strip() == "":
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    start_time = time.time()
    
    try:
        answer, sources, found_answer = rag.query(
            request.query, 
            top_k=request.top_k or Config.TOP_K
        )
        
        response_time = int((time.time() - start_time) * 1000)
   
        db.log_query(
            query=request.query,
            answer=answer,
            sources=sources,
            found_answer=found_answer,
            response_time_ms=response_time,
            top_k=request.top_k or Config.TOP_K
        )
        
        return AskResponse(
            query=request.query,
            answer=answer,
            sources=[Source(**source) for source in sources],
            found_answer=found_answer,
            response_time_ms=response_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
async def get_analytics():
    """Return usage analytics from SQL queries."""
    try:
        analytics = db.get_analytics()
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "RAG System"}