from hashlib import sha256
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/pipeline", tags=["pipeline"])


class PipelineProcessRequest(BaseModel):
    content: str = Field(..., min_length=1)
    event_type: str = Field("generic")
    metadata: dict[str, object] = Field(default_factory=dict)


@router.post("/process")
async def process(payload: PipelineProcessRequest, request: Request) -> dict[str, object]:
    task_id = str(uuid4())
    request.app.state.pipeline_tasks[task_id] = {
        "status": "queued",
        "event_type": payload.event_type,
        "content_hash": sha256(payload.content.encode("utf-8")).hexdigest(),
        "metadata": payload.metadata,
    }
    return {"task_id": task_id, "status": "queued"}


@router.get("/status/{task_id}")
async def status(task_id: str, request: Request) -> dict[str, object]:
    task = request.app.state.pipeline_tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, **task}


@router.post("/query")
async def query_vector_store(payload: dict[str, object]) -> dict[str, object]:
    return {
        "status": "accepted",
        "message": "Vector store abstractions were migrated; connect a live backend before querying.",
        "request": payload,
    }

