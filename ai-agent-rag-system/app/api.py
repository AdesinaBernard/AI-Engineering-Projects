from fastapi import FastAPI
from pydantic import BaseModel


from agents.autonomous_research_agent import run_autonomous_research
from rag.rag import ask_rag
from core.coordinator import coordinate

from app.schemas import (
    QueryRequest,
    RAGResponse,
    ResearchResponse,
    AgentResponse,
    HealthResponse
)


from app.config import config
from app.logging_config import logger


app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION
)


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {
        "message": "AI Agent RAG System is running",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
def health_check():
    return {
        "status": "ok",
        "service": "ai-agent-rag-system"
    }

@app.get("/health")

def health():

    logger.info("Health check requested.")

    return {

        "status": "healthy",

        "llm": "connected",

        "vector_db": "loaded"

    }

@app.post("/rag", response_model=RAGResponse)
def rag_endpoint(request: QueryRequest):
    return {
        "type": "rag",
        "query": request.query,
        "result": ask_rag(request.query)
    }


@app.post("/research/quick", response_model=RAGResponse)
def quick_research_endpoint(request: QueryRequest):
    return {
        "type": "quick_research",
        "query": request.query,
        "result": ask_rag(request.query)
    }

@app.post("/research/full", response_model=ResearchResponse)
def full_research_endpoint(request: QueryRequest):
    result = run_autonomous_research(request.query)

    return {
        "type": "full_research",
        "query": request.query,
        "report": result["report"],
        "details": result["result"]
    }

@app.post("/agent", response_model=AgentResponse)
def agent_endpoint(request: QueryRequest):
    result = coordinate(request.query)

    return {
        "type": "agent",
        "query": request.query,
        "result": result
    }

@app.post("/rag")
def rag_endpoint(request: QueryRequest):

    logger.info(
        f"RAG Request: {request.query}"
    )

    result = ask_rag(request.query)

    logger.info("RAG completed.")

    return {
        "type": "rag",
        "query": request.query,
        "result": result
    }