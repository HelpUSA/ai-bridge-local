// AI Bridge Local v0. - HelpUS AI compatible bridge
const VERSION = "0.5.85";
const GATEWAY = "http://127.0.0.1:8766";
const registry = {};


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

async function routeBridgeCommand(cmd, sourceLabel) {
  const gatewayResult = await postCommand(cmd);
  pollMessagesSoon(sourceLabel || "postCommand");
  return { ok: true, direct: false, route: "local_gateway", data: gatewayResult };
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


chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

  if (message && message.type === "AI_BRIDGE_CAPTURED_ENVELOPE") {
    const validation = validateAiBridgeCapturedEnvelopeMessage(message, sender);
    if (!validation.ok) {
      console.warn("[bg] captured envelope rejected:", validation.error);
      sendResponse({ ok: false, error: validation.error });
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

/* AI_BRIDGE_MANAGED:COMPACT_BACKGROUND_0585:START */
(() => {
  if (globalThis.__AI_BRIDGE_COMPACT_BACKGROUND_0585__) return;
  globalThis.__AI_BRIDGE_COMPACT_BACKGROUND_0585__ = true;
  chrome.runtime.onMessage.addListener((message, sender, reply) => {
    if (!message || message.type !== "ai_bridge_compact_command_0585") return false;
    fetch("http://127.0.0.1:8767/v1/commands/compact", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(message.command)})
      .then(async r => reply({ok:r.ok,status:r.status,data:await r.json().catch(()=>({}))}))
      .catch(e => reply({ok:false,error:String(e)}));
    return true;
  });
})();
/* AI_BRIDGE_MANAGED:COMPACT_BACKGROUND_0585:END */
