# AI Bridge Local 0.4.27 - supervisor local de gateway e worker

Data: 2026-06-10

## Objetivo

A versão 0.4.27 adiciona uma camada simples de supervisão local para reduzir queda silenciosa do gateway ou do worker.

O novo script observa:

- `gateway_local.py`
- `brain_worker.py`
- porta local `127.0.0.1:8766`

## Arquivos adicionados

- `scripts/watcher/ai_bridge_local_supervisor.py`
- `scripts/watcher/start_ai_bridge_local_supervisor.ps1`
- `docs/AI_BRIDGE_LOCAL_0427_SUPERVISOR_WORKER_ROBUSTNESS_2026-06-10.md`

## Modos principais

Status sem iniciar nada:

```powershell
python scripts/watcher/ai_bridge_local_supervisor.py --status
```

Uma checagem sem iniciar processos ausentes:

```powershell
python scripts/watcher/ai_bridge_local_supervisor.py --once --no-start
```

Uma checagem com restart de processos ausentes:

```powershell
python scripts/watcher/ai_bridge_local_supervisor.py --once
```

Loop de supervisão:

```powershell
python scripts/watcher/ai_bridge_local_supervisor.py --loop --interval 15
```

Via PowerShell helper:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/watcher/start_ai_bridge_local_supervisor.ps1 -Loop -Interval 15
```

## Política inicial

A versão 0.4.27 reinicia processos ausentes, mas não mata duplicados automaticamente. Duplicados devem ser analisados antes de qualquer dedupe, porque pode haver processo antigo ainda terminando ou execução manual temporária.

## Logs

Os logs ficam em:

```text
logs/supervisor/
```

Arquivos principais:

- `ai_bridge_local_supervisor.log`
- `gateway_local.stdout.log`
- `gateway_local.stderr.log`
- `brain_worker.stdout.log`
- `brain_worker.stderr.log`

## Observação operacional

Na inspeção anterior foram vistos dois workers simultâneos. A próxima etapa recomendada, após validar este supervisor, é criar uma política explícita de dedupe controlado para manter apenas um `brain_worker.py` ativo.
