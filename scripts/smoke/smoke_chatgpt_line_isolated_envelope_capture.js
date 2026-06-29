const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..", "..");
const contentPath = path.join(root, "extension", "content_script.js");
const content = fs.readFileSync(contentPath, "utf8");

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

assert(content.includes("0.5.65"), "content script version must be 0.5.65");

const at = "@@";
const start = at + "AI_BRIDGE_LOCAL_START" + at;
const begin = at + "AI_BRIDGE_LOCAL_BEGIN" + at;
const finish = at + "AI_BRIDGE_LOCAL_END" + at;
const schema = "ai_bridge_local.envelope";

const startRegex = new RegExp(
  "(?:^|\\n)[ \\t]*" + escapeRegExp(start) + "[ \\t]*\\r?\\n([\\s\\S]*?)\\r?\\n[ \\t]*" + escapeRegExp(finish) + "[ \\t]*(?=\\r?\\n|$)",
  "g"
);
const beginRegex = new RegExp(
  "(?:^|\\n)[ \\t]*" + escapeRegExp(begin) + "[ \\t]*\\r?\\n([\\s\\S]*?)\\r?\\n[ \\t]*" + escapeRegExp(finish) + "[ \\t]*(?=\\r?\\n|$)",
  "g"
);

const inlineMention = "Texto explicativo menciona " + start + " e " + finish + " com " + schema + " na mesma linha.";
const badInlineBlock = "prefix " + start + "\n" + JSON.stringify({ schema, command_id: "bad" }) + "\n" + finish;
const isolatedBlock = start + "\n" + JSON.stringify({ schema, command_id: "ok" }) + "\n" + finish + "\n";
const isolatedBeginBlock = begin + "\n" + JSON.stringify({ schema, command_id: "ok2" }) + "\n" + finish + "\n";

assert(!startRegex.test(inlineMention), "must ignore inline marker mentions");
startRegex.lastIndex = 0;
assert(!startRegex.test(badInlineBlock), "must ignore marker not isolated at line start");
startRegex.lastIndex = 0;

const match = startRegex.exec(isolatedBlock);
assert(match && match[1].includes('"command_id":"ok"'), "must capture isolated START/END block");

const beginMatch = beginRegex.exec(isolatedBeginBlock);
assert(beginMatch && beginMatch[1].includes('"command_id":"ok2"'), "must capture isolated BEGIN/END block");

console.log("OK smoke_chatgpt_line_isolated_envelope_capture");
