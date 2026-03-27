# enterprise-ai-infra

Unified infrastructure repo created from `enterprise-ai-systems` for stream processing and AI guardrails.

## Included sources

- `src/pipeline/*` wrappers over migrated StreamProcess modules
- `src/guardrails/*` wrappers over migrated AIGuard modules
- `src/api/main.py` unified shell for `/pipeline/*` and `/guard/*`
- `k8s/` manifests copied from `StreamProcess-Pipeline`

## Unified API shell

Run:

```bash
uvicorn src.api.main:app --reload
```

Key routes:

- `POST /api/v1/pipeline/process`
- `GET /api/v1/pipeline/status/{task_id}`
- `POST /api/v1/guard/scan`
- `POST /api/v1/guard/pii`
- `GET /health`

