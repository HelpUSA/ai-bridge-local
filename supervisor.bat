@echo off
title AI Bridge Local - Gateway
cd /d D:\dev\autocode\ai-bridge-local
echo =============================================
echo AI BRIDGE LOCAL - Gateway HTTP
echo Porta: http://127.0.0.1:8766
echo Pressione Ctrl+C para parar
echo =============================================
python gateway_local.py
pause
