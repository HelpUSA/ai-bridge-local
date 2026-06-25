const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "../..");
const backgroundPath = path.join(root, "extension", "background.js");
const background = fs.readFileSync(backgroundPath, "utf8");

assert(background.includes("AIBRIDGE_DIRECT_INTERCHAT_DELIVERY_START"), "missing direct interchat helper marker");
assert(background.includes("async function aiBridgeDirectDeliverCapturedEnvelope"), "missing direct delivery helper");
assert(background.includes("const route = globalThis.aiBridgeClassifyRouteSafe(validation.envelope);"), "captured envelope handler does not classify route");
assert(background.includes('if (route === "direct_interchat")'), "missing direct interchat branch");
assert(background.includes("aiBridgeDirectDeliverCapturedEnvelope(validation.envelope)"), "missing direct delivery call");
assert(background.includes('sendResponse({ ok: true, route: "direct_interchat", data: result })'), "missing direct success response");
assert(background.includes('sendResponse({ ok: true, route: "local_gateway" })'), "missing local gateway success response");
assert(background.includes("postCommand(validation.envelope)"), "missing local gateway postCommand fallback");

const capturedBlockStart = background.indexOf('if (message && message.type === "AI_BRIDGE_CAPTURED_ENVELOPE")');
const bridgeCommandStart = background.indexOf('if (message && message.type === "AI_BRIDGE_BRIDGE_COMMAND")');

assert(capturedBlockStart >= 0, "missing captured envelope block");
assert(bridgeCommandStart > capturedBlockStart, "bridge command block should follow captured envelope block");

const capturedBlock = background.slice(capturedBlockStart, bridgeCommandStart);
assert(capturedBlock.includes("aiBridgeClassifyRouteSafe"), "captured block must use classifier");
assert(capturedBlock.includes('route === "direct_interchat"'), "captured block must have direct route branch");
assert(capturedBlock.includes("postCommand(validation.envelope)"), "captured block must keep gateway fallback");

console.log("OK smoke_captured_envelope_route_integration");