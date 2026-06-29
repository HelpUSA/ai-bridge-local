const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "../..");
const expected = "0.5.65";

const versionPath = path.join(root, "VERSION");
const manifestPath = path.join(root, "extension", "manifest.json");

const version = fs.readFileSync(versionPath, "utf8").trim();
const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));

assert.strictEqual(version, expected, `VERSION expected ${expected}, got ${version}`);
assert.strictEqual(manifest.version, expected, `manifest.version expected ${expected}, got ${manifest.version}`);
assert(
  String(manifest.name || "").includes(expected),
  `manifest.name should include ${expected}, got ${manifest.name}`
);

const extensionDir = path.join(root, "extension");
const oldVersions = ["0.5.52", "0.5.58"];

function walk(dir) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      out.push(...walk(full));
    } else {
      out.push(full);
    }
  }
  return out;
}

for (const file of walk(extensionDir)) {
  if (!/\.(js|json|html|css)$/.test(file)) continue;
  const text = fs.readFileSync(file, "utf8");
  for (const oldVersion of oldVersions) {
    assert(
      !text.includes(oldVersion),
      `${path.relative(root, file)} still contains old version ${oldVersion}`
    );
  }
}

console.log("OK smoke_extension_version_sync");