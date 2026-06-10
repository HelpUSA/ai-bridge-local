# AI Bridge Local 0.4.22 - cleanup policy

Data: 2026-06-10

## Objetivo

A frente 0.4.22 adiciona uma política de limpeza segura para `temp/watcher_scripts`, evitando remoções acidentais.

## Arquivo adicionado

- `scripts/watcher/ai_bridge_local_cleanup_policy.py`

## Comportamento

O script lista os arquivos temporários mais antigos que excedem a retenção configurada por `--keep`.

Por padrão, ele roda em modo seguro e apenas imprime `WOULD_DELETE`.

## Uso seguro

```text
python scripts/watcher/ai_bridge_local_cleanup_policy.py --keep 30
```

## Uso efetivo com remoção

A remoção exige duas condições:

1. passar `--delete`;
2. passar `--confirm AI_BRIDGE_LOCAL_DELETE_TEMP_SCRIPTS`.

```text
python scripts/watcher/ai_bridge_local_cleanup_policy.py --keep 30 --delete --confirm AI_BRIDGE_LOCAL_DELETE_TEMP_SCRIPTS
```

## Validação

Nesta etapa, o script foi executado em dry-run. Como a quantidade atual estava abaixo da retenção 30, nenhuma remoção foi necessária.

## Relação com versões anteriores

- 0.4.18 criou o utilitário simples de cleanup.
- 0.4.21 criou health check rápido.
- 0.4.22 adiciona uma camada de política segura para uso real de remoção.
