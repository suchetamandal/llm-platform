# LLM Platform

A production-oriented LLM Platform demonstrating the architecture and engineering practices expected for Senior/Staff LLM Backend Infrastructure roles.

## Architecture

```text
                        +----------------------+
                        |      Client          |
                        +----------+-----------+
                                   |
                                   | HTTP
                                   |
                        +----------v-----------+
                        |   API Gateway (Go)   |
                        |----------------------|
                        | JWT Authentication   |
                        | Rate Limiting        |
                        | Request IDs          |
                        | Logging              |
                        | Timeouts             |
                        | Provider Routing     |
                        +----------+-----------+
                                   |
                 +-----------------+-----------------+
                 |                                   |
                 |                                   |
        +--------v--------+                 +--------v--------+
        | OpenAI Provider |                 |   RAG Service   |
        +-----------------+                 |   (FastAPI)     |
                                            |-----------------|
                                            | Query Embedding |
                                            | Similarity      |
                                            | Context Builder |
                                            | Prompt Builder  |
                                            +--------+--------+
                                                     |
                                                     |
                                          +----------v----------+
                                          | PostgreSQL +        |
                                          | pgvector            |
                                          +----------+----------+
                                                     |
                                                     |
                                          +----------v----------+
                                          | Ollama / OpenAI     |
                                          +---------------------+
```

## Components

### API Gateway (Go)

Responsibilities:

* JWT Authentication
* Redis Rate Limiting
* Request ID propagation
* Structured logging
* Request timeouts
* Provider routing
* Service-to-service communication

Public APIs:

```
POST /v1/chat
POST /v1/rag
GET  /healthz
GET  /metrics
```

---

### RAG Service (Python)

Responsibilities:

* Document upload
* Text extraction
* Token-aware chunking
* Embedding generation
* Similarity search using pgvector
* Context construction
* Prompt construction
* LLM interaction

Internal APIs:

```
POST /v1/documents
POST /v1/rag
POST /v1/retrieval
```

The RAG service is intended to be an internal service. Clients communicate only with the Gateway.

---

## RAG Pipeline

### Document Ingestion

```text
Upload Document
        │
        ▼
Text Extraction
        │
        ▼
Token-aware Chunking
        │
        ▼
Embedding Generation
        │
        ▼
PostgreSQL + pgvector
```

### Question Answering

```text
User Question
       │
       ▼
Query Embedding
       │
       ▼
Similarity Search
       │
       ▼
Top-K Chunks
       │
       ▼
Context Builder
       │
       ▼
Prompt Builder
       │
       ▼
LLM
       │
       ▼
Answer
```

---

# Local Development

## Start the Platform

From the repository root:

```bash
docker compose up --build
```

This starts:

* API Gateway
* RAG Service
* PostgreSQL + pgvector
* Redis

---

## Generate a Development JWT

Install PyJWT once:

```bash
python3 -m pip install PyJWT
```

Generate and export a development token:

```bash
eval "$(python3 generate_jwt.py)"
```

Verify:

```bash
echo $TOKEN
```

---

## Upload a Document

Example:

```bash
curl -X POST http://localhost:8000/v1/documents \
  -F "file=@sample.txt"
```

---

## Query Through the Gateway

```bash
curl -X POST http://localhost:8080/v1/rag \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query":"What is RAG?",
    "top_k":3
  }'
```

Example response:

```json
{
  "answer": "RAG stands for Retrieval Augmented Generation."
}
```

---

## Project Structure

```text
llm-platform/
├── gateway/              # Go API Gateway
├── rag-service/          # FastAPI RAG service
├── agent-service/        # Future work
├── docker/
├── docs/
├── docker-compose.yml
└── README.md
```

---

## Current Version

### v0.2.0

Completed:

* Go API Gateway
* JWT Authentication
* Redis Rate Limiting
* Request ID Middleware
* Structured Logging
* Provider Abstraction
* OpenAI Provider
* Ollama Provider
* FastAPI RAG Service
* PostgreSQL
* pgvector
* Token-aware Chunking
* Embedding Providers
* Similarity Search
* Context Builder
* Prompt Builder
* Gateway → RAG Integration
* Docker Compose Platform
* End-to-End RAG through Gateway

---

## Next Milestone

Gateway-managed document ingestion:

```
Client
    │
    ▼
Gateway
    │
    ▼
RAG Service
    │
    ▼
PostgreSQL + pgvector
```

Clients will interact exclusively with the Gateway, while internal services remain private.
