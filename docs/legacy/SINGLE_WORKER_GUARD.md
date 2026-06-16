
# AI Bridge Local - Single worker guard 0.5.8

## Objective
Prevent multiple `brain_worker.py` processes from running concurrently.

## Behavior
When the worker starts, it creates `temp/brain_worker.pid`.

If another live worker PID is already recorded, the new worker exits safely with:

`another brain_worker.py is already running`

If the PID file is stale, it is removed and replaced.

## Why
Multiple workers can duplicate queue processing, duplicate feedback, and make watcher diagnostics unreliable.
