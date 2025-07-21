from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Automotive RAG System",
    description="AI-powered automotive knowledge assistant",
    version="1.0.0"
)

# Data models
class QueryRequest(BaseModel):
    question: str
    max_results: Optional[int] = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float

class DocumentUpload(BaseModel):
    filename: str
    content: str
    document_type: str

# In-memory storage for now
automotive_knowledge = {
    "oil_change": "Most vehicles require oil changes every 3,000-5,000 miles depending on oil type and driving conditions.",
    "brake_pads": "Brake pads typically need replacement every 25,000-70,000 miles depending on driving habits.",
    "tire_rotation": "Tires should be rotated every 5,000-7,500 miles to ensure even wear.",
    "engine_maintenance": "Regular engine maintenance includes oil changes, filter replacements, and spark plug inspection."
}

# Routes
@app.get("/")
async def root():
    return {
        "message": "Welcome to Automotive RAG System",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "query": "/query",
            "upload": "/upload",
            "documents": "/documents"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "automotive-rag"}

@app.post("/query", response_model=QueryResponse)
async def query_knowledge(request: QueryRequest):
    """
    Query the automotive knowledge base
    """
    question = request.question.lower()
    
    # Simple keyword matching for now
    best_match = None
    best_score = 0
    
    for key, value in automotive_knowledge.items():
        if key in question:
            score = question.count(key)
            if score > best_score:
                best_score = score
                best_match = value
    
    if best_match:
        return QueryResponse(
            answer=best_match,
            sources=[f"automotive_knowledge_{key}"],
            confidence=min(best_score * 0.3, 1.0)
        )
    else:
        return QueryResponse(
            answer="I don't have specific information about that topic in my current knowledge base.",
            sources=[],
            confidence=0.0
        )

@app.post("/upload")
async def upload_document(document: DocumentUpload):
    """
    Upload automotive document (placeholder for now)
    """
    return {
        "message": f"Document '{document.filename}' uploaded successfully",
        "type": document.document_type,
        "size": len(document.content),
        "status": "processed"
    }

@app.get("/documents")
async def list_documents():
    """
    List all uploaded documents
    """
    return {
        "documents": list(automotive_knowledge.keys()),
        "total": len(automotive_knowledge)
    }

# Development server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)