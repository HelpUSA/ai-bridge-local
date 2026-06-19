param(
  [string]$Root = "D:\dev\autocode\ai-bridge-local"
)

$ErrorActionPreference = "Stop"

Set-Location $Root

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$out = "reports\obsidian_context_$stamp.md"
New-Item -ItemType Directory -Force .\reports | Out-Null

$files = @(
  "docs\index.md",
  "docs\_meta\obsidian-setup-report.md",
  "docs\_meta\docs-inventory.md",
  "docs\_meta\topic-map.md",
  "docs\_meta\duplicates.md",
  "docs\_meta\status-marker-index.md",
  "docs\_meta\tag-index.md",
  "docs\history\evolution-timeline.md",
  "docs\history\legacy-map.md",
  "docs\architecture\overview.md",
  "docs\architecture\extension-router.md",
  "docs\architecture\direct-interchat.md",
  "docs\architecture\local-gateway-client.md",
  "docs\architecture\adapter-isolation.md",
  "docs\reference\envelope-contract.md",
  "docs\reference\router-contract.md",
  "docs\reference\adapter-contract.md",
  "docs\reference\transport-modes.md",
  "docs\reference\error-taxonomy.md",
  "docs\reference\smoke-test-matrix.md",
  "docs\operations\runbook.md",
  "docs\operations\diagnostics.md",
  "docs\operations\release-process.md",
  "docs\operations\rollback.md",
  "docs\decisions\ADR-0001-docs-architecture.md",
  "docs\decisions\ADR-0002-extension-internal-router.md",
  "docs\decisions\ADR-0003-direct-interchat-no-gateway.md",
  "docs\decisions\ADR-0004-adapter-isolation.md",
  "docs\how-to\send-message-between-chats.md",
  "docs\how-to\run-local-command.md",
  "docs\how-to\add-new-ai-adapter.md",
  "docs\how-to\recover-from-envelope-error.md"
)

$buf = New-Object System.Collections.Generic.List[string]

$buf.Add("# Obsidian context export")
$buf.Add("")
$buf.Add("Generated: $(Get-Date -Format s)")
$buf.Add("Root: $Root")
$buf.Add("")
$buf.Add("## Git status")
$buf.Add("")
$buf.Add("~~~text")

try {
  $status = git status -sb
  foreach ($line in $status) {
    $buf.Add($line)
  }
} catch {
  $buf.Add("git status failed")
}

$buf.Add("~~~")
$buf.Add("")

foreach ($file in $files) {
  if (-not (Test-Path $file)) {
    continue
  }

  $buf.Add("")
  $buf.Add("---")
  $buf.Add("")
  $buf.Add("# FILE: $file")
  $buf.Add("")
  $buf.Add("~~~markdown")

  $text = Get-Content $file -Raw -Encoding UTF8
  $buf.Add($text)

  $buf.Add("~~~")
}

Set-Content -Path $out -Value ($buf -join [Environment]::NewLine) -Encoding UTF8

Write-Host "OBSIDIAN_CONTEXT_EXPORTED"
Write-Host $out

Write-Host ""
Write-Host "Git status:"
git status -sb
