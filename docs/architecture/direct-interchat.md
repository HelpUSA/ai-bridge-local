---
type: explanation
status: draft
tags:
  - architecture
  - interchat
---

# Direct interchat

## Definicao

Direct interchat e o caminho para conversa entre chats abertos no navegador.

## Regra

Nao usa gateway local, fila local, banco local nem API web.

## Fluxo

Chat origem envia envelope. A extensao roteia para a aba destino. O adapter da IA destino injeta e envia a mensagem.
