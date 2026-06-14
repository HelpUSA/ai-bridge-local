# Command Intake Roadmap

## Objective

Move command organization out of chat-authored envelopes and into the local gateway control layer. The chat should send short intentions. The gateway should validate, classify, materialize and execute approved work through the worker.

## Desired flow

chat intention -> gateway command intake -> preflight -> job queue -> worker -> structured result

## Core rule

The chat must not assemble complex commands. The gateway must assemble commands from a small catalog of approved intentions and templates.

## Proposed component

Create scripts/watcher/command_intake.py.

Responsibilities:

- receive a short intention
- validate required parameters
- classify command risk
- reject unsafe or oversized inline commands
- materialize large work into real script files
- return a clear execution plan
- produce structured results for the gateway

## Initial intention catalog

Read-only and validation-safe operations:

- inspect_repo
- inspect_docs
- run_smokes
- run_release_check
- diagnose_failure
- backup_queue
- cleanup_plan

Later write operations:

- apply_patch_file
- bump_version
- commit_and_tag
- push_release

## Risk classes

- read_only: execute directly
- validation: execute with timeout
- write_file: require clean repo and planned file list
- git_write: require smokes and release_check
- destructive: require dry-run and explicit acknowledgement
- network_push: require successful release_check

## Preflight checks

- command_id is unique
- source_chat_id is present
- target_chat_id is allowed
- delivery_kind matches action
- cwd exists
- timeout_seconds is within policy
- payload.command is a list
- inline command size is below limit
- raw envelope markers are not present inside payload or message text
- destructive commands are blocked without dry-run and acknowledgement
- large patches are moved to script files before execution

## Implementation phases

### v0.4.41-command-intake

- add command_intake.py
- implement inspect_repo, inspect_docs and run_smokes
- add smoke_command_intake.py
- document intention catalog
- integrate smoke into release_check.ps1

### v0.4.42-command-risk-policy

- add risk classes
- add inline command size limit
- add destructive command detection
- add duplicate command_id policy
- add negative smokes

### v0.4.43-builder-output-file

- add command_builder.py --validate
- add command_builder.py --output-file
- write generated envelopes to files instead of watcher chats by default

## Operating rule

Use the watcher for short commands only. For complex patches, create a real script file and execute that file. Command intake should become the preferred gateway path for repeated operations.
