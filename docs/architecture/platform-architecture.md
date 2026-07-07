# Platform Architecture

```mermaid
flowchart TD
    Client[Client]

    Gateway[API Gateway<br/>Go / Gin<br/><br/>JWT Auth<br/>Rate Limiting<br/>Request IDs<br/>Logging<br/>Timeouts]

    Redis[(Redis<br/>Rate Limit Store)]

    RAG[RAG Service<br/>FastAPI<br/><br/>Query Embedding<br/>Similarity Search<br/>Context Builder<br/>Prompt Builder]

    Postgres[(PostgreSQL<br/>pgvector)]

    LLM[Ollama / OpenAI]

    Client -->|HTTP /v1/rag| Gateway
    Gateway -->|Rate limit check| Redis
    Gateway -->|Internal HTTP /v1/rag| RAG
    RAG -->|Vector Search| Postgres
    RAG -->|LLM Call| LLM
    LLM --> RAG
    RAG --> Gateway
    Gateway --> Client