# AI Bridge Local 0.4.28 - supervisor dedupe seguro

Data: 2026-06-10

## Objetivo

A versão 0.4.28 corrige a etapa de dedupe do worker local.

O problema visto na validação anterior foi que o filtro operacional pegou também o processo PowerShell do comando em execução, porque a linha de comando continha o texto `brain_worker.py`. Ao tentar matar duplicados, o comando matou a si próprio, retornando falha.

## Correção

O supervisor agora só considera como worker candidatos que sejam processos Python:

```text
Name LIKE 'python%' AND CommandLine LIKE '%brain_worker.py%'
```

Com isso, processos PowerShell que apenas citam `brain_worker.py` não entram mais como worker.

## Comando de status

```powershell
python scripts/watcher/ai_bridge_local_supervisor.py --status
```

## Dedupe controlado

```powershell
python scripts/watcher/ai_bridge_local_supervisor.py --dedupe
```

Política de escolha:

1. Se o comando estiver rodando a partir de um worker, mantém o worker pai do comando.
2. Caso contrário, mantém o worker mais antigo.
3. Mata apenas outros processos Python cujo comando contenha `brain_worker.py`.

## Loop robusto

```powershell
python scripts/watcher/ai_bridge_local_supervisor.py --loop --interval 15 --dedupe
```

Ou via helper:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/watcher/start_ai_bridge_local_supervisor.ps1 -Loop -Interval 15
```

## Observação

A supervisão reinicia processos ausentes e o dedupe remove duplicatas do worker. A política ainda é conservadora: não mata gateway duplicado automaticamente, pois a porta `127.0.0.1:8766` deve ser validada antes de qualquer ação desse tipo.
