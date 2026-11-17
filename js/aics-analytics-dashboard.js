(() => {
  const TOKEN_KEY = "aics_report_token_v1";
  const statusEl = document.getElementById("dash-status");
  const tokenInput = document.getElementById("dash-token");
  const daysSelect = document.getElementById("dash-days");
  const fromInput = document.getElementById("dash-from");
  const toInput = document.getElementById("dash-to");
  const liveUpdated = document.getElementById("live-updated");

  let pollTimer = null;
  let lastPayload = null;

  const setStatus = (text, kind) => {
    statusEl.textContent = text;
    statusEl.className = `status-line${kind ? ` is-${kind}` : ""}`;
  };

  const token = () => {
    const value = String(tokenInput.value || "").trim();
    if (value) {
      try {
        sessionStorage.setItem(TOKEN_KEY, value);
      } catch (_) {}
    }
    return value;
  };

  const restoreToken = () => {
    try {
      const saved = sessionStorage.getItem(TOKEN_KEY) || "";
      if (saved) tokenInput.value = saved;
    } catch (_) {}
  };

  const fmt = (n) => new Intl.NumberFormat("en-US").format(Number(n) || 0);

  const bars = (items, maxFallback = 1) => {
    const max = Math.max(maxFallback, ...items.map((item) => Number(item.count) || 0));
    return items
      .map((item) => {
        const count = Number(item.count) || 0;
        const width = max ? Math.max(4, Math.round((count / max) * 100)) : 0;
        return `<div class="bar-row"><span>${escapeHtml(item.key)}</span><div class="bar-track"><div class="bar-fill" style="width:${width}%"></div></div><strong>${fmt(count)}</strong></div>`;
      })
      .join("") || `<p class="muted small">No data in this window yet.</p>`;
  };

  const escapeHtml = (value) =>
    String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");

  const spark = (growth) => {
    if (!growth || !growth.length) return `<p class="muted small">No growth series yet.</p>`;
    const max = Math.max(1, ...growth.map((d) => d.page_views || 0));
    return `<div class="chart">${growth
      .slice(-14)
      .map((d) => {
        const width = Math.max(3, Math.round(((d.page_views || 0) / max) * 100));
        return `<div class="bar-row"><span>${escapeHtml(d.day.slice(5))}</span><div class="bar-track"><div class="bar-fill" style="width:${width}%"></div></div><strong>${fmt(d.page_views)} / ${fmt(d.sessions)} sess</strong></div>`;
      })
      .join("")}</div>`;
  };

  const renderRealtime = (rt) => {
    document.getElementById("kpi-live").textContent = fmt(rt.live_visitors);
    document.getElementById("kpi-entering").textContent = fmt(rt.entering_visitors);
    document.getElementById("live-pages").innerHTML = bars(rt.pages_in_view || []);
    document.getElementById("live-sources").innerHTML = bars(rt.traffic_sources || []);
    document.getElementById("live-locations").innerHTML = bars(rt.locations || []);
    document.getElementById("live-feed").innerHTML = (rt.feed || [])
      .map(
        (row) =>
          `<li><time>${escapeHtml(String(row.at || "").slice(11, 19))}</time><div><strong>${escapeHtml(row.name)}</strong> · ${escapeHtml(row.path)}${row.detail ? ` · ${escapeHtml(row.detail)}` : ""}</div></li>`,
      )
      .join("") || `<li><time>--</time><div class="muted">Waiting for live activity…</div></li>`;
    liveUpdated.textContent = `Auto-refresh every ${rt.refresh_hint_seconds || 15}s · window ${rt.window_seconds || 120}s · aggregated only`;
  };

  const renderDashboard = (data) => {
    lastPayload = data;
    const ov = data.overview || {};
    const aud = data.audience || {};
    const traf = data.traffic || {};
    const eng = data.engagement || {};
    const leads = data.leads || {};

    document.getElementById("kpi-visitors").textContent = fmt(ov.visitors);
    document.getElementById("kpi-views").textContent = fmt(ov.page_views);
    document.getElementById("kpi-sessions").textContent = fmt(ov.sessions);
    document.getElementById("kpi-conversions").textContent = fmt(ov.conversions);
    document.getElementById("growth-chart").innerHTML = spark(ov.growth || []);

    document.getElementById("audience-new-returning").innerHTML = bars(
      Object.entries(aud.new_vs_returning || {}).map(([key, count]) => ({ key, count })),
    );
    document.getElementById("audience-locations").innerHTML = bars(aud.locations || []);
    document.getElementById("audience-browsers").innerHTML = bars(aud.browsers || []);
    document.getElementById("audience-devices").innerHTML = bars(aud.devices || []);
    document.getElementById("age-note").textContent =
      (aud.age && aud.age.note) || "Age is not available from browsers.";

    document.getElementById("traffic-buckets").innerHTML = bars(
      Object.entries(traf.buckets || {}).map(([key, count]) => ({ key, count })),
    );
    document.getElementById("traffic-providers").innerHTML = bars(traf.providers || []);

    const contentRows = (data.content || [])
      .map(
        (row) => `<tr>
        <td>${escapeHtml(row.path)}</td>
        <td>${fmt(row.page_views)}</td>
        <td>${fmt(row.avg_dwell_seconds)}s</td>
        <td>${fmt(row.cta_clicks)} (${row.cta_rate || 0}%)</td>
        <td>${fmt(row.scroll_50_plus)}</td>
        <td>${fmt(row.downloads)}</td>
      </tr>`,
      )
      .join("");
    document.getElementById("content-table").innerHTML =
      contentRows || `<tr><td colspan="6" class="muted">No content metrics yet.</td></tr>`;

    document.getElementById("engagement-note").textContent =
      eng.note || "CTA rate is on-page click-through, not ad impressions.";
    document.getElementById("engagement-events").innerHTML = bars(
      Object.entries(eng.events || {})
        .map(([key, count]) => ({ key, count }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 16),
    );

    const leadRows = (leads.items || [])
      .map((lead) => {
        const page = lead.landing_page || lead.stage || "—";
        return `<tr>
          <td>${escapeHtml(lead.name || "—")}</td>
          <td><a href="mailto:${escapeHtml(lead.email)}">${escapeHtml(lead.email || "—")}</a></td>
          <td>${escapeHtml(lead.company || "—")}</td>
          <td>${escapeHtml(lead.source || lead.stage || "—")}</td>
          <td>${escapeHtml(page)}</td>
          <td>${escapeHtml(String(lead.submitted_at || "").replace("T", " ").slice(0, 19))}</td>
        </tr>`;
      })
      .join("");
    document.getElementById("leads-count").textContent = fmt(leads.count || 0);
    document.getElementById("leads-table").innerHTML =
      leadRows || `<tr><td colspan="6" class="muted">No voluntary leads in this range yet.</td></tr>`;

    renderRealtime(data.realtime || {});
    document.getElementById("generated-at").textContent = `Generated ${data.generated_at || ""}`;
  };

  const queryUrl = () => {
    const params = new URLSearchParams();
    params.set("mode", "dashboard");
    const preset = daysSelect.value;
    if (preset === "custom") {
      if (fromInput.value) params.set("from", fromInput.value);
      if (toInput.value) params.set("to", toInput.value);
      params.set("days", "90");
    } else {
      params.set("days", preset);
    }
    return `/api/metrics?${params.toString()}`;
  };

  const load = async ({ silent } = { silent: false }) => {
    const auth = token();
    if (!auth) {
      setStatus("Enter the report token to load metrics.", "error");
      return;
    }
    if (!silent) setStatus("Loading…");
    try {
      const response = await fetch(queryUrl(), {
        headers: { Authorization: `Bearer ${auth}` },
        cache: "no-store",
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok || !data.ok) {
        throw new Error(data.error || `Request failed (${response.status})`);
      }
      renderDashboard(data);
      setStatus("Live. Real-time panel polls automatically.", "ok");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Failed to load metrics.", "error");
    }
  };

  const startPolling = () => {
    if (pollTimer) window.clearInterval(pollTimer);
    pollTimer = window.setInterval(() => load({ silent: true }), 15000);
  };

  document.getElementById("dash-load").addEventListener("click", () => {
    load({ silent: false });
    startPolling();
  });
  document.getElementById("dash-clear").addEventListener("click", () => {
    tokenInput.value = "";
    try {
      sessionStorage.removeItem(TOKEN_KEY);
    } catch (_) {}
    if (pollTimer) window.clearInterval(pollTimer);
    setStatus("Token cleared.");
  });
  daysSelect.addEventListener("change", () => {
    const custom = daysSelect.value === "custom";
    fromInput.disabled = !custom;
    toInput.disabled = !custom;
  });

  restoreToken();
  if (tokenInput.value) {
    load({ silent: false });
    startPolling();
  }
})();
