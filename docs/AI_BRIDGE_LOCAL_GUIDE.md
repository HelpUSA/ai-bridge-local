AI Bridge Local guide 0.4.37
Repo D:/dev/autocode/ai-bridge-local
Use send-chat-message with inter_agent_message and top level message.
Use run-command with local_capability and gateway-brain-supervisor.
Use new command_id every try.
Do not mix explanation and real envelope.
Use placeholders for documentation.
Do not test HelpUSAI now.
Validate with node checks health_check self_heal dry-run smoke_robustness and git diff check.

## Diagnostics report

Use scripts/watcher/control_center_diagnostics.py to inspect queue counts, invalid_messages, dead_letters, and recent failed commands.
Run with: python scripts/watcher/control_center_diagnostics.py
The report uses ASCII-safe output so Windows console encoding does not break on stored error text.
