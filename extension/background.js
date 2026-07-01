/* AIBRIDGE_ROUTE_CLASSIFIER_LOAD_START */
try {
  if (
    typeof importScripts === "function" &&
    typeof globalThis.AIBridgeRouteClassifier === "undefined"
  ) {
    importScripts("route_classifier.js");
  }
} catch (error) {
  console.warn("[AI Bridge Local] route classifier load failed", error);
}

globalThis.aiBridgeClassifyRouteSafe = function aiBridgeClassifyRouteSafe(envelope) {
  if (
    globalThis.AIBridgeRouteClassifier &&
    typeof globalThis.AIBridgeRouteClassifier.classifyRoute === "function"
  ) {
    return globalThis.AIBridgeRouteClassifier.classifyRoute(envelope);
  }

  const payload = envelope && typeof envelope.payload === "object" ? envelope.payload : {};
  const forceGateway = envelope && (envelope.force_gateway === true || envelope.force_gateway === "true" || payload.force_gateway === true || payload.force_gateway === "true");

  if (forceGateway) {
    return "local_gateway";
  }

  const action = String((envelope && (envelope.action || payload.action)) || "").trim().toLowerCase();
  const transport = String((envelope && (envelope.transport || payload.transport)) || "").trim().toLowerCase();

  if (transport === "direct_interchat" || transport === "direct-interchat" || transport === "direct") {
    return "direct_interchat";
  }

  if (transport === "local_gateway" || transport === "local-gateway" || transport === "gateway") {
    return "local_gateway";
  }

  if (action === "send-chat-message" || action === "send_chat_message") {
    return "direct_interchat";
  }

  return "local_gateway";
};
/* AIBRIDGE_ROUTE_CLASSIFIER_LOAD_END */
// AI Bridge Local v0. - HelpUS AI compatible bridge
const VERSION = "0.5.74";
const GATEWAY = "http://127.0.0.1:8766";
const registry = {};
const DIRECT_INTERCHAT_ENABLED = true;
const DIRECT_INTERCHAT_ALLOW_GATEWAY_FALLBACK = true;


async function postJson(path, body) {
  const res = await fetch(GATEWAY + path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });

  let data = {};
  try {
    data = await res.json();
  } catch (e) {
    data = { ok: false, error: "invalid_json_response" };
  }

  if (!res.ok) {
    throw new Error(data.error || ("http_" + res.status));
  }

  return data;
}

async function postTelemetryEvent(eventType, details = {}) {
 try {
 await postJson('/event', {
 event_type: eventType,
 command_id: details.command_id || details.commandId || null,
 message: details.message || '',
 payload: Object.assign({ extension_version: VERSION, source: 'background' }, details)
 });
 } catch (e) {
 console.warn('[AI_LOCAL] telemetry failed', eventType, e.message);
 }
}

postTelemetryEvent('extension_version', { version: VERSION });
async function postCommand(cmd) {
  console.log("[bg] Sending:", cmd.command_id);
  try {
    return await postJson("/bridge/commands", cmd);
  } catch (e) {
    const errorText = String((e && e.message) || e || "");
    if (errorText === "duplicate") {
      console.log("[bg] Command already queued:", cmd && cmd.command_id);
      return {
        ok: true,
        already_queued: true,
        idempotent: true,
        command_id: cmd && cmd.command_id ? cmd.command_id : null,
        error: "duplicate"
      };
    }
    throw e;
  }
}

async function postAck(commandId, status, extra = {}) {
  const body = Object.assign({
    command_id: commandId,
    status: status
  }, extra);

  return await postJson("/bridge/acks", body);
}

function isUuid(value) {
  return /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/.test(String(value || "").trim());
}

function safeIdPart(value) {
  return String(value || "unknown").replace(/[^a-zA-Z0-9_-]/g, "_").slice(0, 80);
}
const postedDeliveryStatusKeys = new Set();

async function postDeliveryStatus(action, status, detail, result = {}) {
  try {
    if (!action || !action.command_id) return;
 if (status === 'delivering') postTelemetryEvent('delivery_attempt', { command_id: action.command_id, target_chat_id: action.target_chat_id, action: action.action });
 if (status === 'sent') postTelemetryEvent('delivery_ok', { command_id: action.command_id, target_chat_id: action.target_chat_id, action: action.action });
 if (status === 'failed') postTelemetryEvent('delivery_failed', { command_id: action.command_id, target_chat_id: action.target_chat_id, action: action.action, message: String(detail || 'unknown') });
    if (String(action.command_id).startsWith("local_status_")) return;

    const statusKey = String(status || "unknown") + ":" + String(action.command_id || "unknown");
    if (postedDeliveryStatusKeys.has(statusKey)) {
      console.log("[bg] Suppressed duplicate delivery status:", statusKey);
      return;
    }
    postedDeliveryStatusKeys.add(statusKey);

    const sourceChatId = canonicalChatId(action.source_chat_id || "");
    const targetChatId = canonicalChatId(action.target_chat_id || "");

    if (!isUuid(sourceChatId)) {
      console.log("[bg] Skip compact delivery status: invalid source_chat_id", action.source_chat_id);
      return;
    }

    const resultText = String(detail || "unknown").replace(/[\r\n]+/g, " ").slice(0, 120);
    const method = result.method || "unknown";
    const attempts = result.attempts ?? "unknown";

    let statusMessage = "";

    if (status === "sent") {
      statusMessage =
        "[AI_LOCAL] enviado id=" + action.command_id +
        " destino=" + (targetChatId || "unknown") +
        " resultado=" + resultText +
        " metodo=" + method +
        " tentativas=" + attempts +
        "; no_reply=1; aguarde.";
    } else {
      statusMessage =
        "[AI_LOCAL_ERRO]\n" +
        "acao=verifique_destino_ou_reenvie\n" +
        "no_reply=0\n" +
        "tipo=delivery_result\n" +
        "versao=" + VERSION + "\n" +
        "id_original=" + action.command_id + "\n" +
        "origem=" + sourceChatId + "\n" +
        "destino=" + (targetChatId || "unknown") + "\n" +
        "erro=" + resultText + "\n" +
        "correcao=Se a mensagem nao chegou ao destino, reenvie o envelope local com novo command_id ou verifique se a aba destino esta aberta, com extensao recarregada e chat_id correto.";
    }

    await postCommand({
      schema: "ai_bridge_local.envelope",
      schema_version: 1,
      created_at_utc: new Date().toISOString(),
      command_id: "local_status_delivery_" + safeIdPart(status) + "_" + safeIdPart(action.command_id),
      action: "send-chat-message",
      source_chat_id: targetChatId || "gateway-brain-supervisor",
      target_chat_id: sourceChatId,
      delivery_kind: "inter_agent_message",
      conversation_id: (action.conversation_id || "local_delivery_status") + "_status",
      from_agent: "AI Bridge Local Extension " + VERSION,
      message: statusMessage
    });

    console.log("[bg] Compact delivery status queued:", action.command_id, status);
  } catch (e) {
    console.log("[bg] postDeliveryStatus compact error:", e.message);
  }
}

function canonicalChatId(value) {
  const raw = String(value || "").trim().replace(/^(chat|deepseek|gemini):/i, "");
  const m = raw.match(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);
  return m ? m[0].toLowerCase() : raw;
}

function withTimeout(promise, timeoutMs, fallback) {
  return new Promise((resolve) => {
    let done = false;

    const finish = (value) => {
      if (done) return;
      done = true;
      resolve(value);
    };

    const timer = setTimeout(() => {
      finish(fallback);
    }, timeoutMs);

    Promise.resolve(promise)
      .then((value) => {
        clearTimeout(timer);
        finish(value);
      })
      .catch((error) => {
        clearTimeout(timer);
        finish({
          ok: false,
          reason: "promise_exception",
          error: error && error.message ? error.message : String(error)
        });
      });
  });
}

function boolFlag(value) {
  return value === true || value === "true" || value === 1 || value === "1";
}

function shouldForceGateway(cmd) {
  return Boolean(
    cmd &&
    (
      boolFlag(cmd.force_gateway) ||
      boolFlag(cmd.audit_required) ||
      boolFlag(cmd.persist_required) ||
      boolFlag(cmd.require_gateway)
    )
  );
}

function isDirectInterChatCommand(cmd) {
  return Boolean(
    DIRECT_INTERCHAT_ENABLED &&
    cmd &&
    cmd.action === "send-chat-message" &&
    cmd.delivery_kind === "inter_agent_message" &&
    cmd.target_chat_id &&
    cmd.message &&
    !shouldForceGateway(cmd)
  );
}

function mustUseGateway(cmd) {
  if (!cmd) return true;

  if (shouldForceGateway(cmd)) return true;

  if (cmd.action === "run-command") return true;
  if (cmd.delivery_kind === "local_capability") return true;

  if (cmd.action === "send-chat-message" && cmd.delivery_kind === "inter_agent_message") {
    return false;
  }

  return true;
}


/* AIBRIDGE_DIRECT_TARGET_DISCOVERY_063_START */
function aiBridgeUrlMatchesDirectTarget(url, targetChatId, targetUrl) {
  const urlText = String(url || "");
  const chatId = canonicalChatId(targetChatId || "");
  const wantedUrl = String(targetUrl || "").trim();
  if (!urlText || !chatId) return false;
  if (urlText.includes(chatId)) return true;
  try {
    if (decodeURIComponent(urlText).includes(chatId)) return true;
  } catch (_) {}
  if (wantedUrl) {
    if (urlText === wantedUrl) return true;
    try {
      const current = new URL(urlText);
      const wanted = new URL(wantedUrl);
      if (current.origin === wanted.origin && current.pathname === wanted.pathname) return true;
    } catch (_) {}
  }
  return false;
}

async function aiBridgeDiscoverDirectTargetTab(targetChatId, targetUrl, commandId) {
  const canonicalTargetChatId = canonicalChatId(targetChatId || "");
  if (!canonicalTargetChatId) return { ok: false, error: "missing_target_chat_id" };
  if (typeof chrome === "undefined" || !chrome.tabs || !chrome.tabs.query) {
    return { ok: false, error: "tabs_query_unavailable", target_chat_id: canonicalTargetChatId };
  }
  let tabs = [];
  try {
    tabs = await chrome.tabs.query({});
  } catch (error) {
    return { ok: false, error: "tabs_query_failed", target_chat_id: canonicalTargetChatId, detail: error && error.message ? error.message : String(error || "unknown") };
  }
  const tabDiagnostics = (tabs || []).slice(0, 20).map((tab) => ({ id: tab && tab.id, url: tab && tab.url ? String(tab.url).slice(0, 300) : "", title: tab && tab.title ? String(tab.title).slice(0, 120) : "" }));
 const matches = (tabs || []).filter((tab) => tab && aiBridgeUrlMatchesDirectTarget(tab.url, canonicalTargetChatId, targetUrl));
 const activeMatches = matches.filter((tab) => tab && tab.active);
 const match = activeMatches[0] || matches[0];
  if (!match || !Number.isFinite(Number(match.id))) {
    return { ok: false, error: "target_tab_not_open", target_chat_id: canonicalTargetChatId, target_url: targetUrl || "", tab_count: (tabs || []).length, tabs_sample: tabDiagnostics };
  }
  const tabId = Number(match.id);
  registry[canonicalTargetChatId] = tabId;
  try {
    await aiBridgeReinjectContentScriptForDirectDelivery(tabId, commandId || "unknown");
  } catch (error) {
    console.warn("[bg] direct target discovery reinject failed:", error);
  }
  return { ok: true, discovered: true, tab_id: tabId, target_chat_id: canonicalTargetChatId, url: match.url || "" };
}
/* AIBRIDGE_DIRECT_TARGET_DISCOVERY_063_END */

async function deliverInterChatDirect(cmd) {
  const targetChatId = canonicalChatId(cmd.target_chat_id || "");
  const sourceChatId = canonicalChatId(cmd.source_chat_id || "");

  if (!targetChatId) {
    return { ok: false, direct: true, error: "missing_target_chat_id" };
  }

 let tabId = registry[targetChatId];
 const discoveredTarget = await aiBridgeDiscoverDirectTargetTab(targetChatId, cmd.target_url || cmd.url || "", cmd.command_id || "unknown");
 if (discoveredTarget && discoveredTarget.ok && discoveredTarget.tab_id) {
 tabId = discoveredTarget.tab_id;
 } else if (!tabId) {
 return {
 ok: false,
 direct: true,
 error: "target_chat_not_registered",
 target_chat_id: targetChatId,
 discovery: discoveredTarget || null,
 hint: "Abra/recarregue a aba destino para a extensao registrar o chat_id, ou informe target_url de uma aba aberta."
 };
 }
  const directAction = Object.assign({}, cmd, {
    command_id: cmd.command_id,
    action: cmd.action,
    message: cmd.message || "",
    target_chat_id: targetChatId,
    source_chat_id: sourceChatId || cmd.source_chat_id || ""
  });

  console.log("[bg] Direct inter-chat delivery:", directAction.command_id, "to", targetChatId, "tab", tabId);

  const result = await withTimeout(
    injectText(tabId, directAction),
    20000,
    { ok: false, reason: "direct_interchat_inject_timeout" }
  );

  if (result && result.ok) {
    console.log("[bg] Direct inter-chat delivered:", directAction.command_id, JSON.stringify(result));
    return { ok: true, direct: true, command_id: directAction.command_id, target_chat_id: targetChatId, result };
  }

  const reason = result && (result.reason || result.error) ? (result.reason || result.error) : "direct_interchat_inject_failed";
  console.log("[bg] Direct inter-chat failed:", directAction.command_id, reason);
  return { ok: false, direct: true, command_id: directAction.command_id, target_chat_id: targetChatId, error: reason, result };
}

/* AIBRIDGE_DIRECT_CROSS_PROFILE_GATEWAY_FALLBACK_065_START */
function shouldFallbackDirectFailureToGateway(cmd, directResult) {
  if (!DIRECT_INTERCHAT_ALLOW_GATEWAY_FALLBACK) return false;
  if (!cmd || !directResult || directResult.ok) return false;

  const action = String(cmd.action || cmd.type || "").trim().toLowerCase();
  const deliveryKind = String(cmd.delivery_kind || "").trim().toLowerCase();

  if (action !== "send-chat-message" && action !== "send_chat_message") return false;
  if (deliveryKind !== "inter_agent_message") return false;

  // Safety gate: local runtime capabilities must never be re-routed by the direct fallback.
  if (action === "run-command" || action === "run_command") return false;
  if (deliveryKind === "local_capability") return false;
  if (boolFlag(cmd.disable_gateway_fallback) || boolFlag(cmd.no_gateway_fallback)) return false;

  const reasonText = String(
    (directResult && (directResult.error || directResult.reason || directResult.message)) ||
    JSON.stringify(directResult || {})
  );

  if (boolFlag(cmd.allow_gateway_fallback) || boolFlag(cmd.force_gateway_on_direct_failure)) return true;

  return /target_chat_not_registered|direct_delivery_target_not_registered|target_tab_not_open|target_tab_not_found|tabs_query_unavailable|tabs_query_failed|direct_delivery_target_not_registered|direct_interchat_inject_timeout|direct_interchat_inject_failed|Receiving end does not exist|Could not establish connection/i.test(reasonText);
}
/* AIBRIDGE_DIRECT_CROSS_PROFILE_GATEWAY_FALLBACK_065_END */

async function routeBridgeCommand(cmd, sourceLabel) {
  if (isDirectInterChatCommand(cmd)) {
    const directResult = await deliverInterChatDirect(cmd);
    if (directResult && directResult.ok) {
      return { ok: true, direct: true, data: directResult };
    }

    if (shouldFallbackDirectFailureToGateway(cmd, directResult)) {
      console.log("[bg] Direct inter-chat fallback to gateway:", cmd.command_id, directResult && directResult.error);
      const gatewayResult = await postCommand(cmd);
      pollMessagesSoon(sourceLabel + "_directFallback");
      return { ok: true, direct: false, fallback: true, data: gatewayResult, direct_error: directResult && directResult.error };
    }

    return { ok: false, direct: true, error: (directResult && directResult.error) || "direct_interchat_failed", data: directResult };
  }

  if (mustUseGateway(cmd)) {
    const gatewayResult = await postCommand(cmd);
    pollMessagesSoon(sourceLabel || "postCommand");
    return { ok: true, direct: false, data: gatewayResult };
  }

  return { ok: false, direct: false, error: "unroutable_command" };
}

/* AIBRIDGE_DIRECT_REINJECT_ON_MISSING_RECEIVER_062_START */
function aiBridgeLooksLikeMissingReceiverResult(result) {
  const text = String(
    (result && (result.error || result.reason || result.message)) ||
    JSON.stringify(result || {})
  );
  return /Receiving end does not exist|Could not establish connection/i.test(text);
}

function aiBridgeSleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function aiBridgeReinjectContentScriptForDirectDelivery(tabId, commandId) {
  const numericTabId = Number(tabId);
  if (!Number.isFinite(numericTabId)) {
    return { ok: false, error: "invalid_tab_id_for_reinject", tab_id: tabId, command_id: commandId || "unknown" };
  }

  try {
    await chrome.scripting.executeScript({
      target: { tabId: numericTabId },
      files: ["content_script.js"]
    });
    await aiBridgeSleep(900);
    return {
      ok: true,
      method: "content_script_reinjected",
      tab_id: numericTabId,
      command_id: commandId || "unknown"
    };
  } catch (err) {
    return {
      ok: false,
      method: "content_script_reinject_failed",
      tab_id: numericTabId,
      command_id: commandId || "unknown",
      error: String(err && err.message ? err.message : err)
    };
  }
}
/* AIBRIDGE_DIRECT_REINJECT_ON_MISSING_RECEIVER_062_HELPERS_END */

async function injectTextOnce(tabId, action) {
  const message = {
    type: "AI_BRIDGE_INJECT_TEXT",
    action: {
      action: "inject_text",
      text: action.message || "",
      auto_submit: true,
      action_id: action.command_id,
      command_id: action.command_id
    }
  };

  return await new Promise((resolve) => {
    let done = false;

    const finish = (payload) => {
      if (done) return;
      done = true;
      resolve(payload || { ok: false, reason: "empty_inject_response" });
    };

    const timer = setTimeout(() => {
      finish({
        ok: false,
        reason: "inject_timeout",
        error: "chrome.tabs.sendMessage callback timeout"
      });
    }, 15000);

    try {
      chrome.tabs.sendMessage(tabId, message, (response) => {
        clearTimeout(timer);
        const runtimeError = chrome.runtime.lastError;
        if (runtimeError) {
          finish({
            ok: false,
            reason: "inject_runtime_error",
            error: runtimeError.message
          });
          return;
        }

        console.log("[bg] Inject result:", action.command_id, JSON.stringify(response));
        finish(response || { ok: false, reason: "empty_inject_response" });
      });
    } catch (e) {
      clearTimeout(timer);
      finish({ ok: false, reason: "inject_exception", error: e.message });
    }
  });
}

async function injectText(tabId, action) {
  const first = await injectTextOnce(tabId, action);
  if (first && first.ok) return first;

  if (!aiBridgeLooksLikeMissingReceiverResult(first)) {
    return first;
  }

  console.warn("[bg] direct delivery receiver missing; reinjecting content_script.js:", "unknown", "tab:", tabId);
  const reinject = await aiBridgeReinjectContentScriptForDirectDelivery(tabId, "unknown");

  if (!reinject || !reinject.ok) {
    return Object.assign({}, first || {}, {
      ok: false,
      reason: "content_script_reinject_failed",
      reinject
    });
  }

  const second = await injectTextOnce(tabId, action);
  if (second && typeof second === "object") {
    second.reinjected_content_script = true;
    second.reinject = reinject;
  }
  return second;
}
/* AIBRIDGE_DIRECT_REINJECT_ON_MISSING_RECEIVER_062_END */
const POLL_INTERVAL_MS = 1000;
const POLL_SOON_DEBOUNCE_MS = 150;
const MAX_ACTIONS_PER_CHAT_CYCLE = 3;
let pollInFlight = false;
let pollSoonTimer = null;
let pollRequestedAgain = false;
const perChatInFlight = new Set();

function pollMessagesSoon(reason = 'manual') {
  if (pollSoonTimer) clearTimeout(pollSoonTimer);
  pollSoonTimer = setTimeout(() => {
    pollSoonTimer = null;
    pollMessages(reason);
  }, POLL_SOON_DEBOUNCE_MS);
}

async function pollOneChat(chatId) {
  if (chatId === 'unknown') return;
  if (perChatInFlight.has(chatId)) return;

  perChatInFlight.add(chatId);
  try {
    for (let actionIndex = 0; actionIndex < MAX_ACTIONS_PER_CHAT_CYCLE; actionIndex += 1) {
      const tabId = registry[chatId];
      if (!tabId) return;

      const pollStartedAt = Date.now();
      const res = await fetch(GATEWAY + '/bridge/next-action?chat_id=' + encodeURIComponent(chatId));
      const data = await res.json();

      if (!(data.action && data.action.message)) return;

      const action = data.action;
      postTelemetryEvent('action_received', {
        command_id: action.command_id,
        target_chat_id: chatId,
        action: action.action,
        action_index: actionIndex,
        poll_latency_ms: Date.now() - pollStartedAt
      });

      console.log('[bg] Injecting to:', chatId, action.command_id);
      console.log('[bg] Inject start:', action.command_id, 'tab', tabId);

      const injectStartedAt = Date.now();
      postTelemetryEvent('inject_started', {
        command_id: action.command_id,
        target_chat_id: chatId,
        tab_id: tabId,
        action_index: actionIndex
      });

      const result = await withTimeout(
        injectText(tabId, action),
        20000,
        {
          ok: false,
          reason: 'inject_outer_timeout',
          error: 'injectText outer timeout'
        }
      );

      const injectDurationMs = Date.now() - injectStartedAt;
      postTelemetryEvent('inject_done', {
        command_id: action.command_id,
        target_chat_id: chatId,
        ok: !!(result && result.ok),
        duration_ms: injectDurationMs,
        reason: result && (result.reason || result.error) ? (result.reason || result.error) : ''
      });

      console.log('[bg] Inject completed:', action.command_id, JSON.stringify(result));

      if (result && result.ok) {
        await postAck(action.command_id, 'acked', {
          stdout: JSON.stringify({
            method: result.method || 'unknown',
            attempts: result.attempts ?? null,
            text_length: result.text_length ?? null
          })
        });
        postTelemetryEvent('ack_posted', {
          command_id: action.command_id,
          target_chat_id: chatId,
          status: 'acked'
        });
        console.log('[bg] ACKed:', action.command_id);
        await postDeliveryStatus(action, 'sent', 'acked', result);
      } else {
        const reason = result?.reason || result?.error || 'inject_failed';
        await postAck(action.command_id, 'failed', {
          return_code: -1,
          stderr: reason,
          error: reason
        });
        postTelemetryEvent('ack_posted', {
          command_id: action.command_id,
          target_chat_id: chatId,
          status: 'failed',
          reason: reason
        });
        console.log('[bg] FAILED:', action.command_id, reason);
        await postDeliveryStatus(action, 'error', reason, result || {});
      }
    }
  } catch (e) {
    console.log('[bg] Poll error:', chatId, e.message);
  } finally {
    perChatInFlight.delete(chatId);
  }
}

function pollMessages(reason = 'interval') {
  if (pollInFlight) {
    pollRequestedAgain = true;
    return;
  }

  pollInFlight = true;
  try {
    const chatIds = Object.keys(registry).filter((chatId) => chatId !== 'unknown' && registry[chatId]);
    postTelemetryEvent('poll_started', {
      reason: reason,
      chat_count: chatIds.length
    });

    void Promise.allSettled(chatIds.map((chatId) => pollOneChat(chatId))).then((results) => {
      const rejected = results.filter((result) => result.status === 'rejected').length;
      if (rejected > 0) {
        postTelemetryEvent('poll_completed_with_rejections', {
          reason: reason,
          rejected: rejected,
          chat_count: chatIds.length
        });
      }
    });
  } finally {
    pollInFlight = false;
    if (pollRequestedAgain) {
      pollRequestedAgain = false;
      pollMessagesSoon('queued_again');
    }
  }
}


function aiBridgeCapturedPlainObject(value) {
  return Boolean(value && typeof value === "object" && !Array.isArray(value));
}

function aiBridgeCapturedString(value) {
  return String(value || "").trim();
}

function aiBridgeCapturedCommandText(envelope) {
  const payload = aiBridgeCapturedPlainObject(envelope && envelope.payload) ? envelope.payload : {};
  const parts = [];
  if (Array.isArray(payload.command)) parts.push(payload.command.join(" "));
  if (payload.script_text) parts.push(String(payload.script_text));
  if (payload.cwd) parts.push(String(payload.cwd));
  return (" " + parts.join(" ") + " ").toLowerCase();
}

function aiBridgeCapturedReadonlyAllowed(envelope) {
  const text = aiBridgeCapturedCommandText(envelope);
  const blocked = ["remove-item", " set-content", " add-content", " out-file", " git add", " git commit", " git push", " npm install", " pip install", " invoke-expression", " iex", " curl", " del ", " erase ", " rm ", " rmdir ", " move ", " mv ", " copy ", " cp "];
  if (blocked.some((token) => text.includes(token))) return false;
  return text.includes("get-childitem") || text.includes(" dir ") || text.includes("git status") || text.includes("git diff --name-only") || text.includes("git diff --stat");
}

function validateAiBridgeCapturedEnvelopeMessage(message, sender) {
  const envelope = message && message.envelope;
  if (!aiBridgeCapturedPlainObject(envelope)) return { ok: false, error: "captured_envelope_not_object" };

  const sourceChatId = aiBridgeCapturedString(message.source_chat_id || envelope.source_chat_id);
  const commandId = aiBridgeCapturedString(envelope.command_id);
  const targetChatId = aiBridgeCapturedString(envelope.target_chat_id);

  const conversationId = aiBridgeCapturedString(envelope.conversation_id);
  const action = aiBridgeCapturedString(envelope.action || envelope.type);
  const deliveryKind = aiBridgeCapturedString(envelope.delivery_kind);

  if (!sourceChatId) return { ok: false, error: "missing_source_chat_id" };
  if (!commandId) return { ok: false, error: "missing_command_id" };
  if (!targetChatId) return { ok: false, error: "missing_target_chat_id" };
  if (!conversationId) return { ok: false, error: "missing_conversation_id" };
  if (!action) return { ok: false, error: "missing_action" };

  const forwardedEnvelope = { ...envelope, source_chat_id: sourceChatId, action, type: envelope.type || action };

  if (action === "send-chat-message") {
    if (deliveryKind !== "inter_agent_message") return { ok: false, error: "send_chat_message_requires_inter_agent_message" };
    return { ok: true, envelope: forwardedEnvelope, command_id: commandId };
  }

  if (action === "run-command") {
    if (deliveryKind !== "local_capability") return { ok: false, error: "run_command_requires_local_capability" };
    if (!aiBridgeCapturedPlainObject(envelope.payload)) return { ok: false, error: "run_command_requires_payload_object" };
    if (!aiBridgeCapturedReadonlyAllowed(envelope)) return { ok: false, error: "run_command_rejected_by_readonly_gate" };
    return { ok: true, envelope: forwardedEnvelope, command_id: commandId };
  }

  return { ok: false, error: "captured_action_not_allowed" };
}



/* AIBRIDGE_DIRECT_INTERCHAT_DELIVERY_START */
/* AIBRIDGE_DIRECT_CROSS_PROFILE_GATEWAY_FALLBACK_065_CAPTURED_START */
async function aiBridgeDirectDeliverCapturedEnvelope(envelope) {
  const targetChatId = canonicalChatId(envelope && envelope.target_chat_id ? envelope.target_chat_id : "");
  const sourceChatId = canonicalChatId(envelope && envelope.source_chat_id ? envelope.source_chat_id : "");
  const commandId = envelope && envelope.command_id ? envelope.command_id : "unknown";
  const action = String((envelope && (envelope.action || envelope.type)) || "").trim().toLowerCase();
  const deliveryKind = String((envelope && envelope.delivery_kind) || "").trim().toLowerCase();

  if (!targetChatId) {
    return { ok: false, route: "direct_interchat", error: "direct_delivery_missing_target_chat_id" };
  }

  if (action !== "send-chat-message" && action !== "send_chat_message") {
    return { ok: false, route: "direct_interchat", error: "direct_delivery_unsupported_action", action };
  }

  if (deliveryKind !== "inter_agent_message") {
    return { ok: false, route: "direct_interchat", error: "direct_delivery_requires_inter_agent_message" };
  }

  let tabId = registry[targetChatId];
  if (!tabId) {
    const discoveredTarget = await aiBridgeDiscoverDirectTargetTab(targetChatId, envelope && (envelope.target_url || envelope.url) ? (envelope.target_url || envelope.url) : "", commandId);

    if (discoveredTarget && discoveredTarget.ok && discoveredTarget.tab_id) {
      tabId = discoveredTarget.tab_id;
    } else {
      const directResult = {
        ok: false,
        direct: true,
        route: "direct_interchat",
        error: "direct_delivery_target_not_registered",
        direct_error: "target_chat_not_registered",
        target_chat_id: targetChatId,
        discovery: discoveredTarget || null
      };

      if (shouldFallbackDirectFailureToGateway(envelope, directResult)) {
        console.log("[bg] Captured direct fallback to gateway:", commandId, directResult.error);
        const gatewayResult = await postCommand(envelope);
        pollMessagesSoon("capturedEnvelope_directCrossProfileFallback");
        return {
          ok: true,
          route: "local_gateway_cross_profile",
          direct: false,
          fallback: true,
          command_id: commandId,
          target_chat_id: targetChatId,
          direct_error: directResult.error,
          discovery: discoveredTarget || null,
          data: gatewayResult
        };
      }

      return directResult;
    }
  }

  Object.assign(envelope, {
    command_id: commandId,
    action: "send-chat-message",
    message: envelope && envelope.message ? envelope.message : "",
    target_chat_id: targetChatId,
    source_chat_id: sourceChatId || (envelope && envelope.source_chat_id) || ""
  });

  postTelemetryEvent("direct_interchat_delivery_started", {
    command_id: commandId,
    target_chat_id: targetChatId,
    route: "captured_envelope"
  });

  const result = await withTimeout(
    injectText(tabId, envelope),
    20000,
    { ok: false, reason: "direct_interchat_inject_timeout" }
  );

  if (result && result.ok) {
    postTelemetryEvent("direct_interchat_delivery_ok", {
      command_id: commandId,
      target_chat_id: targetChatId,
      route: "captured_envelope"
    });

    return {
      ok: true,
      route: "direct_interchat",
      direct: true,
      command_id: commandId,
      target_chat_id: targetChatId,
      data: result
    };
  }

  const reason = result && (result.reason || result.error) ? (result.reason || result.error) : "direct_interchat_inject_failed";

  postTelemetryEvent("direct_interchat_delivery_failed", {
    command_id: commandId,
    target_chat_id: targetChatId,
    route: "captured_envelope",
    reason: reason
  });

  const directResult = {
    ok: false,
    route: "direct_interchat",
    direct: true,
    command_id: commandId,
    target_chat_id: targetChatId,
    error: reason,
    data: result || null
  };

  if (shouldFallbackDirectFailureToGateway(envelope, directResult)) {
    console.log("[bg] Captured direct inject fallback to gateway:", commandId, reason);
    const gatewayResult = await postCommand(envelope);
    pollMessagesSoon("capturedEnvelope_directInjectFallback");
    return {
      ok: true,
      route: "local_gateway_cross_profile",
      direct: false,
      fallback: true,
      command_id: commandId,
      target_chat_id: targetChatId,
      direct_error: reason,
      data: gatewayResult
    };
  }

  return directResult;
}
/* AIBRIDGE_DIRECT_CROSS_PROFILE_GATEWAY_FALLBACK_065_CAPTURED_END */

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

  if (message && message.type === "AI_BRIDGE_CAPTURED_ENVELOPE") {
    const validation = validateAiBridgeCapturedEnvelopeMessage(message, sender);
    if (!validation.ok) {
      console.warn("[bg] captured envelope rejected:", validation.error);
      sendResponse({ ok: false, error: validation.error });
      return true;
    }

    const route = globalThis.aiBridgeClassifyRouteSafe(validation.envelope);

    if (route === "direct_interchat") {
      aiBridgeDirectDeliverCapturedEnvelope(validation.envelope)
        .then((result) => {
          if (result && result.ok) {
            sendResponse({ ok: true, route: "direct_interchat", data: result });
          } else {
            const error = result && result.error ? result.error : "direct_interchat_delivery_failed";
            sendResponse({ ok: false, route: "direct_interchat", error, data: result || null });
          }
        })
        .catch((e) => {
          console.log("[bg] direct interchat captured envelope error:", e.message);
          sendResponse({ ok: false, route: "direct_interchat", error: e.message });
        });
      return true;
    }

    routeBridgeCommand(validation.envelope, "capturedEnvelope")
      .then((result) => {
        if (result && result.ok) {
          sendResponse(Object.assign({ route: result.route || "local_gateway" }, result));
        } else {
          const error = result && result.error ? result.error : "captured_envelope_route_failed";
          sendResponse({ ok: false, route: "local_gateway", error, data: result || null });
        }
      })
      .catch((e) => {
        console.log("[bg] captured envelope routeBridgeCommand error:", e.message);
        sendResponse({ ok: false, route: "local_gateway", error: e.message });
      });
    return true;
  }


 if (message?.type === 'AI_LOCAL_TELEMETRY_EVENT') {
 postTelemetryEvent(message.event_type, message.payload || {});
 sendResponse({ ok: true });
 return true;
 }
  if (message && message.type === "AI_BRIDGE_BRIDGE_COMMAND") {
    const cmd = message.command || message;
    console.log("[bg] Received:", cmd.command_id);

    routeBridgeCommand(cmd, "postCommand")
      .then((r) => {
        sendResponse(r);
      })
      .catch((e) => {
        console.log("[bg] route command error:", e.message);
        sendResponse({ ok: false, error: e.message });
      });

    return true;
  }

  if (message && message.type === "AI_BRIDGE_REGISTER_CHAT") {
    const cid = canonicalChatId(message.chat_id);
    if (cid && sender.tab) {
      registry[cid] = sender.tab.id;
      console.log("[bg] Registered:", cid, "tab:", sender.tab.id);
      pollMessagesSoon('registerChat');
    }
    sendResponse({ ok: true });
    return true;
  }
});

setInterval(() => pollMessages('interval'), POLL_INTERVAL_MS);
pollMessagesSoon('startup');
console.log("[AI Bridge Local] v" + VERSION);
