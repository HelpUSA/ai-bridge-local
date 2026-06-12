
from pathlib import Path

p = Path("extension/content_script.js")
text = p.read_text(encoding="utf-8-sig")

if "function extractSimpleBridgeCommands(text)" not in text:
    marker = "  function extract(text) {\n"
    insert = """  function extractSimpleBridgeCommands(text) {
    const cmds = [];
    const source = canonicalUuid(getChatId()) || getChatId() || "unknown";
    const blockRegex = /(?:^|\\n)BRIDGE_SEND_CHAT_MESSAGE[ \\t]*\\r?\\n([\\s\\S]*?)(?=\\n(?:BRIDGE_SEND_CHAT_MESSAGE|@@AI_BRIDGE_LOCAL_START@@)|$)/gi;
    let m;

    while ((m = blockRegex.exec(String(text || ""))) !== null) {
      const raw = String(m[1] || "").trim();
      const fields = {};
      for (const line of raw.split(/\\r?\\n/)) {
        const parts = String(line || "").split("=");
        if (parts.length < 2) continue;
        const key = parts.shift().trim().toLowerCase();
        const value = parts.join("=").trim();
        if (key) fields[key] = value;
      }

      const target = canonicalUuid(fields.target_chat_id || fields.target || fields.to);
      const message = String(fields.message || fields.text || "").trim();

      if (!target || !message) {
        reportEnvelopeError("simple_bridge_missing_fields", "BRIDGE_SEND_CHAT_MESSAGE precisa de target_chat_id e message", raw);
        continue;
      }

      const commandId = fields.command_id || ("simple_bridge_send_" + safeIdPart(target).slice(0, 8) + "_" + hashString(target + "|" + message).slice(0, 12));
      cmds.push(normalizeLocalCommand({
        schema: LOCAL_SCHEMA,
        schema_version: LOCAL_SCHEMA_VERSION,
        command_id: commandId,
        action: "send-chat-message",
        source_chat_id: source,
        target_chat_id: target,
        delivery_kind: "inter_agent_message",
        conversation_id: fields.conversation_id || ("simple_bridge_" + safeIdPart(source).slice(0, 8) + "_to_" + safeIdPart(target).slice(0, 8)),
        from_agent: fields.from_agent || ("AI Bridge Simple Mode " + VERSION),
        message
      }));
    }

    const oneLineRegex = /(?:^|\\n)BRIDGE_REPLY_TO[ \\t]*=[ \\t]*([0-9a-fA-F-]{36})[ \\t]*\\r?\\nBRIDGE_MESSAGE[ \\t]*=[ \\t]*([^\\r\\n]{1,2000})/g;
    while ((m = oneLineRegex.exec(String(text || ""))) !== null) {
      const target = canonicalUuid(m[1]);
      const message = String(m[2] || "").trim();
      if (!target || !message) continue;
      const commandId = "simple_bridge_reply_" + safeIdPart(target).slice(0, 8) + "_" + hashString(target + "|" + message).slice(0, 12);
      cmds.push(normalizeLocalCommand({
        schema: LOCAL_SCHEMA,
        schema_version: LOCAL_SCHEMA_VERSION,
        command_id: commandId,
        action: "send-chat-message",
        source_chat_id: source,
        target_chat_id: target,
        delivery_kind: "inter_agent_message",
        conversation_id: "simple_bridge_reply",
        from_agent: "AI Bridge Simple Mode " + VERSION,
        message
      }));
    }

    return cmds;
  }

"""
    if marker not in text:
        raise SystemExit("EXTRACT_MARKER_NOT_FOUND")
    text = text.replace(marker, insert + marker, 1)

old = "  function extract(text) {\n    const cmds = [];\n"
new = "  function extract(text) {\n    const cmds = extractSimpleBridgeCommands(text);\n"
if old in text:
    text = text.replace(old, new, 1)
elif "const cmds = extractSimpleBridgeCommands(text);" not in text:
    raise SystemExit("EXTRACT_CMDS_MARKER_NOT_FOUND")

text = text.replace('const VERSION = "0.4.36";', 'const VERSION = "0.4.37";')
p.write_text(text, encoding="utf-8")
print("PATCH_SIMPLE_BRIDGE_MODE_OK")
