// AI Bridge Local v0.3.8
const VERSION = "0.3.8";
const GATEWAY = "http://127.0.0.1:8766";
const registry = {};

async function postCommand(cmd) {
  console.log("[bg] Sending:", cmd.command_id);
  const res = await fetch(GATEWAY + "/bridge/commands", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(cmd)
  });
  return await res.json();
}

function canonicalChatId(value) {
  const raw = String(value || "").trim().replace(/^(chat|deepseek):/i, "");
  const m = raw.match(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);
  return m ? m[0].toLowerCase() : raw;
}

async function injectText(tabId, text, cmdId) {
  try {
    const response = await chrome.tabs.sendMessage(tabId, {
      type: "AI_BRIDGE_INJECT_TEXT",
      action: { action: "inject_text", text: text, auto_submit: true, action_id: cmdId }
    });
    console.log("[bg] Inject result:", JSON.stringify(response));
    return response;
  } catch (e) {
    console.log("[bg] Inject error:", e.message);
    return { ok: false, error: e.message };
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
        console.log("[bg] Injecting to:", chatId);
        const result = await injectText(tabId, data.action.message, data.action.command_id);
        if (result && result.ok) {
          await fetch(GATEWAY + "/bridge/acks", {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ command_id: data.action.command_id, status: "acked" })
          });
          console.log("[bg] ACKed:", data.action.command_id);
        }
      }
    } catch (e) {
      console.log("[bg] Poll error:", e.message);
    }
  }
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message && message.type === "AI_BRIDGE_BRIDGE_COMMAND") {
    console.log("[bg] Received:", message.command?.command_id);
    postCommand(message.command || message).then(r => sendResponse({ok: true, data: r}));
    return true;
  }
  if (message && message.type === "AI_BRIDGE_REGISTER_CHAT") {
    const cid = canonicalChatId(message.chat_id);
    if (cid && sender.tab) {
      registry[cid] = sender.tab.id;
      console.log("[bg] Registered:", cid, "tab:", sender.tab.id);
    }
    sendResponse({ok: true});
    return true;
  }
});

setInterval(pollMessages, 5000);
console.log("[AI Bridge Local] v" + VERSION);
