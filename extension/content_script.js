// AI Bridge Local v0.4.17 - Visual dedupe and temp script workflow
(() => {
  const VERSION = "0.4.31";
  const LOCAL_SCHEMA = "ai_bridge_local.envelope";
  const LOCAL_SCHEMA_VERSION = 1;
  const reportedEnvelopeErrors = new Set();

  console.log("[Local v" + VERSION + "] Active");

  function showNotice(title, detail = "", kind = "info") {
    // No floating visual toast. Keep diagnostics in console only.
    try {
      const prefix = "[AI Bridge Local " + VERSION + "][" + kind + "]";
      if (detail) {
        console.log(prefix, title, detail);
      } else {
        console.log(prefix, title);
      }
    } catch (e) {
      console.log("[Local] notice error:", e.message);
    }
  }

  function getChatId() {
    const href = location.href;
    const patterns = [
      /chat\.deepseek\.com\/a\/chat\/s\/([0-9a-fA-F-]{36})/i,
      /chat\.deepseek\.com\/.*\/s\/([0-9a-fA-F-]{36})/i,
      /chatgpt\.com\/c\/([0-9a-fA-F-]{36})/i,
      /\/c\/([0-9a-fA-F-]{36})/i,
      /\/chat\/([0-9a-fA-F-]{36})/i
    ];

    for (const pattern of patterns) {
      const match = href.match(pattern);
      if (match && match[1]) return match[1].toLowerCase();
    }

    return "unknown";
  }

  function registerChatWithBridge() {
    const chat_id = getChatId();
    console.log("[Local v" + VERSION + "] Register chat:", chat_id, location.href);
    chrome.runtime.sendMessage({
      type: "AI_BRIDGE_REGISTER_CHAT",
      chat_id
    });
  }

  registerChatWithBridge();
  setInterval(registerChatWithBridge, 5000);

  function findComposer() {
    const selectors = [
      '#prompt-textarea',
      '[data-testid="composer"] [contenteditable="true"]',
      '[contenteditable="true"][role="textbox"]',
      '[contenteditable="true"]',
      'textarea',
      '[role="textbox"]'
    ];

    for (const selector of selectors) {
      const el = document.querySelector(selector);
      if (el) return el;
    }

    return null;
  }

  function isVisible(el) {
    if (!el) return false;
    const style = window.getComputedStyle(el);
    if (!style || style.display === "none" || style.visibility === "hidden" || Number(style.opacity) === 0) return false;
    const rect = el.getBoundingClientRect();
    return rect.width > 4 && rect.height > 4;
  }

  function isDisabled(el) {
    if (!el) return true;
    if (el.disabled) return true;
    const aria = String(el.getAttribute("aria-disabled") || "").toLowerCase();
    if (aria === "true") return true;
    const cls = String(el.className || "").toLowerCase();
    if (cls.includes("disabled")) return true;
    return false;
  }

  function clickElement(el) {
    if (!el) return false;
    try {
      el.focus?.();
      for (const type of ["pointerdown", "mousedown", "mouseup", "click"]) {
        el.dispatchEvent(new MouseEvent(type, {
          bubbles: true,
          cancelable: true,
          view: window
        }));
      }
      el.click?.();
      return true;
    } catch (e) {
      console.warn("[Local v" + VERSION + "] clickElement failed:", e.message);
      return false;
    }
  }

  function candidateText(el) {
    return [
      el.innerText || "",
      el.textContent || "",
      el.getAttribute("aria-label") || "",
      el.getAttribute("title") || "",
      el.getAttribute("data-testid") || "",
      el.getAttribute("class") || ""
    ].join(" ").toLowerCase();
  }

  function scoreSendCandidate(el, composer) {
    if (!isVisible(el) || isDisabled(el)) return -999;

    const txt = candidateText(el);
    let score = 0;

    if (/send|enviar|submit|å‘é€|send-button|composer-submit|paper|plane|arrow|up/.test(txt)) score += 10;
    if (/stop|cancel|attach|upload|file|mic|microphone|voice|image|search|tool/.test(txt)) score -= 8;

    const r = el.getBoundingClientRect();
    const cr = composer?.getBoundingClientRect?.();

    if (cr) {
      const nearY = Math.abs((r.top + r.bottom) / 2 - (cr.top + cr.bottom) / 2);
      const nearX = r.left >= cr.left - 80 && r.left <= cr.right + 160;
      if (nearY < 140) score += 4;
      if (nearX) score += 4;
      if (r.left > cr.left + cr.width * 0.55) score += 3;
    }

    if (r.width <= 80 && r.height <= 80) score += 2;

    return score;
  }

  function findSendButton(composer = null) {
    const selectors = [
      'button[data-testid="send-button"]',
      'button[data-testid="composer-submit-button"]',
      'button[aria-label*="Send" i]',
      'button[aria-label*="Enviar" i]',
      'button[title*="Send" i]',
      'button[title*="Enviar" i]',
      'button[type="submit"]',
      '[role="button"][aria-label*="Send" i]',
      '[role="button"][aria-label*="Enviar" i]',
      '[class*="send" i]',
      '[class*="submit" i]'
    ];

    for (const selector of selectors) {
      for (const el of Array.from(document.querySelectorAll(selector))) {
        if (isVisible(el) && !isDisabled(el)) return el;
      }
    }

    const generic = Array.from(document.querySelectorAll('button, [role="button"], [aria-label], [title]'))
      .map(el => ({ el, score: scoreSendCandidate(el, composer) }))
      .filter(x => x.score > 0)
      .sort((a, b) => b.score - a.score);

    if (generic.length) {
      console.log("[Local v" + VERSION + "] Generic send candidate:", {
        score: generic[0].score,
        text: candidateText(generic[0].el).slice(0, 160)
      });
      return generic[0].el;
    }

    return null;
  }

  function getComposerText(el) {
    if (!el) return "";
    if (el.tagName === "TEXTAREA" || el.tagName === "INPUT") return el.value || "";
    return el.innerText || el.textContent || "";
  }

  function setText(el, text) {
    el.focus();

    if (el.tagName === "TEXTAREA" || el.tagName === "INPUT") {
      const proto = el.tagName === "TEXTAREA" ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
      const nativeSetter = Object.getOwnPropertyDescriptor(proto, "value").set;
      nativeSetter.call(el, text);
    } else {
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(el);
      selection.removeAllRanges();
      selection.addRange(range);

      const inserted = document.execCommand && document.execCommand("insertText", false, text);
      if (!inserted || !getComposerText(el).includes(text.slice(0, Math.min(20, text.length)))) {
        el.textContent = text;
      }
    }

    el.dispatchEvent(new InputEvent("input", {bubbles: true, cancelable: true, inputType: "insertText", data: text}));
    el.dispatchEvent(new Event("change", {bubbles: true}));
    el.dispatchEvent(new KeyboardEvent("keyup", {key: " ", code: "Space", bubbles: true}));
  }

  function pressEnter(el) {
    el.focus();
    for (const type of ["keydown", "keypress", "keyup"]) {
      el.dispatchEvent(new KeyboardEvent(type, {
        key: "Enter",
        code: "Enter",
        keyCode: 13,
        which: 13,
        bubbles: true,
        cancelable: true
      }));
    }
  }

  function documentContainsSentMessage(text) {
    const needle = String(text || "").trim();
    if (!needle) return false;

    const shortNeedle = needle.slice(0, Math.min(120, needle.length));
    const candidates = Array.from(document.querySelectorAll(
      '[data-message-author-role], article, .markdown, [role="article"]'
    ));

    return candidates.some(el => {
      const body = (el.innerText || el.textContent || "").trim();
      return body.includes(shortNeedle);
    });
  }

  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message && message.type === "AI_BRIDGE_INJECT_TEXT") {
      const actionId = message.action?.action_id || message.action?.command_id || "unknown";
      const text = message.action?.text || message.action?.message || message.text || "";

      showNotice("Mensagem recebida para injeÃ§Ã£o", "command_id=" + actionId, "info");

      if (!text) {
        showNotice("Falha: texto vazio", "command_id=" + actionId, "error");
        sendResponse({ok: false, reason: "empty_text"});
        return false;
      }

      const composer = findComposer();
      if (!composer) {
        showNotice("Falha: composer nÃ£o encontrado", "command_id=" + actionId, "error");
        sendResponse({ok: false, reason: "no_composer"});
        return false;
      }

 const beforeText = getComposerText(composer).trim();
 if (beforeText) {
 const ownedPreflightText = beforeText.includes("AI_BRIDGE_LOCAL_START") || beforeText.includes("ai_bridge_local.envelope") || beforeText.includes("[AI_LOCAL]") || beforeText.includes("[AI_LOCAL_ERRO]");
 if (ownedPreflightText) {
 showNotice("Limpando composer travado da extensao", "command_id=" + actionId, "warn");
 setText(composer, String());
 } else {
 showNotice("Falha: composer nao vazio antes da injecao", "command_id=" + actionId, "error");
 sendResponse({
 ok: false,
 reason: "composer_not_empty_before_inject",
 text_length: beforeText.length,
 preview: beforeText.slice(0, 200)
 });
 return false;
 }
 }

      setText(composer, text);

      let attempts = 0;
      const maxAttempts = 24;
      let responded = false;

      const safeRespond = (payload) => {
        if (responded) return;
        responded = true;
        sendResponse(payload);
      };

      const expectedPrefix = text.slice(0, Math.min(40, text.length));
      let clickedAtLeastOnce = false;
      let lastMethod = "none";

      const isSubmitted = () => {
        const current = getComposerText(composer).trim();
        if (!current) return true;
        if (expectedPrefix && current.includes(expectedPrefix)) return false;
 return false;
      };

      const trySubmit = () => {
        const currentText = getComposerText(composer);
        const hasText = currentText.length > 0 || currentText.includes(text.slice(0, Math.min(20, text.length)));
        const btn = findSendButton(composer);

        if (clickedAtLeastOnce && isSubmitted()) {
          showNotice("Mensagem enviada ao chat", "command_id=" + actionId + "\nmethod=" + lastMethod, "success");
          console.log("[Local v" + VERSION + "] Submit confirmed by composer clear after " + (attempts * 250) + "ms");
          safeRespond({ok: true, method: lastMethod, attempts, text_length: text.length, confirmed: true});
          return;
        }

        if (btn && hasText && (attempts === 0 || attempts === 3 || attempts === 8 || attempts === 14)) {
          clickedAtLeastOnce = true;
          lastMethod = "button_click_confirmed";
          clickElement(btn);
          console.log("[Local v" + VERSION + "] Button submit attempt " + attempts);
        }

        if (hasText && (attempts === 2 || attempts === 6 || attempts === 10 || attempts === 18)) {
          clickedAtLeastOnce = true;
          lastMethod = "enter_confirmed";
          pressEnter(composer);
          showNotice("Tentativa por Enter", "command_id=" + actionId + "\nattempt=" + attempts, "warn");
          console.log("[Local v" + VERSION + "] Enter fallback attempt " + attempts);
        }

        attempts++;

        if (attempts <= maxAttempts) {
          setTimeout(trySubmit, 250);
        } else {
          const finalText = getComposerText(composer);
          const ownedStuckText = finalText && expectedPrefix && finalText.includes(expectedPrefix);
 if (ownedStuckText) setText(composer, String());
 const reason = clickedAtLeastOnce ? "submit_not_confirmed_composer_still_has_text" : "submit_button_not_found_or_disabled";
          showNotice("Falha ao confirmar envio", "command_id=" + actionId + "\nreason=" + reason, "error");
          console.warn("[Local v" + VERSION + "] Submit failed", {hasButton: !!findSendButton(composer), finalTextLength: finalText.length, clickedAtLeastOnce});
          safeRespond({
            ok: false,
            reason,
            final_text_length: finalText.length,
            attempts,
            clicked: clickedAtLeastOnce
          });
        }
      };

      setTimeout(trySubmit, 300);
      return true;
    }
  });

  function normalizeLocalCommand(cmd) {
    if (!cmd.schema) cmd.schema = LOCAL_SCHEMA;
    if (!cmd.schema_version) cmd.schema_version = LOCAL_SCHEMA_VERSION;
    if (!cmd.created_at_utc) cmd.created_at_utc = new Date().toISOString();

    if (cmd.delivery_kind === "inter_agent_message") {
      cmd.delivery_kind = "local_inter_agent_message";
    }

    return cmd;
  }

  function safeIdPart(value) {
    return String(value || "unknown").replace(/[^a-zA-Z0-9_-]/g, "_").slice(0, 80);
  }

  function canonicalUuid(value) {
    const m = String(value || "").match(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);
    return m ? m[0].toLowerCase() : "";
  }

  function extractJsonStringField(raw, field) {
    try {
      const re = new RegExp('"' + field + '"\\s*:\\s*"([^"\\r\\n]{0,500})"', "m");
      const m = String(raw || "").match(re);
      return m ? m[1] : "";
    } catch (e) {
      return "";
    }
  }

  function extractJsonUuidField(raw, field) {
    return canonicalUuid(extractJsonStringField(raw, field));
  }

  function sanitizeForStatus(value) {
    return String(value || "")
      .replace(/@@AI_BRIDGE_LOCAL_START@@/g, "[AI_BRIDGE_LOCAL_START]")
      .replace(/@@AI_BRIDGE_LOCAL_END@@/g, "[AI_BRIDGE_LOCAL_END]")
      .replace(/\r/g, "")
      .slice(0, 1200);
  }

  function classifyEnvelopeParseProblem(raw, errorMessage) {
    const source = String(raw || "");
    const causes = [];

    if (/[\\u2018\\u2019\\u201c\\u201d\\u2032\\u2033]/.test(source)) {
      causes.push("aspas curvas/Unicode no lugar de aspas JSON validas");
    }
    if (/[\\u200b\\u200c\\u200d\\ufeff]/.test(source)) {
      causes.push("caracteres invisiveis/zero-width no comando");
    }
    if (/(?:\\n\\s*[A-Za-z0-9_.-]\\s*){8,}/.test(source)) {
      causes.push("texto quebrado letra por letra ou colado com quebras artificiais");
    }
    if (/"command"\\s*:\\s*\\[[\\s\\S]{0,4000}\\n[\\s\\S]{0,4000}\\]/.test(source)) {
      causes.push("quebra de linha dentro de string JSON sem escape");
    }
 if (source.length > 900 && (source.includes('command') || source.includes('python -c') || source.includes('EncodedCommand') || source.includes('base64') || source.includes('script_text'))) {
      causes.push("comando inline grande/frágil; prefira script_text/script_ext ou arquivo real");
    }
    if (!causes.length) {
      causes.push("JSON invalido, aspas/backslashes nao escapados ou estrutura incompleta");
    }

    return {
      summary: causes.join("; "),
      correction:
        "Nada foi executado. Reenvie um envelope novo com command_id novo, JSON estrito, aspas duplas ASCII, sem caracteres invisiveis e sem texto quebrado. Para comandos grandes, use script_text/script_ext ou salve um .ps1/.py real antes de executar.",
      safeModel:
        "Modelo seguro: use marcadores locais de inicio/fim sozinhos nas linhas; dentro deles envie um unico JSON valido com payload.cwd, payload.timeout_seconds, payload.script_ext e payload.script_text. Exemplo de script_text curto: Write-Output 'OK'; git status -sb."
    };
  }

  function buildLocalStatusMessage(kind, errorMessage, raw) {
    const currentChatId = canonicalUuid(getChatId());
    const originalCommandId = extractJsonStringField(raw, "command_id") || "unknown";
    const originalSource = extractJsonUuidField(raw, "source_chat_id");
    const originalTarget = extractJsonUuidField(raw, "target_chat_id");
    const originalConversation = extractJsonStringField(raw, "conversation_id") || "local_bridge_diagnostics";
    const originalPreview = sanitizeForStatus(raw);
    const diagnosis = classifyEnvelopeParseProblem(raw, errorMessage);

    return {
      currentChatId,
      originalCommandId,
      originalSource,
      originalTarget,
      originalConversation,
      text:
        "[AI_LOCAL_ERRO]\\n" +
        "acao=corrija_e_reenvie\\n" +
        "no_reply=0\\n" +
        "executado=nao\\n" +
        "tipo=" + kind + "\\n" +
        "versao=" + VERSION + "\\n" +
        "id_original=" + originalCommandId + "\\n" +
        "chat_atual=" + (currentChatId || "unknown") + "\\n" +
        "origem=" + (originalSource || "unknown") + "\\n" +
        "destino=" + (originalTarget || "unknown") + "\\n" +
        "erro=" + String(errorMessage || "unknown_error").replace(/[\\r\\n]+/g, " ").slice(0, 500) + "\\n" +
        "causa_provavel=" + diagnosis.summary.slice(0, 900) + "\\n" +
        "correcao=" + diagnosis.correction + "\\n" +
        "modelo_seguro=" + diagnosis.safeModel + "\\n" +
 "observacao=Se o comando original continha limpeza/move/delete, reenvie primeiro em modo dry-run/listagem antes de executar alteracoes.\\n" +
        "original_sanitizado=\\n" + originalPreview
    };
  }

  function hashTextForStatus(value) {
    const s = String(value || "");
    let h = 0;
    for (let i = 0; i < s.length; i++) {
      h = ((h << 5) - h + s.charCodeAt(i)) | 0;
    }
    return Math.abs(h).toString(36);
  }


  function shouldReportEnvelopeError(kind, raw) {
    const originalCommandId = extractJsonStringField(raw, "command_id") || "unknown";
    const key = "ai_bridge_local_error_reported_" + safeIdPart(kind) + "_" + safeIdPart(originalCommandId) + "_" + hashTextForStatus(raw);

    if (reportedEnvelopeErrors.has(key)) {
      console.warn("[Local v" + VERSION + "] Skipping duplicate envelope error in memory:", originalCommandId);
      return false;
    }

    try {
      if (localStorage.getItem(key)) {
        reportedEnvelopeErrors.add(key);
        console.warn("[Local v" + VERSION + "] Skipping duplicate envelope error in localStorage:", originalCommandId);
        return false;
      }
    } catch (e) {}


    reportedEnvelopeErrors.add(key);
    try { localStorage.setItem(key, String(Date.now())); } catch (e) {}
    return true;
  }

  function reportEnvelopeError(kind, errorMessage, raw) {
    try {
      if (!shouldReportEnvelopeError(kind, raw)) return;

      const info = buildLocalStatusMessage(kind, errorMessage, raw);
      const targets = [];

      if (info.currentChatId) targets.push(info.currentChatId);
      if (info.originalTarget && !targets.includes(info.originalTarget)) targets.push(info.originalTarget);

      if (!targets.length) {
        console.warn("[Local v" + VERSION + "] Could not report envelope error: no valid target chat");
        return;
      }

      for (const targetChatId of targets) {
        const validTarget = canonicalUuid(targetChatId);
        if (!validTarget) {
          console.warn("[Local v" + VERSION + "] Skipping invalid status target:", targetChatId);
          continue;
        }

        const cmd = {
          schema: LOCAL_SCHEMA,
          schema_version: LOCAL_SCHEMA_VERSION,
          created_at_utc: new Date().toISOString(),
          command_id: "local_status_" + safeIdPart(kind) + "_" + safeIdPart(info.originalCommandId) + "_to_" + safeIdPart(validTarget).slice(0, 8) + "_" + Date.now(),
          action: "send-chat-message",
          source_chat_id: info.currentChatId || info.originalSource || "unknown",
          target_chat_id: validTarget,
          delivery_kind: "local_inter_agent_message",
          conversation_id: info.originalConversation + "_diagnostics",
          from_agent: "AI Bridge Local Extension " + VERSION,
          message: info.text
        };

        console.warn("[Local v" + VERSION + "] Reporting envelope error to chat:", validTarget, kind, errorMessage);
        send(cmd);
      }
    } catch (e) {
      console.warn("[Local v" + VERSION + "] reportEnvelopeError failed:", e.message);
    }
  }

  function extract(text) {
    const cmds = [];
    const regex = /(?:^|\n)@@AI_BRIDGE_LOCAL_START@@[ \t]*\r?\n([\s\S]*?)\r?\n@@AI_BRIDGE_LOCAL_END@@[ \t]*(?=\n|$)/g;
    let m;

    while ((m = regex.exec(text)) !== null) {
      const raw = m[1].trim();

      try {
        const c = normalizeLocalCommand(JSON.parse(raw));

        if (!c.command_id) {
          reportEnvelopeError("envelope_missing_command_id", "command_id ausente", raw);
          continue;
        }

        if (c.schema !== LOCAL_SCHEMA) {
          reportEnvelopeError("envelope_invalid_schema", "schema invalido: " + c.schema, raw);
          continue;
        }

        cmds.push(c);
      } catch (e) {
        const errorKey = safeIdPart((extractJsonStringField(raw, "command_id") || String(raw).slice(0, 80)) + "_" + String(e.message || ""));
      if (!reportedEnvelopeErrors.has(errorKey)) {
        reportedEnvelopeErrors.add(errorKey);
        reportEnvelopeError("envelope_parse_error", e.message, raw);
      } else {
        console.warn("[Local v" + VERSION + "] Suppressed duplicate envelope_parse_error:", errorKey);
      }
        console.warn("[Local v" + VERSION + "] Invalid local envelope JSON:", e.message, raw.slice(0, 400));
      }
    }

    return cmds;
  }

  const reportedEnvelopeErrorKeys = new Set();

  function hashString(value) {
    const s = String(value || "");
    let h = 0;
    for (let i = 0; i < s.length; i++) {
      h = ((h << 5) - h + s.charCodeAt(i)) | 0;
    }
    return String(Math.abs(h));
  }

  const sentIds = new Set();

  function send(cmd) {
    if (sentIds.has(cmd.command_id)) {
      showNotice("Comando duplicado ignorado", "command_id=" + cmd.command_id, "warn");
      return;
    }

    sentIds.add(cmd.command_id);
    if (sentIds.size > 100) sentIds.clear();

    showNotice("Comando local capturado", "command_id=" + cmd.command_id + "\naction=" + cmd.action, "info");

    chrome.runtime.sendMessage({type: "AI_BRIDGE_BRIDGE_COMMAND", command: cmd}, (response) => {
      if (chrome.runtime.lastError) {
        showNotice("Falha ao enviar comando ao gateway", chrome.runtime.lastError.message, "error");
        return;
      }

      if (response && response.ok) {
        const status = response.data?.status || "unknown";
        showNotice("Comando enviado ao gateway", "command_id=" + cmd.command_id + "\nstatus=" + status, "success");
      } else {
        showNotice("Gateway recusou comando", JSON.stringify(response || {}), "error");
      }
    });
  }

  let last = "";
  setInterval(() => {
    const t = document.body?.innerText || "";
    if (t !== last) {
      last = t;
      extract(t).forEach(send);
    }
  }, 2000);
})();
