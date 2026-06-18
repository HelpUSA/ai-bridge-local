// AI Bridge Local v0.5.37 - HelpUS AI compatible bridge
(() => {
  const VERSION = "0.5.37";
  const ENVELOPE_ERROR_DEDUPE_MS = 30 * 60 * 1000;
  const LOCAL_STATUS_PREFIXES = ["[AI_LOCAL_ERRO]", "[AI_LOCAL_RUN]", "[AI_LOCAL]"];
  const LOCAL_SCHEMA = "ai_bridge_local.envelope";
  const LOCAL_SCHEMA_VERSION = 1;
  const reportedEnvelopeErrors = new Set();
  const reportedEnvelopeErrorTimes = new Map();

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
      /ai\.helpusbr\.com\/c\/([0-9a-fA-F-]{36})/i,
      /chat\.deepseek\.com\/a\/chat\/s\/([0-9a-fA-F-]{36})/i,
      /chat\.deepseek\.com\/.*\/s\/([0-9a-fA-F-]{36})/i,
      /chatgpt\.com\/c\/([0-9a-fA-F-]{36})/i,
    /gemini\.google\.com\/app\/([0-9a-zA-Z_-]+)/i,
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

  const REGISTER_CHAT_INTERVAL_MS = 1500;
  registerChatWithBridge();
  setInterval(registerChatWithBridge, REGISTER_CHAT_INTERVAL_MS);

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


  function isUnsafeSubmitCandidate(el) {
    if (!el) return true;

    const txt = (
      (el.innerText || "") + " " +
      (el.textContent || "") + " " +
      (el.getAttribute("aria-label") || "") + " " +
      (el.getAttribute("title") || "") + " " +
      (el.getAttribute("data-testid") || "") + " " +
      (el.getAttribute("class") || "")
    ).toLowerCase();

    if (/share|compartilhar|copy link|copiar link|cancel|cancelar|close|fechar|menu|more|mais/.test(txt)) {
      return true;
    }

    const dialog = el.closest('[role="dialog"], dialog, [aria-modal="true"]');
    if (dialog) return true;

    return false;
  }

  function findBlockingModal() {
    const nodes = Array.from(document.querySelectorAll('[role="dialog"], dialog, [aria-modal="true"]'));

    return nodes.find((node) => {
      if (!isVisible(node)) return false;

      const txt = ((node.innerText || "") + " " + (node.textContent || "")).toLowerCase();
      return /compartilhar|share|copiar link|copy link|link de chat/.test(txt);
    }) || null;
  }

  function closeBlockingModalIfPresent() {
    const modal = findBlockingModal();
    if (!modal) return false;

    console.warn("[Local v" + VERSION + "] Closing blocking modal before composer submit");

    const cancelBtn = Array.from(modal.querySelectorAll('button, [role="button"]')).find((btn) => {
      const txt = (
        (btn.innerText || "") + " " +
        (btn.getAttribute("aria-label") || "") + " " +
        (btn.getAttribute("title") || "")
      ).toLowerCase();

      return /cancel|cancelar|close|fechar/.test(txt);
    });

    if (cancelBtn && isVisible(cancelBtn)) {
      clickElement(cancelBtn);
      return true;
    }

    document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", code: "Escape", bubbles: true }));
    document.dispatchEvent(new KeyboardEvent("keyup", { key: "Escape", code: "Escape", bubbles: true }));
    return true;
  }

  function scoreSendCandidate(el, composer) {
    if (isUnsafeSubmitCandidate(el)) return -9999;
    if (!isVisible(el) || isDisabled(el)) return -999;

    const txt = candidateText(el);
    let score = 0;

    if (/send|enviar|submit|ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¥ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚ÂÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¹Ã…â€œÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â|send-button|composer-submit|paper|plane|arrow|up/.test(txt)) score += 10;
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
      .filter(el => !isUnsafeSubmitCandidate(el))
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

      showNotice("Mensagem recebida para injeÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â£o", "command_id=" + actionId, "info");

      if (!text) {
        showNotice("Falha: texto vazio", "command_id=" + actionId, "error");
        sendResponse({ok: false, reason: "empty_text"});
        return false;
      }

      closeBlockingModalIfPresent();
      const composer = findComposer();
      if (!composer) {
        showNotice("Falha: composer nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â£o encontrado", "command_id=" + actionId, "error");
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

 function collectSubmitDiagnostics(composer, btn, currentText, clickedAtLeastOnce) {
 const buttons = Array.from(document.querySelectorAll('button, [role=button], [aria-label], [title]'));
 const visibleButtons = buttons.filter(isVisible).length;
 const disabledVisibleButtons = buttons.filter(el => isVisible(el) && isDisabled(el)).length;
 const composerVisible = isVisible(composer);
 const textLength = String(currentText || '').length;
 let reason = 'submit_button_not_found_or_disabled';
 if (!composer) reason = 'no_composer';
 else if (!composerVisible) reason = 'composer_not_visible';
 else if (!textLength) reason = 'composer_empty_after_inject';
 else if (!btn && disabledVisibleButtons > 0) reason = 'send_button_disabled_or_blocked';
 else if (!btn) reason = 'send_button_not_found';
 else if (isDisabled(btn)) reason = 'send_button_disabled';
 else if (!isVisible(btn)) reason = 'send_button_not_visible';
 else if (!clickedAtLeastOnce) reason = 'submit_button_not_clicked';
 return {
 reason,
 composer_visible: composerVisible,
 composer_text_length: textLength,
 has_button: !!btn,
 button_visible: !!btn && isVisible(btn),
 button_disabled: !!btn && isDisabled(btn),
 visible_button_count: visibleButtons,
 disabled_visible_button_count: disabledVisibleButtons
 };
 }

      const trySubmit = () => {
        closeBlockingModalIfPresent();
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
 const finalBtn = findSendButton(composer);
 const diagnostic = collectSubmitDiagnostics(composer, finalBtn, finalText, clickedAtLeastOnce);
 const reason = clickedAtLeastOnce ? 'submit_not_confirmed_composer_still_has_text' : diagnostic.reason;
          showNotice("Falha ao confirmar envio", "command_id=" + actionId + "\nreason=" + reason, "error");
          console.warn("[Local v" + VERSION + "] Submit failed", {hasButton: !!findSendButton(composer), finalTextLength: finalText.length, clickedAtLeastOnce});
          safeRespond({
            ok: false,
            reason,
            final_text_length: finalText.length,
            attempts,
 clicked: clickedAtLeastOnce,
 diagnostics: diagnostic
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

    if (cmd.delivery_kind === "local_inter_agent_message") {
      cmd.delivery_kind = "inter_agent_message";
    }

    if (cmd.delivery_kind === "inter_agent_message") {
      cmd.delivery_kind = "inter_agent_message";
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
      const re = new RegExp('"' + field + '"\\s*:\\s*"([^"\\r\\n]{0,2000})"', "m");
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
      causes.push("comando inline grande/frÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡gil; prefira script_text/script_ext ou arquivo real");
    }
    if (!causes.length) {
      causes.push("JSON invalido, aspas/backslashes nao escapados ou estrutura incompleta");
    }

    return {
      summary: causes.join("; "),
      correction:
        "Nada foi executado. Reenvie um envelope novo com command_id novo, JSON estrito, aspas duplas ASCII, sem caracteres invisiveis e sem texto quebrado. Para comandos grandes, prefira payload.command com python -c + base64; se usar script_text, escape quebras de linha como \\n.",
      safeModel:
        "Modelo seguro: use marcadores locais de inicio/fim sozinhos nas linhas; dentro deles envie um unico JSON valido com payload.cwd, payload.timeout_seconds e payload.command. Para comandos grandes, use python -c com base64; script_text somente curto com \\n escapado."
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

    const now = Date.now();
    const memoryReportedAt = reportedEnvelopeErrorTimes.get(key);
    if (memoryReportedAt && now - memoryReportedAt < ENVELOPE_ERROR_DEDUPE_MS) {
      console.warn("[Local v" + VERSION + "] Skipping duplicate envelope error in memory:", originalCommandId);
      return false;
    }

    try {
      const storedReportedAt = Number(localStorage.getItem(key) || 0);
      if (storedReportedAt && now - storedReportedAt < ENVELOPE_ERROR_DEDUPE_MS) {
        reportedEnvelopeErrors.add(key);
        reportedEnvelopeErrorTimes.set(key, storedReportedAt);
        console.warn("[Local v" + VERSION + "] Skipping duplicate envelope error in localStorage:", originalCommandId);
        return false;
      }
      if (storedReportedAt) localStorage.removeItem(key);
    } catch (e) {}

    reportedEnvelopeErrors.add(key);
    reportedEnvelopeErrorTimes.set(key, now);
    try { localStorage.setItem(key, String(now)); } catch (e) {}
    return true;
  }

  function sendTelemetryEvent(eventType, payload = {}) {
 try {
 chrome.runtime.sendMessage({ type: 'AI_LOCAL_TELEMETRY_EVENT', event_type: eventType, payload });
 } catch (e) {
 console.warn('[AI_LOCAL] telemetry send failed', eventType, e.message);
 }
}

function sendChatHeartbeat() {
 sendTelemetryEvent('chat_heartbeat', { chat_id: getChatId(), href: location.href });
}

function reportEnvelopeError(kind, errorMessage, raw) {
    try {
      if (!shouldReportEnvelopeError(kind, raw)) return;
 sendTelemetryEvent(kind === 'envelope_parse_error' ? 'envelope_parse_error' : 'envelope_semantic_error', { message: String(errorMessage || 'unknown'), error_kind: kind, chat_id: getChatId(), raw_preview: String(raw || '').slice(0, 500) });

      const info = buildLocalStatusMessage(kind, errorMessage, raw);
      const targets = [];
      const targetCandidates = [info.originalSource, info.currentChatId, info.originalTarget];

      for (const candidate of targetCandidates) {
        const validTarget = canonicalUuid(candidate);
        if (validTarget && !targets.includes(validTarget)) targets.push(validTarget);
      }

      if (!targets.length) {
        console.warn("[Local v" + VERSION + "] Could not report envelope error: no valid target chat");
        return;
      }

      for (const validTarget of targets) {

        const cmd = {
          schema: LOCAL_SCHEMA,
          schema_version: LOCAL_SCHEMA_VERSION,
          created_at_utc: new Date().toISOString(),
          command_id: "local_status_" + safeIdPart(kind) + "_" + safeIdPart(info.originalCommandId) + "_to_" + safeIdPart(validTarget).slice(0, 8) + "_" + Date.now(),
          action: "send-chat-message",
          source_chat_id: info.currentChatId || info.originalSource || "unknown",
          target_chat_id: validTarget,
          delivery_kind: "inter_agent_message",
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
    const sourceText = String(text || "");
    if (LOCAL_STATUS_PREFIXES.some((prefix) => sourceText.includes(prefix))) {
      return cmds;
    }
    const regex = /(?:^|\n)?@@AI_BRIDGE_LOCAL_START@@[ \t]*(?:\r?\n)?([\s\S]*?)(?:\r?\n)?@@AI_BRIDGE_LOCAL_END@@[ \t]*(?=\n|$)/g;
    let m;

    while ((m = regex.exec(sourceText)) !== null) {
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

 const actualSourceChatId = getChatId();
 if (actualSourceChatId) {
 if (cmd.source_chat_id && cmd.source_chat_id !== actualSourceChatId) {
 const declaredSource = cmd.source_chat_id;
 const statusText = [
 '[AI_LOCAL_ERRO]',
 'acao=corrija_e_reenvie',
 'no_reply=0',
 'executado=nao',
 'tipo=source_chat_id_mismatch',
 'versao=' + VERSION,
 'id_original=' + (cmd.command_id || 'unknown'),
 'chat_atual=' + actualSourceChatId,
 'origem_declarada=' + declaredSource,
 'destino=' + (cmd.target_chat_id || 'unknown'),
 'erro=source_chat_id do envelope nao corresponde ao chat atual. Nada foi executado nem enviado ao gateway.',
 'correcao=Reenvie o envelope a partir do chat correto ou ajuste source_chat_id para o chat atual.'
 ].join(String.fromCharCode(10));
 showNotice('Source chat divergente', 'command_id=' + (cmd.command_id || 'unknown') + String.fromCharCode(10) + 'origem=' + declaredSource + String.fromCharCode(10) + 'chat_atual=' + actualSourceChatId, 'error');
 sendTextToChat(statusText, 'source_chat_id_mismatch_' + (cmd.command_id || 'unknown'));
 return;
 }
 cmd.source_chat_id = actualSourceChatId;
 cmd.source_url = location.href;
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

setInterval(sendChatHeartbeat, 30000);
sendChatHeartbeat();

/* AI Bridge Local: Gemini auto envelope capture. */
(function installAiBridgeGeminiCapturedEnvelopeBridge() {
  if (window.__AI_BRIDGE_GEMINI_CAPTURE_INSTALLED__) return;
  window.__AI_BRIDGE_GEMINI_CAPTURE_INSTALLED__ = true;

  const START_MARKER = "@@" + "AI_BRIDGE_LOCAL_START" + "@@";
  const END_MARKER = "@@" + "AI_BRIDGE_LOCAL_END" + "@@";
  const MAX_CAPTURE_CHARS = 20000;
  const DEDUPE_PREFIX = "ai_bridge_captured_envelope:";

  function isGeminiAppPage() {
    return /gemini\.google\.com\/app\/([0-9a-zA-Z_-]+)/i.test(location.href);
  }

  function getGeminiChatId() {
    const match = location.href.match(/gemini\.google\.com\/app\/([0-9a-zA-Z_-]+)/i);
    return match ? match[1] : "";
  }

  function countOccurrences(text, needle) {
    let count = 0;
    let offset = 0;
    while (true) {
      const foundAt = text.indexOf(needle, offset);
      if (foundAt < 0) return count;
      count += 1;
      offset = foundAt + needle.length;
    }
  }

  function parseCapturedEnvelopeText(rawText) {
    const text = String(rawText || "").trim();
    if (!text || !text.includes(START_MARKER) || !text.includes(END_MARKER)) {
      return { ok: false, error: "marker_missing" };
    }
    if (text.length > MAX_CAPTURE_CHARS) {
      return { ok: false, error: "capture_too_large" };
    }
    if (countOccurrences(text, START_MARKER) !== 1 || countOccurrences(text, END_MARKER) !== 1) {
      return { ok: false, error: "multiple_or_missing_blocks" };
    }

    const startIndex = text.indexOf(START_MARKER);
    const endIndex = text.indexOf(END_MARKER);
    if (startIndex < 0 || endIndex < 0 || endIndex <= startIndex) {
      return { ok: false, error: "invalid_marker_order" };
    }

    const before = text.slice(0, startIndex).trim();
    const body = text.slice(startIndex + START_MARKER.length, endIndex).trim();
    const after = text.slice(endIndex + END_MARKER.length).trim();
    if (before || after) return { ok: false, error: "text_outside_block" };
    if (!body) return { ok: false, error: "empty_json_body" };

    let envelope;
    try {
      envelope = JSON.parse(body);
    } catch (err) {
      return { ok: false, error: "invalid_json", detail: String(err && err.message ? err.message : err) };
    }
    if (!envelope || typeof envelope !== "object" || Array.isArray(envelope)) {
      return { ok: false, error: "json_not_object" };
    }
    if (!String(envelope.command_id || "").trim()) {
      return { ok: false, error: "missing_command_id" };
    }
    return { ok: true, envelope, raw_text: text };
  }

  function isComposerOrInputNode(node) {
    if (!node || !(node instanceof Element)) return false;
    return Boolean(node.closest('textarea,input,[contenteditable="true"],[role="textbox"],form'));
  }

  function wasCaptured(commandId) {
    try {
      return sessionStorage.getItem(DEDUPE_PREFIX + commandId) === "1";
    } catch (err) {
      return false;
    }
  }

  function markCaptured(commandId) {
    try {
      sessionStorage.setItem(DEDUPE_PREFIX + commandId, "1");
    } catch (err) {
      // best effort only
    }
  }

  function tryCaptureEnvelopeFromNode(node) {
    if (!isGeminiAppPage()) return;
    if (!node || !(node instanceof Element)) return;
    if (isComposerOrInputNode(node)) return;

    const candidateTexts = [];
    const addCandidateText = (element) => {
      if (!element || !(element instanceof Element)) return;
      if (isComposerOrInputNode(element)) return;
      const candidateText = String(element.innerText || element.textContent || "").trim();
      if (!candidateText) return;
      if (LOCAL_STATUS_PREFIXES.some((prefix) => candidateText.includes(prefix))) return;
      if (candidateText.length > MAX_CAPTURE_CHARS) return;
      if (!candidateText.includes(START_MARKER) || !candidateText.includes(END_MARKER)) return;
      candidateTexts.push(candidateText);
    };

    addCandidateText(node);
    node.querySelectorAll("pre, code, markdown, [class*='message'], [class*='response'], [data-message-author-role]").forEach(addCandidateText);
    candidateTexts.sort((a, b) => a.length - b.length);

    let parsed = null;
    for (const candidateText of candidateTexts) {
      const attempt = parseCapturedEnvelopeText(candidateText);
      if (attempt.ok) {
        parsed = attempt;
        break;
      }
      console.warn("[Local] Gemini envelope candidate rejected:", attempt.error);
    }
    if (!parsed) return;

    const commandId = String(parsed.envelope.command_id || "").trim();
    if (wasCaptured(commandId)) {
      console.warn("[Local] Gemini envelope duplicate ignored:", commandId);
      return;
    }
    markCaptured(commandId);

    chrome.runtime.sendMessage({
      type: "AI_BRIDGE_CAPTURED_ENVELOPE",
      source_chat_id: getGeminiChatId(),
      raw_text: parsed.raw_text,
      envelope: parsed.envelope
    }, (response) => {
      const runtimeError = chrome.runtime.lastError;
      if (runtimeError) {
        console.warn("[Local] Gemini envelope capture sendMessage failed:", runtimeError.message);
        return;
      }
      if (!response || !response.ok) {
        console.warn("[Local] Gemini envelope capture rejected by background:", response && response.error);
      } else {
        console.log("[Local] Gemini envelope captured:", commandId);
      }
    });
  }

  function installGeminiEnvelopeObserver() {
    if (!isGeminiAppPage() || !document.body) return;

    const seenNodes = new WeakSet();
    document.body.querySelectorAll("*").forEach((el) => seenNodes.add(el));

    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        for (const addedNode of mutation.addedNodes) {
          if (!(addedNode instanceof Element)) continue;
          if (seenNodes.has(addedNode)) continue;
          seenNodes.add(addedNode);
          window.setTimeout(() => tryCaptureEnvelopeFromNode(addedNode), 250);
        }
      }
    });

    observer.observe(document.body, { childList: true, subtree: true });
    console.log("[Local] Gemini envelope observer installed for chat:", getGeminiChatId());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", installGeminiEnvelopeObserver, { once: true });
  } else {
    installGeminiEnvelopeObserver();
  }
})();
