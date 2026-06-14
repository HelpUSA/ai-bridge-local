import json
payload = {'schema': 'ai_bridge_local.chat_bridge_plan', 'schema_version': 1, 'executes_commands': False, 'storage': {'inbox': 'local persistent inbox', 'outbox': 'local persistent outbox', 'status': ['queued', 'acked', 'failed', 'delivering']}, 'flow': ['write message envelope', 'store in outbox', 'delivery worker moves to inbox', 'receiver emits ack', 'auditor reconciles status'], 'extension_dependency': 'optional after local API exists'}
print(json.dumps(payload, ensure_ascii=False, indent=2))
