const fs = require("fs");
const path = require("path");
const assert = require("assert");

const root = path.resolve(__dirname, "..", "..");
const background = fs.readFileSync(path.join(root, "extension", "background.js"), "utf8");
const version = fs.readFileSync(path.join(root, "VERSION"), "utf8").trim();

assert.strictEqual(version, "0.5.66");
assert(background.includes('const VERSION = "0.5.66";'), "background version not synced");
assert(background.includes("AIBRIDGE_DIRECT_CROSS_PROFILE_GATEWAY_FALLBACK_065_START"), "fallback marker missing");
assert(background.includes("AIBRIDGE_DIRECT_CROSS_PROFILE_GATEWAY_FALLBACK_065_CAPTURED_START"), "captured fallback marker missing");
assert(background.includes("const DIRECT_INTERCHAT_ALLOW_GATEWAY_FALLBACK = true;"), "gateway fallback constant must be enabled");

assert(background.includes('action !== "send-chat-message"'), "fallback must be send-chat-message gated");
assert(background.includes('deliveryKind !== "inter_agent_message"'), "fallback must be inter_agent_message gated");
assert(background.includes('deliveryKind === "local_capability"'), "fallback must block local_capability");
assert(background.includes('action === "run-command"'), "fallback must block run-command");
assert(background.includes("target_chat_not_registered"), "fallback must include unregistered target error");
assert(background.includes("target_tab_not_open"), "fallback must include target tab not open error");
assert(background.includes("postCommand(cmd)"), "routeBridgeCommand gateway fallback must postCommand");
assert(background.includes("pollMessagesSoon(sourceLabel + \"_directFallback\")"), "routeBridgeCommand fallback must poll soon");
assert(background.includes("postCommand(envelope)"), "captured envelope fallback must postCommand");
assert(background.includes('route: "local_gateway_cross_profile"'), "captured fallback route must be explicit");

console.log("OK smoke_direct_cross_profile_gateway_fallback_065");
