const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..", "..");
const contentPath = path.join(root, "extension", "content_script.js");
const manifestPath = path.join(root, "extension", "manifest.json");
const versionPath = path.join(root, "VERSION");

const content = fs.readFileSync(contentPath, "utf8");
const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
const version = fs.readFileSync(versionPath, "utf8").trim();

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

assert(version === "0.5.61", "VERSION must be 0.5.61");
assert(manifest.version === "0.5.61", "manifest version must be 0.5.61");
assert(content.includes("AIBRIDGE_INLINE_MARKER_PARSE_GUARD_061"), "missing inline marker parse guard");

const guardLines = content
  .split(/\r?\n/)
  .filter((line) => line.includes("AIBRIDGE_INLINE_MARKER_PARSE_GUARD_061"));

assert(guardLines.length >= 1, "expected at least one inline marker guard line");
assert(
  guardLines.some((line) => line.includes("raw") || line.includes("block.raw")),
  "guard should protect raw envelope parsing"
);
assert(
  guardLines.some((line) => line.includes("continue") || line.includes("return")),
  "guard should skip or reject non-json blocks"
);

const at = "@@";
const start = at + "AI_BRIDGE_LOCAL_START" + at;
const finish = at + "AI_BRIDGE_LOCAL_END" + at;
const schema = "ai_bridge_local.envelope";

const lineRegex = new RegExp(
  "(?:^|\\n)[ \\t]*" + escapeRegExp(start) + "[ \\t]*\\r?\\n([\\s\\S]*?)\\r?\\n[ \\t]*" + escapeRegExp(finish) + "[ \\t]*(?=\\r?\\n|$)",
  "g"
);

const inlineMention = "Teste mencionando " + start + " e " + finish + " em frase explicativa com " + schema + ".";
const isolatedBlock = start + "\n" + JSON.stringify({ schema, command_id: "ok" }) + "\n" + finish + "\n";

assert(!lineRegex.test(inlineMention), "line-isolated regex must ignore inline marker mentions");
lineRegex.lastIndex = 0;

const match = lineRegex.exec(isolatedBlock);
assert(match && match[1].includes('"command_id":"ok"'), "line-isolated regex must capture isolated envelope blocks");

console.log("OK smoke_chatgpt_inline_marker_parse_guard_061");
