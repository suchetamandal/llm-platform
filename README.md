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

# v0.3.0 – Asynchronous Document Ingestion

## Overview

The RAG platform now supports asynchronous document ingestion. Documents are accepted through the API and immediately acknowledged, while ingestion (text extraction, chunking, embedding generation, and vector storage) executes asynchronously.

This design decouples document upload latency from indexing latency and establishes the foundation for production-scale ingestion pipelines.

---

## Architecture

```text
                    Public API
                         │
                         ▼
                API Gateway (Go)
                         │
                         ▼
               RAG Service (FastAPI)
                         │
              POST /v1/documents
                         │
                         ▼
              Save Uploaded Document
                         │
                         ▼
         Create Document Metadata (UPLOADED)
                         │
                         ▼
             Return Response Immediately
                         │
────────────────────────────────────────────────────────

              Background Processing Pipeline

────────────────────────────────────────────────────────
                         │
                         ▼
                  PROCESSING
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
          PostgreSQL + pgvector Storage
                         │
                         ▼
                      READY
```

---

## Document Lifecycle

Every uploaded document moves through a well-defined lifecycle.

```text
UPLOADED
    │
    ▼
PROCESSING
    │
    ├──────────────► FAILED
    │                    │
    ▼                    ▼
READY              Error Message Stored
```

### Status Definitions

| Status         | Description                                                |
| -------------- | ---------------------------------------------------------- |
| **UPLOADED**   | File successfully stored and metadata created.             |
| **PROCESSING** | Background ingestion pipeline is running.                  |
| **READY**      | Document has been indexed and is available for retrieval.  |
| **FAILED**     | Processing failed. Error details are stored for debugging. |

---

## Public APIs

### Upload Document

```http
POST /v1/documents
```

Uploads a document through the Gateway. The Gateway forwards the request to the internal RAG service.

Example response:

```json
{
  "document_id": "a1bcfd41-f264-44c4-a067-ab432378a424",
  "filename": "test.txt",
  "content_type": "text/plain",
  "status": "UPLOADED"
}
```

---

### Document Status

```http
GET /v1/documents/{document_id}
```

Example response:

```json
{
  "document_id": "a1bcfd41-f264-44c4-a067-ab432378a424",
  "filename": "test.txt",
  "content_type": "text/plain",
  "status": "READY",
  "error_message": null
}
```

---

## Current Ingestion Pipeline

The background ingestion pipeline performs the following steps:

1. Save uploaded document
2. Create document metadata
3. Extract text
4. Perform token-aware chunking
5. Generate embeddings
6. Store vectors in PostgreSQL with pgvector
7. Update document status

---

## Current Platform Architecture

```text
                Client
                   │
                   ▼
           API Gateway (Go)
          ├───────────────┐
          │               │
          ▼               ▼
     Chat Requests   Document Uploads
          │               │
          └──────┬────────┘
                 ▼
         RAG Service (FastAPI)
                 │
      ┌──────────┴──────────┐
      ▼                     ▼
Document Processing    Retrieval Pipeline
      │                     │
      ▼                     ▼
PostgreSQL + pgvector    Ollama / OpenAI
```

---

## Next Milestone

**v0.4.0 – Durable Background Processing**

The current implementation uses FastAPI BackgroundTasks for asynchronous ingestion.

The next milestone replaces in-process background tasks with a production-ready job queue and worker architecture using Redis, enabling durable jobs, retries, worker scaling, and improved fault tolerance.


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


## v0.5.0 – Streaming RAG Responses

The platform now supports end-to-end streaming RAG responses through the Gateway.

### API

```http
POST /v1/rag/stream

```

Example 

```bash
curl -N -X POST http://localhost:8080/v1/rag/stream \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query":"What is RAG?",
    "top_k":3
  }'
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
