# AI Bridge Local 0.5.85 thin-extension gateway-first audit

Date: 2026-07-09

## Purpose

This audit maps where the Chrome extension still appears to own routing, direct interchat, queue, or browser action responsibilities that should be evaluated during the gateway-first migration.

## Summary

- chrome_mutation: 1
- direct_interchat: 161
- gateway_fetch: 2
- id_fields: 189
- intent_sender: 14
- local_gateway: 1
- queue_words: 46
- route_decision: 8

## Details

### extension/background.js

- Status: exists
- Lines: 975
- Audit hits: 202

```text
10: queue_words: console.warn("[AI Bridge Local] route classifier load failed", error);
13: route_decision: globalThis.aiBridgeClassifyRouteSafe = function aiBridgeClassifyRouteSafe(envelope) {
16: route_decision: typeof globalThis.AIBridgeRouteClassifier.classifyRoute === "function"
18: route_decision: return globalThis.AIBridgeRouteClassifier.classifyRoute(envelope);
31: direct_interchat: if (transport === "direct_interchat" || transport === "direct-interchat" || transport === "direct") {
32: direct_interchat: return "direct_interchat";
40: direct_interchat: return "direct_interchat";
48: local_gateway: const GATEWAY = "http://127.0.0.1:8766";
50: direct_interchat: const DIRECT_INTERCHAT_ENABLED = true;
51: direct_interchat: const DIRECT_INTERCHAT_ALLOW_GATEWAY_FALLBACK = true;
55: gateway_fetch: const res = await fetch(GATEWAY + path, {
79: id_fields: command_id: details.command_id || details.commandId || null,
84: queue_words: console.warn('[AI_LOCAL] telemetry failed', eventType, e.message);
89: intent_sender: async function postCommand(cmd) {
90: id_fields: console.log("[bg] Sending:", cmd.command_id);
92: intent_sender: return await postJson("/bridge/commands", cmd);
96: queue_words: console.log("[bg] Command already queued:", cmd && cmd.command_id);
96: id_fields: console.log("[bg] Command already queued:", cmd && cmd.command_id);
99: queue_words: already_queued: true,
101: id_fields: command_id: cmd && cmd.command_id ? cmd.command_id : null,
111: id_fields: command_id: commandId,
129: id_fields: if (!action || !action.command_id) return;
130: queue_words: if (status === 'delivering') postTelemetryEvent('delivery_attempt', { command_id: action.command_id, target_chat_id: action.target_chat_id, action: action.action });
130: id_fields: if (status === 'delivering') postTelemetryEvent('delivery_attempt', { command_id: action.command_id, target_chat_id: action.target_chat_id, action: action.action });
131: id_fields: if (status === 'sent') postTelemetryEvent('delivery_ok', { command_id: action.command_id, target_chat_id: action.target_chat_id, action: action.action });
132: queue_words: if (status === 'failed') postTelemetryEvent('delivery_failed', { command_id: action.command_id, target_chat_id: action.target_chat_id, action: action.action, message: String(detail
132: id_fields: if (status === 'failed') postTelemetryEvent('delivery_failed', { command_id: action.command_id, target_chat_id: action.target_chat_id, action: action.action, message: String(detail
133: id_fields: if (String(action.command_id).startsWith("local_status_")) return;
135: id_fields: const statusKey = String(status || "unknown") + ":" + String(action.command_id || "unknown");
142: id_fields: const sourceChatId = canonicalChatId(action.source_chat_id || "");
143: id_fields: const targetChatId = canonicalChatId(action.target_chat_id || "");
146: id_fields: console.log("[bg] Skip compact delivery status: invalid source_chat_id", action.source_chat_id);
158: id_fields: "[AI_LOCAL] enviado id=" + action.command_id +
171: id_fields: "id_original=" + action.command_id + "\n" +
175: id_fields: "correcao=Se a mensagem nao chegou ao destino, reenvie o envelope local com novo command_id ou verifique se a aba destino esta aberta, com extensao recarregada e chat_id correto.";
178: intent_sender: await postCommand({
182: id_fields: command_id: "local_status_delivery_" + safeIdPart(status) + "_" + safeIdPart(action.command_id),
184: id_fields: source_chat_id: targetChatId || "gateway-brain-supervisor",
185: id_fields: target_chat_id: sourceChatId,
192: queue_words: console.log("[bg] Compact delivery status queued:", action.command_id, status);
192: id_fields: console.log("[bg] Compact delivery status queued:", action.command_id, status);
250: direct_interchat: function isDirectInterChatCommand(cmd) {
252: direct_interchat: DIRECT_INTERCHAT_ENABLED &&
256: id_fields: cmd.target_chat_id &&
301: id_fields: if (!canonicalTargetChatId) return { ok: false, error: "missing_target_chat_id" };
303: id_fields: return { ok: false, error: "tabs_query_unavailable", target_chat_id: canonicalTargetChatId };
309: queue_words: return { ok: false, error: "tabs_query_failed", target_chat_id: canonicalTargetChatId, detail: error && error.message ? error.message : String(error || "unknown") };
309: id_fields: return { ok: false, error: "tabs_query_failed", target_chat_id: canonicalTargetChatId, detail: error && error.message ? error.message : String(error || "unknown") };
316: id_fields: return { ok: false, error: "target_tab_not_open", target_chat_id: canonicalTargetChatId, target_url: targetUrl || "", tab_count: (tabs || []).length, tabs_sample: tabDiagnostics };
323: queue_words: console.warn("[bg] direct target discovery reinject failed:", error);
325: id_fields: return { ok: true, discovered: true, tab_id: tabId, target_chat_id: canonicalTargetChatId, url: match.url || "" };
330: id_fields: const targetChatId = canonicalChatId(cmd.target_chat_id || "");
331: id_fields: const sourceChatId = canonicalChatId(cmd.source_chat_id || "");
334: id_fields: return { ok: false, direct: true, error: "missing_target_chat_id" };
338: id_fields: const discoveredTarget = await aiBridgeDiscoverDirectTargetTab(targetChatId, cmd.target_url || cmd.url || "", cmd.command_id || "unknown");
346: id_fields: target_chat_id: targetChatId,
352: id_fields: command_id: cmd.command_id,
355: id_fields: target_chat_id: targetChatId,
356: id_fields: source_chat_id: sourceChatId || cmd.source_chat_id || ""
359: id_fields: console.log("[bg] Direct inter-chat delivery:", directAction.command_id, "to", targetChatId, "tab", tabId);
364: direct_interchat: { ok: false, reason: "direct_interchat_inject_timeout" }
368: id_fields: console.log("[bg] Direct inter-chat delivered:", directAction.command_id, JSON.stringify(result));
369: id_fields: return { ok: true, direct: true, command_id: directAction.command_id, target_chat_id: targetChatId, result };
372: direct_interchat: const reason = result && (result.reason || result.error) ? (result.reason || result.error) : "direct_interchat_inject_failed";
372: queue_words: const reason = result && (result.reason || result.error) ? (result.reason || result.error) : "direct_interchat_inject_failed";
373: queue_words: console.log("[bg] Direct inter-chat failed:", directAction.command_id, reason);
373: id_fields: console.log("[bg] Direct inter-chat failed:", directAction.command_id, reason);
374: id_fields: return { ok: false, direct: true, command_id: directAction.command_id, target_chat_id: targetChatId, error: reason, result };
379: direct_interchat: if (!DIRECT_INTERCHAT_ALLOW_GATEWAY_FALLBACK) return false;
400: direct_interchat: return /target_chat_not_registered|direct_delivery_target_not_registered|target_tab_not_open|target_tab_not_found|tabs_query_unavailable|tabs_query_failed|direct_delivery_target_no
400: queue_words: return /target_chat_not_registered|direct_delivery_target_not_registered|target_tab_not_open|target_tab_not_found|tabs_query_unavailable|tabs_query_failed|direct_delivery_target_no
405: direct_interchat: if (isDirectInterChatCommand(cmd)) {
412: id_fields: console.log("[bg] Direct inter-chat fallback to gateway:", cmd.command_id, directResult && directResult.error);
413: intent_sender: const gatewayResult = await postCommand(cmd);
418: direct_interchat: return { ok: false, direct: true, error: (directResult && directResult.error) || "direct_interchat_failed", data: directResult };
418: queue_words: return { ok: false, direct: true, error: (directResult && directResult.error) || "direct_interchat_failed", data: directResult };
422: intent_sender: const gatewayResult = await postCommand(cmd);
423: intent_sender: pollMessagesSoon(sourceLabel || "postCommand");
446: id_fields: return { ok: false, error: "invalid_tab_id_for_reinject", tab_id: tabId, command_id: commandId || "unknown" };
450: chrome_mutation: await chrome.scripting.executeScript({
... 122 more hits truncated ...
```

### extension/content_script.js

- Status: exists
- Lines: 2708
- Audit hits: 212

```text
123: queue_words: console.warn("[Local v" + VERSION + "] clickElement failed:", e.message);
403: queue_words: console.warn("[Local v" + VERSION + "] aiBridgeSetContentEditableByRange failed", e && e.message);
426: queue_words: console.warn("[Local v" + VERSION + "] aiBridgeSetContentEditableByParagraphDom failed", e && e.message);
440: queue_words: console.warn("[Local v" + VERSION + "] aiBridgeSetContentEditableByExecCommand failed", e && e.message);
484: queue_words: console.warn("[Local v" + VERSION + "] aiBridgeRobustSetText failed", {
605: id_fields: const actionId = message.action?.action_id || message.action?.command_id || "unknown";
608: id_fields: showNotice("Mensagem recebida para injeÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚
611: id_fields: showNotice("Falha: texto vazio", "command_id=" + actionId, "error");
619: id_fields: showNotice("Falha: composer nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚
630: id_fields: showNotice("Limpando composer travado da extensao", "command_id=" + actionId, "warn");
633: id_fields: showNotice("Falha: composer nao vazio antes da injecao", "command_id=" + actionId, "error");
702: id_fields: showNotice("Mensagem enviada ao chat", "command_id=" + actionId + "\nmethod=" + lastMethod, "success");
719: id_fields: showNotice("Tentativa por Enter", "command_id=" + actionId + "\nattempt=" + attempts, "warn");
734: id_fields: showNotice("Falha ao confirmar envio", "command_id=" + actionId + "\nreason=" + reason, "error");
735: queue_words: console.warn("[Local v" + VERSION + "] Submit failed", {hasButton: !!findSendButton(composer), finalTextLength: finalText.length, clickedAtLeastOnce});
844: route_decision: function classifyEnvelopeParseProblem(raw, errorMessage) {
873: id_fields: "Nada foi executado. Reenvie um envelope novo com command_id novo, JSON estrito, aspas duplas ASCII, sem caracteres invisiveis e sem texto quebrado. Para mensagens inter-chat, mant
875: queue_words: "Modelo seguro: marcadores locais de inicio/fim sozinhos nas linhas; dentro deles envie um unico JSON valido. Eventos com no_reply=1, como queued ou sent_direct, sao silenciosos e 
881: id_fields: const originalCommandId = extractJsonStringField(raw, "command_id") || "unknown";
882: id_fields: const originalSource = extractJsonUuidField(raw, "source_chat_id");
883: id_fields: const originalTarget = extractJsonUuidField(raw, "target_chat_id");
886: route_decision: const diagnosis = classifyEnvelopeParseProblem(raw, errorMessage);
925: id_fields: const originalCommandId = extractJsonStringField(raw, "command_id") || "unknown";
956: queue_words: console.warn('[AI_LOCAL] telemetry send failed', eventType, e.message);
971: queue_words: console.warn("[AI Bridge Local] sendChatHeartbeat failed; skipped heartbeat direct_call", e && e.message);
978: queue_words: console.warn("[AI Bridge Local] sendChatHeartbeat failed; skipped heartbeat", reason || "", e && e.message);
1012: id_fields: command_id: "local_status_" + safeIdPart(kind) + "_" + safeIdPart(info.originalCommandId) + "_to_" + safeIdPart(validTarget).slice(0, 8) + "_" + Date.now(),
1014: id_fields: source_chat_id: info.currentChatId || info.originalSource || "unknown",
1015: id_fields: target_chat_id: validTarget,
1026: queue_words: console.warn("[Local v" + VERSION + "] reportEnvelopeError failed:", e.message);
1037: direct_interchat: const regex = /(?:^|\n)[ \t]*@@AI_BRIDGE_LOCAL_START@@[ \t]*\r?\n([\s\S]*?)\r?\n[ \t]*@@AI_BRIDGE_LOCAL_END@@[ \t]*(?=\r?\n|$)/g; // AIBRIDGE_LINE_ISOLATED_ENVELOPE_CAPTURE
1047: id_fields: if (!c.command_id) {
1048: id_fields: reportEnvelopeError("envelope_missing_command_id", "command_id ausente", raw);
1059: id_fields: const errorKey = safeIdPart((extractJsonStringField(raw, "command_id") || String(raw).slice(0, 80)) + "_" + String(e.message || ""));
1087: id_fields: if (sentIds.has(cmd.command_id)) {
1088: id_fields: showNotice("Comando duplicado ignorado", "command_id=" + cmd.command_id, "warn");
1094: id_fields: if (cmd.source_chat_id && cmd.source_chat_id !== actualSourceChatId) {
1095: id_fields: const declaredSource = cmd.source_chat_id;
1104: id_fields: 'observacao=Evento final de erro pre-gateway. O chat deve analisar a causa, corrigir o envelope, usar command_id novo e continuar.',
1105: id_fields: 'tipo=source_chat_id_mismatch',
1107: id_fields: 'id_original=' + (cmd.command_id || 'unknown'),
1110: id_fields: 'destino=' + (cmd.target_chat_id || 'unknown'),
1111: id_fields: 'erro=source_chat_id do envelope nao corresponde ao chat atual. Nada foi executado nem enviado ao gateway.',
1112: id_fields: 'correcao=Reenvie o envelope a partir do chat correto ou ajuste source_chat_id para o chat atual.'
1114: id_fields: showNotice('Source chat divergente', 'command_id=' + (cmd.command_id || 'unknown') + String.fromCharCode(10) + 'origem=' + declaredSource + String.fromCharCode(10) + 'chat_atual=' 
1115: id_fields: const mismatchKey = 'ai_bridge_source_chat_id_mismatch:' + (cmd.command_id || 'unknown');
1118: id_fields: console.warn('[Local v' + VERSION + '] source_chat_id_mismatch suppressed duplicate for', cmd.command_id || 'unknown');
1121: id_fields: sendTextToChat(statusText, 'source_chat_id_mismatch_' + (cmd.command_id || 'unknown'));
1124: id_fields: sendTextToChat(statusText, 'source_chat_id_mismatch_' + (cmd.command_id || 'unknown'));
1128: id_fields: cmd.source_chat_id = actualSourceChatId;
1132: id_fields: sentIds.add(cmd.command_id);
1135: id_fields: showNotice("Comando local capturado", "command_id=" + cmd.command_id + "\naction=" + cmd.action, "info");
1145: id_fields: showNotice("Comando enviado ao gateway", "command_id=" + cmd.command_id + "\nstatus=" + status, "success");
1154: direct_interchat: The standalone ChatGPT scanner with visible feedback is now responsible for outbound envelope capture. */
1166: queue_words: console.warn("[AI Bridge Local] sendChatHeartbeat failed; skipped heartbeat interval", e && e.message);
1176: queue_words: console.warn("[AI Bridge Local] sendChatHeartbeat failed; skipped heartbeat direct_call", e && e.message);
1179: direct_interchat: /* AI Bridge Local: Gemini auto envelope capture. */
1180: direct_interchat: (function installAiBridgeGeminiCapturedEnvelopeBridge() {
1181: direct_interchat: if (window.__AI_BRIDGE_GEMINI_CAPTURE_INSTALLED__) return;
1182: direct_interchat: window.__AI_BRIDGE_GEMINI_CAPTURE_INSTALLED__ = true;
1186: direct_interchat: const MAX_CAPTURE_CHARS = 20000;
1187: direct_interchat: const DEDUPE_PREFIX = "ai_bridge_captured_envelope:";
1209: direct_interchat: function parseCapturedEnvelopeText(rawText) {
1214: direct_interchat: if (text.length > MAX_CAPTURE_CHARS) {
1215: direct_interchat: return { ok: false, error: "capture_too_large" };
1242: id_fields: if (!String(envelope.command_id || "").trim()) {
1243: id_fields: return { ok: false, error: "missing_command_id" };
1253: direct_interchat: function wasCaptured(commandId) {
1261: direct_interchat: function markCaptured(commandId) {
1269: direct_interchat: function tryCaptureEnvelopeFromNode(node) {
1281: direct_interchat: if (candidateText.length > MAX_CAPTURE_CHARS) return;
1292: direct_interchat: const attempt = parseCapturedEnvelopeText(candidateText);
1301: id_fields: const commandId = String(parsed.envelope.command_id || "").trim();
1302: direct_interchat: if (wasCaptured(commandId)) {
1306: direct_interchat: markCaptured(commandId);
1309: direct_interchat: type: "AI_BRIDGE_CAPTURED_ENVELOPE",
1310: id_fields: source_chat_id: getGeminiChatId(),
1316: direct_interchat: console.warn("[Local] Gemini envelope capture sendMessage failed:", runtimeError.message);
1316: queue_words: console.warn("[Local] Gemini envelope capture sendMessage failed:", runtimeError.message);
1320: direct_interchat: console.warn("[Local] Gemini envelope capture rejected by background:", response && response.error);
... 132 more hits truncated ...
```

### extension/route_classifier.js

- Status: exists
- Lines: 104
- Audit hits: 8

```text
11: direct_interchat: const ROUTE_DIRECT_INTERCHAT = "direct_interchat";
45: route_decision: function classifyRoute(envelope) {
59: direct_interchat: if (transport === ROUTE_DIRECT_INTERCHAT || transport === "direct-interchat" || transport === "direct") {
60: direct_interchat: return ROUTE_DIRECT_INTERCHAT;
83: direct_interchat: return ROUTE_DIRECT_INTERCHAT;
87: direct_interchat: return ROUTE_DIRECT_INTERCHAT;
94: direct_interchat: ROUTE_DIRECT_INTERCHAT,
96: route_decision: classifyRoute
```

## Gateway-first reading

- The extension should stay a thin transport plus UI/browser action surface.
- The local gateway should own envelope validation, queue state, retry diagnostics, and routing decision auditability.
- Extension code paths that change target/source chat IDs or command IDs should be reviewed before behavior changes.
- This audit does not change extension behavior.

