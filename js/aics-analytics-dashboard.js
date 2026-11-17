(() => {
  const TOKEN_KEY = "aics_report_token_v1";
  const FETCH_TIMEOUT_MS = 25000;
  const CHART_TIMEOUT_MS = 8000;
  const REALTIME_POLL_MS = 15000;

  const statusEl = document.getElementById("dash-status");
  const tokenInput = document.getElementById("dash-token");
  const daysSelect = document.getElementById("dash-days");
  const fromInput = document.getElementById("dash-from");
  const toInput = document.getElementById("dash-to");
  const liveUpdated = document.getElementById("live-updated");

  const charts = {};
  let pollTimer = null;
  let loadSeq = 0;
  let lastDashboard = null;

  const palette = ["#0d7a75", "#0f3350", "#1aa39b", "#4a6075", "#7fd4cf", "#c45c26", "#5b7cfa", "#8a4b12"];

  const setStatus = (text, kind) => {
    statusEl.textContent = text;
    statusEl.className = `status-line${kind ? ` is-${kind}` : ""}`;
  };

  const normalizeToken = (value) => {
    let token = String(value || "").replace(/^\uFEFF/, "").trim();
    if ((token.startsWith('"') && token.endsWith('"')) || (token.startsWith("'") && token.endsWith("'"))) {
      token = token.slice(1, -1).trim();
    }
    token = token.replace(/^Bearer\s+/i, "").trim();
    return token;
  };

  const token = () => {
    const value = normalizeToken(tokenInput.value);
    if (value && tokenInput.value !== value) tokenInput.value = value;
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

  const escapeHtml = (value) =>
    String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");

  const withTimeout = (promise, ms, label) =>
    new Promise((resolve, reject) => {
      const timer = window.setTimeout(() => reject(new Error(`${label} timed out after ${Math.round(ms / 1000)}s`)), ms);
      promise.then(
        (value) => {
          window.clearTimeout(timer);
          resolve(value);
        },
        (err) => {
          window.clearTimeout(timer);
          reject(err);
        },
      );
    });

  const fetchJson = async (url, auth, timeoutMs = FETCH_TIMEOUT_MS) => {
    const controller = typeof AbortController !== "undefined" ? new AbortController() : null;
    const timer = window.setTimeout(() => controller && controller.abort(), timeoutMs);
    try {
      const response = await fetch(url, {
        headers: { Authorization: `Bearer ${auth}` },
        cache: "no-store",
        signal: controller ? controller.signal : undefined,
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok || data.ok === false) {
        const detail = data.code ? ` [${data.code}]` : "";
        throw new Error((data.error || `Request failed (${response.status})`) + detail);
      }
      return data;
    } catch (error) {
      if (error && error.name === "AbortError") {
        throw new Error(`Request timed out after ${Math.round(timeoutMs / 1000)}s`);
      }
      throw error;
    } finally {
      window.clearTimeout(timer);
    }
  };

  const ensureChartJs = () =>
    withTimeout(
      new Promise((resolve, reject) => {
        if (window.Chart) return resolve(window.Chart);
        const existing = document.querySelector("script[data-aics-chartjs]");
        if (existing) {
          existing.addEventListener("load", () => resolve(window.Chart));
          existing.addEventListener("error", () => reject(new Error("Chart.js failed to load")));
          return;
        }
        const script = document.createElement("script");
        script.src = "https://cdn.jsdelivr.net/npm/chart.js@4.4.6/dist/chart.umd.min.js";
        script.defer = true;
        script.dataset.aicsChartjs = "1";
        script.onload = () => resolve(window.Chart);
        script.onerror = () => reject(new Error("Chart.js failed to load"));
        document.head.appendChild(script);
      }),
      CHART_TIMEOUT_MS,
      "Chart.js",
    );

  const destroyChart = (key) => {
    if (charts[key]) {
      charts[key].destroy();
      delete charts[key];
    }
  };

  const upsertChart = (key, canvasId, config) => {
    const canvas = document.getElementById(canvasId);
    if (!canvas || !window.Chart) return null;
    if (charts[key]) {
      charts[key].data = config.data;
      charts[key].options = { ...charts[key].options, ...config.options };
      charts[key].update("none");
      return charts[key];
    }
    charts[key] = new window.Chart(canvas.getContext("2d"), config);
    return charts[key];
  };

  const baseOptions = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: "nearest", intersect: false },
    plugins: {
      legend: { position: "bottom", labels: { boxWidth: 12, color: "#64748b" } },
      tooltip: { backgroundColor: "#0f3350", titleColor: "#fff", bodyColor: "#e8f2f8" },
    },
  };

  const sparkOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false }, tooltip: { enabled: true } },
    elements: { point: { radius: 0 }, line: { tension: 0.35, borderWidth: 2 } },
    scales: { x: { display: false }, y: { display: false } },
  };

  const entriesToXY = (items, limit = 12) => {
    const rows = (items || []).slice(0, limit);
    return {
      labels: rows.map((row) => String(row.key || row.path || "—")),
      values: rows.map((row) => Number(row.count ?? row.value ?? row.avg_dwell_seconds ?? 0) || 0),
    };
  };

  const engagementTotal = (events) => {
    const e = events || {};
    return (
      (e.cta_click || 0) +
      (e.button_click || 0) +
      (e.scroll_depth || 0) +
      (e.download_click || 0) +
      (e.chat_open || 0) +
      (e.chat_query || 0) +
      (e.email_capture_open || 0)
    );
  };

  const renderSparklines = (growth, leadsCount) => {
    const labels = (growth || []).map((d) => d.day);
    const views = (growth || []).map((d) => d.page_views || 0);
    const sessions = (growth || []).map((d) => d.sessions || 0);
    const engageProxy = views.map((v, i) => Math.round(v * 0.15 + (sessions[i] || 0) * 0.35));
    const leadProxy = labels.map((_, i) => (i === labels.length - 1 ? leadsCount : Math.max(0, Math.round((leadsCount / Math.max(labels.length, 1)) * (i + 1) * 0.15))));

    const mk = (key, id, data, color) =>
      upsertChart(key, id, {
        type: "line",
        data: {
          labels,
          datasets: [{ data, borderColor: color, backgroundColor: color + "22", fill: true }],
        },
        options: sparkOptions,
      });

    mk("sparkViews", "spark-views", views, "#0d7a75");
    mk("sparkVisitors", "spark-visitors", sessions, "#0f3350");
    mk("sparkEngagement", "spark-engagement", engageProxy, "#5b7cfa");
    mk("sparkSubscribers", "spark-subscribers", leadProxy, "#c45c26");
  };

  const renderGeo = (locations) => {
    const rows = locations || [];
    const total = rows.reduce((sum, row) => sum + (Number(row.count) || 0), 0) || 1;
    const india = rows.find((row) => String(row.key).toUpperCase() === "IN");
    const indiaCount = india ? Number(india.count) || 0 : 0;
    const indiaPct = Math.round((indiaCount / total) * 100);
    const outsidePct = Math.max(0, 100 - indiaPct);
    document.getElementById("geo-india-pct").textContent = `${indiaPct}%`;
    document.getElementById("geo-outside-pct").textContent = `${outsidePct}%`;
    const blob = document.getElementById("geo-india-blob");
    if (blob) blob.setAttribute("opacity", String(0.35 + Math.min(0.65, indiaPct / 100)));

    document.getElementById("geo-rank").innerHTML = rows.slice(0, 8)
      .map((row, index) => {
        const count = Number(row.count) || 0;
        const pct = Math.round((count / total) * 100);
        return `<li>
          <span class="pos">${index + 1}</span>
          <div>
            <strong>${escapeHtml(row.key)}</strong>
            <div class="bar"><div class="fill" style="width:${Math.max(4, pct)}%"></div></div>
          </div>
          <span>${fmt(count)} · ${pct}%</span>
        </li>`;
      })
      .join("") || `<li><span class="pos">–</span><div class="muted">No country data yet</div><span></span></li>`;

    const loc = entriesToXY(rows);
    upsertChart("audienceLoc", "chart-audience-locations", {
      type: "bar",
      data: { labels: loc.labels, datasets: [{ label: "Views", data: loc.values, backgroundColor: "#1aa39b" }] },
      options: {
        ...baseOptions,
        plugins: { ...baseOptions.plugins, legend: { display: false } },
        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
      },
    });
  };

  const renderRealtime = (rt) => {
    document.getElementById("kpi-live").textContent = fmt(rt.live_visitors);
    document.getElementById("kpi-entering").textContent = fmt(rt.entering_visitors);

    const pages = entriesToXY(rt.pages_in_view || []);
    upsertChart("livePages", "chart-live-pages", {
      type: "bar",
      data: { labels: pages.labels, datasets: [{ label: "Active", data: pages.values, backgroundColor: "#0d7a75" }] },
      options: {
        ...baseOptions,
        indexAxis: "y",
        plugins: { ...baseOptions.plugins, legend: { display: false } },
        scales: { x: { beginAtZero: true, ticks: { precision: 0 } } },
      },
    });

    const sources = entriesToXY(rt.traffic_sources || []);
    upsertChart("liveSources", "chart-live-sources", {
      type: "doughnut",
      data: { labels: sources.labels, datasets: [{ data: sources.values, backgroundColor: palette }] },
      options: { ...baseOptions, cutout: "55%" },
    });

    const locations = entriesToXY(rt.locations || []);
    upsertChart("liveLocations", "chart-live-locations", {
      type: "bar",
      data: { labels: locations.labels, datasets: [{ label: "Active", data: locations.values, backgroundColor: "#0f3350" }] },
      options: {
        ...baseOptions,
        plugins: { ...baseOptions.plugins, legend: { display: false } },
        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
      },
    });

    document.getElementById("live-feed").innerHTML = (rt.feed || [])
      .map(
        (row) =>
          `<li><time>${escapeHtml(String(row.at || "").slice(11, 19))}</time><div><strong>${escapeHtml(row.name)}</strong> · ${escapeHtml(row.path)}${row.detail ? ` · ${escapeHtml(row.detail)}` : ""}</div></li>`,
      )
      .join("") || `<li><time>--</time><div class="muted">Waiting for live activity…</div></li>`;
    liveUpdated.textContent = `Realtime every ${rt.refresh_hint_seconds || 15}s · window ${rt.window_seconds || 120}s · aggregated only`;
  };

  const renderDashboard = (data) => {
    lastDashboard = data;
    const ov = data.overview || {};
    const aud = data.audience || {};
    const traf = data.traffic || {};
    const eng = data.engagement || {};
    const leads = data.leads || {};
    const growth = ov.growth || [];
    const engage = engagementTotal(eng.events);

    document.getElementById("kpi-views").textContent = fmt(ov.page_views);
    document.getElementById("kpi-visitors").textContent = fmt(ov.visitors);
    document.getElementById("kpi-engagement").textContent = fmt(engage);
    document.getElementById("kpi-subscribers").textContent = fmt(leads.count || 0);
    document.getElementById("delta-views").textContent = `${fmt(ov.sessions || 0)} sessions · ${data.period_days || "—"} day range`;
    document.getElementById("delta-visitors").textContent = "Anonymous visitor / session ids";
    document.getElementById("delta-engagement").textContent = "CTA, scroll, downloads, chat, capture opens";
    document.getElementById("delta-subscribers").textContent = "Voluntary contacts only (not passive)";

    if (window.Chart) {
      renderSparklines(growth, leads.count || 0);
      upsertChart("growth", "chart-growth", {
        type: "line",
        data: {
          labels: growth.map((d) => d.day),
          datasets: [
            {
              label: "Views",
              data: growth.map((d) => d.page_views || 0),
              borderColor: "#0d7a75",
              backgroundColor: "rgba(13,122,117,0.14)",
              tension: 0.3,
              fill: true,
            },
            {
              label: "Sessions",
              data: growth.map((d) => d.sessions || 0),
              borderColor: "#0f3350",
              backgroundColor: "rgba(15,51,80,0.08)",
              tension: 0.3,
              fill: true,
            },
          ],
        },
        options: { ...baseOptions, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } },
      });

      renderGeo(aud.locations || []);

      const nr = Object.entries(aud.new_vs_returning || {}).map(([key, count]) => ({ key, count }));
      const nrXY = entriesToXY(nr);
      upsertChart("audienceNR", "chart-audience-nr", {
        type: "doughnut",
        data: { labels: nrXY.labels, datasets: [{ data: nrXY.values, backgroundColor: ["#0d7a75", "#0f3350", "#4a6075"] }] },
        options: { ...baseOptions, cutout: "50%" },
      });

      const browsers = entriesToXY(aud.browsers || []);
      upsertChart("browsers", "chart-browsers", {
        type: "pie",
        data: { labels: browsers.labels, datasets: [{ data: browsers.values, backgroundColor: palette }] },
        options: baseOptions,
      });

      const devices = entriesToXY(aud.devices || []);
      upsertChart("devices", "chart-devices", {
        type: "doughnut",
        data: { labels: devices.labels, datasets: [{ data: devices.values, backgroundColor: palette.slice().reverse() }] },
        options: { ...baseOptions, cutout: "45%" },
      });

      const buckets = Object.entries(traf.buckets || {}).map(([key, count]) => ({ key, count }));
      const bucketXY = entriesToXY(buckets);
      upsertChart("trafficBuckets", "chart-traffic-buckets", {
        type: "doughnut",
        data: { labels: bucketXY.labels, datasets: [{ data: bucketXY.values, backgroundColor: palette }] },
        options: { ...baseOptions, cutout: "52%" },
      });

      const providers = entriesToXY(traf.providers || []);
      upsertChart("trafficProviders", "chart-traffic-providers", {
        type: "bar",
        data: { labels: providers.labels, datasets: [{ label: "Views", data: providers.values, backgroundColor: "#0f3350" }] },
        options: {
          ...baseOptions,
          indexAxis: "y",
          plugins: { ...baseOptions.plugins, legend: { display: false } },
          scales: { x: { beginAtZero: true, ticks: { precision: 0 } } },
        },
      });

      const content = (data.content || []).slice(0, 12);
      upsertChart("contentDwell", "chart-content-dwell", {
        type: "bar",
        data: {
          labels: content.map((row) => row.path),
          datasets: [
            { label: "Avg dwell (s)", data: content.map((row) => row.avg_dwell_seconds || 0), backgroundColor: "#0d7a75" },
            { label: "Views", data: content.map((row) => row.page_views || 0), backgroundColor: "#0f3350" },
          ],
        },
        options: {
          ...baseOptions,
          indexAxis: "y",
          scales: { x: { beginAtZero: true, ticks: { precision: 0 } } },
        },
      });

      const events = Object.entries(eng.events || {})
        .map(([key, count]) => ({ key, count }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 14);
      const eventXY = entriesToXY(events);
      upsertChart("engagement", "chart-engagement", {
        type: "bar",
        data: { labels: eventXY.labels, datasets: [{ label: "Events", data: eventXY.values, backgroundColor: "#5b7cfa" }] },
        options: {
          ...baseOptions,
          plugins: { ...baseOptions.plugins, legend: { display: false } },
          scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
        },
      });
    }

    document.getElementById("age-note").textContent =
      (aud.age && aud.age.note) || "Age is not available from browsers.";
    document.getElementById("engagement-note").textContent =
      eng.note || "CTA rate is on-page click-through, not ad impressions.";

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
    const timing = data.duration_ms != null ? ` · API ${data.duration_ms}ms` : "";
    document.getElementById("generated-at").textContent = `Generated ${data.generated_at || ""}${timing}`;
  };

  const queryUrl = (mode = "dashboard") => {
    const params = new URLSearchParams();
    params.set("mode", mode);
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

  const pollRealtime = async () => {
    const auth = token();
    if (!auth) return;
    try {
      const data = await fetchJson(`${queryUrl("realtime")}&realtime=1`, auth, 12000);
      if (data.realtime) renderRealtime(data.realtime);
    } catch (error) {
      liveUpdated.textContent = `Realtime refresh failed: ${error instanceof Error ? error.message : "error"}`;
    }
  };

  const startPolling = () => {
    if (pollTimer) window.clearInterval(pollTimer);
    pollTimer = window.setInterval(pollRealtime, REALTIME_POLL_MS);
  };

  const load = async ({ silent } = { silent: false }) => {
    const auth = token();
    if (!auth) {
      setStatus("Enter the report token to load metrics.", "error");
      return;
    }
    const seq = ++loadSeq;
    if (!silent) setStatus("Loading analytics…");

    // Do not block the metrics request on Chart.js CDN.
    const chartPromise = ensureChartJs().catch((error) => {
      console.warn(error);
      return null;
    });

    try {
      const data = await fetchJson(queryUrl("dashboard"), auth, FETCH_TIMEOUT_MS);
      if (seq !== loadSeq) return;
      await chartPromise;
      if (seq !== loadSeq) return;
      renderDashboard(data);
      const extra =
        data.keys_listed != null
          ? ` · scanned ${fmt(data.keys_listed)} keys` +
            (data.presence_skipped ? `, skipped ${fmt(data.presence_skipped)} presence` : "")
          : "";
      setStatus(`Loaded successfully${extra}. Realtime panel polls separately.`, "ok");
      startPolling();
    } catch (error) {
      if (seq !== loadSeq) return;
      setStatus(error instanceof Error ? error.message : "Failed to load metrics.", "error");
    }
  };

  document.getElementById("dash-load").addEventListener("click", () => load({ silent: false }));
  document.getElementById("dash-clear").addEventListener("click", () => {
    tokenInput.value = "";
    try {
      sessionStorage.removeItem(TOKEN_KEY);
    } catch (_) {}
    if (pollTimer) window.clearInterval(pollTimer);
    Object.keys(charts).forEach(destroyChart);
    setStatus("Token cleared.");
  });
  daysSelect.addEventListener("change", () => {
    const custom = daysSelect.value === "custom";
    fromInput.disabled = !custom;
    toInput.disabled = !custom;
  });

  restoreToken();
  if (tokenInput.value) load({ silent: false });
})();
