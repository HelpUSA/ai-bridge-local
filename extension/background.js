// AI Bridge Local v0.4.14
const VERSION = "0.4.14";
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

async function postCommand(cmd) {
  console.log("[bg] Sending:", cmd.command_id);
  return await postJson("/bridge/commands", cmd);
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
        "acao=aguarde_ou_verifique\n" +
        "no_reply=1\n" +
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
      command_id: "local_status_delivery_" + safeIdPart(status) + "_" + safeIdPart(action.command_id) + "_" + Date.now(),
      action: "send-chat-message",
      source_chat_id: targetChatId || "gateway-brain-supervisor",
      target_chat_id: sourceChatId,
      delivery_kind: "local_inter_agent_message",
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
  const raw = String(value || "").trim().replace(/^(chat|deepseek):/i, "");
  const m = raw.match(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);
  return m ? m[0].toLowerCase() : raw;
}

async function injectText(tabId, action) {
  try {
    const response = await chrome.tabs.sendMessage(tabId, {
      type: "AI_BRIDGE_INJECT_TEXT",
      action: {
        action: "inject_text",
        text: action.message || "",
        auto_submit: true,
        action_id: action.command_id,
        command_id: action.command_id
      }
    });
    console.log("[bg] Inject result:", action.command_id, JSON.stringify(response));
    return response || { ok: false, reason: "empty_inject_response" };
  } catch (e) {
    console.log("[bg] Inject error:", action.command_id, e.message);
    return { ok: false, reason: "inject_exception", error: e.message };
  }
}

async function pollMessages() {
  for (const chatId of Object.keys(registry)) {
    if (chatId === "unknown") continue;

    const tabId = registry[chatId];
    if (!tabId) continue;

    try {
      const res = await fetch(GATEWAY + "/bridge/next-action?chat_id=" + encodeURIComponent(chatId));
      const data = await res.json();

      if (data.action && data.action.message) {
        const action = data.action;
        console.log("[bg] Injecting to:", chatId, action.command_id);

        const result = await injectText(tabId, action);

        if (result && result.ok) {
          await postAck(action.command_id, "acked", {
            stdout: JSON.stringify({
              method: result.method || "unknown",
              attempts: result.attempts ?? null,
              text_length: result.text_length ?? null
            })
          });
          console.log("[bg] ACKed:", action.command_id);
          await postDeliveryStatus(action, "sent", "acked", result);
        } else {
          const reason = result?.reason || result?.error || "inject_failed";
          await postAck(action.command_id, "failed", {
            return_code: -1,
            stderr: reason,
            error: reason
          });
          console.log("[bg] FAILED:", action.command_id, reason);
          await postDeliveryStatus(action, "error", reason, result || {});
        }
      }
    } catch (e) {
      console.log("[bg] Poll error:", chatId, e.message);
    }
  }
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message && message.type === "AI_BRIDGE_BRIDGE_COMMAND") {
    const cmd = message.command || message;
    console.log("[bg] Received:", cmd.command_id);

    postCommand(cmd)
      .then(r => sendResponse({ ok: true, data: r }))
      .catch(e => {
        console.log("[bg] postCommand error:", e.message);
        sendResponse({ ok: false, error: e.message });
      });

    return true;
  }

  if (message && message.type === "AI_BRIDGE_REGISTER_CHAT") {
    const cid = canonicalChatId(message.chat_id);
    if (cid && sender.tab) {
      registry[cid] = sender.tab.id;
      console.log("[bg] Registered:", cid, "tab:", sender.tab.id);
    }
    sendResponse({ ok: true });
    return true;
  }
});

setInterval(pollMessages, 5000);
console.log("[AI Bridge Local] v" + VERSION);
