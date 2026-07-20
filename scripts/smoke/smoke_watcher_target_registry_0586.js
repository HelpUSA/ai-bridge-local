"use strict";

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.resolve(
  __dirname,
  "..",
  ".."
);

const source = fs.readFileSync(
  path.join(
    root,
    "extension",
    "background.js"
  ),
  "utf8"
);

function block(text, start, end) {
  const begin = text.indexOf(start);
  const finish = text.indexOf(end);

  if (
    begin < 0 ||
    finish < begin
  ) {
    throw new Error(
      "managed block missing: "
      + start
    );
  }

  return text.slice(
    begin,
    finish + end.length
  );
}

const state = {
  tabs: [],
  listeners: [],
  events: []
};

const chrome = {
  runtime: {
    lastError: null,
    onMessage: {
      addListener(listener) {
        state.listeners.push(
          listener
        );
      }
    }
  },

  tabs: {
    get(tabId, callback) {
      callback(
        state.tabs.find(
          (tab) => tab.id === tabId
        ) || null
      );
    },

    query(queryInfo, callback) {
      void queryInfo;
      callback(state.tabs.slice());
    }
  }
};

const context = {
  chrome,
  console,
  URL,
  Map,
  Date,
  postTelemetryEvent(
    name,
    payload
  ) {
    state.events.push({
      name,
      payload
    });
  }
};

vm.createContext(context);

vm.runInContext(
  block(
    source,
    "/* AI_BRIDGE_MANAGED:M11_TARGET_REGISTRY_0586:START */",
    "/* AI_BRIDGE_MANAGED:M11_TARGET_REGISTRY_0586:END */"
  ),
  context
);

const target =
  "6a563525-4740-83e9-a8a1-212c8e5baf1e";

const other =
  "6a562cee-5420-83e9-8a87-8113ee0d14cf";

async function main() {
  if (
    context.aiBridgeM11ExtractChatIdFromUrl(
      "https://chatgpt.com/g/project/c/"
      + target
    ) !== target
  ) {
    throw new Error(
      "project URL parsing failed"
    );
  }

  state.tabs = [
    {
      id: 10,
      url:
        "https://chatgpt.com/c/"
        + other
    },
    {
      id: 11,
      url:
        "https://chatgpt.com/g/project/c/"
        + target
    }
  ];

  let result =
    await context
      .aiBridgeM11ResolveExactTargetTab(
        target,
        10
      );

  if (
    !result.ok ||
    result.tab_id !== 11
  ) {
    throw new Error(
      "exact target resolution failed"
    );
  }

  state.tabs.push({
    id: 12,
    url:
      "https://chatgpt.com/c/"
      + target
  });

  result =
    await context
      .aiBridgeM11ResolveExactTargetTab(
        target,
        10
      );

  if (
    result.ok ||
    result.reason
      !== "target_chat_tab_ambiguous"
  ) {
    throw new Error(
      "ambiguous target was not blocked"
    );
  }

  state.tabs = [
    {
      id: 20,
      url:
        "https://chatgpt.com/g/project/c/"
        + target
    }
  ];

  let heartbeatResult = null;

  state.listeners[0](
    {
      type:
        "AI_BRIDGE_CHAT_HEARTBEAT",
      chat_id: target,
      url:
        "https://chatgpt.com/g/project/c/"
        + target,
      title: "Project",
      visible: true,
      reason: "test",
      observed_at:
        new Date().toISOString()
    },
    {
      tab: state.tabs[0]
    },
    (value) => {
      heartbeatResult = value;
    }
  );

  if (
    !heartbeatResult ||
    !heartbeatResult.ok ||
    heartbeatResult.tab_id !== 20
  ) {
    throw new Error(
      "heartbeat registration failed"
    );
  }

  result =
    await context
      .aiBridgeM11ResolveExactTargetTab(
        target,
        20
      );

  if (
    !result.ok ||
    result.tab_id !== 20
  ) {
    throw new Error(
      "registered resolution failed"
    );
  }

  if (
    state.events.length !== 1 ||
    state.events[0].name
      !== "chat_registration_heartbeat"
  ) {
    throw new Error(
      "heartbeat telemetry failed"
    );
  }

  console.log(
    "SMOKE_WATCHER_TARGET_REGISTRY_0586_OK"
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
