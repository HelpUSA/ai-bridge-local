var LOCAL_STATUS_PREFIXES = globalThis.__AI_BRIDGE_LOCAL_STATUS_PREFIXES__ || [
  "[AI_LOCAL_ERRO]",
  "[AI_LOCAL_RUN]",
  "[AI_LOCAL]"
];
globalThis.__AI_BRIDGE_LOCAL_STATUS_PREFIXES__ = LOCAL_STATUS_PREFIXES;
window.__AI_BRIDGE_LOCAL_STATUS_PREFIXES__ = LOCAL_STATUS_PREFIXES;

// AI Bridge Local v0.5.39 - HelpUS AI compatible bridge
(() => {
  const VERSION = "0.5.71";
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
  const aiBridgePreferredComposer = aiBridgeFindChatGptPromptTextarea();
  if (aiBridgePreferredComposer) {
    console.log("[Local v" + VERSION + "] using preferred ChatGPT composer", aiBridgeDescribeComposerElement(aiBridgePreferredComposer));
    return aiBridgePreferredComposer;
  }
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

    if (/send|enviar|submit|ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¥ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚ÂÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¹ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â|send-button|composer-submit|paper|plane|arrow|up/.test(txt)) score += 10;
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

    el.dispatchEvent(new InputEvent("input:not([type='file']):not(#upload-photos):not(#upload-camera)", {bubbles: true, cancelable: true, inputType: "insertText", data: text}));
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


function aiBridgeDispatchInputEvents(element, text) {
  try {
    element.dispatchEvent(new InputEvent("beforeinput", {
      bubbles: true,
      cancelable: true,
      inputType: "insertText",
      data: text
    }));
  } catch (_) {}

  try {
    element.dispatchEvent(new InputEvent("input:not([type='file']):not(#upload-photos):not(#upload-camera)", {
      bubbles: true,
      inputType: "insertText",
      data: text
    }));
  } catch (_) {
    element.dispatchEvent(new Event("input:not([type='file']):not(#upload-photos):not(#upload-camera)", { bubbles: true }));
  }

  try {
    element.dispatchEvent(new Event("change", { bubbles: true }));
  } catch (_) {}

  try {
    element.dispatchEvent(new KeyboardEvent("keyup", {
      bubbles: true,
      cancelable: true,
      key: " ",
      code: "Space",
      which: 32,
      keyCode: 32
    }));
  } catch (_) {}
}

function aiBridgeSetNativeValue(element, value) {
  const tag = String(element.tagName || "").toUpperCase();
  if (tag !== "TEXTAREA" && tag !== "INPUT") return false;

  const proto = tag === "TEXTAREA" ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
  const descriptor = Object.getOwnPropertyDescriptor(proto, "value");
  if (descriptor && descriptor.set) {
    descriptor.set.call(element, value);
  } else {
    element.value = value;
  }

  aiBridgeDispatchInputEvents(element, value);
  return true;
}

function aiBridgeSetContentEditableByRange(element, value) {
  try {
    element.focus();

    const selection = window.getSelection();
    if (!selection) return false;

    const range = document.createRange();
    range.selectNodeContents(element);
    range.deleteContents();
    range.collapse(true);

    const lines = String(value || "").split(/\n/);
    lines.forEach((line, index) => {
      if (index > 0) {
        range.insertNode(document.createElement("br"));
        range.collapse(false);
      }
      range.insertNode(document.createTextNode(line));
      range.collapse(false);
    });

    selection.removeAllRanges();
    selection.addRange(range);
    aiBridgeDispatchInputEvents(element, value);
    return true;
  } catch (e) {
    console.warn("[Local v" + VERSION + "] aiBridgeSetContentEditableByRange failed", e && e.message);
    return false;
  }
}

function aiBridgeSetContentEditableByParagraphDom(element, value) {
  try {
    element.focus();
    element.innerHTML = "";

    const lines = String(value || "").split(/\n/);
    const wrapper = document.createDocumentFragment();

    lines.forEach((line) => {
      const p = document.createElement("p");
      p.textContent = line || "";
      wrapper.appendChild(p);
    });

    element.appendChild(wrapper);
    aiBridgeDispatchInputEvents(element, value);
    return true;
  } catch (e) {
    console.warn("[Local v" + VERSION + "] aiBridgeSetContentEditableByParagraphDom failed", e && e.message);
    return false;
  }
}

function aiBridgeSetContentEditableByExecCommand(element, value) {
  try {
    element.focus();
    document.execCommand("selectAll", false, null);
    document.execCommand("delete", false, null);
    const ok = document.execCommand("insertText", false, String(value || ""));
    aiBridgeDispatchInputEvents(element, value);
    return Boolean(ok);
  } catch (e) {
    console.warn("[Local v" + VERSION + "] aiBridgeSetContentEditableByExecCommand failed", e && e.message);
    return false;
  }
}

function aiBridgeRobustSetText(element, value) {
  const text = String(value || "");
  if (!element) return false;

  try {
    element.focus();
  } catch (_) {}

  if (aiBridgeSetNativeValue(element, text)) {
    return true;
  }

  const before = String(getComposerText(element) || "").trim();

  const attempts = [
    () => aiBridgeSetContentEditableByExecCommand(element, text),
    () => aiBridgeSetContentEditableByRange(element, text),
    () => aiBridgeSetContentEditableByParagraphDom(element, text)
  ];

  for (const attempt of attempts) {
    try {
      attempt();
      const after = String(getComposerText(element) || "").trim();
      if (text.trim() === "" || after === text.trim() || after.length > 0) {
        return true;
      }
    } catch (_) {}
  }

  try {
    element.textContent = text;
    aiBridgeDispatchInputEvents(element, text);
    const finalText = String(getComposerText(element) || "").trim();
    if (text.trim() === "" || finalText === text.trim() || finalText.length > 0) {
      return true;
    }
  } catch (_) {}

  console.warn("[Local v" + VERSION + "] aiBridgeRobustSetText failed", {
    before_length: before.length,
    requested_length: text.length,
    after_length: String(getComposerText(element) || "").trim().length
  });

  return false;
}



function aiBridgeIsElementVisibleForComposer(element) {
  if (!element || !(element instanceof Element)) return false;

  const rect = element.getBoundingClientRect();
  const style = getComputedStyle(element);

  return rect.width > 0 &&
    rect.height > 0 &&
    style.visibility !== "hidden" &&
    style.display !== "none";
}

function aiBridgeIsUsableComposerCandidate(element) {
  if (!element || !(element instanceof Element)) return false;
  if (!aiBridgeIsElementVisibleForComposer(element)) return false;

  const tag = String(element.tagName || "").toUpperCase();
  const type = String(element.getAttribute("type") || "").toLowerCase();
  const id = String(element.id || "").toLowerCase();
  const ariaHidden = String(element.getAttribute("aria-hidden") || "").toLowerCase();
  const disabled = element.disabled || String(element.getAttribute("aria-disabled") || "").toLowerCase() === "true";

  if (disabled) return false;
  if (ariaHidden === "true") return false;
  if (type === "file") return false;
  if (id.includes("upload")) return false;

  if (tag === "TEXTAREA") return true;

  if (tag === "INPUT") {
    return ["", "text", "search"].includes(type);
  }

  if (String(element.getAttribute("contenteditable") || "").toLowerCase() === "true") {
    return true;
  }

  if (String(element.getAttribute("role") || "").toLowerCase() === "textbox") {
    return true;
  }

  return false;
}


/* AI Bridge Local repair marker: composer_descriptor: aiBridgeDescribeComposerElement(composer)
   The direct-inject failure path in this build did not expose a simple diagnostics object to patch.
   The preferred composer is still logged via using preferred ChatGPT composer. */

function aiBridgeDescribeComposerElement(element) {
  if (!element || !(element instanceof Element)) return { found: false };

  return {
    found: true,
    tag: String(element.tagName || ""),
    id: String(element.id || ""),
    role: String(element.getAttribute("role") || ""),
    contenteditable: String(element.getAttribute("contenteditable") || ""),
    testid: String(element.getAttribute("data-testid") || ""),
    aria_label: String(element.getAttribute("aria-label") || ""),
    type: String(element.getAttribute("type") || ""),
    class_name: String(element.className || "").slice(0, 160),
    text_length: String(getComposerText(element) || "").trim().length
  };
}

function aiBridgeFindChatGptPromptTextarea() {
  const preferredSelectors = [
    "#prompt-textarea.ProseMirror[contenteditable='true']",
    "div#prompt-textarea[contenteditable='true'][role='textbox']",
    "#prompt-textarea[contenteditable='true']",
    "#prompt-textarea",
    "[data-testid='prompt-textarea']",
    "[aria-label='Converse com o ChatGPT'][contenteditable='true']",
    "[aria-label='Message ChatGPT'][contenteditable='true']",
    "[aria-label='Send a message'][contenteditable='true']",
    "main form .ProseMirror[contenteditable='true']",
    "form .ProseMirror[contenteditable='true']",
    ".ProseMirror[contenteditable='true'][role='textbox']"
  ];

  for (const selector of preferredSelectors) {
    const element = document.querySelector(selector);
    if (aiBridgeIsUsableComposerCandidate(element)) {
      return element;
    }
  }

  const fallbackSelectors = [
    "textarea:not([type='file'])",
    "[contenteditable='true'][role='textbox']",
    "[contenteditable='true']",
    "[role='textbox']"
  ];

  for (const selector of fallbackSelectors) {
    const elements = Array.from(document.querySelectorAll(selector));
    for (const element of elements) {
      if (aiBridgeIsUsableComposerCandidate(element)) {
        return element;
      }
    }
  }

  return null;
}


chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message && message.type === "AI_BRIDGE_INJECT_TEXT") {
      const actionId = message.action?.action_id || message.action?.command_id || "unknown";
      const text = message.action?.text || message.action?.message || message.text || "";

      showNotice("Mensagem recebida para injeÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â£o", "command_id=" + actionId, "info");

      if (!text) {
        showNotice("Falha: texto vazio", "command_id=" + actionId, "error");
        sendResponse({ok: false, reason: "empty_text"});
        return false;
      }

      closeBlockingModalIfPresent();
      const composer = findComposer();
      if (!composer) {
        showNotice("Falha: composer nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â£o encontrado", "command_id=" + actionId, "error");
        sendResponse({ok: false, reason: "no_composer"});
        return false;
      }

 const beforeText = getComposerText(composer).trim();
const requestedTextBeforeInject = String(text || "").trim();
const composerAlreadyHasRequestedText = Boolean(beforeText && requestedTextBeforeInject && beforeText === requestedTextBeforeInject);
 if (beforeText) {
 const ownedPreflightText = composerAlreadyHasRequestedText || beforeText.includes("AI_BRIDGE_LOCAL_START") || beforeText.includes("ai_bridge_local.envelope") || beforeText.includes("[AI_LOCAL]") || beforeText.includes("[AI_LOCAL_ERRO]");
 if (ownedPreflightText) {
 showNotice("Limpando composer travado da extensao", "command_id=" + actionId, "warn");
 aiBridgeRobustSetText(composer, String());
 } else {
 showNotice("Falha: composer nao vazio antes da injecao", "command_id=" + actionId, "error");
 sendResponse({
 ok: false,
 reason: "composer_not_empty_before_inject",
  composer_text_matches_requested_text: composerAlreadyHasRequestedText,
 text_length: beforeText.length,
 preview: beforeText.slice(0, 200)
 });
 return false;
 }
 }

      aiBridgeRobustSetText(composer, text);

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
 if (ownedStuckText) aiBridgeRobustSetText(composer, String());
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
      causes.push("comando inline grande/frÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡gil; prefira script_text/script_ext ou arquivo real");
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


function aiBridgeSafeCallSendChatHeartbeat(reason) {
  try {
    if (typeof sendChatHeartbeat === "function") {
      try {
  if (typeof sendChatHeartbeat === "function") {
    sendChatHeartbeat();
  } else {
    console.warn("[AI Bridge Local] sendChatHeartbeat unavailable; skipped heartbeat direct_call");
  }
} catch (e) {
  console.warn("[AI Bridge Local] sendChatHeartbeat failed; skipped heartbeat direct_call", e && e.message);
}
      return true;
    }
    console.warn("[AI Bridge Local] sendChatHeartbeat unavailable; skipped heartbeat", reason || "");
    return false;
  } catch (e) {
    console.warn("[AI Bridge Local] sendChatHeartbeat failed; skipped heartbeat", reason || "", e && e.message);
    return false;
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
    const trimmedSourceText = sourceText.trim();
    if (LOCAL_STATUS_PREFIXES.some((prefix) => trimmedSourceText.startsWith(prefix))) {
      return cmds;
    }
    const regex = /(?:^|\n)[ \t]*@@AI_BRIDGE_LOCAL_START@@[ \t]*\r?\n([\s\S]*?)\r?\n[ \t]*@@AI_BRIDGE_LOCAL_END@@[ \t]*(?=\r?\n|$)/g; // AIBRIDGE_LINE_ISOLATED_ENVELOPE_CAPTURE
    let m;

    while ((m = regex.exec(sourceText)) !== null) {
      const raw = m[1].trim();

      try {
        if (!/^\s*\{/.test(raw || "")) { continue; } // AIBRIDGE_INLINE_MARKER_PARSE_GUARD_061
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
 const mismatchKey = 'ai_bridge_source_chat_id_mismatch:' + (cmd.command_id || 'unknown');
try {
  if (sessionStorage.getItem(mismatchKey) === '1') {
    console.warn('[Local v' + VERSION + '] source_chat_id_mismatch suppressed duplicate for', cmd.command_id || 'unknown');
  } else {
    sessionStorage.setItem(mismatchKey, '1');
    sendTextToChat(statusText, 'source_chat_id_mismatch_' + (cmd.command_id || 'unknown'));
  }
} catch (_) {
  sendTextToChat(statusText, 'source_chat_id_mismatch_' + (cmd.command_id || 'unknown'));
}
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

  /* AI Bridge Local: legacy global body scanner disabled in 0.5.66.
   Reason: it scans document.body, reprocesses stale envelopes, and can call sendTextToChat outside scope.
   The standalone ChatGPT scanner with visible feedback is now responsible for outbound envelope capture. */
let last = "";
})();

setInterval(() => {
  try {
    if (typeof sendChatHeartbeat === "function") {
      sendChatHeartbeat();
    } else {
      console.warn("[AI Bridge Local] sendChatHeartbeat unavailable; skipped heartbeat interval");
    }
  } catch (e) {
    console.warn("[AI Bridge Local] sendChatHeartbeat failed; skipped heartbeat interval", e && e.message);
  }
}, 30000);
try {
  if (typeof sendChatHeartbeat === "function") {
    sendChatHeartbeat();
  } else {
    console.warn("[AI Bridge Local] sendChatHeartbeat unavailable; skipped heartbeat direct_call");
  }
} catch (e) {
  console.warn("[AI Bridge Local] sendChatHeartbeat failed; skipped heartbeat direct_call", e && e.message);
}

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


/* AI Bridge Local: ChatGPT outbound envelope capture. */
(function installAiBridgeChatGptOutboundEnvelopeCapture() {
  if (window.__AI_BRIDGE_CHATGPT_OUTBOUND_CAPTURE_INSTALLED__) return;
  window.__AI_BRIDGE_CHATGPT_OUTBOUND_CAPTURE_INSTALLED__ = true;

  const CAPTURE_VERSION = "0.5.71";
  const MAX_CAPTURE_CHARS = 30000;
  const DEDUPE_PREFIX = "ai_bridge_chatgpt_outbound_capture:";

  const START_MARKERS = [
    "@@" + "AI_BRIDGE_LOCAL_START" + "@@",
    "@@" + "AI_BRIDGE_LOCAL_BEGIN" + "@@"
  ];
  const END_MARKER = "@@" + "AI_BRIDGE_LOCAL_END" + "@@";

  function isChatGptPage() {
    return /chatgpt\.com/i.test(location.hostname);
  }

  function getCurrentChatId() {
    const href = String(location.href || "");
    const patterns = [
      /\/c\/([0-9a-fA-F-]{36})/i,
      /chatgpt\.com\/c\/([0-9a-fA-F-]{36})/i,
      /chatgpt\.com\/g\/[^/]+\/c\/([0-9a-fA-F-]{36})/i
    ];
    for (const pattern of patterns) {
      const match = href.match(pattern);
      if (match) return match[1];
    }
    return "";
  }

  function isComposerOrInputNode(element) {
    if (!element || !(element instanceof Element)) return false;
    return Boolean(
      element.closest("textarea, input, [contenteditable='true'], form") ||
      element.matches("textarea, input, [contenteditable='true']")
    );
  }

  function safeIdPart(value) {
    return String(value || "unknown").replace(/[^a-zA-Z0-9_.-]+/g, "_").slice(0, 80) || "unknown";
  }

  function wasCaptured(commandId) {
    if (!commandId) return false;
    const key = DEDUPE_PREFIX + commandId;
    try {
      if (sessionStorage.getItem(key)) return true;
      sessionStorage.setItem(key, String(Date.now()));
    } catch (_) {
      if (window.__AI_BRIDGE_CHATGPT_CAPTURED_IDS__ && window.__AI_BRIDGE_CHATGPT_CAPTURED_IDS__.has(commandId)) return true;
      window.__AI_BRIDGE_CHATGPT_CAPTURED_IDS__ = window.__AI_BRIDGE_CHATGPT_CAPTURED_IDS__ || new Set();
      window.__AI_BRIDGE_CHATGPT_CAPTURED_IDS__.add(commandId);
    }
    return false;
  }

  function showCaptureNotice(title, text, kind) {
    try {
      const id = "ai-bridge-chatgpt-outbound-capture-notice";
      let box = document.getElementById(id);
      if (!box) {
        box = document.createElement("div");
        box.id = id;
        box.style.position = "fixed";
        box.style.right = "12px";
        box.style.bottom = "12px";
        box.style.zIndex = "2147483647";
        box.style.maxWidth = "520px";
        box.style.padding = "10px 12px";
        box.style.borderRadius = "8px";
        box.style.font = "12px/1.35 system-ui, sans-serif";
        box.style.whiteSpace = "pre-wrap";
        box.style.boxShadow = "0 4px 18px rgba(0,0,0,.25)";
        document.documentElement.appendChild(box);
      }
      box.style.background = kind === "error" ? "#7f1d1d" : "#064e3b";
      box.style.color = "white";
      box.textContent = "[AI Bridge Local " + CAPTURE_VERSION + "] " + title + "\n" + String(text || "").slice(0, 1000);
      window.setTimeout(() => {
        try { box.remove(); } catch (_) {}
      }, 7000);
    } catch (_) {}
  }

  function sendCommandToBackground(cmd) {
    chrome.runtime.sendMessage({ type: "AI_BRIDGE_BRIDGE_COMMAND", command: cmd }, (response) => {
      const runtimeError = chrome.runtime.lastError;
      if (runtimeError) {
        console.warn("[Local v" + CAPTURE_VERSION + "] ChatGPT outbound capture sendMessage failed:", runtimeError.message);
        showCaptureNotice("Falha ao enviar ao background", runtimeError.message, "error");
        return;
      }
      if (!response || !response.ok) {
        const err = response && response.error ? response.error : "unknown_background_error";
        console.warn("[Local v" + CAPTURE_VERSION + "] ChatGPT outbound capture rejected:", err);
        showCaptureNotice("Captura rejeitada", err, "error");
        return;
      }
      showCaptureNotice("Comando local capturado", "command_id=" + (cmd.command_id || "unknown") + "\naction=" + (cmd.action || "unknown"), "info");
    });
  }

  function sendLocalError(kind, commandId, message, raw) {
    const currentChatId = getCurrentChatId();
    if (!currentChatId) {
      showCaptureNotice("Erro de envelope", kind + "\n" + message, "error");
      return;
    }
    const errCmd = {
      schema: "ai_bridge_local.envelope",
      schema_version: 1,
      command_id: "local_status_" + safeIdPart(kind) + "_" + safeIdPart(commandId) + "_" + Date.now(),
      action: "send-chat-message",
      source_chat_id: currentChatId,
      target_chat_id: currentChatId,
      delivery_kind: "inter_agent_message",
      conversation_id: "chatgpt_outbound_capture_diagnostics",
      from_agent: "AI Bridge Local Extension " + CAPTURE_VERSION,
      to_agent: "Current ChatGPT Chat",
      message:
        "[AI_LOCAL_ERRO]\n" +
        "acao=corrija_e_reenvie\n" +
        "no_reply=0\n" +
        "executado=nao\n" +
        "tipo=" + kind + "\n" +
        "versao=" + CAPTURE_VERSION + "\n" +
        "id_original=" + (commandId || "unknown") + "\n" +
        "chat_atual=" + currentChatId + "\n" +
        "erro=" + String(message || "unknown_error").replace(/[\r\n]+/g, " ").slice(0, 500) + "\n" +
        "correcao=Use JSON estrito entre @@AI_BRIDGE_LOCAL_START@@ e @@AI_BRIDGE_LOCAL_END@@, com source_chat_id igual ao chat atual.\n" +
        "original_sanitizado=\n" + String(raw || "").replace(/\r/g, "").slice(0, 1200),
      no_reply: 1
    };
    sendCommandToBackground(errCmd);
  }

  function extractEnvelopeBlocks(text) {
    const source = String(text || "");
    const blocks = [];
    for (const start of START_MARKERS) {
      let offset = 0;
      while (true) {
        const startIndex = source.indexOf(start, offset);
        if (startIndex < 0) break;
        const bodyStart = startIndex + start.length;
        const endIndex = source.indexOf(END_MARKER, bodyStart);
        if (endIndex < 0) break;
        const raw = source.slice(bodyStart, endIndex).trim();
        blocks.push({ raw, start });
        offset = endIndex + END_MARKER.length;
      }
    }
    return blocks;
  }

  function processText(text) {
    const source = String(text || "").trim();
    if (!source || source.length > MAX_CAPTURE_CHARS) return;
    if (!source.includes("AI_BRIDGE_LOCAL_") || !source.includes("ai_bridge_local.envelope")) return;
    if (source.includes("[AI_LOCAL]") || source.includes("[AI_LOCAL_ERRO]") || source.includes("[AI_LOCAL_RUN]")) return;

    const blocks = extractEnvelopeBlocks(source);
    if (!blocks.length) return;

    const currentChatId = getCurrentChatId();

    for (const block of blocks) {
      let cmd;
      try {
        if (!/^\s*\{/.test(block.raw || "")) { continue; } // AIBRIDGE_INLINE_MARKER_PARSE_GUARD_061
        cmd = JSON.parse(block.raw);
      } catch (e) {
        sendLocalError("envelope_parse_error", "unknown", e && e.message ? e.message : String(e), block.raw);
        continue;
      }

      const commandId = String(cmd.command_id || "").trim();
      if (!commandId) {
        sendLocalError("envelope_missing_command_id", "unknown", "command_id ausente", block.raw);
        continue;
      }
      if (wasCaptured(commandId)) continue;

      if (cmd.source_chat_id && currentChatId && cmd.source_chat_id !== currentChatId) {
        sendLocalError("source_chat_id_mismatch", commandId, "source_chat_id do envelope nao corresponde ao chat atual", block.raw);
        continue;
      }

      cmd.source_chat_id = currentChatId || cmd.source_chat_id || "unknown";
      cmd.source_url = location.href;
      sendCommandToBackground(cmd);
    }
  }

  function collectCandidateText(element) {
    const candidates = [];
    const push = (el) => {
      if (!el || !(el instanceof Element)) return;
      if (isComposerOrInputNode(el)) return;
      const text = String(el.innerText || el.textContent || "").trim();
      if (text) candidates.push(text);
    };

    push(element);
    push(element.closest("article"));
    push(element.closest("[data-message-author-role]"));
    push(element.closest("[role='article']"));
    push(element.parentElement);

    candidates.sort((a, b) => a.length - b.length);
    return [...new Set(candidates)];
  }

  function tryCaptureFromElement(element) {
    if (!isChatGptPage()) return;
    if (!element || !(element instanceof Element)) return;
    if (isComposerOrInputNode(element)) return;

    for (const text of collectCandidateText(element)) {
      processText(text);
    }
  }

  function installObserver() {
    if (!isChatGptPage() || !document.body) return;

    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        if (mutation.type === "childList") {
          for (const node of mutation.addedNodes) {
            if (node instanceof Element) {
              window.setTimeout(() => tryCaptureFromElement(node), 300);
              window.setTimeout(() => tryCaptureFromElement(node), 1200);
            }
          }
        } else if (mutation.type === "characterData" && mutation.target && mutation.target.parentElement) {
          const parent = mutation.target.parentElement;
          window.setTimeout(() => tryCaptureFromElement(parent), 500);
        }
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true
    });

    console.log("[Local v" + CAPTURE_VERSION + "] ChatGPT outbound envelope observer installed for chat:", getCurrentChatId());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", installObserver, { once: true });
  } else {
    installObserver();
  }
})();


/* AI Bridge Local: ChatGPT candidate envelope periodic scanner. */
(function installAiBridgeChatGptCandidateEnvelopeScanner() {
  if (window.__AI_BRIDGE_CHATGPT_CANDIDATE_SCANNER_INSTALLED__) return;
  window.__AI_BRIDGE_CHATGPT_CANDIDATE_SCANNER_INSTALLED__ = true;

  const SCANNER_VERSION = "0.5.71";
  const START_MARKER = "@@" + "AI_BRIDGE_LOCAL_START" + "@@";
  const BEGIN_MARKER = "@@" + "AI_BRIDGE_LOCAL_BEGIN" + "@@";
  const END_MARKER = "@@" + "AI_BRIDGE_LOCAL_END" + "@@";
  const MAX_TEXT_CHARS = 30000;
  const SCAN_INTERVAL_MS = 1500;
  const CANDIDATE_SELECTOR = [
    "article",
    "[data-message-author-role]",
    "pre",
    "code",
    ".markdown",
    "[class*='message']",
    "[class*='response']",
    "[role='article']"
  ].join(",");

  function isChatGptCandidatePage() {
    return /chatgpt\.com/i.test(location.hostname);
  }

  function candidateStartsWithLocalStatus(text) {
    const t = String(text || "").trim();
    return t.startsWith("[AI_LOCAL]") || t.startsWith("[AI_LOCAL_ERRO]") || t.startsWith("[AI_LOCAL_RUN]");
  }

  function hasEnvelopeMarkers(text) {
    const t = String(text || "");
    return (t.includes(START_MARKER) || t.includes(BEGIN_MARKER)) &&
      t.includes(END_MARKER) &&
      t.includes("ai_bridge_local.envelope");
  }

  function getCandidateElements() {
    if (!document.body) return [];
    const nodes = Array.from(document.querySelectorAll(CANDIDATE_SELECTOR));
    const filtered = [];
    const seen = new WeakSet();

    for (const node of nodes) {
      if (!(node instanceof Element)) continue;
      if (seen.has(node)) continue;
      seen.add(node);

      const text = String(node.innerText || node.textContent || "").trim();
      if (!text || text.length > MAX_TEXT_CHARS) continue;
      if (!hasEnvelopeMarkers(text)) continue;
      if (candidateStartsWithLocalStatus(text)) continue;
      filtered.push(node);
    }

    return filtered;
  }

  function scanCandidateElements(reason) {
    if (!isChatGptCandidatePage()) return;
    const candidates = getCandidateElements();

    if (candidates.length) {
      console.log("[Local v" + SCANNER_VERSION + "] ChatGPT candidate scanner found", candidates.length, "candidate(s), reason=" + reason);
    }

    for (const node of candidates) {
      try {
        const text = String(node.innerText || node.textContent || "").trim();
        if (typeof extract === "function") {
          const cmds = extract(text);
          if (cmds && cmds.length) {
            console.log("[Local v" + SCANNER_VERSION + "] Candidate scanner extracted", cmds.length, "command(s)");
            for (const cmd of cmds) {
              try {
                if (typeof send === "function") {
                  send(cmd);
                } else {
                  chrome.runtime.sendMessage({ type: "AI_BRIDGE_BRIDGE_COMMAND", command: cmd });
                }
              } catch (sendError) {
                console.warn("[Local v" + SCANNER_VERSION + "] Candidate scanner send failed:", sendError && sendError.message);
              }
            }
          }
        }
      } catch (e) {
        console.warn("[Local v" + SCANNER_VERSION + "] Candidate scanner failed:", e && e.message);
      }
    }
  }

  function installCandidateScanner() {
    if (!isChatGptCandidatePage()) return;

    window.setTimeout(() => scanCandidateElements("startup_500ms"), 500);
    window.setTimeout(() => scanCandidateElements("startup_2000ms"), 2000);
    window.setInterval(() => scanCandidateElements("interval"), SCAN_INTERVAL_MS);

    if (document.body) {
      const observer = new MutationObserver(() => {
        window.setTimeout(() => scanCandidateElements("mutation"), 400);
      });
      observer.observe(document.body, { childList: true, subtree: true, characterData: true });
    }

    console.log("[Local v" + SCANNER_VERSION + "] ChatGPT candidate envelope scanner installed");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", installCandidateScanner, { once: true });
  } else {
    installCandidateScanner();
  }
})();


/* AI Bridge Local: ChatGPT standalone envelope scanner with visible feedback. */
(function installAiBridgeChatGptStandaloneEnvelopeScannerFeedback() {
  if (window.__AI_BRIDGE_CHATGPT_STANDALONE_SCANNER_FEEDBACK_INSTALLED__) return;
  window.__AI_BRIDGE_CHATGPT_STANDALONE_SCANNER_FEEDBACK_INSTALLED__ = true;

  const STANDALONE_VERSION = "0.5.71";
  const START_MARKER = "@@" + "AI_BRIDGE_LOCAL_START" + "@@";
  const BEGIN_MARKER = "@@" + "AI_BRIDGE_LOCAL_BEGIN" + "@@";
  const END_MARKER = "@@" + "AI_BRIDGE_LOCAL_END" + "@@";
  const LOCAL_SCHEMA = "ai_bridge_local.envelope";
  const MAX_TEXT_CHARS = 35000;
  const SCAN_INTERVAL_MS = 1400;
  const BOOTSTRAP_SUPPRESS_MS = 2500;
  const bootUntil = Date.now() + BOOTSTRAP_SUPPRESS_MS;
  const DEDUPE_PREFIX = "ai_bridge_standalone_scanner_seen:";
  const STATUS_PREFIXES = ["[AI_LOCAL]", "[AI_LOCAL_ERRO]", "[AI_LOCAL_RUN]"];
  const CANDIDATE_SELECTOR = [
    "article",
    "[data-message-author-role]",
    "pre",
    "code",
    ".markdown",
    "[class*='message']",
    "[class*='response']",
    "[role='article']"
  ].join(",");

  function isChatGptPage() {
    return /chatgpt\.com/i.test(location.hostname);
  }

  function safePart(value) {
    return String(value || "unknown").replace(/[^a-zA-Z0-9_-]+/g, "_").slice(0, 96);
  }

  function getCurrentChatId() {
    const href = String(location.href || "");
    const patterns = [
      /\/c\/([0-9a-fA-F-]{36})(?:[/?#]|$)/,
      /[?&]chat_id=([0-9a-fA-F-]{36})(?:&|$)/
    ];

    for (const pattern of patterns) {
      const match = href.match(pattern);
      if (match) return match[1];
    }

    return "";
  }

  function isLocalStatusText(text) {
    const t = String(text || "").trim();
    return STATUS_PREFIXES.some((prefix) => t.startsWith(prefix));
  }

  function hasEnvelopeMarkers(text) {
    const t = String(text || "");
    if (!t.includes(LOCAL_SCHEMA)) return false;
    const startRe = /(?:^|\n)[\t ]*(?:@@AI_BRIDGE_LOCAL_START@@|@@AI_BRIDGE_LOCAL_BEGIN@@)[\t ]*(?:\r?\n)/;
    const endRe = /(?:^|\n)[\t ]*@@AI_BRIDGE_LOCAL_END@@[\t ]*(?=\r?\n|$)/;
    return startRe.test(t) && endRe.test(t);
  }

  function extractEnvelopeBlocks(text) {
    const source = String(text || "");
    const blocks = [];
    const startPattern = "(@@AI_BRIDGE_LOCAL_START@@|@@AI_BRIDGE_LOCAL_BEGIN@@)";
    const regex = new RegExp("(?:^|\\n)[\\t ]*" + startPattern + "[\\t ]*\\r?\\n([\\s\\S]*?)\\r?\\n[\\t ]*@@AI_BRIDGE_LOCAL_END@@[\\t ]*(?=\\r?\\n|$)", "g"); // AIBRIDGE_LINE_ISOLATED_ENVELOPE_CAPTURE
    let match;

    while ((match = regex.exec(source)) !== null) {
      blocks.push({
        raw: String(match[2] || "").trim(),
        full: match[0]
      });
    }

    return blocks;
  }

  function normalizeCommand(cmd) {
    if (!cmd || typeof cmd !== "object" || Array.isArray(cmd)) {
      throw new Error("envelope_not_object");
    }

    const normalized = Object.assign({}, cmd);
    normalized.action = normalized.action || normalized.type;
    normalized.type = normalized.type || normalized.action;

    if (normalized.schema !== LOCAL_SCHEMA) {
      throw new Error("bad_schema");
    }

    if (!normalized.command_id) throw new Error("missing_command_id");
    if (!normalized.action) throw new Error("missing_action");
    if (!normalized.target_chat_id) throw new Error("missing_target_chat_id");
    if (!normalized.delivery_kind) throw new Error("missing_delivery_kind");

    if (normalized.action === "send-chat-message") {
      if (normalized.delivery_kind !== "inter_agent_message") throw new Error("send_chat_message_requires_inter_agent_message");
      if (!normalized.message) throw new Error("missing_message");
    }

    if (normalized.action === "run-command") {
      if (normalized.delivery_kind !== "local_capability") throw new Error("run_command_requires_local_capability");
      if (!normalized.payload || typeof normalized.payload !== "object" || Array.isArray(normalized.payload)) throw new Error("run_command_requires_payload_object");
    }

    const currentChatId = getCurrentChatId();
    if (currentChatId) {
      if (normalized.source_chat_id && normalized.source_chat_id !== currentChatId) {
        throw new Error("source_chat_id_mismatch:" + normalized.source_chat_id + ":current:" + currentChatId);
      }
      normalized.source_chat_id = currentChatId;
      normalized.source_url = location.href;
    }

    return normalized;
  }

  function seenKey(commandId) {
    return DEDUPE_PREFIX + safePart(commandId);
  }

  function hasSeen(commandId) {
    try {
      return Boolean(sessionStorage.getItem(seenKey(commandId)));
    } catch (_) {
      window.__AI_BRIDGE_STANDALONE_SEEN_IDS__ = window.__AI_BRIDGE_STANDALONE_SEEN_IDS__ || new Set();
      return window.__AI_BRIDGE_STANDALONE_SEEN_IDS__.has(String(commandId));
    }
  }

  function markSeen(commandId, reason) {
    try {
      sessionStorage.setItem(seenKey(commandId), String(Date.now()) + ":" + String(reason || ""));
    } catch (_) {
      window.__AI_BRIDGE_STANDALONE_SEEN_IDS__ = window.__AI_BRIDGE_STANDALONE_SEEN_IDS__ || new Set();
      window.__AI_BRIDGE_STANDALONE_SEEN_IDS__.add(String(commandId));
    }
  }

  function getCandidateTexts() {
    if (!document.body) return [];
    const nodes = Array.from(document.querySelectorAll(CANDIDATE_SELECTOR));
    const texts = [];
    const seenText = new Set();

    for (const node of nodes) {
      if (!(node instanceof Element)) continue;

      const text = String(node.innerText || node.textContent || "").trim();
      if (!text || text.length > MAX_TEXT_CHARS) continue;
      if (isLocalStatusText(text)) continue;
      if (!hasEnvelopeMarkers(text)) continue;
      if (seenText.has(text)) continue;

      seenText.add(text);
      texts.push(text);
    }

    return texts;
  }


function aiBridgeStandaloneElementVisible(element) {
  if (!element || !(element instanceof Element)) return false;

  const rect = element.getBoundingClientRect();
  const style = getComputedStyle(element);

  return rect.width > 0 &&
    rect.height > 0 &&
    style.visibility !== "hidden" &&
    style.display !== "none";
}

function aiBridgeStandaloneGetText(element) {
  if (!element) return "";
  if ("value" in element) return String(element.value || "");
  return String(element.innerText || element.textContent || "");
}

function aiBridgeStandaloneUsableComposer(element) {
  if (!element || !(element instanceof Element)) return false;
  if (!aiBridgeStandaloneElementVisible(element)) return false;

  const tag = String(element.tagName || "").toUpperCase();
  const type = String(element.getAttribute("type") || "").toLowerCase();
  const id = String(element.id || "").toLowerCase();
  const ariaHidden = String(element.getAttribute("aria-hidden") || "").toLowerCase();
  const disabled = element.disabled || String(element.getAttribute("aria-disabled") || "").toLowerCase() === "true";

  if (disabled) return false;
  if (ariaHidden === "true") return false;
  if (type === "file") return false;
  if (id.includes("upload")) return false;

  if (tag === "TEXTAREA") return true;

  if (tag === "INPUT") {
    return ["", "text", "search"].includes(type);
  }

  if (String(element.getAttribute("contenteditable") || "").toLowerCase() === "true") return true;
  if (String(element.getAttribute("role") || "").toLowerCase() === "textbox") return true;

  return false;
}

function aiBridgeStandaloneDescribeComposerElement(element) {
  if (!element || !(element instanceof Element)) return { found: false };

  return {
    found: true,
    tag: String(element.tagName || ""),
    id: String(element.id || ""),
    role: String(element.getAttribute("role") || ""),
    contenteditable: String(element.getAttribute("contenteditable") || ""),
    testid: String(element.getAttribute("data-testid") || ""),
    aria_label: String(element.getAttribute("aria-label") || ""),
    type: String(element.getAttribute("type") || ""),
    class_name: String(element.className || "").slice(0, 160),
    text_length: aiBridgeStandaloneGetText(element).trim().length
  };
}

function aiBridgeStandaloneFindPreferredComposer() {
  const preferredSelectors = [
    "#prompt-textarea.ProseMirror[contenteditable='true']",
    "div#prompt-textarea[contenteditable='true'][role='textbox']",
    "#prompt-textarea[contenteditable='true']",
    "#prompt-textarea",
    "[data-testid='prompt-textarea']",
    "[aria-label='Converse com o ChatGPT'][contenteditable='true']",
    "[aria-label='Message ChatGPT'][contenteditable='true']",
    "[aria-label='Send a message'][contenteditable='true']",
    "main form .ProseMirror[contenteditable='true']",
    "form .ProseMirror[contenteditable='true']",
    ".ProseMirror[contenteditable='true'][role='textbox']"
  ];

  for (const selector of preferredSelectors) {
    const element = document.querySelector(selector);
    if (aiBridgeStandaloneUsableComposer(element)) return element;
  }

  const fallbackSelectors = [
    "textarea:not([type='file'])",
    "input:not([type='file']):not(#upload-photos):not(#upload-camera)",
    "[contenteditable='true'][role='textbox']",
    "[contenteditable='true']",
    "[role='textbox']"
  ];

  for (const selector of fallbackSelectors) {
    const elements = Array.from(document.querySelectorAll(selector));
    for (const element of elements) {
      if (aiBridgeStandaloneUsableComposer(element)) return element;
    }
  }

  return null;
}


function findComposer() {
  const aiBridgePreferredComposer = aiBridgeStandaloneFindPreferredComposer();
  if (aiBridgePreferredComposer) {
    console.log("[Local v" + STANDALONE_VERSION + "] standalone using preferred ChatGPT composer", aiBridgeStandaloneDescribeComposerElement(aiBridgePreferredComposer));
    return aiBridgePreferredComposer;
  }
    const selectors = [
      "#prompt-textarea",
      "[data-testid='composer'] [contenteditable='true']",
      "[contenteditable='true'][role='textbox']",
      "[contenteditable='true']",
      "textarea",
      "[role='textbox']"
    ];

    for (const selector of selectors) {
      const el = document.querySelector(selector);
      if (el) return el;
    }

    return null;
  }

  function setComposerText(composer, text) {
    composer.focus();

    if (composer.tagName === "TEXTAREA" || composer.tagName === "INPUT") {
      composer.value = text;
      composer.dispatchEvent(new Event("input:not([type='file']):not(#upload-photos):not(#upload-camera)", { bubbles: true }));
      composer.dispatchEvent(new Event("change", { bubbles: true }));
      return;
    }

    try {
      composer.textContent = "";
      composer.dispatchEvent(new InputEvent("beforeinput", {
        bubbles: true,
        inputType: "insertText",
        data: text
      }));
    } catch (_) {}

    try {
      document.execCommand("insertText", false, text);
    } catch (_) {
      composer.textContent = text;
    }

    composer.dispatchEvent(new InputEvent("input:not([type='file']):not(#upload-photos):not(#upload-camera)", {
      bubbles: true,
      inputType: "insertText",
      data: text
    }));
  }

  function findSendButton() {
    const selectors = [
      "button[data-testid='send-button']",
      "button[aria-label='Send prompt']",
      "button[aria-label='Send message']",
      "button[aria-label*='Send']",
      "button[type='submit']"
    ];

    for (const selector of selectors) {
      const btn = document.querySelector(selector);
      if (btn && !btn.disabled && btn.getAttribute("aria-disabled") !== "true") return btn;
    }

    return null;
  }

  function injectVisibleStatus(text, statusId) {
    window.setTimeout(() => {
      try {
        const composer = findComposer();
        if (!composer) {
          console.warn("[Local v" + STANDALONE_VERSION + "] visible status failed: no composer", statusId);
          return;
        }

        setComposerText(composer, text);

        window.setTimeout(() => {
          const btn = findSendButton();
          if (btn) {
            btn.click();
            console.log("[Local v" + STANDALONE_VERSION + "] visible status sent", statusId);
            return;
          }

          try {
            composer.dispatchEvent(new KeyboardEvent("keydown", {
              bubbles: true,
              cancelable: true,
              key: "Enter",
              code: "Enter",
              which: 13,
              keyCode: 13
            }));
          } catch (_) {}

          console.log("[Local v" + STANDALONE_VERSION + "] visible status attempted enter", statusId);
        }, 350);
      } catch (e) {
        console.warn("[Local v" + STANDALONE_VERSION + "] visible status error", statusId, e && e.message);
      }
    }, 350);
  }

  function directOkStatus(cmd, response) {
    return [
      "[AI_LOCAL]",
      "comando enviado direto pela extensao",
      "id=" + String(cmd.command_id || "unknown"),
      "status=sent_direct",
      "versao=" + STANDALONE_VERSION,
      "no_reply=1",
      "origem=" + String(cmd.source_chat_id || getCurrentChatId() || "unknown"),
      "destino=" + String(cmd.target_chat_id || "unknown"),
      "observacao=Mensagem inter-chat entregue sem gateway/DB. Nao precisa responder a esta mensagem."
    ].join("\n");
  }

  function errorStatus(cmd, error, detail) {
    const commandId = cmd && cmd.command_id ? cmd.command_id : "unknown";
    const target = cmd && cmd.target_chat_id ? cmd.target_chat_id : "unknown";
    const source = cmd && cmd.source_chat_id ? cmd.source_chat_id : (getCurrentChatId() || "unknown");

    return [
      "[AI_LOCAL_ERRO]",
      "acao=verifique_destino_ou_reenvie",
      "no_reply=0",
      "executado=nao",
      "tipo=direct_interchat_or_capture_failed",
      "versao=" + STANDALONE_VERSION,
      "id_original=" + String(commandId),
      "chat_atual=" + String(getCurrentChatId() || "unknown"),
      "origem=" + String(source),
      "destino=" + String(target),
      "erro=" + String(error || "unknown_error").replace(/[\r\n]+/g, " ").slice(0, 700),
      "detalhe=" + String(detail || "").replace(/[\r\n]+/g, " ").slice(0, 700),
      "correcao=Recarregue a aba destino para registrar o chat_id, confira target_chat_id, ou reenvie com force_gateway=true se quiser usar gateway."
    ].join("\n");
  }

  function sendCommandToBackground(cmd, raw) {
    const commandId = String(cmd.command_id || "unknown");
    if (hasSeen(commandId)) return;
    markSeen(commandId, "send_start");

    console.log("[Local v" + STANDALONE_VERSION + "] Standalone scanner sending command", commandId, cmd.action, cmd.delivery_kind);

    chrome.runtime.sendMessage({ type: "AI_BRIDGE_BRIDGE_COMMAND", command: cmd }, (response) => {
      const runtimeError = chrome.runtime.lastError;
      if (runtimeError) {
        const msg = runtimeError.message || "runtime_error";
        console.warn("[Local v" + STANDALONE_VERSION + "] Standalone scanner runtime error:", msg);
        injectVisibleStatus(errorStatus(cmd, msg, "chrome.runtime.lastError"), "runtime_" + commandId);
        return;
      }

      if (response && response.ok) {
        console.log("[Local v" + STANDALONE_VERSION + "] Standalone scanner background ok:", commandId, JSON.stringify(response));
        if (response.direct) {
          injectVisibleStatus(directOkStatus(cmd, response), "direct_ok_" + commandId);
        }
        return;
      }

      const err = response && response.error ? response.error : "background_rejected_command";
      console.warn("[Local v" + STANDALONE_VERSION + "] Standalone scanner background rejected:", commandId, JSON.stringify(response || {}));
      injectVisibleStatus(errorStatus(cmd, err, JSON.stringify(response || {})), "direct_err_" + commandId);
    });
  }

  function processText(text, reason, bootstrapOnly, sourceNode) {
    const blocks = extractEnvelopeBlocks(text);
    if (!blocks.length) return;

    for (const block of blocks) {
      let parsed;
      try {
        if (!/^\s*\{/.test(block.raw || "")) { continue; } // AIBRIDGE_INLINE_MARKER_PARSE_GUARD_061
        parsed = JSON.parse(block.raw);
      } catch (e) {
        continue;
      }

      let cmd;
      try {
        cmd = normalizeCommand(parsed);
      } catch (e) {
        const rawCommandId = parsed && parsed.command_id ? parsed.command_id : "unknown";
        if (!hasSeen(rawCommandId) && !bootstrapOnly && Date.now() >= bootUntil) {
          markSeen(rawCommandId, "normalize_error");
          injectVisibleStatus(errorStatus(parsed || {}, e && e.message, "normalizeCommand"), "normalize_" + rawCommandId);
        }
        continue;
      }

      if (bootstrapOnly || Date.now() < bootUntil) {
        markSeen(cmd.command_id, "bootstrap_existing");
        continue;
      }

      sendCommandToBackground(cmd, block.raw);
    }
  }

  function scan(reason, bootstrapOnly) {
    if (!isChatGptPage()) return;

    const texts = getCandidateTexts();
    if (texts.length) {
      console.log("[Local v" + STANDALONE_VERSION + "] Standalone candidate scan", reason, "candidates=" + texts.length, "bootstrapOnly=" + Boolean(bootstrapOnly));
    }

    for (const text of texts) {
      processText(text, reason, bootstrapOnly, null);
    }
  }

  function install() {
    if (!isChatGptPage()) return;

    scan("bootstrap_existing", true);

    window.setTimeout(() => scan("startup_after_bootstrap", false), BOOTSTRAP_SUPPRESS_MS + 300);
    window.setInterval(() => scan("interval", false), SCAN_INTERVAL_MS);

    if (document.body) {
      const observer = new MutationObserver(() => {
        window.setTimeout(() => scan("mutation", false), 450);
      });
      observer.observe(document.body, { childList: true, subtree: true, characterData: true });
    }

    console.log("[Local v" + STANDALONE_VERSION + "] ChatGPT standalone envelope scanner with visible feedback installed");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", install, { once: true });
  } else {
    install();
  }
})();


/* AI Bridge Local: DeepSeek outbound envelope capture with inline receipt after envelope 0.5.66. */
(function installAiBridgeDeepSeekCapturedEnvelopeBridge() {
  if (window.__AI_BRIDGE_DEEPSEEK_CAPTURE_INSTALLED__) return;
  window.__AI_BRIDGE_DEEPSEEK_CAPTURE_INSTALLED__ = true;

  const CAPTURE_VERSION = "0.5.71";
  const START_MARKER = "@@" + "AI_BRIDGE_LOCAL_START" + "@@";
  const END_MARKER = "@@" + "AI_BRIDGE_LOCAL_END" + "@@";
  const MAX_CAPTURE_CHARS = 30000;
  const DEDUPE_PREFIX = "ai_bridge_deepseek_captured_envelope:";
  const BOOTSTRAP_MS = 2500;
  const bootUntil = Date.now() + BOOTSTRAP_MS;

  function isDeepSeekPage() {
    return /(^|\.)chat\.deepseek\.com$/i.test(location.hostname || "");
  }

  function getDeepSeekChatId() {
    const href = String(location.href || "");
    const match = href.match(/\/a\/chat\/s\/([^/?#]+)/i);
    return match ? decodeURIComponent(match[1]) : "";
  }

  function countOccurrences(haystack, needle) {
    let count = 0;
    let offset = 0;
    while (true) {
      const foundAt = haystack.indexOf(needle, offset);
      if (foundAt < 0) break;
      count += 1;
      offset = foundAt + needle.length;
    }
    return count;
  }

  function extractEnvelopeBlocks(rawText) {
    const text = String(rawText || "");
    if (!text || !text.includes(START_MARKER) || !text.includes(END_MARKER)) return [];
    if (text.length > MAX_CAPTURE_CHARS) return [];

    const blocks = [];
    let offset = 0;
    while (offset < text.length) {
      const start = text.indexOf(START_MARKER, offset);
      if (start < 0) break;
      const bodyStart = start + START_MARKER.length;
      const end = text.indexOf(END_MARKER, bodyStart);
      if (end < 0) break;

      const raw = text.slice(bodyStart, end).trim();
      const rawTextBlock = text.slice(start, end + END_MARKER.length).trim();
      blocks.push({ raw, raw_text: rawTextBlock });
      offset = end + END_MARKER.length;
    }
    return blocks;
  }

  function wasCaptured(commandId) {
    if (!commandId) return true;
    const key = DEDUPE_PREFIX + commandId;
    try {
      if (sessionStorage.getItem(key) === "1") return true;
      sessionStorage.setItem(key, "1");
      return false;
    } catch (_) {
      window.__AI_BRIDGE_DEEPSEEK_CAPTURED_IDS__ = window.__AI_BRIDGE_DEEPSEEK_CAPTURED_IDS__ || new Set();
      if (window.__AI_BRIDGE_DEEPSEEK_CAPTURED_IDS__.has(commandId)) return true;
      window.__AI_BRIDGE_DEEPSEEK_CAPTURED_IDS__.add(commandId);
      return false;
    }
  }

  function isComposerOrInputNode(node) {
    if (!node || !(node instanceof Element)) return false;
    return Boolean(node.closest('textarea,input,[contenteditable="true"],[role="textbox"],form'));
  }

  function parseBlock(block) {
    let envelope;
    try {
      if (!/^\s*\{/.test(block.raw || "")) { return { ok: false, error: "non_json_envelope_block" }; } // AIBRIDGE_INLINE_MARKER_PARSE_GUARD_061
      envelope = JSON.parse(block.raw);
    } catch (err) {
      return { ok: false, error: "json_parse_error" };
    }

    if (!envelope || typeof envelope !== "object" || Array.isArray(envelope)) {
      return { ok: false, error: "envelope_not_object" };
    }

    const commandId = String(envelope.command_id || "").trim();
    const sourceChatId = String(envelope.source_chat_id || "").trim();
    const targetChatId = String(envelope.target_chat_id || "").trim();
    const action = String(envelope.action || envelope.type || "").trim();
    const deliveryKind = String(envelope.delivery_kind || "").trim();
    const currentChatId = getDeepSeekChatId();

    if (!commandId) return { ok: false, error: "missing_command_id" };
    if (!currentChatId) return { ok: false, error: "deepseek_chat_id_unknown" };
    if (sourceChatId !== currentChatId) return { ok: false, error: "source_chat_id_mismatch" };
    if (!targetChatId) return { ok: false, error: "missing_target_chat_id" };
    if (action !== "send-chat-message" && action !== "run-command") return { ok: false, error: "action_not_allowed" };
    if (action === "send-chat-message" && deliveryKind !== "inter_agent_message") {
      return { ok: false, error: "send_chat_message_requires_inter_agent_message" };
    }
    if (action === "run-command" && deliveryKind !== "local_capability") {
      return { ok: false, error: "run_command_requires_local_capability" };
    }

    return {
      ok: true,
      command_id: commandId,
      envelope,
      raw_text: block.raw_text
    };
  }

  function showNotice(kind, title, detail) {
    try {
      const id = "ai-bridge-deepseek-capture-notice";
      let box = document.getElementById(id);
      if (!box) {
        box = document.createElement("div");
        box.id = id;
        box.style.position = "fixed";
        box.style.zIndex = "2147483647";
        box.style.right = "16px";
        box.style.bottom = "16px";
        box.style.maxWidth = "520px";
        box.style.padding = "10px 12px";
        box.style.borderRadius = "10px";
        box.style.fontFamily = "Arial, sans-serif";
        box.style.fontSize = "12px";
        box.style.lineHeight = "1.35";
        box.style.boxShadow = "0 8px 24px rgba(0,0,0,.24)";
        document.documentElement.appendChild(box);
      }
      box.style.background = kind === "error" ? "#4b1111" : kind === "warn" ? "#4a3608" : "#102a16";
      box.style.color = "#fff";
      box.textContent = title + (detail ? "\n" + detail : "");
      clearTimeout(window.__AI_BRIDGE_DEEPSEEK_CAPTURE_NOTICE_TIMER__);
      window.__AI_BRIDGE_DEEPSEEK_CAPTURE_NOTICE_TIMER__ = setTimeout(() => {
        try { box.remove(); } catch (_) {}
      }, 9000);
    } catch (_) {}
  }



  function sanitizeReceiptId(value) {
    return String(value || "unknown").replace(/[^a-zA-Z0-9_-]+/g, "_").slice(0, 180);
  }

  function formatReceiptLines(lines) {
    return (lines || []).filter(Boolean).join("\n");
  }

  function nodeTextContainsEnvelope(node, commandId) {
    try {
      if (!node) return false;
      const text = String(node.innerText || node.textContent || "");
      return text.includes(commandId) && text.includes(START_MARKER) && text.includes(END_MARKER);
    } catch (_) {
      return false;
    }
  }

  function isBadReceiptAnchor(node) {
    try {
      if (!node || !(node instanceof Element)) return true;
      if (node === document.body || node === document.documentElement) return true;
      if (node.closest('[data-ai-bridge-deepseek-receipt="1"]')) return true;
      if (isComposerOrInputNode(node)) return true;
      return false;
    } catch (_) {
      return true;
    }
  }

  function chooseSmallestEnvelopeElement(commandId, preferredNode) {
    const candidates = [];

    function pushCandidate(node, reason) {
      if (!node || !(node instanceof Element)) return;
      if (isBadReceiptAnchor(node)) return;
      if (!nodeTextContainsEnvelope(node, commandId)) return;
      const len = String(node.innerText || node.textContent || "").length;
      if (len < 20 || len > MAX_CAPTURE_CHARS + 5000) return;
      candidates.push({ node, len, reason });
    }

    try {
      if (preferredNode && preferredNode instanceof Element) {
        pushCandidate(preferredNode, "preferred");
        const closest = preferredNode.closest('[data-testid], [data-message-id], [class*="message"], [class*="chat"], [class*="markdown"], .ds-markdown, article, section, div');
        pushCandidate(closest, "closest");
        let p = preferredNode.parentElement;
        let depth = 0;
        while (p && depth < 6) {
          pushCandidate(p, "parent");
          p = p.parentElement;
          depth += 1;
        }
      }

      const selectors = [
        ".ds-markdown",
        '[class*="markdown"]',
        '[class*="message"]',
        '[data-message-id]',
        '[data-testid]',
        "article",
        "section",
        "pre",
        "code",
        "div"
      ];

      for (const sel of selectors) {
        const nodes = document.querySelectorAll(sel);
        for (const node of nodes) {
          pushCandidate(node, sel);
          if (candidates.length > 80) break;
        }
        if (candidates.length > 80) break;
      }
    } catch (_) {}

    candidates.sort((a, b) => a.len - b.len);
    return candidates.length ? candidates[0].node : null;
  }

  function findDeepSeekEnvelopeAnchor(parsed) {
    try {
      const commandId = parsed && parsed.command_id ? parsed.command_id : "";
      if (!commandId) return null;

      let sourceNode = parsed && parsed.source_node ? parsed.source_node : null;
      if (sourceNode && sourceNode.nodeType === Node.TEXT_NODE) {
        sourceNode = sourceNode.parentElement;
      }

      const best = chooseSmallestEnvelopeElement(commandId, sourceNode);
      if (best) return best;
    } catch (err) {
      console.warn("[Local v" + CAPTURE_VERSION + "] DeepSeek receipt anchor lookup failed:", err && err.message ? err.message : err);
    }
    return null;
  }

  function insertReceiptAfterAnchor(receipt, anchor) {
    try {
      if (!receipt || !anchor || !anchor.parentNode) return false;
      if (anchor.nextSibling === receipt) return true;

      anchor.parentNode.insertBefore(receipt, anchor.nextSibling);
      receipt.scrollIntoView({ block: "nearest", behavior: "smooth" });
      return true;
    } catch (err) {
      console.warn("[Local v" + CAPTURE_VERSION + "] DeepSeek inline receipt insert failed:", err && err.message ? err.message : err);
      return false;
    }
  }

  function appendPersistentReceipt(parsed, kind, title, lines) {
    try {
      const commandId = parsed && parsed.command_id ? parsed.command_id : "unknown";
      const receiptId = "ai-bridge-deepseek-persistent-receipt-" + sanitizeReceiptId(commandId);

      let receipt = document.getElementById(receiptId);
      if (!receipt) {
        receipt = document.createElement("div");
        receipt.id = receiptId;
        receipt.setAttribute("data-ai-bridge-deepseek-receipt", "1");
        receipt.style.margin = "10px 0";
        receipt.style.padding = "10px 12px";
        receipt.style.borderRadius = "10px";
        receipt.style.whiteSpace = "pre-wrap";
        receipt.style.fontFamily = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace";
        receipt.style.fontSize = "12px";
        receipt.style.lineHeight = "1.35";
        receipt.style.border = "1px solid rgba(255,255,255,.22)";
        receipt.style.boxShadow = "0 4px 14px rgba(0,0,0,.20)";
      }

      receipt.style.background = kind === "error" ? "rgba(120, 20, 20, .94)" : kind === "warn" ? "rgba(120, 82, 10, .94)" : "rgba(15, 95, 45, .94)";
      receipt.style.color = "#fff";

      receipt.textContent = title + "\n" + formatReceiptLines(lines);

      const anchor = findDeepSeekEnvelopeAnchor(parsed);
      if (insertReceiptAfterAnchor(receipt, anchor)) {
        console.log("[Local v" + CAPTURE_VERSION + "] DeepSeek inline receipt inserted after envelope:", commandId);
        return;
      }

      let panel = document.getElementById("ai-bridge-deepseek-persistent-receipt-panel");
      if (!panel) {
        panel = document.createElement("div");
        panel.id = "ai-bridge-deepseek-persistent-receipt-panel";
        panel.style.position = "fixed";
        panel.style.zIndex = "2147483646";
        panel.style.right = "16px";
        panel.style.bottom = "16px";
        panel.style.width = "min(560px, calc(100vw - 32px))";
        panel.style.maxHeight = "45vh";
        panel.style.overflow = "auto";
        panel.style.pointerEvents = "auto";
        document.documentElement.appendChild(panel);
      }

      if (receipt.parentNode !== panel) {
        panel.appendChild(receipt);
      }

      console.warn("[Local v" + CAPTURE_VERSION + "] DeepSeek inline receipt anchor not found; used fixed panel:", commandId);
    } catch (err) {
      console.warn("[Local v" + CAPTURE_VERSION + "] DeepSeek persistent receipt failed:", err && err.message ? err.message : err);
    }
  }


  function sendCapturedEnvelope(parsed) {
    if (wasCaptured(parsed.command_id)) return;

    console.log("[Local v" + CAPTURE_VERSION + "] DeepSeek outbound scanner sending", parsed.command_id);

    chrome.runtime.sendMessage({
      type: "AI_BRIDGE_CAPTURED_ENVELOPE",
      source_chat_id: getDeepSeekChatId(),
      raw_text: parsed.raw_text,
      envelope: parsed.envelope
    }, (response) => {
      const runtimeError = chrome.runtime.lastError;
      if (runtimeError) {
        const msg = runtimeError.message || "runtime_error";
        console.warn("[Local v" + CAPTURE_VERSION + "] DeepSeek captured envelope runtime error:", msg);
        appendPersistentReceipt(parsed, "error", "[AI_LOCAL_ERRO] DeepSeek watcher local", [
          "id=" + parsed.command_id,
          "status=runtime_error",
          "versao=" + CAPTURE_VERSION,
          "origem=" + getDeepSeekChatId(),
          "destino=" + (parsed.envelope && parsed.envelope.target_chat_id ? parsed.envelope.target_chat_id : "unknown"),
          "erro=" + msg
        ]);
        showNotice("error", "[AI_LOCAL_ERRO] DeepSeek watcher local", "id=" + parsed.command_id + "\nerro=" + msg);
        return;
      }

      if (response && response.ok) {
        console.log("[Local v" + CAPTURE_VERSION + "] DeepSeek captured envelope accepted:", parsed.command_id);
        const directFlag = response && response.direct ? "sent_direct" : "accepted";
        appendPersistentReceipt(parsed, "success", "[AI_LOCAL] DeepSeek watcher local", [
          "envelope capturado e entregue pela extensao",
          "id=" + parsed.command_id,
          "status=" + directFlag,
          "versao=" + CAPTURE_VERSION,
          "origem=" + getDeepSeekChatId(),
          "destino=" + (parsed.envelope && parsed.envelope.target_chat_id ? parsed.envelope.target_chat_id : "unknown"),
          "observacao=Mensagem inter-chat enviada pelo watcher local."
        ]);
        showNotice("success", "[AI_LOCAL] DeepSeek watcher local", "envelope enviado\nid=" + parsed.command_id);
        return;
      }

      const err = response && response.error ? response.error : "background_rejected_captured_envelope";
      console.warn("[Local v" + CAPTURE_VERSION + "] DeepSeek captured envelope rejected:", parsed.command_id, JSON.stringify(response || {}));
      appendPersistentReceipt(parsed, "error", "[AI_LOCAL_ERRO] DeepSeek watcher local", [
        "id=" + parsed.command_id,
        "status=rejected",
        "versao=" + CAPTURE_VERSION,
        "origem=" + getDeepSeekChatId(),
        "destino=" + (parsed.envelope && parsed.envelope.target_chat_id ? parsed.envelope.target_chat_id : "unknown"),
        "erro=" + err
      ]);
      showNotice("error", "[AI_LOCAL_ERRO] DeepSeek watcher local", "id=" + parsed.command_id + "\nerro=" + err);
    });
  }

  function processText(text, reason, bootstrapOnly, sourceNode) {
    const blocks = extractEnvelopeBlocks(text);
    if (!blocks.length) return;

    for (const block of blocks) {
      const parsed = parseBlock(block);
      if (!parsed.ok) continue;

      if (bootstrapOnly || Date.now() < bootUntil) {
        wasCaptured(parsed.command_id);
        continue;
      }

      parsed.source_node = sourceNode || null;
      sendCapturedEnvelope(parsed);
    }
  }

  function scanNode(node, reason, bootstrapOnly) {
    if (!node) return;

    if (node.nodeType === Node.TEXT_NODE) {
      processText(node.textContent || "", reason, bootstrapOnly, node.parentElement || null);
      return;
    }

    if (!(node instanceof Element)) return;
    if (isComposerOrInputNode(node)) return;

    const text = node.innerText || node.textContent || "";
    processText(text, reason, bootstrapOnly, null);
  }

  function scanDocument(reason, bootstrapOnly) {
    if (!document.body) return;
    scanNode(document.body, reason, bootstrapOnly);
  }

  function installObserver() {
    if (!isDeepSeekPage()) return;
    if (!document.body) return;

    scanDocument("bootstrap", true);

    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        for (const node of mutation.addedNodes || []) {
          scanNode(node, "mutation", false);
        }
        if (mutation.type === "characterData" && mutation.target) {
          scanNode(mutation.target, "characterData", false);
        }
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true
    });

    setTimeout(() => scanDocument("post_bootstrap", false), BOOTSTRAP_MS + 500);
    setInterval(() => scanDocument("interval", false), 5000);

    console.log("[Local v" + CAPTURE_VERSION + "] DeepSeek outbound envelope observer installed for chat:", getDeepSeekChatId());
  }

  if (!isDeepSeekPage()) return;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", installObserver, { once: true });
  } else {
    installObserver();
  }
})();
