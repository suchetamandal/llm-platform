# LLM Platform

> A production-style LLM Platform built to explore modern AI infrastructure and backend engineering patterns.

This project is designed to demonstrate the architecture, engineering practices, and infrastructure commonly used in production LLM systems. Rather than building a simple chatbot, the goal is to build a scalable platform capable of serving multiple models, supporting Retrieval-Augmented Generation (RAG), AI agents, observability, and distributed deployment.

---

# Project Goals

* Build a production-grade AI Gateway in Go
* Support multiple LLM providers through a common interface
* Implement streaming responses using Server-Sent Events (SSE)
* Build an enterprise RAG pipeline
* Learn AI infrastructure and distributed systems
* Demonstrate software engineering practices expected from Senior/Staff Backend Engineers

---

# Current Architecture

```
                Client
                   │
                   ▼
          Go AI Gateway (Gin)
                   │
 ┌─────────────────────────────────────┐
 │ Middleware                          │
 │                                     │
 │ • Request ID                        │
 │ • JWT Authentication                │
 │ • Redis Rate Limiting               │
 │ • Structured Logging                │
 │ • Timeout                           │
 │ • Prometheus Metrics                │
 └─────────────────────────────────────┘
                   │
                   ▼
             Chat Handler
                   │
                   ▼
              LLM Service
                   │
        ┌──────────┼──────────┐
        │          │          │
     Mock      Ollama     OpenAI
```

---

# Repository Structure

```
llm-platform/

├── gateway/
│   ├── cmd/
│   │   └── server/
│   ├── internal/
│   │   ├── config/
│   │   ├── handlers/
│   │   ├── middleware/
│   │   ├── models/
│   │   └── service/
│   │       └── llm/
│   ├── Dockerfile
│   ├── go.mod
│   └── go.sum
│
├── docker-compose.yml
└── README.md
```

---

# Features

## API

* `POST /v1/chat`
* `GET /healthz`
* `GET /metrics`

## Authentication

* JWT validation
* User claims extraction
* Context propagation

## Provider Abstraction

* Mock Provider
* Ollama Provider
* OpenAI Provider

## Middleware

* Request ID
* Structured Logging
* Redis Rate Limiting
* Request Timeout
* Prometheus Metrics

## Infrastructure

* Docker
* Docker Compose
* Redis
* Graceful Shutdown

---

# Streaming

The gateway streams responses using Server-Sent Events (SSE).

```
Client

↓

Gateway

↓

Provider

↓

Go Channel

↓

SSE Response
```

---

# Provider Routing

The gateway selects the provider based on the incoming request.

Example:

```json
{
  "provider": "ollama",
  "model": "llama3.2",
  "message": "Explain Retrieval-Augmented Generation."
}
```

or

```json
{
  "provider": "openai",
  "model": "gpt-4o-mini",
  "message": "Explain Retrieval-Augmented Generation."
}
```

---

# Running Locally

## Start Ollama

```bash
ollama serve
```

Pull a model:

```bash
ollama pull llama3.2
```

## Start Redis

```bash
docker compose up redis
```

## Run the Gateway

```bash
REDIS_ADDR=localhost:6379 \
JWT_SECRET=dev-secret \
CGO_ENABLED=0 \
go run ./gateway/cmd/server
```

---

# Running with Docker Compose

```bash
docker compose up --build
```

---

# Example Request

```bash
curl -N \
  -X POST http://localhost:8080/v1/chat \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
        "provider":"ollama",
        "model":"llama3.2",
        "message":"Explain vector databases."
      }'
```

---

# Technology Stack

## Backend

* Go
* Gin

## AI

* Ollama
* OpenAI

## Infrastructure

* Docker
* Docker Compose
* Redis

## Observability

* Prometheus

---

# Roadmap

## Phase 1 — AI Gateway ✅

* Go API Gateway
* JWT Authentication
* Provider Routing
* Redis Rate Limiting
* Streaming Responses
* Metrics
* Docker

## Phase 2 — Retrieval-Augmented Generation (Next)

* PDF Upload
* Document Chunking
* Embeddings
* PostgreSQL + pgvector
* Semantic Search
* Context Injection

## Phase 3 — Agents

* Tool Calling
* Memory
* Planner
* Multi-Agent Workflows

## Phase 4 — Production

* Kubernetes
* CI/CD
* OpenTelemetry
* Grafana
* Horizontal Scaling

---

# Why This Project?

Most open-source LLM projects focus on building chat applications.

This project focuses on building the infrastructure that powers those applications—API gateways, model routing, observability, scalability, authentication, and production-ready engineering patterns.

The goal is to simulate the architecture and engineering practices used by companies building large-scale AI platforms.
