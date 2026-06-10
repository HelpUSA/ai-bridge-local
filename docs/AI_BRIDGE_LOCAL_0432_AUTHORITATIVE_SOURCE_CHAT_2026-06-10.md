# AI Bridge Local 0.4.32 - authoritative source_chat_id

A extensao passa a sobrescrever source_chat_id com o chat_id real da aba atual antes de enviar o envelope ao gateway.

Se o envelope declarou outro source_chat_id, o valor antigo e preservado em declared_source_chat_id para auditoria.

Isto evita que resultados voltem para chat antigo quando um envelope e copiado de outra aba ou de uma URL anterior.
