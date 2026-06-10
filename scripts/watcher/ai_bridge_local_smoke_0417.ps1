$ErrorActionPreference = 'Stop'
Write-Output 'AI_BRIDGE_LOCAL_SMOKE_0417_START'
Write-Output 'STATUS'
git status -sb
Write-Output 'LOG_TOP'
git log --oneline -5
Write-Output 'TAGS_TOP'
git tag --list 'v0.4.*' --sort=-creatordate
Write-Output 'VERSION_LINES'
Select-String -Path './extension/manifest.json','./extension/background.js','./extension/content_script.js','./brain_worker.py' -Pattern '0.4.17','0.1.3'
Write-Output 'VALIDATE_DIFF_CHECK'
git diff --check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'VALIDATE_NODE_BACKGROUND'
node --check ./extension/background.js
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'VALIDATE_NODE_CONTENT'
node --check ./extension/content_script.js
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'VALIDATE_PY_COMPILE'
python -m py_compile ./gateway_local.py ./brain_worker.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'PROCESSES'
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'brain_worker.py|gateway_local.py' } | Select-Object ProcessId,CommandLine
Write-Output 'AI_BRIDGE_LOCAL_SMOKE_0417_END'
