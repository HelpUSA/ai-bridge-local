const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..", "..");
const background = fs.readFileSync(path.join(root, "extension", "background.js"), "utf8");
const manifest = JSON.parse(fs.readFileSync(path.join(root, "extension", "manifest.json"), "utf8"));
const version = fs.readFileSync(path.join(root, "VERSION"), "utf8").trim();

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

assert(version === "0.5.63", "VERSION must be 0.5.63");
assert(manifest.version === "0.5.63", "manifest version must be 0.5.63");
assert(background.includes("AIBRIDGE_DIRECT_REINJECT_ON_MISSING_RECEIVER_062"), "missing direct reinject marker");
assert(background.includes("aiBridgeLooksLikeMissingReceiverResult"), "missing missing-receiver detector");
assert(background.includes("aiBridgeReinjectContentScriptForDirectDelivery"), "missing content script reinject helper");
assert(background.includes('files: ["content_script.js"]'), "missing content_script.js reinjection");
assert(background.includes("Receiving end does not exist"), "missing receiving-end error check");
assert(background.includes("Could not establish connection"), "missing connection error check");
assert(background.includes("reinjected_content_script"), "missing retry success marker");

const injectResultIndex = background.indexOf("[bg] Inject result:");
assert(injectResultIndex >= 0, "missing inject result log");
const reinjectIndex = background.indexOf("AIBRIDGE_DIRECT_REINJECT_ON_MISSING_RECEIVER_062");
assert(reinjectIndex >= 0 && reinjectIndex < injectResultIndex, "reinject wrapper should be installed before original inject log body");

console.log("OK smoke_direct_reinject_missing_receiver_062");
