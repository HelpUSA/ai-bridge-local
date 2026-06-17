from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE = ROOT / "knowledge"

KINDS = {
    "task": "tasks",
    "decision": "decisions",
    "error": "errors",
    "smoke": "smokes",
    "release": "releases",
}


def slugify(value: str) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "note"


def now_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def ensure_vault() -> None:
    required = [
        KNOWLEDGE / "00_HOME.md",
        KNOWLEDGE / "projects" / "ai-bridge-local" / "status.md",
        KNOWLEDGE / "templates" / "task.md",
        KNOWLEDGE / "templates" / "decision.md",
        KNOWLEDGE / "templates" / "error.md",
        KNOWLEDGE / "templates" / "smoke.md",
        KNOWLEDGE / "templates" / "release.md",
    ]

    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise SystemExit("missing knowledge vault files: " + repr(missing))


def build_note(kind: str, title: str, body: str, tags: list[str]) -> str:
    date = now_date()
    tag_lines = "\n".join(f"- {tag}" for tag in tags if tag)

    if not tag_lines:
        tag_lines = "- ai-bridge-local"

    safe_body = body.strip() or "Sem detalhes adicionais."

    return f"""# {title}

Tipo: {kind}
Data: {date}
Repo: ai-bridge-local

## Tags

{tag_lines}

## Links

- [[../projects/ai-bridge-local/status]]
- [[../00_HOME]]

## Conteudo

{safe_body}
"""


def write_note(kind: str, title: str, body: str, slug: str | None = None, tags: list[str] | None = None) -> Path:
    if kind not in KINDS:
        raise SystemExit("invalid kind: " + kind)

    ensure_vault()

    note_slug = slugify(slug or title)
    target_dir = KNOWLEDGE / KINDS[kind]
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{note_slug}.md"

    text = build_note(kind, title, body, tags or [])
    target.write_text(text.rstrip() + "\n", encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=sorted(KINDS))
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", default="")
    parser.add_argument("--slug", default="")
    parser.add_argument("--tags", default="")
    args = parser.parse_args()

    tags = [item.strip() for item in args.tags.split(",") if item.strip()]
    path = write_note(args.kind, args.title, args.body, slug=args.slug or None, tags=tags)
    print(path.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
