from pathlib import Path
import re
from collections import Counter, defaultdict
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
REPORTS = ROOT / "reports"
META = DOCS / "_meta"

DOC_EXTS = {".md", ".txt", ".rst", ".adoc"}
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
VERSION_RE = re.compile(r"\b(?:v)?0\.\d+\.\d+(?:-[A-Za-z0-9._-]+)?\b")
TAG_RE = re.compile(r"#([A-Za-z0-9_-]+)")
STATUS_RE = re.compile(r"\b(DONE|TODO|FIXME|PENDING|PENDENTE|LEGACY|DEPRECATED|RISK|RISCO|ERROR|ERRO|FAIL)\b", re.I)

TOPICS = {
    "architecture": ["architecture", "arquitetura", "router", "adapter", "contract", "adr"],
    "interchat": ["interchat", "send-chat-message", "direct", "chat"],
    "gateway": ["gateway", "worker", "queue", "run-command", "local bridge"],
    "chatgpt": ["chatgpt", "gpt", "prosemirror", "prompt-textarea"],
    "gemini": ["gemini"],
    "deepseek": ["deepseek"],
    "helpusai": ["helpusai", "helpus ai"],
    "operations": ["runbook", "recovery", "triage", "rollback", "release"],
    "governance": ["governance", "risk", "approval", "audit"],
    "smoke-tests": ["smoke", "validation", "validacao", "test"],
    "diagnostics": ["diagnostic", "diagnostico", "error", "erro", "failure"],
}

def read_text(path: Path) -> str:
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except Exception:
            pass
    return path.read_text(encoding="utf-8", errors="replace")

def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def title_of(text: str, fallback: str) -> str:
    for line in text.splitlines():
        m = HEADING_RE.match(line)
        if m:
            return m.group(2).strip()
    return fallback

def headings_of(text: str):
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        m = HEADING_RE.match(line)
        if m:
            out.append((i, len(m.group(1)), m.group(2).strip()))
    return out

def classify(path: Path, text: str) -> str:
    hay = (rel(path) + "\n" + text[:5000]).lower()
    scores = []
    for topic, terms in TOPICS.items():
        score = sum(1 for term in terms if term.lower() in hay)
        if score:
            scores.append((score, topic))
    return sorted(scores, reverse=True)[0][1] if scores else "uncategorized"

def should_include(path: Path) -> bool:
    if path.suffix.lower() not in DOC_EXTS:
        return False
    s = rel(path)
    return s.startswith("docs/") or s.startswith("reports/") or ("/" not in s and path.suffix.lower() == ".md")

def version_key(v: str):
    m = re.search(r"0\.(\d+)\.(\d+)", v)
    return (int(m.group(1)), int(m.group(2))) if m else (-1, -1)

def main():
    files = sorted([p for p in ROOT.rglob("*") if p.is_file() and should_include(p)], key=lambda p: rel(p).lower())

    records = []
    topic_map = defaultdict(list)
    version_map = defaultdict(list)
    status_rows = []
    tag_counter = Counter()

    for path in files:
        text = read_text(path)
        title = title_of(text, path.stem)
        topic = classify(path, text)
        versions = sorted(set(VERSION_RE.findall(text)), key=version_key)
        tags = sorted(set(TAG_RE.findall(text)))

        for tag in tags:
            tag_counter[tag] += 1
        for v in versions:
            version_map[v].append(path)
        topic_map[topic].append(path)

        status_count = 0
        for i, line in enumerate(text.splitlines(), 1):
            if STATUS_RE.search(line):
                status_count += 1
                if len(status_rows) < 1000:
                    status_rows.append((path, i, line.strip()[:220]))

        records.append({
            "path": path,
            "title": title,
            "topic": topic,
            "versions": versions,
            "tags": tags,
            "headings": headings_of(text),
            "status_count": status_count,
            "lines": len(text.splitlines()),
        })

    inventory = [
        "---",
        "type: generated-index",
        "status: generated",
        "tags:",
        "  - docs",
        "  - inventory",
        "---",
        "",
        "# Documentation inventory",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "| File | Topic | Lines | Status markers | Title |",
        "|---|---:|---:|---:|---|",
    ]

    for r in records:
        inventory.append(f"| [[{rel(r['path']).replace('.md','')}]] | {r['topic']} | {r['lines']} | {r['status_count']} | {r['title']} |")

    write(META / "docs-inventory.md", "\n".join(inventory))

    topic_doc = [
        "---",
        "type: generated-index",
        "status: generated",
        "tags:",
        "  - docs",
        "  - topics",
        "---",
        "",
        "# Topic map",
        "",
    ]

    for topic, paths in sorted(topic_map.items()):
        topic_doc.append(f"## {topic}")
        topic_doc.append("")
        for p in paths:
            topic_doc.append(f"- [[{rel(p).replace('.md','')}]]")
        topic_doc.append("")

    write(META / "topic-map.md", "\n".join(topic_doc))

    timeline = [
        "---",
        "type: generated-index",
        "status: generated",
        "tags:",
        "  - docs",
        "  - history",
        "---",
        "",
        "# Evolution timeline by version",
        "",
    ]

    for v in sorted(version_map.keys(), key=version_key):
        timeline.append(f"## {v}")
        timeline.append("")
        for p in sorted(version_map[v], key=lambda x: rel(x).lower()):
            timeline.append(f"- [[{rel(p).replace('.md','')}]]")
        timeline.append("")

    write(DOCS / "history" / "evolution-timeline.md", "\n".join(timeline))

    status_doc = [
        "---",
        "type: generated-index",
        "status: generated",
        "tags:",
        "  - docs",
        "  - status",
        "---",
        "",
        "# Status marker index",
        "",
    ]

    for p, line_no, line in status_rows:
        status_doc.append(f"- [[{rel(p).replace('.md','')}]] L{line_no}: {line}")

    write(META / "status-marker-index.md", "\n".join(status_doc))

    tags_doc = [
        "---",
        "type: generated-index",
        "status: generated",
        "tags:",
        "  - docs",
        "  - tags",
        "---",
        "",
        "# Tag index",
        "",
        "| Tag | Count |",
        "|---|---:|",
    ]

    for tag, count in tag_counter.most_common():
        tags_doc.append(f"| #{tag} | {count} |")

    write(META / "tag-index.md", "\n".join(tags_doc))

    print("OBSIDIAN_INDEXES_DONE")
    print(f"files={len(records)}")
    print(f"inventory={META / 'docs-inventory.md'}")
    print(f"timeline={DOCS / 'history' / 'evolution-timeline.md'}")

if __name__ == "__main__":
    main()