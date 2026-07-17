@echo off
setlocal EnableExtensions

set "LAUNCHER=%~dp0controlcenter_launcher.ps1"

if /I "%~1"=="--validate" (
    powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "%LAUNCHER%" -ValidateOnly
    exit /b %ERRORLEVEL%
)

powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "%LAUNCHER%"
set "RC=%ERRORLEVEL%"

if not "%RC%"=="0" (
    echo.
    echo Falha ao abrir a Central de Controle.
    echo Consulte logs\controlcenter_launcher.log
    pause
)

exit /b %RC%
