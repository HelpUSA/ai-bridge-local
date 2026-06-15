from pathlib import Path
doc = Path('docs/LATENCY_PARALLEL_POLLING_ARCHITECTURE.md').read_text(encoding='utf-8')
report = Path('reports/AI_BRIDGE_LOCAL_LATENCY_PARALLEL_POLLING_REPORT_2026-06-14.md').read_text(encoding='utf-8')
for term in ['pollOneChat', 'Promise.allSettled', 'pollInFlight', 'perChatInFlight', 'MAX_ACTIONS_PER_CHAT_CYCLE', 'pollMessagesSoon']:
 assert term in doc
for term in ['poll_started', 'action_received', 'inject_started', 'inject_done', 'ack_posted']:
 assert term in doc
assert '5000 ms para 1000 ms' in report
assert 'Um chat lento nao bloqueia os demais' in report
print('OK latency_parallel_polling_docs_smoke')
