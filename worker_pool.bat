@echo off
setlocal
set WORKERS=%1
if "%WORKERS%"=="" set WORKERS=1

echo =============================================
echo AI BRIDGE LOCAL - Worker Pool
echo Workers: %WORKERS%
echo =============================================

for /L %%I in (1,1,%WORKERS%) do (
  start "AI Bridge Local Worker %%I" cmd /k "cd /d %~dp0 && python brain_worker.py"
)

echo Worker pool started.
echo Close worker windows or press Ctrl+C inside each worker to stop.
