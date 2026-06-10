param(
    [switch]$Loop,
    [switch]$NoStart,
    [int]$Interval = 15
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location -LiteralPath $Root

$argsList = @("scripts/watcher/ai_bridge_local_supervisor.py")
if ($Loop) { $argsList += "--loop" } else { $argsList += "--once" }
if ($NoStart) { $argsList += "--no-start" }
$argsList += "--interval"
$argsList += [string]$Interval

python @argsList
