---
type: decision
status: accepted
date: 2026-07-06
tags:
 - architecture
 - control-plane
 - thin-extension
---

# ADR: AI Bridge Local control plane boundary

## Decision

AI Bridge Local is the durable control plane.

The browser extension is a thin browser adapter. It observes chats and tabs, forwards browser events to localhost, receives browser actions, injects short messages, and reports action results. It is not the source of truth and must not own workflow decisions.

Workers are supervised executors. The Control Center is an operational UI over AI Bridge Local state. Chats are producers of intent and consumers of summaries, not terminal operators.

## Final boundary

| Component | Owns | Must not own |
| --- | --- | --- |
| Browser extension | DOM observation, chat snapshots, browser event forwarding, message injection, action result reporting | retry policy, command workflow, official queue state, log summarization, envelope repair, silence policy |
| AI Bridge Local | durable chat state, commands, runs, queue, leases, retries, dead letters, recipes, summarizer, security gate, decision policy | DOM selectors, browser click mechanics |
| Worker | command execution under lease, heartbeat, stdout/stderr capture | orchestration, retry policy, chat response policy |
| Control Center | display and manual operations over durable state | independent business rules |
| Chats | intent and reasoning | local control plane decisions |

## Consequences

New orchestration features must be implemented in AI Bridge Local first. Legacy envelopes remain supported during migration. Automatic retry or resume must be backed by durable state, cooldown and dedupe.
