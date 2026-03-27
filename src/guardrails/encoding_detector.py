"""Lightweight encoding attack heuristics for the unified repo."""

import base64
import binascii
import re


def detect_encoding_layers(text: str) -> dict[str, object]:
    normalized = text.strip()
    findings: list[str] = []

    if re.fullmatch(r"[A-Za-z0-9+/=\s]{16,}", normalized):
        try:
            base64.b64decode(normalized, validate=True)
            findings.append("possible_base64")
        except (binascii.Error, ValueError):
            pass

    if re.fullmatch(r"(?:0x)?[0-9a-fA-F\s]{16,}", normalized):
        findings.append("possible_hex")

    if "\\u" in normalized or "\\x" in normalized:
        findings.append("escaped_unicode_or_hex")

    if re.search(r"\brot13\b|\bcaesar\b|\bdecode\b", normalized, re.IGNORECASE):
        findings.append("decoder_language")

    return {
        "status": "ok",
        "suspicious": bool(findings),
        "findings": findings,
    }
