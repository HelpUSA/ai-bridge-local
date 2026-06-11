$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot
python -m pip install -r app_windows/requirements-windows-app.txt
python -m PyInstaller --noconsole --name AI-Bridge-Local-Control-Center app_windows/control_center_app.py
Write-Output "Build concluido. Executavel em dist/AI-Bridge-Local-Control-Center/"
