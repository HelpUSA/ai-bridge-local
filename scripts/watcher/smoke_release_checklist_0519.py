from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def version_tuple(value):
    return tuple(int(part) for part in value.split("."))

VERSION = (ROOT / "VERSION").read_text(encoding="utf-8-sig").strip()
assert version_tuple(VERSION) >= version_tuple("0.5.19"), VERSION

doc = (ROOT / "docs" / "RELEASE_CHECKLIST_0519.md").read_text(encoding="utf-8-sig")
guide = (ROOT / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md").read_text(encoding="utf-8-sig")

normalized = doc.replace("Não", "Nao").replace("não", "nao").replace("N�o", "Nao")

required_terms = [
    "Confirmar branch limpa",
    "Atualizar VERSION em UTF-8 sem BOM",
    "smoke_version_alignment.py",
    "smoke_docs.py",
    "git diff --check",
    "git add com caminhos explicitos",
    "push de main e tag",
    "Nao executar entrega inter-chat",
]

for term in required_terms:
    assert term in normalized, term

assert "Release checklist 0.5.19" in doc
assert "Release checklist 0.5.19" in guide
print("OK release_checklist_0519 " + VERSION)