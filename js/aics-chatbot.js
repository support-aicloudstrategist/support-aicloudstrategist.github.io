(() => {
  if (window.__AICS_CHATBOT__) return;
  window.__AICS_CHATBOT__ = true;

  const SESSION_KEY = "aicsChatSession";
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const isNarrow = window.matchMedia("(max-width: 820px)").matches;

  const mountChatbot = () => {
  if (document.querySelector(".aics-chat")) return;

  const getSessionId = () => {
    try {
      const existing = sessionStorage.getItem(SESSION_KEY);
      if (existing) return existing;
      const id = `web-${crypto.randomUUID()}`;
      sessionStorage.setItem(SESSION_KEY, id);
      return id;
    } catch (_) {
      return `web-${Date.now()}`;
    }
  };

  const history = [];
  const sessionId = getSessionId();

  const localKnowledgeReply = (message) => {
    const hay = String(message || "").toLowerCase();
    const entries = [
      ["price|pricing|fee|cost|how much", "Fit review is free. Typical single-estate diagnostic: USD 2,500–3,000 (India visitors see an INR band). Complex multi-cloud/GPU work: USD 5,500–12,000. Fixed fee after scope — no savings share."],
      ["fit review|book|start|contact", "Start with a free fit review at /request-fit-review/. No billing files or credentials required to begin."],
      ["aws|azure|gcp|kubernetes|k8s|gpu|ai", "The diagnostic covers material spend in scope across AWS, Azure, GCP, Kubernetes, and AI/GPU or model estates."],
      ["process|how it works|timeline", "Process: free fit review → evidence intake → ownership map → 30-day action plan. Typical single-estate readout is 10–15 business days after complete evidence intake."],
      ["guarantee|savings|risk|roi", "We do not guarantee savings percentages. Recommendations use act / investigate / hold so thin evidence does not become a forced cut."],
      ["service|diagnostic|finops|what do you", "AICloudStrategist offers one fixed-fee Cloud & AI Cost Governance Diagnostic: connect spend to owners, then prioritize safe next actions."],
    ];
    for (const [pattern, answer] of entries) {
      if (new RegExp(pattern, "i").test(hay)) return `${answer} Book a free fit review at /request-fit-review/.`;
    }
    return "Ask about scope, pricing, process, platforms, or the free fit review—or go to /request-fit-review/.";
  };

  const root = document.createElement("div");
  root.className = "aics-chat";
  root.innerHTML = `
    <button type="button" class="aics-chat-launcher" aria-expanded="false" aria-controls="aics-chat-panel" aria-label="Open chat">
      <span class="aics-chat-bot" aria-hidden="true">
        <svg class="aics-chat-bot-svg" viewBox="0 0 100 108" width="72" height="78" focusable="false">
          <defs>
            <linearGradient id="aicsBotPastel" x1="18%" y1="8%" x2="82%" y2="95%">
              <stop offset="0%" stop-color="#ffffff"/>
              <stop offset="42%" stop-color="#e8faf7"/>
              <stop offset="100%" stop-color="#b8ebe4"/>
            </linearGradient>
            <linearGradient id="aicsBotBelly" x1="30%" y1="0%" x2="70%" y2="100%">
              <stop offset="0%" stop-color="#ffffff"/>
              <stop offset="100%" stop-color="#dff7f3"/>
            </linearGradient>
            <radialGradient id="aicsBotCheek" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#ffb7c8" stop-opacity="0.9"/>
              <stop offset="100%" stop-color="#ffb7c8" stop-opacity="0"/>
            </radialGradient>
          </defs>
          <ellipse class="aics-bot-shadow" cx="50" cy="101" rx="22" ry="4.5" fill="rgba(8,121,137,0.16)"/>
          <g class="aics-bot-figure">
            <g class="aics-bot-leg aics-bot-leg-left">
              <ellipse cx="38" cy="88" rx="8" ry="10" fill="#c9efe9"/>
              <ellipse cx="36" cy="96" rx="9" ry="5" fill="#dff7f3"/>
            </g>
            <g class="aics-bot-leg aics-bot-leg-right">
              <ellipse cx="62" cy="88" rx="8" ry="10" fill="#c9efe9"/>
              <ellipse cx="64" cy="96" rx="9" ry="5" fill="#dff7f3"/>
            </g>
            <g class="aics-bot-arm aics-bot-arm-left">
              <ellipse cx="22" cy="58" rx="9" ry="12" fill="#d4f3ee"/>
              <circle cx="18" cy="68" r="6.5" fill="#e8faf7"/>
            </g>
            <ellipse class="aics-bot-body" cx="50" cy="62" rx="28" ry="26" fill="url(#aicsBotPastel)"/>
            <ellipse cx="50" cy="68" rx="16" ry="12" fill="url(#aicsBotBelly)" opacity="0.9"/>
            <g class="aics-bot-head">
              <circle cx="50" cy="34" r="22" fill="url(#aicsBotPastel)"/>
              <circle cx="50" cy="12" r="4.5" fill="#d4f3ee"/>
              <circle cx="50" cy="8" r="3.2" fill="#9ee8e0"/>
              <ellipse cx="38" cy="40" rx="6" ry="3.5" fill="url(#aicsBotCheek)"/>
              <ellipse cx="62" cy="40" rx="6" ry="3.5" fill="url(#aicsBotCheek)"/>
              <g class="aics-bot-eyes">
                <ellipse cx="41" cy="32" rx="7" ry="8" fill="#fff"/>
                <ellipse cx="59" cy="32" rx="7" ry="8" fill="#fff"/>
                <ellipse cx="41.5" cy="33" rx="4.2" ry="5" fill="#2a5f6a"/>
                <ellipse cx="59.5" cy="33" rx="4.2" ry="5" fill="#2a5f6a"/>
                <circle cx="39.5" cy="30.5" r="1.8" fill="#fff"/>
                <circle cx="57.5" cy="30.5" r="1.8" fill="#fff"/>
              </g>
              <path d="M44 43c2 2.8 10 2.8 12 0" fill="none" stroke="#4a8a94" stroke-width="2.2" stroke-linecap="round"/>
            </g>
            <g class="aics-bot-arm aics-bot-arm-right">
              <ellipse cx="78" cy="52" rx="9" ry="12" fill="#d4f3ee"/>
              <circle cx="82" cy="42" r="6.5" fill="#e8faf7"/>
            </g>
          </g>
        </svg>
      </span>
      <span class="aics-chat-plug">Chat</span>
    </button>
    <section id="aics-chat-panel" class="aics-chat-panel" hidden>
      <header class="aics-chat-head">
        <div class="aics-chat-head-copy">
          <span class="aics-chat-head-bot" aria-hidden="true">
            <svg viewBox="0 0 32 32" width="20" height="20" focusable="false">
              <circle cx="16" cy="17" r="11" fill="#d4f3ee"/>
              <circle cx="16" cy="13" r="8" fill="#e8faf7"/>
              <circle cx="13" cy="12.5" r="2.2" fill="#2a5f6a"/>
              <circle cx="19" cy="12.5" r="2.2" fill="#2a5f6a"/>
              <circle cx="12.3" cy="11.7" r="0.7" fill="#fff"/>
              <circle cx="18.3" cy="11.7" r="0.7" fill="#fff"/>
              <path d="M13 16.5c1 1.3 5 1.3 6 0" fill="none" stroke="#4a8a94" stroke-width="1.3" stroke-linecap="round"/>
            </svg>
          </span>
          <div>
            <p class="aics-chat-kicker">AICloudStrategist Assistant</p>
            <strong>Ask about the diagnostic</strong>
          </div>
        </div>
        <button type="button" class="aics-chat-close" aria-label="Close chat">×</button>
      </header>
      <div class="aics-chat-log" role="log" aria-live="polite"></div>
      <form class="aics-chat-form">
        <label class="sr-only" for="aics-chat-input">Your question</label>
        <textarea id="aics-chat-input" rows="2" maxlength="1200" placeholder="Ask about services, pricing, process…" required></textarea>
        <button type="submit" class="button button-primary aics-chat-send">Send</button>
      </form>
      <p class="aics-chat-note">Queries are logged for follow-up. No billing files needed here.</p>
    </section>
  `;
  document.body.appendChild(root);

  const launcher = root.querySelector(".aics-chat-launcher");
  const panel = root.querySelector(".aics-chat-panel");
  const closer = root.querySelector(".aics-chat-close");
  const log = root.querySelector(".aics-chat-log");
  const form = root.querySelector(".aics-chat-form");
  const input = root.querySelector("#aics-chat-input");
  const sendBtn = root.querySelector(".aics-chat-send");

  const addBubble = (role, text) => {
    const bubble = document.createElement("div");
    bubble.className = `aics-chat-bubble aics-chat-${role}`;
    bubble.textContent = text;
    log.appendChild(bubble);
    log.scrollTop = log.scrollHeight;
  };

  addBubble(
    "assistant",
    "Hi. Ask about our fixed-fee Cloud & AI Cost Governance Diagnostic—scope, pricing, process, the platforms we cover, or the free fit review."
  );

  const track = (name, props) => {
    try {
      if (window.aicsAnalytics && typeof window.aicsAnalytics.track === "function") {
        window.aicsAnalytics.track(name, { props: props || {} });
      } else if (typeof window.plausible === "function") {
        window.plausible(name, { props: props || {} });
      }
    } catch (_) {}
  };

  const setOpen = (open) => {
    panel.hidden = !open;
    launcher.setAttribute("aria-expanded", String(open));
    root.classList.toggle("is-open", open);
    if (open) {
      track("chat_open", { section: "chatbot", source: "launcher" });
      if (!reducedMotion) input.focus();
    }
  };

  launcher.addEventListener("click", () => setOpen(panel.hidden));
  closer.addEventListener("click", () => setOpen(false));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !panel.hidden) setOpen(false);
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = String(input.value || "").trim();
    if (!message) return;

    addBubble("user", message);
    history.push({ role: "user", content: message });
    track("chat_query", { section: "chatbot", source: "widget" });
    input.value = "";
    sendBtn.disabled = true;
    sendBtn.textContent = "Thinking…";

    const pending = document.createElement("div");
    pending.className = "aics-chat-bubble aics-chat-assistant is-pending";
    pending.textContent = "Looking that up…";
    log.appendChild(pending);
    log.scrollTop = log.scrollHeight;

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          session_id: sessionId,
          page: window.location.pathname,
          history: history.slice(-6),
        }),
      });
      let reply = "";
      if (response.ok) {
        const data = await response.json().catch(() => ({}));
        reply = data.reply || data.error || "";
      }
      if (!reply) {
        reply = localKnowledgeReply(message);
      }
      pending.classList.remove("is-pending");
      pending.textContent = reply;
      history.push({ role: "assistant", content: reply });
    } catch (_) {
      pending.classList.remove("is-pending");
      pending.textContent = localKnowledgeReply(message);
    } finally {
      sendBtn.disabled = false;
      sendBtn.textContent = "Send";
      log.scrollTop = log.scrollHeight;
    }
  });
  };

  // On phones, defer widget mount so hero/CTA paint and interact first.
  if (isNarrow && "requestIdleCallback" in window) {
    window.requestIdleCallback(() => mountChatbot(), { timeout: 2800 });
  } else if (isNarrow) {
    window.setTimeout(mountChatbot, 1400);
  } else {
    mountChatbot();
  }
})();
