# AI Bridge Local - Aplicativo Windows residente

Data-base: 2026-06-10

## Decisao de produto

A Central de Controle nao sera apenas uma tela HTML. Ela sera um aplicativo Windows instalado na maquina, com janela propria, icone residente na bandeja do sistema e comportamento de continuar ativo quando a janela for fechada.

## Caracteristicas esperadas

- Instalar no Windows como aplicacao local.
- Subir e supervisionar gateway_local.py e brain_worker.py.
- Mostrar status do gateway, fila, comandos recentes e eventos recentes.
- Usar os endpoints locais /control e /control/status como API de leitura.
- Ao fechar a janela, minimizar para a bandeja do sistema.
- Ter menu no icone da bandeja com abrir, reiniciar servicos e sair.
- Incluir empacotamento para gerar executavel e instalador.
- Manter compatibilidade com a extensao do navegador e com o banco queue_local.db.

## Dependencias previstas

A base Python atual possui tkinter e PIL. Para a versao residente completa serao adicionadas dependencias de empacotamento e bandeja: pystray, psutil e PyInstaller.

## Estrutura proposta

- app_windows/control_center_app.py: aplicacao desktop residente.
- app_windows/requirements-windows-app.txt: dependencias do app.
- packaging/build_windows_app.ps1: build do executavel.
- packaging/install_windows_app.ps1: instalacao local inicial.

## Fase 1

Criar scaffold executavel com tkinter, leitura de /control/status, botao de atualizar, botoes de restart do gateway e worker, e comportamento de minimizar para bandeja quando pystray estiver instalado.

## Fase 2

Gerar executavel com PyInstaller e preparar instalador Windows com atalho e inicializacao automatica opcional.

## Fase 3

Adicionar UI completa, logs, status por chat, diagnostico copiavel e configuracao visual.

## Atualizacao 2026-06-11 - requisitos v0.5.0

- Tabela de chats ativos com chat_id, source_chat_id, ultima atividade, fila pendente e comando em execucao.
- Heartbeat por chat enviado pela extensao ao gateway.
- Ultimos ACKs e erros por chat, console ao vivo, filtros, copiar diagnostico e atualizacao segura.
- Diagnostico claro para destino nao registrado, tabId antigo, composer nao encontrado, botao desabilitado, inject timeout e runtime error.
