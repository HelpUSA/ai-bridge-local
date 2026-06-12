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

## Safe validation wrapper

Use scripts/watcher/validate_all.ps1 before commit or push when changing watcher, gateway, worker, diagnostics, or extension files.
Run with: powershell -NoProfile -ExecutionPolicy Bypass -File scripts/watcher/validate_all.ps1
This wrapper stops on native command failures by checking LASTEXITCODE after each critical command.

## Command builder smoke

Use scripts/watcher/smoke_command_builder.py to validate run-command and send-chat-message envelope generation against envelope_validator.py.

## Diagnostics filters

Use: python scripts/watcher/control_center_diagnostics.py --limit 20 --target gateway-brain-supervisor --command-prefix ai_bridge_local
The report supports limit, target_chat_id, and command_id prefix filters for dead letters and failed commands.
