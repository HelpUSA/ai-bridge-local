# M11 watcher delivery audit

Generated: `2026-07-18T19:19:19.136259+00:00`

Baseline: `fb117bf819c745a45a75187636dfb241c93fa579`

Version: `0.5.85`

## Discovered contracts

```json
{
  "command_id": true,
  "composer": true,
  "gateway_first": true,
  "retry": true,
  "submission": true
}
```

## Source inventory

```json
{
  "brain_worker.py": {
    "attempt_hits": 0,
    "command_id_hits": 39,
    "composer_hits": 0,
    "functions": [],
    "lines": 433,
    "retry_hits": 0,
    "sha256": "6653534b96f6c4c49590bdcd1869e0e2ad9db88f239edd82983b6caf629bc709",
    "submit_hits": 4
  },
  "extension/background.js": {
    "attempt_hits": 6,
    "command_id_hits": 52,
    "composer_hits": 0,
    "functions": [
      "aiBridgeCapturedCommandText",
      "aiBridgeCapturedPlainObject",
      "aiBridgeCapturedReadonlyAllowed",
      "aiBridgeCapturedString",
      "aiBridgeLooksLikeMissingReceiverResult",
      "aiBridgeReinjectContentScriptForDirectDelivery",
      "aiBridgeSleep",
      "canonicalChatId",
      "injectText",
      "injectTextOnce",
      "isUuid",
      "pollMessages",
      "pollMessagesSoon",
      "pollOneChat",
      "postAck",
      "postCommand",
      "postDeliveryStatus",
      "postJson",
      "postTelemetryEvent",
      "routeBridgeCommand",
      "safeIdPart",
      "validateAiBridgeCapturedEnvelopeMessage",
      "withTimeout"
    ],
    "lines": 597,
    "retry_hits": 0,
    "sha256": "06a89e07be1108527e761e444f53da5f0beb04b7cbb025f13996b6a0d693ec79",
    "submit_hits": 1
  },
  "extension/content_script.js": {
    "attempt_hits": 31,
    "command_id_hits": 76,
    "composer_hits": 116,
    "functions": [
      "aiBridgeDescribeComposerElement",
      "aiBridgeDispatchInputEvents",
      "aiBridgeFindChatGptPromptTextarea",
      "aiBridgeIsElementVisibleForComposer",
      "aiBridgeIsUsableComposerCandidate",
      "aiBridgeRobustSetText",
      "aiBridgeSafeCallSendChatHeartbeat",
      "aiBridgeSetContentEditableByExecCommand",
      "aiBridgeSetContentEditableByParagraphDom",
      "aiBridgeSetContentEditableByRange",
      "aiBridgeSetNativeValue",
      "aiBridgeStandaloneDescribeComposerElement",
      "aiBridgeStandaloneElementVisible",
      "aiBridgeStandaloneFindPreferredComposer",
      "aiBridgeStandaloneGetText",
      "aiBridgeStandaloneUsableComposer",
      "appendPersistentReceipt",
      "buildLocalStatusMessage",
      "candidateMarkdownElements",
      "candidateStartsWithLocalStatus",
      "candidateText",
      "canonicalUuid",
      "chooseSmallestEnvelopeElement",
      "classifyEnvelopeParseProblem",
      "clickElement",
      "closeBlockingModalIfPresent",
      "collectCandidateText",
      "collectSubmitDiagnostics",
      "countOccurrences",
      "directOkStatus",
      "documentContainsSentMessage",
      "errorStatus",
      "extract",
      "extractEnvelopeBlocks",
      "extractJsonStringField",
      "extractJsonUuidField",
      "findBlockingModal",
      "findComposer",
      "findDeepSeekEnvelopeAnchor",
      "findSendButton",
      "formatReceiptLines",
      "getCandidateElements",
      "getCandidateTexts",
      "getChatId",
      "getComposerText",
      "getCurrentChatId",
      "getDeepSeekChatId",
      "getGeminiChatId",
      "getHelpUsChatId",
      "hasEnvelopeMarkers",
      "hasRawLineBreakInLikelyJsonString",
      "hasSeen",
      "hashString",
      "hashTextForStatus",
      "injectVisibleStatus",
      "insertReceiptAfterAnchor",
      "install",
      "installAiBridgeChatGptCandidateEnvelopeScanner",
      "installAiBridgeChatGptOutboundEnvelopeCapture",
      "installAiBridgeChatGptStandaloneEnvelopeScannerFeedback",
      "installAiBridgeDeepSeekCapturedEnvelopeBridge",
      "installAiBridgeGeminiCapturedEnvelopeBridge",
      "installAiBridgeHelpUsCapturedEnvelopeBridge",
      "installCandidateScanner",
      "installGeminiEnvelopeObserver",
      "installObserver",
      "isAssistantMessageElement",
      "isBadReceiptAnchor",
      "isChatGptCandidatePage",
      "isChatGptPage",
      "isComposerOrInputNode",
      "isDeepSeekPage",
      "isDisabled",
      "isGeminiAppPage",
      "isLocalStatusText",
      "isUnsafeSubmitCandidate",
      "isVisible",
      "markCaptured",
      "markSeen",
      "nodeTextContainsEnvelope",
      "normalizeCommand",
      "normalizeLocalCommand",
      "parseBlock",
      "parseCapturedEnvelopeText",
      "parseEnvelopeBlock",
      "pressEnter",
      "processText",
      "pushCandidate",
      "registerChatWithBridge",
      "registerChatWithBridgeDebounced",
      "reportEnvelopeError",
      "root",
      "safeIdPart",
      "safePart",
      "sanitizeForStatus",
      "sanitizeReceiptId",
      "scan",
      "scanCandidateElements",
      "scanDocument",
      "scanMarkdownElement"
    ],
    "lines": 3353,
    "retry_hits": 0,
    "sha256": "b4c2166c1da493fb11f82a52c2c060f7bc2833a4d2e2dc231917d699c2d0bc44",
    "submit_hits": 24
  },
  "gateway_command_plane.py": {
    "attempt_hits": 24,
    "command_id_hits": 30,
    "composer_hits": 0,
    "functions": [],
    "lines": 291,
    "retry_hits": 10,
    "sha256": "0aef1205c0f8b39f953972aae009f3f4d45ff036386daa4f535b176530a29916",
    "submit_hits": 2
  },
  "gateway_local.py": {
    "attempt_hits": 5,
    "command_id_hits": 49,
    "composer_hits": 0,
    "functions": [],
    "lines": 864,
    "retry_hits": 1,
    "sha256": "7de5f64b7e01777bca21c0b84f715ebeaffcda92122a98f002381a1d1597fe7f",
    "submit_hits": 0
  },
  "queue_adapter.py": {
    "attempt_hits": 0,
    "command_id_hits": 19,
    "composer_hits": 0,
    "functions": [],
    "lines": 159,
    "retry_hits": 0,
    "sha256": "1163ee32d8112c8f194e635cec5f37fd939de5072dc6d4944459dff30f78e2a8",
    "submit_hits": 0
  }
}
```

## Next implementation outcomes

1. Empty-composer preflight.
2. Safe injection confirmation.
3. Observable submission confirmation.
4. Bounded idempotent retries.
5. Specific delivery errors.
6. Duplicate-delivery prevention.
7. Live interchat regression and exact cleanup.

<!-- AI_BRIDGE_MANAGED:M11_ACTIVE_DELIVERY_RELIABILITY_0585:START -->

## Active reliability implementation

The M11 audit was converted into active browser-delivery safeguards.

The content script now preserves unrelated composer content and short-circuits
when the requested delivery is already visible.

The background worker applies bounded retries only to transient failures while
retaining the same command ID.

Static, behavioral and runtime validations are required before commit. The
live browser probe remains gated on reloading the unpacked extension.

<!-- AI_BRIDGE_MANAGED:M11_ACTIVE_DELIVERY_RELIABILITY_0585:END -->

<!-- AI_BRIDGE_MANAGED:M11_TARGET_REGISTRATION_REPAIR_0586:START -->

## Final live acceptance ? release 0.5.86

The initial browser acceptance selected a historical destination because no
active target-tab registry existed. Release `0.5.86` closes that routing gap
by validating the requested chat UUID against the browser tab URL.

Release: `0.5.86`

Live acceptance time: `2026-07-18T23:10:20.069551+00:00`

Confirmed target: `6a563525-4740-83e9-a8a1-212c8e5baf1e`

Live command: `m11_fixed_target_primary_20260718_225107_0bb256ee`

Observed acceptance:

- gateway-first selected `local_gateway`;
- original, routed and persisted target IDs matched;
- delivery used `button_click_confirmed`;
- delivery completed in one wrapper attempt;
- automatic target discovery was disabled;
- historical command and dead-letter fallback were disabled;
- one visible delivery was executed;
- probe database records were removed;
- the live acceptance suite passed 32 tests;
- release validation adds one explicit version test, bringing the suite to 33 tests.

The visible acceptance token was:

`AI_BRIDGE_M11_FIXED_TARGET_OK_20260718_225107_0BB256EE`

The token reached the explicitly confirmed conversation.

<!-- AI_BRIDGE_MANAGED:M11_TARGET_REGISTRATION_REPAIR_0586:END -->
