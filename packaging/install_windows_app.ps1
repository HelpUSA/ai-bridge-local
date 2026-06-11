$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot
$InstallDir = Join-Path $env:LOCALAPPDATA "AI-Bridge-Local-Control-Center"
if (!(Test-Path $InstallDir)) { New-Item -ItemType Directory -Path $InstallDir | Out-Null }
Copy-Item -Recurse -Force dist/AI-Bridge-Local-Control-Center/* $InstallDir
$Shell = New-Object -ComObject WScript.Shell
$Shortcut = $Shell.CreateShortcut((Join-Path ([Environment]::GetFolderPath("Startup")) "AI Bridge Local Control Center.lnk"))
$Shortcut.TargetPath = Join-Path $InstallDir "AI-Bridge-Local-Control-Center.exe"
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.Save()
Write-Output "Instalado e configurado para iniciar com o Windows."
