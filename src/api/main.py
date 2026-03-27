from fastapi import FastAPI

from src.api.routers.guard import router as guard_router
from src.api.routers.pipeline import router as pipeline_router

app = FastAPI(
    title="enterprise-ai-infra",
    version="0.1.0",
    description="Unified infrastructure shell for event pipelines and AI guardrails.",
)

app.state.pipeline_tasks = {}

app.include_router(pipeline_router)
app.include_router(guard_router)


@app.get("/health", tags=["system"])
async def health() -> dict[str, object]:
    return {
        "status": "healthy",
        "repo": "enterprise-ai-infra",
        "queued_tasks": len(app.state.pipeline_tasks),
    }


@app.get("/metrics", tags=["system"])
async def metrics() -> dict[str, object]:
    return {
        "repo": "enterprise-ai-infra",
        "queued_tasks": len(app.state.pipeline_tasks),
        "guardrails": ["prompt_injection", "jailbreak", "pii", "encoding", "output"],
    }
