# AI Bridge Local — Guia operacional completo e corrigido

Atualizado em: 2026-06-12 12:40 UTC  
Projeto local: `D:/dev/autocode/ai-bridge-local`  
Extensão atual: `0.4.37`  
Self-heal atual: `0.1.2`  
Gateway local: `http://127.0.0.1:8766`  
Banco local: `queue_local.db`  
Alvos oficiais da extensão: ChatGPT e HelpUSAI.

> **Regra de segurança deste guia:** os exemplos de envelope usam marcadores escritos como `<AI_BRIDGE_LOCAL_START>` e `<AI_BRIDGE_LOCAL_END>` para impedir que a extensão capture a documentação como comando real. Para executar um envelope real no chat com a extensão ativa, substitua esses placeholders pelos marcadores reais do AI Bridge Local, cada um sozinho em sua própria linha.

---

## 1. Erros encontrados no guia antigo

O guia anterior estava útil como histórico, mas continha pontos perigosos para operação atual:

1. Citava versões antigas, como `0.4.34` e `0.4.35`, quando a extensão atual é `0.4.37`.
2. Trazia caminho incorreto: `D/:dev/autocode/ai-bridge-local`; o correto é `D:/dev/autocode/ai-bridge-local`.
3. Tinha exemplos com marcadores reais dentro da documentação. Isso pode ser interpretado pela extensão como comando ao ser colado em um chat.
4. Havia marcadores malformados, como início com quantidade errada de `@` e fim com sufixo errado.
5. Alguns blocos terminavam com `}` e crases misturadas, quebrando o JSON.
6. Ainda recomendava `delivery_kind: "local_inter_agent_message"` para mensagens novas; o padrão atual é `inter_agent_message`.
7. Repetia trechos antigos de roadmap e status que contradiziam o estado atual.
8. Não separava claramente exemplos seguros, comandos reais e envio direto ao gateway.
9. Não tratava HelpUSAI como alvo oficial com regra de não interferir quando ela estiver sendo alterada por outro chat.
10. Não colocava `script_text/script_ext` como caminho preferencial para comandos longos.

---

## 2. Componentes atuais

### 2.1 Extensão do navegador

Arquivos:

- `extension/manifest.json`
- `extension/content_script.js`
- `extension/background.js`

Responsabilidades:

- detectar envelopes locais;
- enviar comandos ao gateway;
- consultar mensagens pendentes;
- injetar mensagens no chat destino;
- confirmar entrega;
- reportar erro de parse, erro de entrega e status operacional.

A versão deve estar alinhada nos três arquivos:

```text
0.4.37
```

### 2.2 Gateway local

Arquivo:

```text
gateway_local.py
```

Porta padrão:

```text
127.0.0.1:8766
```

Responsabilidades:

- receber envelopes e comandos;
- validar payload;
- gravar em `queue_local.db`;
- expor comandos pendentes para extensão e worker;
- registrar eventos, mensagens inválidas e dead letters;
- manter rastreabilidade de status.

### 2.3 Worker local

Arquivo:

```text
brain_worker.py
```

Responsabilidades:

- buscar comandos `run-command` destinados a `gateway-brain-supervisor`;
- executar comandos locais;
- capturar `stdout`, `stderr` e `return_code`;
- devolver resultado ao `source_chat_id` correto.

### 2.4 Control Center

Arquivos principais:

- `app_windows/control_center_app.py`
- `dist/AI-Bridge-Local-Control-Center/AI-Bridge-Local-Control-Center.exe`

Estado esperado:

- `control_center_count=1`
- `gateway_count=1`
- `worker_count=1`

### 2.5 Self-heal

Arquivo:

```text
scripts/watcher/self_heal.py
```

Versão atual:

```text
0.1.2
```

Funções:

- `--dry-run` explícito;
- `--apply` seguro;
- iniciar gateway ausente;
- iniciar worker ausente;
- parar workers duplicados mantendo o mais antigo;
- marcar `delivering` antigo como `failed`;
- marcar `queued` legado/smoke antigo como `failed`;
- registrar eventos;
- nunca apagar linhas do banco.

---

## 3. Regras obrigatórias

1. Auditar a extensão antes de declarar o sistema normalizado.
2. Sempre versionar a numeração ao alterar extensão, gateway, worker, Control Center, self-heal ou scripts operacionais.
3. Não usar `local_inter_agent_message` em comandos novos.
4. Usar `inter_agent_message` para mensagens entre chats.
5. Usar `local_capability` para comandos locais.
6. Para scripts grandes, usar `payload.script_text` com `payload.script_ext`, ou arquivo real.
7. Evitar `python -c` grande.
8. Evitar JSON cru dentro de `message`.
9. Não matar processos globais de Python, Node, Git, PowerShell ou CMD.
10. Para parar processo, filtrar por caminho exato do projeto e script esperado.
11. Não remover `.git/index.lock` sem verificar processos Git ativos.
12. Antes de `self_heal.py --apply`, fazer backup de `queue_local.db`.
13. Limpeza automática não deve apagar linhas do banco; deve marcar como `failed` e registrar evento.
14. Recarregar a extensão e dar F5 nos chats antes de smoke operacional completo.
15. HelpUSAI é alvo oficial, mas não deve ser testada se estiver sendo alterada por outro chat sem autorização.

---

## 4. IDs e destinos padrão

Destino local para `run-command`:

```text
gateway-brain-supervisor
```

Exemplo de chat operador:

```text
6a2b0a05-e1e4-83e9-9ab8-595c4c6ed1af
```

Chat ChatGPT alvo validado:

```text
6a2bf3a5-db50-83e9-8f12-2ff1f813cd0b
```

Host HelpUSAI:

```text
https://ai.helpusbr.com/*
```

---

## 5. Formato correto de envelope

Todo envelope real deve ter:

1. marcador de início sozinho na linha;
2. exatamente um JSON válido;
3. marcador de fim sozinho na linha.

Neste guia usamos placeholders:

```text
<AI_BRIDGE_LOCAL_START>
{ JSON_VALIDO_AQUI }
<AI_BRIDGE_LOCAL_END>
```

Ao executar de verdade, substitua pelos marcadores reais do AI Bridge Local.

Campos principais:

| Campo | Uso |
|---|---|
| `command_id` | identificador único por tentativa |
| `source_chat_id` | chat que emite o comando |
| `target_chat_id` | destino |
| `action` | `send-chat-message` ou `run-command` |
| `delivery_kind` | `inter_agent_message` ou `local_capability` |
| `conversation_id` | agrupador lógico |
| `from_agent` | emissor |
| `message` | texto para outro chat |
| `payload` | dados técnicos de execução |

---

## 6. Enviar mensagem para outro chat

Use:

```text
action = send-chat-message
delivery_kind = inter_agent_message
```

Exemplo seguro:

```json
<AI_BRIDGE_LOCAL_START>
{
  "command_id": "exemplo_send_chat_message_001",
  "source_chat_id": "CHAT_ORIGEM_UUID",
  "target_chat_id": "CHAT_DESTINO_UUID",
  "action": "send-chat-message",
  "delivery_kind": "inter_agent_message",
  "conversation_id": "exemplo_conversa",
  "from_agent": "AI Bridge Local operator",
  "message": "TESTE. Responda apenas: ACK recebido.",
  "payload": {}
}
<AI_BRIDGE_LOCAL_END>
```

Regras:

- `message` deve estar no topo do JSON.
- Não usar `payload.message` para mensagem entre chats.
- Não usar `local_inter_agent_message` em comandos novos.
- Não colocar JSON grande dentro de `message`.
- Usar `command_id` novo em cada tentativa.

---

## 7. Executar comando local

Use:

```text
action = run-command
delivery_kind = local_capability
target_chat_id = gateway-brain-supervisor
```

Exemplo simples:

```json
<AI_BRIDGE_LOCAL_START>
{
  "command_id": "exemplo_git_status_001",
  "source_chat_id": "CHAT_ORIGEM_UUID",
  "target_chat_id": "gateway-brain-supervisor",
  "action": "run-command",
  "delivery_kind": "local_capability",
  "conversation_id": "exemplo_git_status",
  "from_agent": "AI Bridge Local operator",
  "payload": {
    "cwd": "D:/dev/autocode/ai-bridge-local",
    "timeout_seconds": 60,
    "command": ["git", "status", "-sb"]
  }
}
<AI_BRIDGE_LOCAL_END>
```

Regras:

- `cwd`, `timeout_seconds`, `command`, `script_text` e `script_ext` ficam dentro de `payload`.
- Não usar `target_chat_id: "local"`.
- Não colocar `cwd` ou `command` no topo do JSON.
- Usar barras normais `/` em caminhos escritos manualmente.

---

## 8. Executar script PowerShell seguro

```json
<AI_BRIDGE_LOCAL_START>
{
  "command_id": "exemplo_script_ps1_001",
  "source_chat_id": "CHAT_ORIGEM_UUID",
  "target_chat_id": "gateway-brain-supervisor",
  "action": "run-command",
  "delivery_kind": "local_capability",
  "conversation_id": "exemplo_script_ps1",
  "from_agent": "AI Bridge Local operator",
  "payload": {
    "cwd": "D:/dev/autocode/ai-bridge-local",
    "timeout_seconds": 120,
    "script_ext": ".ps1",
    "script_text": "Write-Output 'SCRIPT_OK'; git status -sb"
  }
}
<AI_BRIDGE_LOCAL_END>
```

---

## 9. Executar script Python seguro

```json
<AI_BRIDGE_LOCAL_START>
{
  "command_id": "exemplo_script_py_001",
  "source_chat_id": "CHAT_ORIGEM_UUID",
  "target_chat_id": "gateway-brain-supervisor",
  "action": "run-command",
  "delivery_kind": "local_capability",
  "conversation_id": "exemplo_script_py",
  "from_agent": "AI Bridge Local operator",
  "payload": {
    "cwd": "D:/dev/autocode/ai-bridge-local",
    "timeout_seconds": 120,
    "script_ext": ".py",
    "script_text": "from pathlib import Path\nprint('PY_OK')\nprint(Path.cwd())"
  }
}
<AI_BRIDGE_LOCAL_END>
```

---

## 10. Envio direto ao gateway local

Use quando o parser visual da extensão estiver capturando exemplos antigos da página.

```powershell
cd D:\dev\autocode\ai-bridge-local

$body = @{
  command_id = "teste_direto_gateway_001"
  source_chat_id = "CHAT_ORIGEM_UUID"
  target_chat_id = "CHAT_DESTINO_UUID"
  action = "send-chat-message"
  delivery_kind = "inter_agent_message"
  conversation_id = "teste_gateway"
  from_agent = "AI Bridge Local operator"
  message = "TESTE. Responda apenas: ACK."
  payload = @{}
} | ConvertTo-Json -Depth 10

Invoke-RestMethod `
  -Method Post `
  -Uri "http://127.0.0.1:8766/bridge/commands" `
  -ContentType "application/json" `
  -Body $body
```

---

## 11. Health check

```powershell
cd D:\dev\autocode\ai-bridge-local
python scripts\watcher\health_check.py
python scripts\watcher\self_heal.py --dry-run
python scripts\watcher\smoke_robustness.py
```

Esperado:

```text
gateway_count=1
worker_count=1
control_center_count=1
ROBUSTNESS_SMOKE_OK
```

No banco, não deve haver `queued` ou `delivering` antigo.

---

## 12. Self-heal

Dry-run:

```powershell
python scripts\watcher\self_heal.py --dry-run
```

Backup antes do apply:

```powershell
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
New-Item -ItemType Directory -Force -Path backups | Out-Null
Copy-Item queue_local.db "backups\queue_local_before_self_heal_$stamp.db" -Force
```

Apply:

```powershell
python scripts\watcher\self_heal.py --apply
```

O self-heal corrige:

- gateway ausente;
- worker ausente;
- worker duplicado;
- `delivering` antigo;
- `queued` legado/smoke antigo.

Não deve:

- apagar linhas do banco;
- parar Python global;
- parar Git;
- parar Node global;
- testar HelpUSAI sem autorização.

---

## 13. Auditoria da extensão

Arquivos:

```text
extension/manifest.json
extension/content_script.js
extension/background.js
```

Validar sintaxe:

```powershell
node --check extension\content_script.js
node --check extension\background.js
```

Conferir versão:

```powershell
Select-String -Path extension\manifest.json,extension\content_script.js,extension\background.js -SimpleMatch "VERSION","version","0.4."
```

Conferir hosts oficiais:

```text
https://chatgpt.com/*
https://ai.helpusbr.com/*
```

Devem estar em:

- `host_permissions`
- `content_scripts.matches`

---

## 14. ChatGPT e HelpUSAI

### ChatGPT

Host:

```text
https://chatgpt.com/*
```

Uso:

- testes gerais do watcher;
- inter-chat;
- run-command via gateway;
- coordenação entre chats do projeto.

### HelpUSAI

Host:

```text
https://ai.helpusbr.com/*
```

Status:

- alvo oficial da extensão;
- deve ser auditada junto com ChatGPT;
- não testar quando a aplicação estiver sendo alterada por outro chat sem autorização.

Checklist antes de testar HelpUSAI:

1. Confirmar autorização.
2. Confirmar que outro chat não está alterando deploy, UI ou backend naquele momento.
3. Recarregar extensão.
4. Dar F5 na página HelpUSAI.
5. Confirmar `ai.helpusbr.com` no manifesto.
6. Enviar mensagem curta.
7. Verificar ACK.
8. Se houver erro, não insistir com múltiplos envios; coletar diagnóstico.

---

## 15. Versionamento

Ao alterar extensão, atualizar:

- `manifest.json`: `name` e `version`;
- `content_script.js`: comentário e `const VERSION`;
- `background.js`: comentário e `const VERSION`.

Ao alterar self-heal:

- atualizar `VERSION` em `scripts/watcher/self_heal.py`.

Ao alterar worker/gateway:

- atualizar constante de versão, se existir;
- atualizar guia/status operacional quando aplicável.

---

## 16. Checklist antes de commit

```powershell
git status -sb
python -m py_compile gateway_local.py brain_worker.py scripts\watcher\health_check.py scripts\watcher\self_heal.py scripts\watcher\smoke_robustness.py
node --check extension\content_script.js
node --check extension\background.js
python scripts\watcher\smoke_robustness.py
git diff --check
```

---

## 17. Smoke operacional com chat alvo

1. Recarregar extensão.
2. Dar F5 no chat origem.
3. Dar F5 no chat destino.
4. Enviar mensagem pequena.
5. Confirmar resposta no destino.
6. Verificar status no banco.

Consulta:

```powershell
@'
import sqlite3
con = sqlite3.connect("queue_local.db")
con.row_factory = sqlite3.Row
for r in con.execute("""
select command_id,status,created_at,delivered_at,acked_at,last_error
from commands
order by id desc
limit 10
"""):
    print(dict(r))
con.close()
'@ | Set-Content -Path temp\recent_commands.py -Encoding UTF8

python temp\recent_commands.py
```

---

## 18. Troubleshooting

### `envelope_parse_error`

Causas comuns:

- exemplo antigo com marcadores ainda visível na página;
- JSON inválido;
- aspas curvas;
- caracteres invisíveis;
- comando grande inline;
- texto fora do JSON dentro dos marcadores;
- marcadores malformados;
- fechamento de bloco quebrado;
- conteúdo antigo capturado pela extensão.

Correção:

1. Usar `command_id` novo.
2. Usar JSON estrito.
3. Usar `script_text/script_ext`.
4. Preferir envio direto pelo gateway se a tela estiver poluída por exemplos antigos.
5. Limpar o chat ou abrir nova conversa para comandos reais.

### `composer_not_empty_before_inject`

Causa: composer do chat destino já tinha texto.

Correção:

1. Limpar composer manualmente.
2. Recarregar chat.
3. Reenviar com `command_id` novo.

### `submit_not_confirmed_composer_still_has_text`

Causa: a extensão tentou enviar, mas o texto continuou no composer.

Correção:

1. Verificar botão de envio.
2. Verificar se a página está travada.
3. Dar F5.
4. Testar mensagem menor.
5. Coletar diagnóstico se persistir.

### `source_chat_id_mismatch`

Causa: envelope foi colado em chat diferente do `source_chat_id` declarado.

Correção:

1. Reenviar do chat correto.
2. Ajustar `source_chat_id`.
3. Usar envio direto ao gateway quando apropriado.

### Mensagem ficou `queued`

Verificar:

1. Chat destino está aberto?
2. Extensão está carregada?
3. Página destino recebeu F5?
4. `target_chat_id` está correto?
5. Gateway está rodando?
6. `self_heal.py --dry-run` mostra fila antiga?

### `delivering` antigo ou worker duplicado

```powershell
python scripts\watcher\self_heal.py --dry-run
python scripts\watcher\self_heal.py --apply
```

---

## 19. Comandos úteis

Estado Git:

```powershell
git status -sb
git log --oneline --decorate -8
git diff --stat
git diff --check
```

Saúde do bridge:

```powershell
python scripts\watcher\health_check.py
python scripts\watcher\self_heal.py --dry-run
python scripts\watcher\smoke_robustness.py
```

Processos:

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $PSItem.CommandLine -match "gateway_local.py|brain_worker.py|AI-Bridge-Local-Control-Center" } |
  Select-Object ProcessId,Name,CreationDate,CommandLine |
  Format-Table -AutoSize |
  Out-String -Width 4096
```

Status do banco:

```powershell
@'
import sqlite3
con = sqlite3.connect("queue_local.db")
con.row_factory = sqlite3.Row
for r in con.execute("select status, count(1) as n from commands group by status order by status"):
    print(dict(r))
con.close()
'@ | Set-Content -Path temp\db_status.py -Encoding UTF8

python temp\db_status.py
```

---

## 20. Roadmap consolidado

### Telemetria da extensão

Eventos desejados:

```text
envelope_detected
envelope_parse_error
envelope_semantic_error
postCommand_attempt
postCommand_ok
postCommand_failed
delivery_attempt
delivery_ok
delivery_failed
chat_heartbeat
extension_version
active_chat_seen
```

### Control Center v0.5.0

Objetivo:

- aplicativo Windows residente;
- tray icon;
- iniciar/parar/reiniciar gateway e worker;
- console ao vivo;
- tabela de chats ativos;
- fila por chat;
- últimos ACKs e erros;
- diagnóstico copiável;
- atualização segura com backup e rollback básico.

### Command Builder e Validator

Objetivo:

- reduzir uso de JSON cru;
- permitir intenções curtas;
- montar envelopes seguros;
- validar por JSON Schema;
- enviar inválidos para `invalid_messages`;
- enviar falhas persistentes para `dead_letters`.

Exemplos futuros de intenção:

```text
AI_LOCAL_INTENT send_chat target=CHAT_UUID message=ACK recebido
AI_LOCAL_INTENT run cwd=D:/dev/autocode/ai-bridge-local command=git status -sb
AI_LOCAL_INTENT run_script cwd=D:/dev/autocode/ai-bridge-local script=scripts/watcher/check_status.py
```

---

## 21. Commits recentes de referência

- `92174e4` — extensão 0.4.37 e HelpUSAI documentada.
- `c73f124` — regras operacionais.
- `b50ebd2` — correção de detecção do Control Center.
- `8949ef5` — `--dry-run` explícito no self-heal.
- `a4258bc` — self-heal inicial.
- `35d2313` — prevenção de workers duplicados.
- `2226317` — compatibilidade HelpUSAI 0.4.36.

---

## 22. Encerramento de ciclo

Um ciclo só deve ser considerado fechado quando:

1. Repo limpo e alinhado.
2. Health check OK.
3. Self-heal dry-run OK.
4. Smoke robustez OK.
5. Extensão auditada.
6. Versionamento conferido.
7. Chats recarregados.
8. Teste real feito no alvo autorizado.
9. HelpUSAI não foi testada durante alteração por outro chat, salvo autorização expressa.
10. Guia e regras operacionais atualizados.
