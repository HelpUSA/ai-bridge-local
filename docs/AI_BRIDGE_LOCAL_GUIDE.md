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

## Diagnostics viewer

Use app_windows/diagnostics_viewer.py for a small visual diagnostics window.
Recommended launcher: powershell -NoProfile -ExecutionPolicy Bypass -File app_windows/start_diagnostics_viewer.ps1

## Dead letters grouped report

Use: python scripts/watcher/dead_letters_report.py --limit 20 --prefix ai_bridge_local
The report separates watcher-local failures from external project noise such as HelpUS, Pizza, or Trading commands.

## Safe large commands

For large commands, prefer script_text/script_ext or a real saved script instead of fragile inline JSON.

## Command builder validation

command_builder.py supports --validate to check generated envelopes with envelope_validator.py.
Examples can be generated with command_builder.py and should be kept as text envelopes when needed.

## Queue database backup

Before any queue cleanup, run: python scripts/watcher/backup_queue_db.py
Use scripts/watcher/repo_health_report.py for a compact repository and queue health summary.

## Windows app runbook

Run Control Center from app_windows/control_center_app.py when operating the bridge locally.
Run diagnostics with: powershell -NoProfile -ExecutionPolicy Bypass -File app_windows/start_diagnostics_viewer.ps1
Confirm extension manifest version, run validate_all.ps1, and keep queue backups before cleanup.

## Final validation checklist

Run git status -sb, git diff --check, smoke_command_builder.py, smoke_robustness.py, validate_all.ps1, health_check.py, and self_heal.py --dry-run before release.

## Cleanup plan
Use python scripts/watcher/cleanup_plan.py to list cleanup candidates only. It must not delete rows. Run backup_queue_db.py before any real cleanup.

## Dead letter error classification
dead_letters_report.py groups errors by kind and by project prefix so AI Bridge failures are not mixed with Pizza, HelpUS, or Trading noise.

## Operational smokes
Use smoke_dead_letters_report.py and smoke_cleanup_plan.py to validate reporting scripts before queue maintenance.

## Cleanup age threshold
cleanup_plan.py supports --min-age-minutes and remains report-only. It marks stale candidates but does not modify the queue.
