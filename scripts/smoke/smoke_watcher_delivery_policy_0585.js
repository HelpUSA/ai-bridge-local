"use strict";

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.resolve(
  __dirname,
  "..",
  ".."
);

const content = fs.readFileSync(
  path.join(
    root,
    "extension",
    "content_script.js"
  ),
  "utf8"
);

const background = fs.readFileSync(
  path.join(
    root,
    "extension",
    "background.js"
  ),
  "utf8"
);

function managedBlock(source, start, end) {
  const begin = source.indexOf(start);
  const finish = source.indexOf(end);

  if (begin < 0 || finish < begin) {
    throw new Error(
      "managed block missing: " + start
    );
  }

  return source.slice(
    begin,
    finish + end.length
  );
}

const contentContext = {
  console,
  documentContainsSentMessage(value) {
    return value === "already visible";
  }
};

vm.createContext(contentContext);

vm.runInContext(
  managedBlock(
    content,
    "/* AI_BRIDGE_MANAGED:M11_CONTENT_DELIVERY_GUARD_0585:START */",
    "/* AI_BRIDGE_MANAGED:M11_CONTENT_DELIVERY_GUARD_0585:END */"
  ),
  contentContext
);

if (
  !contentContext.aiBridgeM11ComposerOwnsRequestedText(
    " same text ",
    "same text"
  )
) {
  throw new Error(
    "same delivery text must be owned"
  );
}

if (
  contentContext.aiBridgeM11ComposerOwnsRequestedText(
    "user draft",
    "bridge text"
  )
) {
  throw new Error(
    "unrelated user draft must not be owned"
  );
}

if (
  !contentContext.aiBridgeM11AlreadyVisible(
    "already visible"
  )
) {
  throw new Error(
    "visible delivery must short-circuit"
  );
}

const events = [];

const backgroundContext = {
  console,

  /* AI_BRIDGE_MANAGED:M11_RETRY_SMOKE_TARGET_STUB_0586:START */
  async aiBridgeM11ResolveExactTargetTab(
    targetChatId,
    tabId
  ) {
    return {
      ok: true,
      tab_id: tabId,
      target_chat_id: targetChatId,
      source: "delivery_policy_smoke_stub"
    };
  },
  /* AI_BRIDGE_MANAGED:M11_RETRY_SMOKE_TARGET_STUB_0586:END */
  async aiBridgeSleep() {},
  postTelemetryEvent(name, payload) {
    events.push({name, payload});
  },
  async injectText() {
    return {
      ok: false,
      reason: "not_configured"
    };
  }
};

vm.createContext(backgroundContext);

vm.runInContext(
  managedBlock(
    background,
    "/* AI_BRIDGE_MANAGED:M11_BACKGROUND_RETRY_0585:START */",
    "/* AI_BRIDGE_MANAGED:M11_BACKGROUND_RETRY_0585:END */"
  ),
  backgroundContext
);

async function main() {
  let calls = 0;

  backgroundContext.injectText =
    async function () {
      calls += 1;

      if (calls === 1) {
        return {
          ok: false,
          reason: "no_composer"
        };
      }

      return {
        ok: true,
        method: "test_success"
      };
    };

  let result =
    await backgroundContext.injectTextWithM11Retry(
      10,
      {
        command_id: "cmd_retry",
        target_chat_id: "target"
      }
    );

  if (
    !result.ok ||
    result.delivery_attempts !== 2 ||
    calls !== 2
  ) {
    throw new Error(
      "transient retry contract failed"
    );
  }

  calls = 0;

  backgroundContext.injectText =
    async function () {
      calls += 1;

      return {
        ok: false,
        reason:
          "composer_not_empty_before_inject"
      };
    };

  result =
    await backgroundContext.injectTextWithM11Retry(
      10,
      {
        command_id: "cmd_user_text",
        target_chat_id: "target"
      }
    );

  if (
    result.ok ||
    result.delivery_attempts !== 1 ||
    calls !== 1
  ) {
    throw new Error(
      "user-content conflict must not retry"
    );
  }

  calls = 0;

  backgroundContext.injectText =
    async function () {
      calls += 1;

      return {
        ok: false,
        reason:
          "submit_not_confirmed_composer_still_has_text"
      };
    };

  result =
    await backgroundContext.injectTextWithM11Retry(
      10,
      {
        command_id: "cmd_bounded",
        target_chat_id: "target"
      }
    );

  if (
    result.ok ||
    result.delivery_attempts !== 3 ||
    calls !== 3
  ) {
    throw new Error(
      "bounded retry contract failed"
    );
  }

  if (events.length !== 3) {
    throw new Error(
      "unexpected retry telemetry count="
      + events.length
    );
  }

  console.log(
    "SMOKE_WATCHER_DELIVERY_POLICY_0585_OK"
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
