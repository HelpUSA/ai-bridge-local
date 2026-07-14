# AI Bridge Local 0.5.85 ? dead direct dispatch removed

Data: 2026-07-13

## Resultado

A extens?o deixou de conter qualquer implementa??o ativa ou ?rf? de
entrega interchat direta.

Foram removidos:

- `extension/route_classifier.js`;
- classifica??o direta dentro da extens?o;
- descoberta de aba para entrega direta;
- `deliverInterChatDirect`;
- `aiBridgeDirectDeliverCapturedEnvelope`;
- pol?tica local de fallback direto ? gateway;
- constantes e overrides usados pela transi??o gateway-first;
- smokes dedicados ao contrato direto aposentado.

## Preservado

A extens?o continua executando browser actions retiradas da fila do
gateway. Por isso, `injectText`, reinje??o ap?s `receiving end does not
exist`, polling e ACK permanecem ativos.

## Contrato atual

1. O content script ou consumidor envia o envelope ao background.
2. `routeBridgeCommand` publica o envelope em `/bridge/commands`.
3. `gateway_local.py` decide a rota e persiste o comando.
4. A extens?o consulta a fila.
5. O executor aplica a browser action e envia ACK.

A extens?o n?o decide mais entre `direct_interchat` e `local_gateway`.
