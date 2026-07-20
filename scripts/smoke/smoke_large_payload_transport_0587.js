"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const { TextEncoder } = require("util");

const root = path.resolve(__dirname, "..", "..");
const backgroundPath = path.join(
  root,
  "extension",
  "background.js"
);

const source = fs.readFileSync(
  backgroundPath,
  "utf8"
);

const startMarker =
  "// AI_BRIDGE_MANAGED:" +
  "M12_LARGE_PAYLOAD_TRANSPORT_0587:START";

const endMarker =
  "// AI_BRIDGE_MANAGED:" +
  "M12_LARGE_PAYLOAD_TRANSPORT_0587:END";

const start = source.indexOf(startMarker);
const end = source.indexOf(endMarker);

assert.ok(start >= 0, "M12 start marker missing");
assert.ok(end > start, "M12 end marker missing");

const managedSource = source.slice(
  start,
  end + endMarker.length
);

const inlineCalls = [];
const fetchCalls = [];

const context = vm.createContext({
  TextEncoder,
  console,
  fetch: async (url, options) => {
    fetchCalls.push({
      url,
      options
    });

    return {
      ok: true,
      status: 201,
      json: async () => ({
        ok: true,
        payload_ref:
          "sha256:" + "a".repeat(64)
      })
    };
  }
});

const prefix = `
async function aiBridgePostCommandInline0586(cmd) {
  globalThis.__inlineCalls.push(cmd);
  return {
    ok: true,
    command: cmd
  };
}
globalThis.__inlineCalls = [];
`;

vm.runInContext(
  prefix + managedSource,
  context
);

async function run() {
  await vm.runInContext(
    `postCommand({
      id: "small-command",
      args: { value: "small" }
    })`,
    context
  );

  assert.strictEqual(
    fetchCalls.length,
    0,
    "small command must remain inline"
  );

  assert.strictEqual(
    context.__inlineCalls.length,
    1
  );

  assert.deepStrictEqual(
    JSON.parse(
      JSON.stringify(
        context.__inlineCalls[0].args
      )
    ),
    { value: "small" }
  );

  await vm.runInContext(
    `postCommand({
      id: "large-command",
      args: {
        script_text: "x".repeat(40000)
      }
    })`,
    context
  );

  assert.strictEqual(
    fetchCalls.length,
    1,
    "large command must upload one payload"
  );

  assert.ok(
    String(fetchCalls[0].url).endsWith(
      "/v1/payloads"
    )
  );

  const uploadBody =
    JSON.parse(fetchCalls[0].options.body);

  assert.strictEqual(
    uploadBody.encoding,
    "utf-8"
  );

  const uploadedArgs =
    JSON.parse(uploadBody.content);

  assert.strictEqual(
    uploadedArgs.script_text.length,
    40000
  );

  assert.strictEqual(
    context.__inlineCalls.length,
    2
  );

  const largeSubmitted =
    context.__inlineCalls[1];

  assert.deepStrictEqual(
    JSON.parse(JSON.stringify(largeSubmitted.args)),
    {}
  );

  assert.strictEqual(
    largeSubmitted.payload_ref,
    "sha256:" + "a".repeat(64)
  );

  await vm.runInContext(
    `postCommand({
      id: "existing-reference",
      args: {},
      payload_ref: "sha256:${"b".repeat(64)}"
    })`,
    context
  );

  assert.strictEqual(
    fetchCalls.length,
    1,
    "existing payload_ref must not be uploaded again"
  );

  assert.strictEqual(
    context.__inlineCalls[2].payload_ref,
    "sha256:" + "b".repeat(64)
  );

  console.log(
    "M12_LARGE_PAYLOAD_TRANSPORT_SMOKE: PASS"
  );
}

run().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
