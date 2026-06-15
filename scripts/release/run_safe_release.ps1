param(
    [Parameter(Mandatory = $true)]
    [string]$Version,

    [Parameter(Mandatory = $true)]
    [string]$Tag,

    [Parameter(Mandatory = $true)]
    [string]$CommitMessage,

    [string[]]$ValidationCommands = @(),

    [string[]]$AddPaths = @(),

    [switch]$Push,

    [switch]$NoTag
)

$ErrorActionPreference = "Stop"

function Invoke-Native {
    param(
        [string]$Label,
        [scriptblock]$Block
    )

    Write-Output ""
    Write-Output "--- $Label ---"

    $global:LASTEXITCODE = 0
    & $Block

    $code = $LASTEXITCODE
    if ($null -ne $code -and $code -ne 0) {
        throw "Native command failed: $Label code=$code"
    }
}

function Write-Utf8NoBomFile {
    param(
        [string]$Path,
        [string]$Text
    )

    $enc = New-Object System.Text.UTF8Encoding($false)
    $full = Join-Path (Get-Location) $Path
    [System.IO.File]::WriteAllText($full, $Text, $enc)
}

function Assert-NoBomVersion {
    $bytes = [System.IO.File]::ReadAllBytes((Resolve-Path -LiteralPath "VERSION"))
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 239 -and $bytes[1] -eq 187 -and $bytes[2] -eq 191) {
        throw "VERSION has UTF-8 BOM. Use UTF-8 without BOM."
    }
}

function Invoke-ValidationCommands {
    param([string[]]$Commands)

    foreach ($cmd in $Commands) {
        Invoke-Native "VALIDATE: $cmd" {
            powershell -NoProfile -ExecutionPolicy Bypass -Command $cmd
        }
    }
}

Write-Output "=== SAFE RELEASE RUNNER START ==="
Write-Output "Version: $Version"
Write-Output "Tag: $Tag"
Write-Output "CommitMessage: $CommitMessage"

Invoke-Native "STATUS BEFORE" {
    git status -sb
}

Assert-NoBomVersion

if ($ValidationCommands.Count -gt 0) {
    Invoke-ValidationCommands -Commands $ValidationCommands
}

Invoke-Native "DIFF CHECK" {
    git diff --check
}

Invoke-Native "STATUS PRE COMMIT" {
    git status -sb
}

if ($AddPaths.Count -eq 0) {
    throw "AddPaths is empty. Refusing to commit without explicit files."
}

Invoke-Native "GIT ADD" {
    git add @AddPaths
}

Invoke-Native "GIT COMMIT" {
    git commit -m $CommitMessage
}

if (-not $NoTag) {
    Invoke-Native "GIT TAG" {
        git tag $Tag
    }
}

if ($ValidationCommands.Count -gt 0) {
    Invoke-ValidationCommands -Commands $ValidationCommands
}

Invoke-Native "FINAL DIFF CHECK" {
    git diff --check
}

if ($Push) {
    Invoke-Native "PUSH MAIN" {
        git push origin main
    }

    if (-not $NoTag) {
        Invoke-Native "PUSH TAG" {
            git push origin $Tag
        }
    }
}

Invoke-Native "STATUS AFTER" {
    git status -sb
}

Write-Output "=== SAFE RELEASE RUNNER END ==="