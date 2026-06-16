# AI Bridge Local - Watcher Notes

## Safe command pattern

Use small watcher commands. For larger changes, create a real file under temp, such as `temp/update_docs_0511.py` or `temp/update_docs_0511.ps1`, then run a short watcher command to execute it.

## Delivery results

A final failure should not stop the chat. Read stdout, stderr, success, result_is_final, chat_can_continue, and next_action before deciding the next step.

## Composer submit guard

Version 0.5.11 improves delivery safety by checking submit behavior and avoiding wrong buttons or blocking modals. If submit is not confirmed and the composer still contains text, do not assume delivery succeeded.

## Docs task rule

Envelope delimiters are transport-only. Do not add local envelope delimiters as documentation content in guide files.
