param(
  [string]$Root = "D:\dev\autocode\ai-bridge-local",
  [switch]$ForceOverwrite,
  [switch]$IncludeReports = $true
)

$ErrorActionPreference = "Stop"

function Info($m) { Write-Host "[INFO] $m" }
function Ok($m) { Write-Host "[OK] $m" }
function Warn($m) { Write-Host "[WARN] $m" }

function Write-TextFile {
  param(
    [Parameter(Mandatory=$true)][string]$Path,
    [Parameter(Mandatory=$true)][string]$Text,
    [switch]$Overwrite
  )

  $dir = Split-Path $Path -Parent
  if ($dir) {
    New-Item -ItemType Directory -Force $dir | Out-Null
  }

  if ((Test-Path $Path) -and (-not $Overwrite)) {
    Info "Mantido existente: $Path"
    return
  }

  Set-Content -Path $Path -Value $Text -Encoding UTF8
  Ok "Criado/atualizado: $Path"
}

function Read-TextSafe {
  param([Parameter(Mandatory=$true)][string]$Path)

  $encodings = @("utf8", "default")
  foreach ($enc in $encodings) {
    try {
      return Get-Content -Path $Path -Raw -Encoding $enc
    } catch {}
  }

  return Get-Content -Path $Path -Raw -ErrorAction SilentlyContinue
}

function Get-RelativePath {
  param(
    [Parameter(Mandatory=$true)][string]$Base,
    [Parameter(Mandatory=$true)][string]$FullPath
  )

  $baseUri = New-Object System.Uri(($Base.TrimEnd("\") + "\"))
  $fileUri = New-Object System.Uri($FullPath)
  return [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri($fileUri).ToString()).Replace("/", "\")
}

function Get-DocTitle {
  param(
    [string]$Text,
    [string]$Fallback
  )

  foreach ($line in ($Text -split "`r?`n")) {
    if ($line -match "^(#{1,6})\s+(.+?)\s*$") {
      return $Matches[2].Trim()
    }
  }

  return $Fallback
}

function Get-Topic {
  param(
    [string]$RelPath,
    [string]$Text
  )

  $hay = ($RelPath + "`n" + $Text.Substring(0, [Math]::Min(5000, $Text.Length))).ToLowerInvariant()

  $rules = [ordered]@{
    "architecture" = @("architecture", "arquitetura", "router", "adapter", "contract", "adr", "design")
    "interchat" = @("interchat", "send-chat-message", "direct", "chat", "handoff")
    "gateway" = @("gateway", "worker", "queue", "run-command", "local bridge", "sqlite")
    "chatgpt" = @("chatgpt", "gpt", "prosemirror", "prompt-textarea")
    "gemini" = @("gemini")
    "deepseek" = @("deepseek")
    "helpusai" = @("helpusai", "helpus ai")
    "operations" = @("runbook", "recovery", "triage", "rollback", "release", "operacional")
    "governance" = @("governance", "governanca", "risk", "risco", "approval", "audit")
    "smoke-tests" = @("smoke", "validation", "validacao", "test")
    "diagnostics" = @("diagnostic", "diagnostico", "error", "erro", "failure", "falha")
  }

  $bestTopic = "uncategorized"
  $bestScore = 0

  foreach ($topic in $rules.Keys) {
    $score = 0
    foreach ($term in $rules[$topic]) {
      if ($hay.Contains($term.ToLowerInvariant())) {
        $score += 1
      }
    }

    if ($score -gt $bestScore) {
      $bestScore = $score
      $bestTopic = $topic
    }
  }

  return $bestTopic
}

function Convert-ToWikiLink {
  param([string]$RelPath)

  $p = $RelPath.Replace("\", "/")
  if ($p.EndsWith(".md")) {
    $p = $p.Substring(0, $p.Length - 3)
  }
  return "[[$p]]"
}

function Add-GitIgnoreBlock {
  $block = @"

# Obsidian local workspace
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache
.obsidian/plugins
"@

  if (Test-Path ".gitignore") {
    $current = Get-Content ".gitignore" -Raw
    if ($current -notmatch "\.obsidian/workspace\.json") {
      Add-Content -Path ".gitignore" -Value $block
      Ok ".gitignore atualizado"
    } else {
      Info ".gitignore ja contem regras do Obsidian"
    }
  } else {
    Set-Content -Path ".gitignore" -Value $block.TrimStart() -Encoding UTF8
    Ok ".gitignore criado"
  }
}

function Setup-ObsidianDocs {
  Info "Preparando estrutura Obsidian"

  $folders = @(
    ".obsidian",
    "docs\_meta",
    "docs\assets",
    "docs\templates",
    "docs\tutorials",
    "docs\how-to",
    "docs\reference",
    "docs\explanation",
    "docs\architecture",
    "docs\operations",
    "docs\decisions",
    "docs\history",
    "docs\releases",
    "docs\legacy",
    "scripts\docs"
  )

  foreach ($folder in $folders) {
    New-Item -ItemType Directory -Force $folder | Out-Null
  }

  Add-GitIgnoreBlock

  Write-TextFile ".obsidian\app.json" @"
{
  "alwaysUpdateLinks": true,
  "newFileLocation": "current",
  "attachmentFolderPath": "docs/assets",
  "promptDelete": false
}
"@ -Overwrite:$ForceOverwrite

  Write-TextFile ".obsidian\core-plugins.json" @"
[
  "file-explorer",
  "global-search",
  "switcher",
  "graph",
  "backlink",
  "outgoing-link",
  "tag-pane",
  "page-preview",
  "templates",
  "note-composer",
  "command-palette",
  "markdown-importer",
  "word-count"
]
"@ -Overwrite:$ForceOverwrite

  Write-TextFile ".obsidian\templates.json" @"
{
  "folder": "docs/templates"
}
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\index.md" @"
---
type: docs-home
status: current
tags:
  - docs
  - index
---

# AI Bridge Local Documentation

Este e o ponto de entrada da documentacao atual.

## Comece por aqui

- [[docs/architecture/overview|Architecture overview]]
- [[docs/reference/envelope-contract|Envelope contract]]
- [[docs/reference/router-contract|Router contract]]
- [[docs/reference/adapter-contract|Adapter contract]]
- [[docs/reference/transport-modes|Transport modes]]
- [[docs/operations/runbook|Operations runbook]]
- [[docs/history/evolution-timeline|Evolution timeline]]
- [[docs/_meta/docs-inventory|Documentation inventory]]
- [[docs/_meta/topic-map|Topic map]]

## Organizacao

- tutorials: primeiros passos guiados.
- how-to: tarefas especificas.
- reference: contratos, schemas, campos e erros.
- explanation: arquitetura e decisoes.
- architecture: visao de arquitetura.
- operations: runbooks, release e rollback.
- decisions: ADRs.
- history: evolucao e legado.
- legacy: documentos antigos preservados.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\architecture\overview.md" @"
---
type: explanation
status: draft
tags:
  - architecture
  - extension
  - router
---

# Architecture overview

## Objetivo

Separar responsabilidades dentro da extensao atual do AI Bridge Local sem mover a extensao de pasta agora.

## Componentes

- Core/router
- App talk-inter-chat
- App local-gateway-client
- Adapters por IA
- Gateway local

## Decisao atual

A extensao continua dentro de ai-bridge-local, mas o codigo deve ser separado por dominio.

## Fronteiras

- Conversa entre chats nao deve depender do gateway local.
- Execucao de comandos locais deve passar pelo gateway local.
- Cada IA deve ter adapter isolado.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\architecture\extension-router.md" @"
---
type: explanation
status: draft
tags:
  - architecture
  - router
---

# Extension router

## Responsabilidade

O router interno decide se um envelope deve ir para conversa direta entre chats ou para o gateway local.

## Principios

- O router decide rota.
- Apps executam a rota.
- Adapters conhecem cada IA.
- Gateway local executa comandos locais.

## Rotas principais

- direct_interchat: conversa entre abas.
- local_gateway: execucao via gateway local.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\architecture\direct-interchat.md" @"
---
type: explanation
status: draft
tags:
  - architecture
  - interchat
---

# Direct interchat

## Definicao

Direct interchat e o caminho para conversa entre chats abertos no navegador.

## Regra

Nao usa gateway local, fila local, banco local nem API web.

## Fluxo

Chat origem envia envelope. A extensao roteia para a aba destino. O adapter da IA destino injeta e envia a mensagem.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\architecture\local-gateway-client.md" @"
---
type: explanation
status: draft
tags:
  - architecture
  - gateway
---

# Local gateway client

## Definicao

Local gateway client e o app interno da extensao responsavel por encaminhar comandos locais ao gateway local.

## Quando usar

- run-command
- smoke
- patch
- inspect
- tarefas locais

## Regra

Nao deve ser o caminho padrao para conversa comum entre chats.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\architecture\adapter-isolation.md" @"
---
type: explanation
status: draft
tags:
  - architecture
  - adapters
---

# Adapter isolation

## Problema

Mudancas no codigo do ChatGPT podem quebrar Gemini, DeepSeek ou HelpUSAI quando os adapters estao acoplados.

## Solucao

Cada IA deve ter adapter proprio com contrato e smokes especificos.

## Regra

Mudanca em um adapter nao deve alterar codigo dos outros adapters.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\reference\envelope-contract.md" @"
---
type: reference
status: draft
tags:
  - reference
  - envelope
  - contract
---

# Envelope contract

## Campos principais

- schema
- schema_version
- command_id
- transport
- action
- source_chat_id
- target_chat_id
- delivery_kind
- message
- payload
- force_gateway

## Transportes

- direct_interchat
- local_gateway

## Compatibilidade

Enquanto envelopes antigos existirem, o router pode inferir rota por action.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\reference\router-contract.md" @"
---
type: reference
status: draft
tags:
  - reference
  - router
  - contract
---

# Router contract

## Responsabilidade

Decidir o caminho correto a partir do envelope.

## Rotas

| Condicao | Rota |
|---|---|
| transport=direct_interchat | apps/talk-inter-chat |
| transport=local_gateway | apps/local-gateway-client |
| action=send-chat-message sem force_gateway | apps/talk-inter-chat |
| action=run-command | apps/local-gateway-client |
| force_gateway=true | apps/local-gateway-client |

## Restricoes

- O router nao deve conhecer detalhes de ChatGPT, Gemini, DeepSeek ou HelpUSAI.
- O router nao deve executar comandos.
- O router nao deve manipular DOM diretamente.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\reference\adapter-contract.md" @"
---
type: reference
status: draft
tags:
  - reference
  - adapters
  - contract
---

# Adapter contract

Cada IA deve ter adapter isolado.

## Adapters atuais

- ChatGPT
- Gemini
- DeepSeek
- HelpUSAI

## Interface esperada

- detectPage
- getChatId
- findComposer
- injectText
- clickSend
- captureOutboundEnvelope
- showReceipt

## Regra de isolamento

Mudanca em um adapter nao pode alterar codigo dos outros adapters.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\reference\transport-modes.md" @"
---
type: reference
status: draft
tags:
  - reference
  - transport
---

# Transport modes

## direct_interchat

Usado para conversa direta entre chats abertos no navegador.

## local_gateway

Usado para comandos locais, patches, smokes e inspecoes locais.

## Regra de prioridade

send-chat-message sem force_gateway deve ir para direct_interchat. run-command deve ir para local_gateway.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\reference\error-taxonomy.md" @"
---
type: reference
status: draft
tags:
  - reference
  - errors
  - diagnostics
---

# Error taxonomy

## envelope_parse_error

Falha ao parsear envelope.

## composer_empty_after_inject

O compositor foi encontrado, mas a injecao nao colocou texto.

## submit_not_confirmed_composer_still_has_text

A extensao tentou enviar, mas a mensagem continuou no compositor.

## source_chat_id_mismatch

O source_chat_id do envelope nao corresponde ao chat atual.

## direct_interchat_or_capture_failed

Falha de envio direto ou captura.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\reference\smoke-test-matrix.md" @"
---
type: reference
status: draft
tags:
  - reference
  - smoke
  - tests
---

# Smoke test matrix

## Core/router

- parse envelope
- classify route
- direct_interchat sem gateway
- local_gateway para run-command
- force_gateway respeitado

## Adapters

Cada adapter deve validar:

- detectPage
- getChatId
- findComposer
- injectText
- clickSend
- captureOutboundEnvelope
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\operations\runbook.md" @"
---
type: operations
status: draft
tags:
  - operations
  - runbook
---

# Operations runbook

## Fluxos principais

- Conversa entre chats.
- Execucao de comando local.
- Diagnostico de falha de parse.
- Diagnostico de falha de composer.
- Release e rollback.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\operations\diagnostics.md" @"
---
type: operations
status: draft
tags:
  - operations
  - diagnostics
---

# Diagnostics

## Checklist rapido

1. Confirmar versao runtime.
2. Confirmar source_chat_id.
3. Confirmar target_chat_id.
4. Confirmar rota esperada.
5. Confirmar se a falha e de parse, captura, injecao ou envio.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\operations\release-process.md" @"
---
type: operations
status: draft
tags:
  - operations
  - release
---

# Release process

## Ordem

1. git status limpo ou mudancas conhecidas.
2. aplicar patch pequeno.
3. node --check quando houver JS.
4. smokes especificos.
5. git diff --check.
6. commit.
7. tag.
8. push.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\operations\rollback.md" @"
---
type: operations
status: draft
tags:
  - operations
  - rollback
---

# Rollback

## Principio

Rollback deve retornar ao ultimo commit/tag validado.

## Checklist

- identificar tag valida
- revisar git status
- criar backup se houver alteracoes locais
- reverter com git revert ou reset controlado
- rodar smokes minimos
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\how-to\send-message-between-chats.md" @"
---
type: how-to
status: draft
tags:
  - how-to
  - interchat
---

# Send message between chats

## Objetivo

Enviar mensagem de um chat para outro sem gateway local.

## Rota esperada

send-chat-message deve ir para talk-inter-chat, salvo force_gateway=true.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\how-to\run-local-command.md" @"
---
type: how-to
status: draft
tags:
  - how-to
  - gateway
---

# Run local command

## Objetivo

Executar comando local pelo gateway local.

## Rota esperada

run-command deve ir para local-gateway-client.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\how-to\add-new-ai-adapter.md" @"
---
type: how-to
status: draft
tags:
  - how-to
  - adapters
---

# Add new AI adapter

## Passos

1. Criar adapter isolado.
2. Declarar capacidades.
3. Implementar detectPage e getChatId.
4. Implementar composer e sender.
5. Implementar captura outbound.
6. Criar smokes especificos.
7. Rodar matriz minima dos adapters antigos.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\how-to\recover-from-envelope-error.md" @"
---
type: how-to
status: draft
tags:
  - how-to
  - diagnostics
---

# Recover from envelope error

## envelope_parse_error

Verificar se o bloco capturado e JSON valido.

## Regras

- Nao usar JSON abreviado.
- Nao usar exemplos com marcador real.
- Envelopes executaveis devem ser JSON estrito.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\decisions\ADR-0001-docs-architecture.md" @"
---
type: adr
status: proposed
tags:
  - adr
  - docs
---

# ADR-0001: Adopt Diataxis-style documentation

## Status

Proposed

## Context

A documentacao cresceu com historico, relatorios, smokes e guias operacionais misturados.

## Decision

Organizar a documentacao em tutorials, how-to, reference, explanation, operations, decisions, releases e history.

## Consequences

- Facilita onboarding.
- Reduz duplicacao.
- Preserva historico sem poluir documentacao atual.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\decisions\ADR-0002-extension-internal-router.md" @"
---
type: adr
status: proposed
tags:
  - adr
  - router
  - extension
---

# ADR-0002: Keep extension in ai-bridge-local and isolate internal apps

## Status

Proposed

## Context

A extensao atual precisa conversar entre chats e tambem encaminhar comandos ao gateway local.

## Decision

Manter a extensao na pasta atual por enquanto, mas separar internamente:

- apps/talk-inter-chat
- apps/local-gateway-client
- adapters
- core/router

## Consequences

- Evita migracao prematura.
- Reduz risco de quebrar gateway ao mexer em interchat.
- Prepara extracao futura se necessario.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\decisions\ADR-0003-direct-interchat-no-gateway.md" @"
---
type: adr
status: proposed
tags:
  - adr
  - interchat
  - gateway
---

# ADR-0003: Direct interchat must not depend on local gateway

## Status

Proposed

## Context

Conversas entre chats precisam funcionar sem gateway local, sem fila e sem banco.

## Decision

send-chat-message entre chats deve usar rota direta por aba registrada, salvo force_gateway=true.

## Consequences

- Menor latencia.
- Menos acoplamento.
- Gateway local fica reservado para comandos e tarefas locais.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\decisions\ADR-0004-adapter-isolation.md" @"
---
type: adr
status: proposed
tags:
  - adr
  - adapters
  - isolation
---

# ADR-0004: Isolate AI platform adapters

## Status

Proposed

## Context

Correcoes em ChatGPT podem quebrar Gemini, DeepSeek ou HelpUSAI quando o codigo fica acoplado.

## Decision

Cada IA deve ter adapter proprio e smokes proprios.

## Consequences

- Mudancas ficam contidas.
- Novas IAs entram sem reescrever adapters antigos.
- Mudancas no core exigem matriz completa de regressao.
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\history\legacy-map.md" @"
---
type: history
status: draft
tags:
  - history
  - legacy
---

# Legacy map

Este arquivo sera usado para mapear documentos antigos para a nova estrutura.

## Categorias

- manter como atual
- consolidar
- mover para legacy
- transformar em ADR
- transformar em runbook
- transformar em referencia
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\templates\ADR-template.md" @"
---
type: adr
status: proposed
tags:
  - adr
---

# ADR-NNNN: Title

## Status

Proposed | Accepted | Deprecated | Superseded

## Context

## Decision

## Consequences

## Related
"@ -Overwrite:$ForceOverwrite

  Write-TextFile "docs\templates\reference-template.md" @"
---
type: reference
status: draft
tags:
  - reference
---

# Title

## Purpose

## Contract

## Fields

## Errors

## Examples

## Related
"@ -Overwrite:$ForceOverwrite

  Ok "Setup base do Obsidian concluido"
}

function Build-ObsidianIndexes {
  Info "Gerando indices do Obsidian"

  $docExts = @(".md", ".txt", ".rst", ".adoc")
  $skipFragments = @(
    "\.git\",
    "\node_modules\",
    "\.venv\",
    "\venv\",
    "\__pycache__\",
    "\reports\docs_reorg_audit_"
  )

  $files = Get-ChildItem -Path $Root -Recurse -File | Where-Object {
    $full = $_.FullName
    $ext = $_.Extension.ToLowerInvariant()
    if ($docExts -notcontains $ext) { return $false }

    foreach ($frag in $skipFragments) {
      if ($full -like "*$frag*") { return $false }
    }

    $rel = Get-RelativePath -Base $Root -FullPath $full
    if ($rel -like "docs\*") { return $true }
    if ($IncludeReports -and $rel -like "reports\*") { return $true }
    if (($rel -notlike "*\*") -and ($ext -eq ".md")) { return $true }

    return $false
  } | Sort-Object FullName

  $records = @()
  $topicMap = @{}
  $versionMap = @{}
  $statusRows = New-Object System.Collections.Generic.List[string]
  $tagCount = @{}
  $hashMap = @{}

  foreach ($file in $files) {
    $rel = Get-RelativePath -Base $Root -FullPath $file.FullName
    $text = Read-TextSafe -Path $file.FullName
    if ($null -eq $text) { $text = "" }

    $title = Get-DocTitle -Text $text -Fallback $file.BaseName
    $topic = Get-Topic -RelPath $rel -Text $text
    $lines = ($text -split "`r?`n").Count

    $versions = @()
    foreach ($m in [regex]::Matches($text, "\b(?:v)?0\.\d+\.\d+(?:-[A-Za-z0-9._-]+)?\b")) {
      $versions += $m.Value
    }
    $versions = $versions | Sort-Object -Unique

    $tags = @()
    foreach ($m in [regex]::Matches($text, "#([A-Za-z0-9_-]+)")) {
      $tags += $m.Groups[1].Value
    }
    $tags = $tags | Sort-Object -Unique

    foreach ($tag in $tags) {
      if (-not $tagCount.ContainsKey($tag)) { $tagCount[$tag] = 0 }
      $tagCount[$tag] += 1
    }

    foreach ($v in $versions) {
      if (-not $versionMap.ContainsKey($v)) { $versionMap[$v] = New-Object System.Collections.Generic.List[string] }
      $versionMap[$v].Add($rel)
    }

    if (-not $topicMap.ContainsKey($topic)) { $topicMap[$topic] = New-Object System.Collections.Generic.List[string] }
    $topicMap[$topic].Add($rel)

    $statusCount = 0
    $lineNo = 0
    foreach ($line in ($text -split "`r?`n")) {
      $lineNo += 1
      if ($line -match "\b(DONE|TODO|FIXME|PENDING|PENDENTE|LEGACY|DEPRECATED|RISK|RISCO|ERROR|ERRO|FAIL)\b") {
        $statusCount += 1
        if ($statusRows.Count -lt 1500) {
          $safeLine = $line.Trim()
          if ($safeLine.Length -gt 220) { $safeLine = $safeLine.Substring(0, 220) }
          $statusRows.Add("- $(Convert-ToWikiLink $rel) L$lineNo`: $safeLine")
        }
      }
    }

    try {
      $hash = (Get-FileHash -Algorithm SHA256 -Path $file.FullName).Hash
      if (-not $hashMap.ContainsKey($hash)) { $hashMap[$hash] = New-Object System.Collections.Generic.List[string] }
      $hashMap[$hash].Add($rel)
    } catch {}

    $records += [pscustomobject]@{
      Path = $rel
      Title = $title
      Topic = $topic
      Lines = $lines
      StatusCount = $statusCount
      Versions = ($versions -join ", ")
      Tags = ($tags -join ", ")
    }
  }

  $inventory = New-Object System.Collections.Generic.List[string]
  $inventory.Add("---")
  $inventory.Add("type: generated-index")
  $inventory.Add("status: generated")
  $inventory.Add("tags:")
  $inventory.Add("  - docs")
  $inventory.Add("  - inventory")
  $inventory.Add("---")
  $inventory.Add("")
  $inventory.Add("# Documentation inventory")
  $inventory.Add("")
  $inventory.Add("Generated: $(Get-Date -Format s)")
  $inventory.Add("")
  $inventory.Add("| File | Topic | Lines | Status markers | Title |")
  $inventory.Add("|---|---:|---:|---:|---|")

  foreach ($r in $records) {
    $inventory.Add("| $(Convert-ToWikiLink $r.Path) | $($r.Topic) | $($r.Lines) | $($r.StatusCount) | $($r.Title.Replace('|','\|')) |")
  }

  Write-TextFile "docs\_meta\docs-inventory.md" ($inventory -join "`n") -Overwrite

  $topicDoc = New-Object System.Collections.Generic.List[string]
  $topicDoc.Add("---")
  $topicDoc.Add("type: generated-index")
  $topicDoc.Add("status: generated")
  $topicDoc.Add("tags:")
  $topicDoc.Add("  - docs")
  $topicDoc.Add("  - topics")
  $topicDoc.Add("---")
  $topicDoc.Add("")
  $topicDoc.Add("# Topic map")
  $topicDoc.Add("")

  foreach ($topic in ($topicMap.Keys | Sort-Object)) {
    $topicDoc.Add("## $topic")
    $topicDoc.Add("")
    foreach ($p in ($topicMap[$topic] | Sort-Object)) {
      $topicDoc.Add("- $(Convert-ToWikiLink $p)")
    }
    $topicDoc.Add("")
  }

  Write-TextFile "docs\_meta\topic-map.md" ($topicDoc -join "`n") -Overwrite

  $timeline = New-Object System.Collections.Generic.List[string]
  $timeline.Add("---")
  $timeline.Add("type: generated-index")
  $timeline.Add("status: generated")
  $timeline.Add("tags:")
  $timeline.Add("  - docs")
  $timeline.Add("  - history")
  $timeline.Add("---")
  $timeline.Add("")
  $timeline.Add("# Evolution timeline by version")
  $timeline.Add("")

  foreach ($v in ($versionMap.Keys | Sort-Object)) {
    $timeline.Add("## $v")
    $timeline.Add("")
    foreach ($p in ($versionMap[$v] | Sort-Object -Unique)) {
      $timeline.Add("- $(Convert-ToWikiLink $p)")
    }
    $timeline.Add("")
  }

  Write-TextFile "docs\history\evolution-timeline.md" ($timeline -join "`n") -Overwrite

  $statusDoc = New-Object System.Collections.Generic.List[string]
  $statusDoc.Add("---")
  $statusDoc.Add("type: generated-index")
  $statusDoc.Add("status: generated")
  $statusDoc.Add("tags:")
  $statusDoc.Add("  - docs")
  $statusDoc.Add("  - status")
  $statusDoc.Add("---")
  $statusDoc.Add("")
  $statusDoc.Add("# Status marker index")
  $statusDoc.Add("")
  foreach ($row in $statusRows) { $statusDoc.Add($row) }

  Write-TextFile "docs\_meta\status-marker-index.md" ($statusDoc -join "`n") -Overwrite

  $tagDoc = New-Object System.Collections.Generic.List[string]
  $tagDoc.Add("---")
  $tagDoc.Add("type: generated-index")
  $tagDoc.Add("status: generated")
  $tagDoc.Add("tags:")
  $tagDoc.Add("  - docs")
  $tagDoc.Add("  - tags")
  $tagDoc.Add("---")
  $tagDoc.Add("")
  $tagDoc.Add("# Tag index")
  $tagDoc.Add("")
  $tagDoc.Add("| Tag | Count |")
  $tagDoc.Add("|---|---:|")

  foreach ($tag in ($tagCount.Keys | Sort-Object)) {
    $tagDoc.Add("| #$tag | $($tagCount[$tag]) |")
  }

  Write-TextFile "docs\_meta\tag-index.md" ($tagDoc -join "`n") -Overwrite

  $dupDoc = New-Object System.Collections.Generic.List[string]
  $dupDoc.Add("---")
  $dupDoc.Add("type: generated-index")
  $dupDoc.Add("status: generated")
  $dupDoc.Add("tags:")
  $dupDoc.Add("  - docs")
  $dupDoc.Add("  - duplicates")
  $dupDoc.Add("---")
  $dupDoc.Add("")
  $dupDoc.Add("# Duplicate exact-content groups")
  $dupDoc.Add("")

  $dupCount = 0
  foreach ($hash in $hashMap.Keys) {
    $items = $hashMap[$hash]
    if ($items.Count -gt 1) {
      $dupCount += 1
      $dupDoc.Add("## Duplicate group $dupCount")
      $dupDoc.Add("")
      foreach ($p in $items) {
        $dupDoc.Add("- $(Convert-ToWikiLink $p)")
      }
      $dupDoc.Add("")
    }
  }

  if ($dupCount -eq 0) {
    $dupDoc.Add("No exact duplicates found.")
  }

  Write-TextFile "docs\_meta\duplicates.md" ($dupDoc -join "`n") -Overwrite

  $report = @"
---
type: generated-report
status: generated
tags:
  - docs
  - obsidian
---

# Obsidian setup report

Generated: $(Get-Date -Format s)

## Summary

- Files indexed: $($records.Count)
- Topics: $($topicMap.Keys.Count)
- Versions found: $($versionMap.Keys.Count)
- Duplicate groups: $dupCount

## Next files to review

- [[docs/_meta/docs-inventory]]
- [[docs/_meta/topic-map]]
- [[docs/history/evolution-timeline]]
- [[docs/_meta/status-marker-index]]
- [[docs/_meta/duplicates]]
"@

  Write-TextFile "docs\_meta\obsidian-setup-report.md" $report -Overwrite

  Ok "Indices gerados. Files indexed: $($records.Count)"
}

function Smoke-ObsidianDocs {
  Info "Rodando smoke da documentacao"

  $required = @(
    "docs\index.md",
    "docs\architecture\overview.md",
    "docs\architecture\extension-router.md",
    "docs\reference\envelope-contract.md",
    "docs\reference\router-contract.md",
    "docs\reference\adapter-contract.md",
    "docs\reference\transport-modes.md",
    "docs\operations\runbook.md",
    "docs\decisions\ADR-0001-docs-architecture.md",
    "docs\decisions\ADR-0002-extension-internal-router.md",
    "docs\decisions\ADR-0003-direct-interchat-no-gateway.md",
    "docs\decisions\ADR-0004-adapter-isolation.md",
    "docs\_meta\docs-inventory.md",
    "docs\_meta\topic-map.md",
    "docs\_meta\status-marker-index.md",
    "docs\_meta\tag-index.md",
    "docs\_meta\duplicates.md",
    "docs\history\evolution-timeline.md"
  )

  $missing = @()
  foreach ($p in $required) {
    if (-not (Test-Path $p)) { $missing += $p }
  }

  if ($missing.Count -gt 0) {
    throw "Smoke falhou. Arquivos ausentes: $($missing -join ', ')"
  }

  $index = Get-Content "docs\index.md" -Raw
  $requiredLinks = @(
    "docs/architecture/overview",
    "docs/reference/envelope-contract",
    "docs/reference/router-contract",
    "docs/reference/adapter-contract",
    "docs/operations/runbook",
    "docs/history/evolution-timeline",
    "docs/_meta/docs-inventory"
  )

  foreach ($link in $requiredLinks) {
    if ($index -notlike "*$link*") {
      throw "Smoke falhou. Link ausente no docs/index.md: $link"
    }
  }

  Ok "OK smoke_obsidian_docs"
}

if (-not (Test-Path $Root)) {
  throw "Root nao existe: $Root"
}

Set-Location $Root

Info "Iniciando setup completo Obsidian em: $Root"

Setup-ObsidianDocs
Build-ObsidianIndexes
Smoke-ObsidianDocs

Info "Git status:"
try {
  git status -sb
} catch {
  Warn "git status falhou ou git nao esta disponivel"
}

Write-Host ""
Ok "OBSIDIAN_ALL_DONE"
Write-Host "Abra no Obsidian como vault: $Root"
Write-Host "Comece por: docs\index.md"
Write-Host "Relatorio: docs\_meta\obsidian-setup-report.md"
