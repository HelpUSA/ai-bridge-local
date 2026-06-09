@echo off
title AI Bridge Local - Worker
cd /d D:\dev\autocode\ai-bridge-local
echo =============================================
echo AI BRIDGE LOCAL - Worker
echo Porta: http://127.0.0.1:8766
echo Pressione Ctrl+C para parar
echo =============================================
python brain_worker.py
pause
