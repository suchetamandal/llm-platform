# LLM Gateway

A production-style LLM Gateway built in Go.

## Features

- Go + Gin
- REST API
- Streaming responses (SSE)
- Provider abstraction
- Authentication middleware
- Rate limiting
- Structured logging
- Request IDs

## Project Structure

```
gateway/
├── config/
├── handlers/
├── middleware/
├── models/
├── services/
│   └── llm/
└── main.go
```

## Roadmap

- [x] Basic API Gateway
- [x] Middleware
- [x] Mock LLM Provider
- [ ] OpenAI Integration
- [ ] Ollama Integration
- [ ] Redis Rate Limiting
- [ ] Metrics
- [ ] Docker
- [ ] Kubernetes
