# AI Bridge Local 0.4.33 - worker pool safe step

Adds worker_pool.bat as a safe reversible first step toward virtual watchers and queue isolation.

This does not modify brain_worker.py or worker.bat.

It starts multiple existing workers in separate windows, so one blocking command is less likely to stop all queues.

Usage:

worker_pool.bat 4

Limitations:

This is not full per-chat queue isolation yet. A later patch should add source_chat_id-aware dispatching and busy-source exclusion.
