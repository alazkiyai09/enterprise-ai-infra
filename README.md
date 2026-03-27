# Enterprise AI Infrastructure (`enterprise-ai-infra`)

AI infrastructure service for **data ingestion pipelines**, **embedding/vector processing**, and **LLM guardrails** (prompt-injection, jailbreak, PII, encoding, and output filtering). Designed for production workloads that need secure, observable AI operations.

## Why This Repository

Enterprise AI systems fail without reliable infra: ingestion, processing, storage, and safety controls. `enterprise-ai-infra` provides that foundation in a deployable API-oriented layout.

## Core Features

- Pipeline routes for process, query, and task status
- Guardrail routes for prompt and output risk controls
- Ingestion and processing modules with queue-oriented structure
- Embedding/vector interfaces for retrieval backends
- Monitoring and metrics integration
- Kubernetes manifests for production deployment baselines

## Project Structure

- `src/api/`: unified FastAPI app and infra route modules
- `src/pipeline/`: ingestion, processing, embedding, storage, workers
- `src/guardrails/`: prompt injection, jailbreak, PII, encoding, output filters
- `src/monitoring/`: metrics, health, tracing helpers
- `src/core/`: auth/security/rate-limit/error/secrets utilities
- `k8s/`: deployment, service, and autoscaling manifests

## API Endpoints

- `POST /api/v1/pipeline/process`
- `GET /api/v1/pipeline/status/{task_id}`
- `POST /api/v1/pipeline/query`
- `POST /api/v1/guard/scan`
- `POST /api/v1/guard/prompt-injection`
- `POST /api/v1/guard/jailbreak`
- `POST /api/v1/guard/pii`
- `POST /api/v1/guard/encoding`
- `POST /api/v1/guard/output`
- `GET /health`
- `GET /metrics`

## Quick Start

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

## SEO Keywords

enterprise ai infrastructure, llm guardrails, ai pipeline service, fastapi ai ops, prompt injection detection api, pii detection service, vector pipeline backend
