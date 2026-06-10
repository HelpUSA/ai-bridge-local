# AI Bridge Local 0.4.24 - local export package

Data: 2026-06-10

## Objetivo

Criar uma forma local de exportar a baseline operacional do AI Bridge Local sem depender de remoto/origin.

## Arquivos gerados localmente

- dist/ai-bridge-local-v0.4.23-consolidated-status.zip
- dist/ai-bridge-local-v0.4.23-consolidated-status.bundle

## Observacao importante

A pasta dist/ fica ignorada pelo git. Os pacotes sao artefatos locais e nao entram no historico.

## Como recriar o zip

git archive --format zip --output dist/ai-bridge-local-v0.4.23-consolidated-status.zip HEAD

## Como recriar o bundle

git bundle create dist/ai-bridge-local-v0.4.23-consolidated-status.bundle --all

## Como verificar

python scripts/watcher/ai_bridge_local_health.py
git status -sb
git tag --list v0.4.* --sort=-creatordate

## Estado base

- Baseline consolidada anterior: v0.4.23-consolidated-status
- Frente atual: v0.4.24-local-export-package
