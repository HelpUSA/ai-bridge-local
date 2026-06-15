from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def build_final_handoff_summary() -> dict[str, object]:
    version = (ROOT / "VERSION").read_text(encoding="utf-8-sig").strip()
    handoff = (ROOT / "docs" / "AI_BRIDGE_LOCAL_FINAL_HANDOFF_0532.md").read_text(encoding="utf-8-sig")

    required_phrases = [
        "Estado final seguro",
        "v0.5.20-release-process-batch",
        "v0.5.23-diagnostic-readonly-batch",
        "v0.5.26-observability-readonly-batch",
        "v0.5.28-preflight-dry-run-batch",
        "v0.5.32-final-safe-handoff",
        "Nenhuma entrega real inter-chat foi executada",
    ]

    missing = [phrase for phrase in required_phrases if phrase not in handoff]

    return {
        "readonly": True,
        "version": version,
        "handoff_doc": "docs/AI_BRIDGE_LOCAL_FINAL_HANDOFF_0532.md",
        "missing_phrases": missing,
        "complete": len(missing) == 0,
    }