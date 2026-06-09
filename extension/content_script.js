// AI Bridge Local v0.3.8 - Receptor local
(() => {
  const VERSION = "0.3.8";
  console.log("[Local v" + VERSION + "] Active");

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
    return document.querySelector('textarea, [contenteditable="true"], #prompt-textarea, [role="textbox"]');
  }

  function setText(el, text) {
    el.focus();
    if (el.tagName === "TEXTAREA" || el.tagName === "INPUT") {
      const nativeSetter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
      nativeSetter.call(el, text);
    } else {
      el.textContent = text;
    }
    el.dispatchEvent(new InputEvent("input", {bubbles: true, cancelable: true, inputType: "insertText", data: text}));
    el.dispatchEvent(new InputEvent("change", {bubbles: true}));
    el.dispatchEvent(new Event("blur", {bubbles: true}));
    el.dispatchEvent(new Event("focus", {bubbles: true}));
  }

  // RECEPTOR
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message && message.type === "AI_BRIDGE_INJECT_TEXT") {
      const text = message.action?.text || message.text || "";
      if (!text) { sendResponse({ok: false}); return false; }
      const composer = findComposer();
      if (!composer) { sendResponse({ok: false, reason: "no_composer"}); return false; }
      setText(composer, text);
      // Aguarda o botao send aparecer
      let attempts = 0;
      const tryClick = () => {
        const btn = document.querySelector('[data-testid="send-button"]:not([disabled]), button[aria-label*="Enviar"]:not([disabled]), button[aria-label*="Send"]:not([disabled])');
        if (btn) {
          btn.click();
          console.log("[Local] Sent after " + (attempts * 200) + "ms");
        } else if (attempts < 15) {
          attempts++;
          setTimeout(tryClick, 200);
        } else {
          composer.dispatchEvent(new KeyboardEvent("keydown", {key: "Enter", code: "Enter", keyCode: 13, which: 13, bubbles: true}));
          console.log("[Local] Enter fallback");
        }
      };
      setTimeout(() => { composer.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true})); console.log('[Local] Enter sent'); }, 800);
      sendResponse({ok: true});
      return true;
    }
  });

  // EXTRATOR
  function extract(text) {
    const cmds = [];
    const regex = /<<<BRIDGE_ASSISTANT_COMMAND_START>>>\s*([\s\S]*?)\s*<<<BRIDGE_ASSISTANT_COMMAND_END>>>/g;
    let m;
    while ((m = regex.exec(text)) !== null) {
      try { const c = JSON.parse(m[1].trim()); if (c.command_id) cmds.push(c); } catch(e) {}
    }
    return cmds;
  }

  const sentIds = new Set();
  function send(cmd) { if (sentIds.has(cmd.command_id)) return; sentIds.add(cmd.command_id); if (sentIds.size > 50) sentIds.clear();
    chrome.runtime.sendMessage({type:"AI_BRIDGE_BRIDGE_COMMAND", command:cmd});
  }

  let last = "";
  setInterval(() => {
    const t = document.body?.innerText || "";
    if (t !== last) { last = t; extract(t).forEach(send); }
  }, 2000);
})();
