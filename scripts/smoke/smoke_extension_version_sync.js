const fs = require("fs");
const path = require("path");
const assert = require("assert");

const root = path.resolve(__dirname, "..", "..");

const versionPath = path.join(root, "VERSION");
const manifestPath = path.join(root, "extension", "manifest.json");
const backgroundPath = path.join(root, "extension", "background.js");

assert.ok(fs.existsSync(versionPath), "VERSION file missing");
assert.ok(fs.existsSync(manifestPath), "extension manifest missing");
assert.ok(fs.existsSync(backgroundPath), "extension background missing");

const version = fs.readFileSync(versionPath, "utf8").trim();
const manifest = JSON.parse(
  fs.readFileSync(manifestPath, "utf8")
);
const background = fs.readFileSync(backgroundPath, "utf8");

assert.match(
  version,
  /^\d+\.\d+\.\d+$/,
  `VERSION must use semantic numeric format, got ${version}`
);

assert.strictEqual(
  manifest.version,
  version,
  `manifest.version expected ${version}, got ${manifest.version}`
);

const backgroundVersionMatch = background.match(
  /const VERSION = "(\d+\.\d+\.\d+)";/
);

assert.ok(
  backgroundVersionMatch,
  "background VERSION constant missing"
);

assert.strictEqual(
  backgroundVersionMatch[1],
  version,
  `background VERSION expected ${version}, got ${backgroundVersionMatch[1]}`
);

assert.ok(
  manifest.background &&
  manifest.background.service_worker === "background.js",
  "manifest background service worker must be background.js"
);

console.log("OK smoke_extension_version_sync");
