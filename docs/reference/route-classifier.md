---
type: reference
status: current
tags:
  - extension
  - router
  - interchat
  - gateway
---

# Route classifier

This document defines the first isolated route classifier for the browser extension.

## Purpose

The classifier decides whether an envelope should use:

- direct_interchat
- local_gateway

## Current Micro 1 status

The classifier is introduced as an isolated, side-effect free file:

- extension/route_classifier.js

Micro 1 does not yet wire it into runtime behavior.

## Rules

| Signal | Route |
|---|---|
| force_gateway=true | local_gateway |
| transport=local_gateway | local_gateway |
| transport=direct_interchat | direct_interchat |
| action=send-chat-message | direct_interchat |
| action=run-command | local_gateway |
| action=smoke | local_gateway |
| action=patch | local_gateway |
| action=inspect | local_gateway |
| unknown action | local_gateway |

## Safety default

Unknown actions default to local_gateway, because command-like operations must never be silently treated as normal chat messages.

## Smoke

Run:

    node .\scripts\smoke\smoke_route_classifier.js

Expected:

    OK smoke_route_classifier

## Related

- [[docs/reference/router-contract]]
- [[docs/reference/transport-modes]]
- [[docs/architecture/extension-router]]
- [[docs/architecture/direct-interchat]]
- [[docs/architecture/local-gateway-client]]

## Current Micro 2 status

The classifier is now loaded by `extension/background.js` using `importScripts("route_classifier.js")`.

Micro 2 still does not change live delivery behavior. It only makes a safe background helper available:

    globalThis.aiBridgeClassifyRouteSafe(envelope)

The next micro can use this helper to route `send-chat-message` directly and keep command-like operations on the local gateway.
## Current Micro 3 status

The captured envelope handler now uses:

    globalThis.aiBridgeClassifyRouteSafe(validation.envelope)

Routing behavior:

| Captured envelope | Route |
|---|---|
| send-chat-message + inter_agent_message | direct_interchat |
| run-command + local_capability | local_gateway |
| force_gateway=true | local_gateway |

Direct interchat delivery uses the registered target tab from the background registry and injects the message with the existing content-script injection path.

Gateway fallback is preserved for command-like and forced-gateway envelopes.