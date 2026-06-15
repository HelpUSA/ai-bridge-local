from pathlib import Path

bg = Path('extension/background.js').read_text(encoding='utf-8')
cs = Path('extension/content_script.js').read_text(encoding='utf-8')

required_bg = [
    'const POLL_INTERVAL_MS = 1000',
    'const POLL_SOON_DEBOUNCE_MS = 150',
    'const MAX_ACTIONS_PER_CHAT_CYCLE = 3',
    'let pollInFlight = false',
    'const perChatInFlight = new Set()',
    'function pollMessagesSoon',
    'async function pollOneChat(chatId)',
    'Promise.allSettled(chatIds.map((chatId) => pollOneChat(chatId)))',
    "pollMessagesSoon('postCommand')",
    "pollMessagesSoon('registerChat')",
    "postTelemetryEvent('poll_started'",
    "postTelemetryEvent('action_received'",
    "postTelemetryEvent('inject_started'",
    "postTelemetryEvent('inject_done'",
    "postTelemetryEvent('ack_posted'",
    "setInterval(() => pollMessages('interval'), POLL_INTERVAL_MS)",
]

for term in required_bg:
    assert term in bg, term

assert 'for (const chatId of Object.keys(registry))' not in bg
assert 'setInterval(pollMessages, 5000)' not in bg
assert 'const REGISTER_CHAT_INTERVAL_MS = 1500' in cs
assert 'setInterval(registerChatWithBridge, 5000)' not in cs

print('OK latency_parallel_polling_smoke')
