from pathlib import Path
import json
import re
from datetime import datetime, timezone

root = Path(".")
version_path = root / "VERSION"
manifest_path = root / "extension" / "manifest.json"
gateway_path = root / "gateway_local.py"
background_path = root / "extension" / "background.js"
content_path = root / "extension" / "content_script.js"
guide_path = root / "docs" / "AI_BRIDGE_LOCAL_GUIDE.md"

old_version = version_path.read_text(encoding="utf-8-sig").strip()
m = re.match(r"^(\d+)\.(\d+)\.(\d+)$", old_version)
if not m:
    raise SystemExit(f"VERSION invalida: {old_version!r}")

major, minor, patch = map(int, m.groups())
new_version = f"{major}.{minor}.{patch + 1}"
tag_name = f"v{new_version}-final-result-feedback-guard"

print(f"OLD_VERSION={old_version}")
print(f"NEW_VERSION={new_version}")
print(f"TAG_NAME={tag_name}")

version_path.write_text(new_version + "\n", encoding="utf-8")

manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
manifest["version"] = new_version
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def update_js_version(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text

    patterns = [
        (r'(const\s+VERSION\s*=\s*")[^"]+(")', rf'\g<1>{new_version}\2'),
        (r'(const\s+AI_BRIDGE_VERSION\s*=\s*")[^"]+(")', rf'\g<1>{new_version}\2'),
        (r'(const\s+AI_BRIDGE_LOCAL_VERSION\s*=\s*")[^"]+(")', rf'\g<1>{new_version}\2'),
        (r'(AI Bridge Local v)[0-9]+\.[0-9]+\.[0-9]+', rf'\g<1>{new_version}'),
    ]

    for pattern, repl in patterns:
        text = re.sub(pattern, repl, text)

    if text != original:
        path.write_text(text, encoding="utf-8")

update_js_version(background_path)
update_js_version(content_path)

gateway = gateway_path.read_text(encoding="utf-8", errors="replace")
original_gateway = gateway

helper_marker = "def is_final_result_feedback_notice(body):"
helper = r'''
def is_final_result_feedback_notice(body):
    """Return True for final-result messages that must not receive local accepted feedback."""
    if not isinstance(body, dict):
        return False

    command_id = str(body.get("command_id", "") or "")
    action = str(body.get("action", "") or "")
    message = str(body.get("message", "") or "")
    payload = body.get("payload", {})
    payload_json = body.get("payload_json", {})

    payload_text = ""
    try:
        payload_text = json.dumps(payload, ensure_ascii=False)
    except Exception:
        payload_text = str(payload or "")

    payload_json_text = ""
    try:
        payload_json_text = json.dumps(payload_json, ensure_ascii=False)
    except Exception:
        payload_json_text = str(payload_json or "")

    blob = "\n".join([message, payload_text, payload_json_text]).lower()

    if command_id.startswith("result_to_"):
        return True

    if "[ai_local_run]" in blob:
        return True

    if "result_is_final=1" in blob and "chat_can_continue=" in blob:
        return True

    if '"result_is_final": true' in blob or '"result_is_final": 1' in blob:
        return True

    if action == "send-chat-message" and "next_action=" in blob and "chat_can_continue=" in blob:
        return True

    return False


def should_skip_source_feedback(body):
    """Prevent feedback loops for local status and final result messages."""
    if not isinstance(body, dict):
        return False

    command_id = str(body.get("command_id", "") or "")
    if command_id.startswith("local_status_"):
        return True

    return is_final_result_feedback_notice(body)


'''

if helper_marker not in gateway:
    idx = gateway.find("def enqueue_source_feedback(")
    if idx < 0:
        raise SystemExit("Nao encontrei def enqueue_source_feedback em gateway_local.py")
    gateway = gateway[:idx] + helper + gateway[idx:]

guard_line = "    if should_skip_source_feedback(body):\n        return None\n"
if "def enqueue_source_feedback(" not in gateway:
    raise SystemExit("Nao encontrei enqueue_source_feedback apos inserir helper")

if guard_line not in gateway:
    gateway = re.sub(
        r"(def enqueue_source_feedback\(body, feedback_type, detail\):\n)",
        r"\1" + guard_line,
        gateway,
        count=1,
    )

if gateway == original_gateway:
    print("GATEWAY_PATCH=already_present_or_no_change")
else:
    gateway_path.write_text(gateway, encoding="utf-8")
    print("GATEWAY_PATCH=applied")

docs_dir = root / "docs"
docs_dir.mkdir(exist_ok=True)
doc_path = docs_dir / f"FINAL_RESULT_FEEDBACK_GUARD_{new_version.replace('.', '')}.md"

doc = f"""# AI Bridge Local {new_version} - final result feedback guard

Data: {datetime.now(timezone.utc).isoformat()}

## Objetivo

Impedir que o gateway gere feedback local intermediario para mensagens de resultado final.

## Problema observado

Quando o worker enfileira um resultado final como `result_to_<command_id>`, o gateway podia gerar tambem linhas `local_status_accepted_result_to_*`.

Essas linhas internas nao sao o resultado final real. Elas podiam ficar queued/delivering/failed e causar ruido, loops, reentrega antiga ou falsa impressao de que o `[AI_LOCAL_RUN]` final nao chegou.

## Correção

`gateway_local.py` agora possui:

- `is_final_result_feedback_notice(body)`
- `should_skip_source_feedback(body)`

A funcao `enqueue_source_feedback(...)` retorna sem gerar feedback quando o comando é:

- `local_status_*`
- `result_to_*`
- mensagem com `[AI_LOCAL_RUN]`
- mensagem com `result_is_final=1` e `chat_can_continue=...`

## Regra operacional

O fluxo esperado continua sendo:

1. feedback inicial de fila/queued;
2. resultado final real via `[AI_LOCAL_RUN]`.

O resultado final real permanece vindo de `brain_worker.py` por `enqueue_result_message(...)`.

## Mitigação temporária

`scripts/watcher/final_result_sweeper_v3.py` pode ser usado temporariamente para recuperar resultados finais recentes presos.

Nao usar v1/v2 em loop contínuo.

## Validação esperada

- `node --check extension/background.js`
- `node --check extension/content_script.js`
- `python -m py_compile gateway_local.py brain_worker.py`
- `python -m py_compile scripts/watcher/final_result_sweeper_v3.py`
- `git diff --check`
- `scripts/watcher/verify_final_result_queue.py`
"""

doc_path.write_text(doc, encoding="utf-8")
print(f"DOC_CREATED={doc_path}")

if guide_path.exists():
    guide = guide_path.read_text(encoding="utf-8", errors="replace")
    guide = re.sub(r"Versao atual:\s*[0-9]+\.[0-9]+\.[0-9]+", f"Versao atual: {new_version}", guide)
    guide = re.sub(r"- Versao atual:\s*[0-9]+\.[0-9]+\.[0-9]+", f"- Versao atual: {new_version}", guide)
    guide = re.sub(r"Marco publicado mais recente:\s*.*", f"Marco publicado mais recente: {tag_name}", guide)

    section_title = f"## Atualização {new_version} - final result feedback guard"
    if section_title not in guide:
        guide += f"""

{section_title}

- Impede feedback local intermediario para `result_to_*`.
- Evita `local_status_accepted_result_to_*` para resultados finais.
- Preserva o fluxo esperado: queued inicial + `[AI_LOCAL_RUN]` final.
- Mantem `final_result_sweeper_v3.py` apenas como mitigacao operacional temporaria.
"""
    guide_path.write_text(guide, encoding="utf-8")
    print("GUIDE_UPDATED=1")
else:
    print("GUIDE_UPDATED=0 guide_missing")

print("PATCHER_OK")
