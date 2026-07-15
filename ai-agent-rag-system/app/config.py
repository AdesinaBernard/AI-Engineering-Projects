import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_NAME = os.getenv(
        "APP_NAME",
        "AI Agent RAG System"
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )

    HOST = os.getenv(
        "HOST",
        "0.0.0.0"
    )

    PORT = int(
        os.getenv(
            "PORT",
            "8000"
        )
    )

    LLM_URL = os.getenv(
        "LLM_URL",
        "http://localhost:8080/completion"
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "all-MiniLM-L6-v2"
    )

    VECTOR_DB = os.getenv(
        "VECTOR_DB",
        "data/vector_db.json"
    )

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

    MAX_RESEARCH_ITERATIONS = int(
        os.getenv(
            "MAX_RESEARCH_ITERATIONS",
            "5"
        )
    )


config = Config()