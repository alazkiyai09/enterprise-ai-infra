from importlib import import_module
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.guardrails.encoding_detector import detect_encoding_layers

router = APIRouter(prefix="/api/v1/guard", tags=["guardrails"])


class GuardScanRequest(BaseModel):
    text: str = Field(..., min_length=1)


def _safe_call(factory_path: str, method_name: str, argument: str) -> dict[str, Any]:
    try:
        module_path, class_name = factory_path.rsplit(".", 1)
        module = import_module(module_path)
        cls = getattr(module, class_name)
        instance = cls()
        method = getattr(instance, method_name)
        result = method(argument)
        if hasattr(result, "__dict__"):
            payload = result.__dict__
        elif isinstance(result, tuple):
            payload = {"result": list(result)}
        elif isinstance(result, dict):
            payload = result
        else:
            payload = {"result": result}
        return {"status": "ok", **payload}
    except Exception as exc:
        return {"status": "unavailable", "error": str(exc)}


@router.post("/scan")
async def scan(payload: GuardScanRequest) -> dict[str, Any]:
    return {
        "prompt_injection": _safe_call(
            "src.guardrails.prompt_injection.prompt_injection.PromptInjectionDetector",
            "detect",
            payload.text,
        ),
        "jailbreak": _safe_call(
            "src.guardrails.jailbreak.jailbreak_detector.JailbreakDetector",
            "detect",
            payload.text,
        ),
        "pii": _safe_call(
            "src.guardrails.pii.pii_detector.PIIDetector",
            "detect",
            payload.text,
        ),
        "encoding": detect_encoding_layers(payload.text),
    }


@router.post("/prompt-injection")
async def prompt_injection(payload: GuardScanRequest) -> dict[str, Any]:
    return _safe_call(
        "src.guardrails.prompt_injection.prompt_injection.PromptInjectionDetector",
        "detect",
        payload.text,
    )


@router.post("/jailbreak")
async def jailbreak(payload: GuardScanRequest) -> dict[str, Any]:
    return _safe_call(
        "src.guardrails.jailbreak.jailbreak_detector.JailbreakDetector",
        "detect",
        payload.text,
    )


@router.post("/pii")
async def pii(payload: GuardScanRequest) -> dict[str, Any]:
    detect_result = _safe_call(
        "src.guardrails.pii.pii_detector.PIIDetector",
        "detect",
        payload.text,
    )
    redact_result = _safe_call(
        "src.guardrails.pii.pii_detector.PIIDetector",
        "redact",
        payload.text,
    )
    return {"detect": detect_result, "redact": redact_result}


@router.post("/encoding")
async def encoding(payload: GuardScanRequest) -> dict[str, Any]:
    return detect_encoding_layers(payload.text)


@router.post("/output")
async def output(payload: GuardScanRequest) -> dict[str, Any]:
    result = _safe_call(
        "src.guardrails.output_filter.output_guard.OutputGuard",
        "filter_output",
        payload.text,
    )
    if "result" in result and isinstance(result["result"], list) and len(result["result"]) == 2:
        sanitized, findings = result["result"]
        return {"status": result["status"], "sanitized_output": sanitized, "findings": findings}
    return result
