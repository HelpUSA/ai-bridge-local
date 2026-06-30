const fs = require("fs");
const path = require("path");
const assert = require("assert");

const root = path.resolve(__dirname, "..", "..");
const background = fs.readFileSync(path.join(root, "extension", "background.js"), "utf8");
const version = fs.readFileSync(path.join(root, "VERSION"), "utf8").trim();

assert.strictEqual(version, "0.5.66");
assert(background.includes('const VERSION = "0.5.66";'), "background version not synced");

const directStart = background.indexOf("async function deliverInterChatDirect(cmd)");
const fallbackStart = background.indexOf("function shouldFallbackDirectFailureToGateway", directStart);
assert(directStart >= 0, "deliverInterChatDirect missing");
assert(fallbackStart > directStart, "fallback function marker missing");

const directFn = background.slice(directStart, fallbackStart);
assert(directFn.includes("injectText(tabId, directAction)"), "same-profile direct must inject directAction");
assert(!directFn.includes("injectText(tabId, envelope)"), "same-profile direct must not reference undefined envelope");

const capturedStart = background.indexOf("async function aiBridgeDirectDeliverCapturedEnvelope(envelope)");
const listenerStart = background.indexOf("chrome.runtime.onMessage.addListener", capturedStart);
assert(capturedStart >= 0, "captured envelope helper missing");
assert(listenerStart > capturedStart, "listener marker missing");

const capturedFn = background.slice(capturedStart, listenerStart);
assert(capturedFn.includes("injectText(tabId, envelope)"), "captured helper must inject envelope");

assert(background.includes('action === "run-command"'), "fallback must block run-command");
assert(background.includes('deliveryKind === "local_capability"'), "fallback must block local_capability");

console.log("OK smoke_same_profile_direct_no_undefined_envelope_066");
