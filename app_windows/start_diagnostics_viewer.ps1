$ErrorActionPreference='Stop'
$root=Resolve-Path (Join-Path $PSScriptRoot '..')
Set-Location $root
python app_windows/diagnostics_viewer.py
if($LASTEXITCODE -ne 0){throw 'diagnostics_viewer_failed'}
