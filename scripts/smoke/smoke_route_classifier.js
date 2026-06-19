const assert = require("assert");

const {
  ROUTE_DIRECT_INTERCHAT,
  ROUTE_LOCAL_GATEWAY,
  classifyRoute
} = require("../../extension/route_classifier.js");

const cases = [
  {
    name: "explicit direct transport",
    envelope: { transport: "direct_interchat", action: "send-chat-message" },
    expected: ROUTE_DIRECT_INTERCHAT
  },
  {
    name: "explicit local gateway transport",
    envelope: { transport: "local_gateway", action: "send-chat-message" },
    expected: ROUTE_LOCAL_GATEWAY
  },
  {
    name: "force gateway wins",
    envelope: { force_gateway: true, action: "send-chat-message" },
    expected: ROUTE_LOCAL_GATEWAY
  },
  {
    name: "send chat message defaults direct",
    envelope: { action: "send-chat-message" },
    expected: ROUTE_DIRECT_INTERCHAT
  },
  {
    name: "run command goes gateway",
    envelope: { action: "run-command" },
    expected: ROUTE_LOCAL_GATEWAY
  },
  {
    name: "smoke goes gateway",
    envelope: { action: "smoke" },
    expected: ROUTE_LOCAL_GATEWAY
  },
  {
    name: "patch goes gateway",
    envelope: { action: "patch" },
    expected: ROUTE_LOCAL_GATEWAY
  },
  {
    name: "inspect goes gateway",
    envelope: { action: "inspect" },
    expected: ROUTE_LOCAL_GATEWAY
  },
  {
    name: "payload force gateway wins",
    envelope: { action: "send-chat-message", payload: { force_gateway: "true" } },
    expected: ROUTE_LOCAL_GATEWAY
  },
  {
    name: "payload transport direct",
    envelope: { payload: { transport: "direct_interchat", action: "send-chat-message" } },
    expected: ROUTE_DIRECT_INTERCHAT
  },
  {
    name: "inter agent delivery kind defaults direct",
    envelope: { delivery_kind: "inter_agent_message" },
    expected: ROUTE_DIRECT_INTERCHAT
  },
  {
    name: "unknown defaults gateway safe",
    envelope: { action: "unknown" },
    expected: ROUTE_LOCAL_GATEWAY
  }
];

for (const item of cases) {
  const actual = classifyRoute(item.envelope);
  assert.strictEqual(actual, item.expected, `${item.name}: expected ${item.expected}, got ${actual}`);
}

console.log("OK smoke_route_classifier");
