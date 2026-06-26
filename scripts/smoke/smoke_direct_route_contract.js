const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "../..");
const backgroundPath = path.join(root, "extension", "background.js");
const contentPath = path.join(root, "extension", "content_script.js");
const routeClassifierPath = path.join(root, "extension", "route_classifier.js");

const background = fs.readFileSync(backgroundPath, "utf8");
const content = fs.readFileSync(contentPath, "utf8");
const routeClassifier = fs.readFileSync(routeClassifierPath, "utf8");

function mustInclude(haystack, needle, label) {
  assert(haystack.includes(needle), `${label}: missing ${needle}`);
}

mustInclude(routeClassifier, "function classifyRoute", "route classifier");
mustInclude(routeClassifier, "ROUTE_DIRECT_INTERCHAT", "route classifier");
mustInclude(routeClassifier, "ROUTE_LOCAL_GATEWAY", "route classifier");

mustInclude(background, "globalThis.aiBridgeClassifyRouteSafe", "background classifier load");
mustInclude(background, "AIBRIDGE_DIRECT_INTERCHAT_DELIVERY_START", "background direct helper");
mustInclude(background, "async function aiBridgeDirectDeliverCapturedEnvelope", "background direct helper");
mustInclude(background, "canonicalChatId(envelope && envelope.target_chat_id", "background target canonicalization");
mustInclude(background, "let tabId = registry[targetChatId];", "background target registry lookup");
mustInclude(background, "injectText(tabId, envelope)", "background direct injection");
mustInclude(background, "direct_interchat_delivery_started", "background direct telemetry start");
mustInclude(background, "direct_interchat_delivery_ok", "background direct telemetry ok");
mustInclude(background, "direct_interchat_delivery_failed", "background direct telemetry failed");

mustInclude(background, 'if (message && message.type === "AI_BRIDGE_CAPTURED_ENVELOPE")', "captured handler");
mustInclude(background, "const route = globalThis.aiBridgeClassifyRouteSafe(validation.envelope);", "captured handler");
mustInclude(background, 'if (route === "direct_interchat")', "captured direct branch");
mustInclude(background, "aiBridgeDirectDeliverCapturedEnvelope(validation.envelope)", "captured direct branch");
mustInclude(background, "postCommand(validation.envelope)", "captured gateway fallback");
mustInclude(background, 'sendResponse({ ok: true, route: "direct_interchat", data: result })', "captured direct response");
mustInclude(background, 'sendResponse({ ok: true, route: "local_gateway" })', "captured gateway response");

mustInclude(background, "async function injectText", "injectText contract");
mustInclude(background, 'type: "AI_BRIDGE_INJECT_TEXT"', "injectText contract");
mustInclude(background, 'action: "inject_text"', "injectText contract");
mustInclude(background, "text: action.message ||", "injectText contract");
mustInclude(background, "auto_submit: true", "injectText contract");
mustInclude(background, "chrome.tabs.sendMessage(tabId, message", "injectText contract");

mustInclude(content, "chrome.runtime.onMessage", "content receiver");
mustInclude(content, "AI_BRIDGE_INJECT_TEXT", "content receiver");
mustInclude(content, "directOkStatus", "content direct status");
mustInclude(content, "status=sent_direct", "content direct status");

const capturedStart = background.indexOf('if (message && message.type === "AI_BRIDGE_CAPTURED_ENVELOPE")');
const bridgeStart = background.indexOf('if (message && message.type === "AI_BRIDGE_BRIDGE_COMMAND")');
assert(capturedStart >= 0, "captured handler not found");
assert(bridgeStart > capturedStart, "bridge command handler should remain after captured handler");

const capturedBlock = background.slice(capturedStart, bridgeStart);
mustInclude(capturedBlock, "aiBridgeClassifyRouteSafe", "captured block");
mustInclude(capturedBlock, 'route === "direct_interchat"', "captured block");
mustInclude(capturedBlock, "postCommand(validation.envelope)", "captured block");

console.log("OK smoke_direct_route_contract");