(() => {
  const TOKEN_KEY = "aics_report_token_v1";
  const FETCH_TIMEOUT_MS = 25000;
  const CHART_TIMEOUT_MS = 8000;
  const REALTIME_POLL_MS = 60000;

  const statusEl = document.getElementById("dash-status");
  const loginStatusEl = document.getElementById("login-status");
  const tokenInput = document.getElementById("dash-token");
  const loginTokenInput = document.getElementById("login-token");
  const loginForm = document.getElementById("login-form");
  const loginSubmit = document.getElementById("login-submit");
  const loginScreen = document.getElementById("login-screen");
  const loginForgot = document.getElementById("login-forgot");
  const loginForgotHelp = document.getElementById("login-forgot-help");
  const dashApp = document.getElementById("dash-app");
  const dashUser = document.getElementById("dash-user");
  const daysSelect = document.getElementById("dash-days");
  const audienceSelect = document.getElementById("dash-audience");
  const fromInput = document.getElementById("dash-from");
  const toInput = document.getElementById("dash-to");
  const liveUpdated = document.getElementById("live-updated");
  const emptyEl = document.getElementById("dash-empty");
  const markInternalBtn = document.getElementById("dash-mark-internal");
  const MARK_KEY = "aics_traffic_mark_v1";

  const charts = {};
  let pollTimer = null;
  let loadSeq = 0;
  let lastDashboard = null;
  let lastDiagnostics = null;

  const palette = ["#087989", "#0a1828", "#0ea3b4", "#1a5a96", "#7ec8d0", "#b8741f", "#3d7ec4", "#8a5a2b"];

  let progressState = { todos: [], plan: [], history: [] };

  const setStatus = (text, kind) => {
    if (!statusEl) return;
    statusEl.textContent = text;
    statusEl.className = `status-line${kind ? ` is-${kind}` : ""}`;
  };

  const setLoginStatus = (text, kind) => {
    if (!loginStatusEl) return;
    loginStatusEl.textContent = text;
    loginStatusEl.className = `status-line${kind ? ` is-${kind}` : ""}`;
  };

  const setLoginLoading = (loading) => {
    if (loginForm) loginForm.classList.toggle("is-loading", Boolean(loading));
    if (loginSubmit) {
      loginSubmit.disabled = Boolean(loading);
      loginSubmit.setAttribute("aria-busy", loading ? "true" : "false");
    }
  };

  const clearLoginInvalid = () => {
    loginTokenInput?.classList.remove("is-invalid");
  };

  const markLoginInvalid = () => {
    loginTokenInput?.classList.add("is-invalid");
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

  const setSession = (accessToken) => {
    tokenInput.value = accessToken;
    try {
      sessionStorage.setItem(TOKEN_KEY, accessToken);
    } catch (_) {}
  };

  const clearSession = () => {
    tokenInput.value = "";
    if (loginTokenInput) loginTokenInput.value = "";
    try {
      sessionStorage.removeItem(TOKEN_KEY);
    } catch (_) {}
  };

  const showLoggedOut = () => {
    document.body.classList.add("is-locked");
    document.body.classList.remove("is-unlocked");
    if (dashApp) dashApp.hidden = true;
    if (loginScreen) loginScreen.hidden = false;
    if (dashUser) dashUser.textContent = "";
    showProgressSection(false);
  };

  const showLoggedIn = () => {
    document.body.classList.remove("is-locked");
    document.body.classList.add("is-unlocked");
    if (dashApp) dashApp.hidden = false;
    if (loginScreen) loginScreen.hidden = true;
    if (dashUser) dashUser.textContent = "Signed in";
  };

  const restoreSession = () => {
    try {
      const savedToken = sessionStorage.getItem(TOKEN_KEY) || "";
      if (savedToken) tokenInput.value = savedToken;
      return { token: savedToken };
    } catch (_) {
      return { token: "" };
    }
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
        const friendly = {
          missing_authorization: "No access key provided. Paste your key and click Load.",
          invalid_token: "Access key does not match. Copy AICS_REPORT_TOKEN from Cloudflare Pages → Production (not Preview).",
          server_token_missing: "Server misconfigured: production AICS_REPORT_TOKEN is missing. Add it in Cloudflare Pages, then redeploy.",
        };
        throw new Error(friendly[data.code] || data.error || `Request failed (${response.status})`);
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
      legend: { position: "bottom", labels: { boxWidth: 12, color: "#3d5368", font: { family: "Figtree, sans-serif", size: 11 } } },
      tooltip: { backgroundColor: "#0a1828", titleColor: "#fff", bodyColor: "#e8f2f8", cornerRadius: 8, padding: 10 },
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

  const MEANINGFUL = new Set([
    "scroll_depth",
    "cta_click",
    "button_click",
    "download_click",
    "chat_open",
    "email_click",
    "phone_click",
    "whatsapp_click",
  ]);

  const engagementTotal = (events, meaningfulFallback) => {
    if (meaningfulFallback != null && Number.isFinite(Number(meaningfulFallback))) {
      return Number(meaningfulFallback) || 0;
    }
    const e = events || {};
    let sum = 0;
    Object.keys(e).forEach((name) => {
      if (!MEANINGFUL.has(name)) return;
      sum += Number(e[name]) || 0;
    });
    return sum;
  };

  const labeledRows = (labeled, fallbackEvents) => {
    if (Array.isArray(labeled) && labeled.length) {
      return labeled.map((row) => ({ key: row.label || row.key, count: row.count }));
    }
    return Object.entries(fallbackEvents || {}).map(([key, count]) => ({ key, count }));
  };

  const syncMarkUi = () => {
    let marked = false;
    try {
      marked = String(localStorage.getItem(MARK_KEY) || "").toLowerCase() === "internal";
    } catch (_) {}
    if (markInternalBtn) {
      markInternalBtn.setAttribute("aria-pressed", marked ? "true" : "false");
      markInternalBtn.textContent = marked ? "Browser marked Internal" : "Mark this browser Internal";
    }
    const unmark = document.getElementById("dash-unmark-internal");
    if (unmark) unmark.hidden = !marked;
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

    mk("sparkViews", "spark-views", views, "#087989");
    mk("sparkVisitors", "spark-visitors", sessions, "#0a1828");
    mk("sparkEngagement", "spark-engagement", engageProxy, "#1a5a96");
    mk("sparkContacts", "spark-contacts", leadProxy, "#b8741f");
  };

  const renderGeo = (locations, denominator) => {
    const rows = (locations || []).filter((row) => Number(row.count) > 0);
    const summed = rows.reduce((sum, row) => sum + (Number(row.count) || 0), 0);
    const denom = Number(denominator);
    const total = denom > 0 ? denom : summed;
    const empty = !(total > 0) || rows.length === 0;

    const emptyEl = document.getElementById("geo-empty");
    const layoutEl = document.getElementById("geo-layout");
    const chartWrap = document.getElementById("geo-chart-wrap");
    const mapTitle = document.getElementById("geo-map-title");
    const indiaEl = document.getElementById("geo-india-pct");
    const outsideEl = document.getElementById("geo-outside-pct");
    const blob = document.getElementById("geo-india-blob");

    if (emptyEl) emptyEl.hidden = !empty;
    if (layoutEl) layoutEl.hidden = false;
    if (layoutEl) layoutEl.classList.toggle("is-geo-empty", empty);
    if (chartWrap) chartWrap.hidden = empty;

    if (empty) {
      if (indiaEl) indiaEl.textContent = "—";
      if (outsideEl) outsideEl.textContent = "—";
      if (blob) blob.setAttribute("opacity", "0.2");
      if (mapTitle) mapTitle.textContent = "No location data for this traffic selection.";
      document.getElementById("geo-rank").innerHTML =
        `<li><span class="pos" aria-hidden="true">–</span><div class="muted">No location data yet.</div><span></span></li>`;
      if (charts.audienceLoc) {
        try {
          charts.audienceLoc.destroy();
        } catch (_) {}
        delete charts.audienceLoc;
      }
      const canvas = document.getElementById("chart-audience-locations");
      if (canvas && canvas.getContext) {
        const ctx = canvas.getContext("2d");
        if (ctx) ctx.clearRect(0, 0, canvas.width, canvas.height);
      }
      return;
    }

    const india = rows.find((row) => /^(IN|INDIA)$/i.test(String(row.key || "")));
    const indiaCount = india ? Number(india.count) || 0 : 0;
    const indiaPct = Math.round((indiaCount / total) * 100);
    const outsidePct = Math.max(0, 100 - indiaPct);
    if (indiaEl) indiaEl.textContent = `${indiaPct}%`;
    if (outsideEl) outsideEl.textContent = `${outsidePct}%`;
    if (blob) blob.setAttribute("opacity", String(0.35 + Math.min(0.65, indiaPct / 100)));
    if (mapTitle) {
      mapTitle.textContent = `India ${indiaPct} percent of visitors; Outside India ${outsidePct} percent (includes Unknown).`;
    }

    document.getElementById("geo-rank").innerHTML = rows.slice(0, 8)
      .map((row, index) => {
        const count = Number(row.count) || 0;
        const pct = Math.round((count / total) * 100);
        const label = String(row.key || "Unknown");
        return `<li>
          <span class="pos">${index + 1}</span>
          <div>
            <strong>${escapeHtml(label)}</strong>
            <div class="bar" aria-hidden="true"><div class="fill" style="width:${Math.max(4, pct)}%"></div></div>
          </div>
          <span>${fmt(count)} · ${pct}%</span>
        </li>`;
      })
      .join("");

    const loc = entriesToXY(rows);
    upsertChart("audienceLoc", "chart-audience-locations", {
      type: "bar",
      data: { labels: loc.labels, datasets: [{ label: "Visitors", data: loc.values, backgroundColor: "#0ea3b4" }] },
      options: {
        ...baseOptions,
        plugins: { ...baseOptions.plugins, legend: { display: false } },
        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
      },
    });
  };

  let showZeroDiagnostics = false;

  const DIAGNOSTIC_DEFS = [
    {
      id: "orphan",
      name: "Orphan / unanchored events",
      explain: "Events without a valid public page-view anchor. Excluded from external business metrics.",
      affects: "Does not affect customer engagement KPIs.",
    },
    {
      id: "long_session",
      name: "Long active-session flags",
      explain: "Unusually long measured sessions retained for review. Not automatically treated as invalid.",
      affects: "Does not remove the session from dwell samples automatically.",
    },
    {
      id: "presence",
      name: "Presence checks",
      explain: "Operational events used for live status. Excluded from engagement.",
      affects: "Excluded from Meaningful Engagement.",
    },
    {
      id: "dwell_ticks",
      name: "Dwell measurement ticks",
      explain: "Operational timing events used to calculate active time. Excluded from engagement.",
      affects: "Excluded from Meaningful Engagement.",
    },
    {
      id: "private_routes",
      name: "Private routes excluded",
      explain: "Events from analytics, login and private operational routes. Excluded from content reports.",
      affects: "Excluded from Top Pages and content reports.",
    },
    {
      id: "duplicates",
      name: "Duplicates rejected",
      explain: "Repeated events removed by idempotency or deduplication rules.",
      affects: "Excluded from reports.",
    },
    {
      id: "invalid",
      name: "Invalid events rejected",
      explain: "Malformed or inconsistent events excluded from reports.",
      affects: "Excluded from reports.",
    },
  ];

  const diagnosticCountsFromPayload = (diag) => {
    const orphans = diag.orphan_unanchored_events || {};
    const telemetry = diag.operational_telemetry || {};
    let orphanSum = 0;
    let longSession = 0;
    Object.entries(orphans).forEach(([key, count]) => {
      const n = Number(count) || 0;
      if (key === "dwell_long_session_flag") longSession += n;
      else orphanSum += n;
    });
    return {
      orphan: orphanSum,
      long_session: longSession,
      presence: Number(telemetry.presence_ping) || 0,
      dwell_ticks: Number(telemetry.dwell_tick) || 0,
      private_routes: Number(diag.private_routes_excluded) || 0,
      duplicates: Number(diag.duplicates_rejected) || 0,
      invalid: Number(diag.invalid_events_rejected) || 0,
    };
  };

  const renderDiagnostics = (diag) => {
    const counts = diagnosticCountsFromPayload(diag || {});
    const list = document.getElementById("diagnostics-list");
    const note = document.getElementById("diagnostics-note");
    if (note) {
      note.textContent =
        "These events help validate tracking and are excluded from customer-facing engagement metrics unless stated otherwise.";
    }
    if (!list) return;
    const rows = DIAGNOSTIC_DEFS.map((def) => {
      const count = counts[def.id] || 0;
      return { ...def, count };
    }).filter((row) => showZeroDiagnostics || row.count > 0);

    list.innerHTML =
      rows
        .map(
          (row) => `<li class="diagnostics-row" data-diag="${escapeHtml(row.id)}">
            <div class="diagnostics-row-main">
              <strong id="diag-label-${escapeHtml(row.id)}">${escapeHtml(row.name)}</strong>
              <span class="diagnostics-count" aria-labelledby="diag-label-${escapeHtml(row.id)}">${fmt(row.count)}</span>
            </div>
            <p class="diagnostics-explain">${escapeHtml(row.explain)}</p>
            <p class="diagnostics-affects muted">${escapeHtml(row.affects)}</p>
          </li>`,
        )
        .join("") ||
      `<li class="diagnostics-row"><div class="diagnostics-row-main"><strong>No diagnostic events in this range</strong><span class="diagnostics-count">0</span></div>
        <p class="diagnostics-explain">Operational counters are empty for the selected traffic filter.</p>
        <p class="diagnostics-affects muted">Business metrics are unaffected.</p></li>`;

    const zeroBtn = document.getElementById("diagnostics-show-zeros");
    if (zeroBtn) {
      zeroBtn.setAttribute("aria-pressed", showZeroDiagnostics ? "true" : "false");
      zeroBtn.textContent = showZeroDiagnostics ? "Hide zero-count diagnostics" : "Show zero-count diagnostics";
    }
  };

  const renderRealtime = (rt) => {
    document.getElementById("kpi-live").textContent = fmt(rt.live_visitors);
    document.getElementById("kpi-entering").textContent = fmt(rt.entering_visitors);

    const pages = entriesToXY(rt.pages_in_view || []);
    upsertChart("livePages", "chart-live-pages", {
      type: "bar",
      data: { labels: pages.labels, datasets: [{ label: "Active", data: pages.values, backgroundColor: "#087989" }] },
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
      data: { labels: locations.labels, datasets: [{ label: "Active", data: locations.values, backgroundColor: "#0a1828" }] },
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
      .join("") || `<li><time>--</time><div class="muted">No live activity yet</div></li>`;
    liveUpdated.textContent = "Updating live";
  };

  const renderDashboard = (data) => {
    lastDashboard = data;
    const ov = data.overview || {};
    const aud = data.audience_metrics || data.audience || {};
    const traf = data.traffic || {};
    const eng = data.engagement || {};
    const leads = data.leads || {};
    const growth = ov.growth || [];
    const engage = engagementTotal(eng.events, ov.engagement_meaningful ?? eng.meaningful_total);

    if (emptyEl) {
      const showEmpty = Boolean(data.empty_external || data.empty_message);
      emptyEl.hidden = !showEmpty;
      emptyEl.textContent = data.empty_message || "No verified external customer traffic in this range.";
    }

    document.getElementById("kpi-views").textContent = fmt(ov.page_views);
    document.getElementById("kpi-visitors").textContent = fmt(ov.visitors);
    document.getElementById("kpi-engagement").textContent = fmt(engage);
    document.getElementById("kpi-contacts").textContent = fmt(leads.count || 0);
    document.getElementById("delta-views").textContent = `${fmt(ov.sessions || 0)} sessions in range`;
    document.getElementById("delta-visitors").textContent = "Unique visitors";
    document.getElementById("delta-engagement").textContent = "Meaningful engagement (excludes page views & telemetry)";
    document.getElementById("delta-contacts").textContent = "Form submissions";

    const invEl = document.getElementById("dash-invariants");
    const issues = (data.diagnostics && data.diagnostics.consistency_issues) || [];
    if (invEl) {
      if (issues.length) {
        invEl.hidden = false;
        invEl.textContent = `Consistency: ${issues.map((i) => i.message || i.code).join(" · ")}`;
      } else {
        invEl.hidden = true;
        invEl.textContent = "";
      }
    }

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
              borderColor: "#087989",
              backgroundColor: "rgba(13,122,117,0.14)",
              tension: 0.3,
              fill: true,
            },
            {
              label: "Sessions",
              data: growth.map((d) => d.sessions || 0),
              borderColor: "#0a1828",
              backgroundColor: "rgba(15,51,80,0.08)",
              tension: 0.3,
              fill: true,
            },
          ],
        },
        options: { ...baseOptions, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } },
      });

      renderGeo(aud.locations || [], aud.location_denominator);

      const nr = Object.entries(aud.new_vs_returning || {}).map(([key, count]) => ({ key, count }));
      const nrXY = entriesToXY(nr);
      upsertChart("audienceNR", "chart-audience-nr", {
        type: "doughnut",
        data: { labels: nrXY.labels, datasets: [{ data: nrXY.values, backgroundColor: ["#087989", "#0a1828", "#3d5368"] }] },
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
        data: { labels: providers.labels, datasets: [{ label: "Views", data: providers.values, backgroundColor: "#0a1828" }] },
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
            {
              label: "Avg dwell (s)",
              data: content.map((row) =>
                row.dwell_available === false || row.avg_dwell_seconds == null ? null : row.avg_dwell_seconds,
              ),
              backgroundColor: "#087989",
              spanGaps: false,
            },
            { label: "Views", data: content.map((row) => row.page_views || 0), backgroundColor: "#0a1828" },
          ],
        },
        options: {
          ...baseOptions,
          indexAxis: "y",
          scales: { x: { beginAtZero: true, ticks: { precision: 0 } } },
        },
      });

      const meaningful = labeledRows(eng.labeled, eng.events).slice(0, 14);
      const eventXY = entriesToXY(meaningful);
      upsertChart("engagement", "chart-engagement", {
        type: "bar",
        data: { labels: eventXY.labels, datasets: [{ label: "Meaningful engagement", data: eventXY.values, backgroundColor: "#5b7cfa" }] },
        options: {
          ...baseOptions,
          plugins: { ...baseOptions.plugins, legend: { display: false } },
          scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
        },
      });

      const conversion = labeledRows(eng.conversion_labeled, eng.conversion_intent).slice(0, 10);
      const convXY = entriesToXY(conversion);
      upsertChart("conversion", "chart-conversion", {
        type: "bar",
        data: { labels: convXY.labels, datasets: [{ label: "Conversion intent", data: convXY.values, backgroundColor: "#b8741f" }] },
        options: {
          ...baseOptions,
          plugins: { ...baseOptions.plugins, legend: { display: false } },
          scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
        },
      });

      const diag = data.diagnostics || {};
      const telemetry = labeledRows(diag.operational_labeled, diag.operational_telemetry).slice(0, 10);
      const telXY = entriesToXY(telemetry);
      upsertChart("telemetry", "chart-telemetry", {
        type: "bar",
        data: { labels: telXY.labels, datasets: [{ label: "Operational telemetry", data: telXY.values, backgroundColor: "#3d5368" }] },
        options: {
          ...baseOptions,
          plugins: { ...baseOptions.plugins, legend: { display: false } },
          scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
        },
      });
      renderDiagnostics(diag);
      lastDiagnostics = diag;
    }

    document.getElementById("age-note").textContent = "New and returning visitors.";
    document.getElementById("engagement-note").textContent =
      eng.note || "Meaningful engagement excludes page views and operational telemetry.";

    const contentRows = (data.content || [])
      .map((row) => {
        const dwell =
          row.dwell_available === false || row.avg_dwell_seconds == null
            ? "—"
            : `${fmt(row.avg_dwell_seconds)}s${row.dwell_samples ? ` · ${fmt(row.dwell_samples)} measured` : ""}`;
        return `<tr>
        <td>${escapeHtml(row.path)}</td>
        <td>${fmt(row.page_views)}</td>
        <td>${dwell}</td>
        <td>${fmt(row.cta_clicks)} (${row.cta_rate || 0}%)</td>
        <td>${fmt(row.scroll_50_plus)}</td>
        <td>${fmt(row.downloads)}</td>
      </tr>`;
      })
      .join("");
    document.getElementById("content-table").innerHTML =
      contentRows || `<tr><td colspan="6" class="muted">No content metrics yet.</td></tr>`;

    renderLeads(leads);
    renderRealtime(data.realtime || {});
    const when = data.generated_at ? String(data.generated_at).replace("T", " ").slice(0, 19) : "";
    document.getElementById("generated-at").textContent = when ? `Updated ${when}` : "";
    syncMarkUi();
  };

  const showProgressSection = (visible) => {
    const section = document.getElementById("progress-section");
    if (!section) return;
    section.hidden = !visible;
    section.classList.toggle("is-hidden", !visible);
  };

  const validateCredentials = async (accessToken) => {
    // Server-side check against AICS_REPORT_TOKEN (or reader key) via metrics.
    await fetchJson(`/api/metrics?days=1&realtime=1&audience=external`, accessToken, 15000);
  };

  const normalizeTodoStatus = (value) => {
    const raw = String(value || "")
      .trim()
      .toLowerCase()
      .replace(/[\s-]+/g, "_");
    if (raw === "completed" || raw === "done" || raw === "complete") return "completed";
    if (raw === "in_progress" || raw === "progress" || raw === "active") return "in_progress";
    return "not_started";
  };

  const statusMeta = (status) => {
    const normalized = normalizeTodoStatus(status);
    if (normalized === "completed") return { key: "completed", cls: "is-done", label: "Completed", mark: "✓" };
    if (normalized === "in_progress") return { key: "in_progress", cls: "is-progress", label: "In progress", mark: "●" };
    return { key: "not_started", cls: "is-open", label: "Not started", mark: "" };
  };

  const statusSortRank = (status) => {
    const key = normalizeTodoStatus(status);
    if (key === "in_progress") return 0;
    if (key === "not_started") return 1;
    return 2;
  };

  const fetchStaticJson = async (url) => {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) throw new Error(`Could not load ${url}`);
    return response.json();
  };

  const loadProgressData = async (auth) => {
    let todos = [];
    try {
      const board = await fetchJson("/api/todos", auth, 12000);
      todos = Array.isArray(board.todos) ? board.todos : [];
    } catch (_) {
      try {
        const seed = await fetchStaticJson("/data/todos.json");
        todos = Array.isArray(seed.todos) ? seed.todos : [];
      } catch (_) {
        todos = [];
      }
    }

    let plan = [];
    try {
      const planData = await fetchStaticJson("/data/progress-plan.json");
      plan = Array.isArray(planData.items) ? planData.items : [];
    } catch (_) {
      plan = [];
    }

    let history = [];
    try {
      const historyData = await fetchStaticJson("/data/git-history.json");
      history = Array.isArray(historyData.commits) ? historyData.commits : [];
    } catch (_) {
      history = [];
    }

    progressState = { todos, plan, history };
    return progressState;
  };

  const renderStatusItem = (item) => {
    const meta = statusMeta(item.status);
    return `<li class="${meta.cls}"><span class="todo-mark" aria-hidden="true">${meta.mark}</span><div><div>${escapeHtml(item.label)}</div><span class="todo-status">${meta.label}</span></div></li>`;
  };

  const renderHistoryItem = (item) => {
    const message = String(item.message || "").trim();
    const date = String(item.date || "").trim();
    const id = String(item.id || "").trim();
    return `<li class="is-done"><span class="todo-mark" aria-hidden="true">✓</span><div><div>${escapeHtml(message)}</div><span class="history-meta">${escapeHtml([date, id].filter(Boolean).join(" · "))}</span></div></li>`;
  };

  const renderProgress = () => {
    const todos = [...(progressState.todos || [])].sort((a, b) => {
      const rank = statusSortRank(a.status) - statusSortRank(b.status);
      if (rank !== 0) return rank;
      return String(a.label || "").localeCompare(String(b.label || ""));
    });
    const done = todos.filter((t) => normalizeTodoStatus(t.status) === "completed");
    const active = todos.filter((t) => normalizeTodoStatus(t.status) === "in_progress");
    const open = todos.filter((t) => normalizeTodoStatus(t.status) === "not_started");
    const pct = todos.length ? Math.round((done.length / todos.length) * 100) : 0;

    const doneEl = document.getElementById("progress-done");
    const activeEl = document.getElementById("progress-active");
    const openEl = document.getElementById("progress-open");
    const pctEl = document.getElementById("progress-pct");
    if (doneEl) doneEl.textContent = String(done.length);
    if (activeEl) activeEl.textContent = String(active.length);
    if (openEl) openEl.textContent = String(open.length);
    if (pctEl) pctEl.textContent = `${pct}%`;

    const todoList = document.getElementById("todo-list");
    const planList = document.getElementById("progress-plan");
    const historyList = document.getElementById("progress-history");

    if (todoList) {
      todoList.innerHTML = todos.length
        ? todos.map(renderStatusItem).join("")
        : `<li class="is-open"><span class="todo-mark" aria-hidden="true"></span><div><div>No to-dos yet</div><span class="todo-status">Not started</span></div></li>`;
    }
    if (planList) {
      planList.innerHTML = (progressState.plan || []).length
        ? progressState.plan.map(renderStatusItem).join("")
        : `<li class="is-open"><span class="todo-mark" aria-hidden="true"></span><div><div>30-day plan unavailable</div><span class="todo-status">Not started</span></div></li>`;
    }
    if (historyList) {
      historyList.innerHTML = (progressState.history || []).length
        ? progressState.history.slice(0, 20).map(renderHistoryItem).join("")
        : `<li class="is-done"><span class="todo-mark" aria-hidden="true">✓</span><div><div>No history yet</div><span class="history-meta">main</span></div></li>`;
    }

    const hasRealProgress =
      (progressState.todos || []).length > 0 ||
      (progressState.plan || []).length > 0 ||
      (progressState.history || []).length > 0;
    showProgressSection(hasRealProgress);
  };

  const renderLeads = (leads) => {
    const items = (leads && leads.items) || [];
    const count = leads && leads.count != null ? leads.count : items.length;
    document.getElementById("kpi-contacts").textContent = fmt(count);
    document.getElementById("delta-contacts").textContent = "Form submissions";
    document.getElementById("leads-count").textContent = fmt(count);
    const leadRows = items
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
    document.getElementById("leads-table").innerHTML =
      leadRows || `<tr><td colspan="6" class="muted">No contacts in this range yet.</td></tr>`;
  };

  const queryUrl = (mode = "dashboard", { refresh = false } = {}) => {
    const params = new URLSearchParams();
    params.set("mode", mode);
    params.set("audience", (audienceSelect && audienceSelect.value) || "external");
    const preset = daysSelect.value;
    if (preset === "custom") {
      if (fromInput.value) params.set("from", fromInput.value);
      if (toInput.value) params.set("to", toInput.value);
      params.set("days", "90");
    } else {
      params.set("days", preset);
    }
    if (refresh) params.set("refresh", "1");
    return `/api/metrics?${params.toString()}`;
  };

  const pollRealtime = async () => {
    const auth = token();
    if (!auth) return;
    try {
      const data = await fetchJson(`${queryUrl("realtime")}&realtime=1`, auth, 12000);
      if (data.realtime) renderRealtime(data.realtime);
      // Contacts load with the dashboard only — realtime polls skip lead KV lists.
      if (data.leads) renderLeads(data.leads);
      liveUpdated.textContent = data.stale
        ? "Live · cached (KV limit)"
        : data.from_cache
          ? "Live · cached"
          : "Updating live";
    } catch (error) {
      liveUpdated.textContent = "Live update paused";
    }
  };

  const startPolling = () => {
    if (pollTimer) window.clearInterval(pollTimer);
    pollTimer = window.setInterval(pollRealtime, REALTIME_POLL_MS);
  };

  const logout = () => {
    if (pollTimer) window.clearInterval(pollTimer);
    Object.keys(charts).forEach(destroyChart);
    clearSession();
    showLoggedOut();
    setLoginStatus("");
  };

  const load = async ({ silent } = { silent: false }) => {
    const auth = token();
    if (!auth) {
      showLoggedOut();
      setLoginStatus("Enter your token to continue.", "error");
      return;
    }
    const seq = ++loadSeq;
    if (!silent) setStatus("Loading…");

    const chartPromise = ensureChartJs().catch((error) => {
      console.warn(error);
      return null;
    });

    try {
      const data = await fetchJson(queryUrl("dashboard", { refresh: !silent }), auth, FETCH_TIMEOUT_MS);
      if (seq !== loadSeq) return;
      await chartPromise;
      if (seq !== loadSeq) return;
      renderDashboard(data);
      try {
        await loadProgressData(auth);
      } catch (_) {}
      renderProgress();
      if (data.stale || data.cache_warning) {
        setStatus(String(data.cache_warning || "Showing cached analytics (KV limit)."), "error");
      } else if (data.from_cache) {
        setStatus("Analytics loaded (cached).", "ok");
      } else {
        setStatus("Analytics loaded.", "ok");
      }
      startPolling();
    } catch (error) {
      if (seq !== loadSeq) return;
      const message = error instanceof Error ? error.message : "Could not load analytics.";
      // Keep last successful paint if quota errors mid-session; avoid wiping to zeros.
      if (/KV list|limit exceeded/i.test(message)) {
        setStatus("KV daily list limit hit. Keeping last loaded analytics.", "error");
        return;
      }
      showProgressSection(false);
      setStatus(message, "error");
      if (/access key|unauthorized|invalid|missing/i.test(message)) {
        logout();
        setLoginStatus(message, "error");
      }
    }
  };

  const login = async (event) => {
    if (event) event.preventDefault();
    const accessToken = normalizeToken(loginTokenInput?.value || "");
    clearLoginInvalid();
    if (!accessToken) {
      markLoginInvalid();
      setLoginStatus("Enter your token.", "error");
      loginTokenInput?.focus();
      return;
    }

    setLoginLoading(true);
    setLoginStatus("Signing in…");
    try {
      await validateCredentials(accessToken);
      clearLoginInvalid();
      setSession(accessToken);
      showLoggedIn();
      setLoginStatus("");
      setStatus("Loading analytics…");
      await load({ silent: false });
    } catch (error) {
      clearSession();
      showLoggedOut();
      markLoginInvalid();
      setLoginStatus(error instanceof Error ? error.message : "Sign-in failed. Check your token and try again.", "error");
      loginTokenInput?.focus();
    } finally {
      setLoginLoading(false);
      if (loginTokenInput) loginTokenInput.value = "";
    }
  };

  if (loginForm) loginForm.addEventListener("submit", login);
  loginTokenInput?.addEventListener("input", () => loginTokenInput.classList.remove("is-invalid"));
  loginForgot?.addEventListener("click", (event) => {
    event.preventDefault();
    if (!loginForgotHelp) return;
    const open = loginForgotHelp.hasAttribute("hidden");
    if (open) loginForgotHelp.removeAttribute("hidden");
    else loginForgotHelp.setAttribute("hidden", "");
  });
  document.getElementById("dash-load").addEventListener("click", () => load({ silent: false }));
  document.getElementById("dash-logout").addEventListener("click", logout);
  daysSelect.addEventListener("change", () => {
    const custom = daysSelect.value === "custom";
    fromInput.disabled = !custom;
    toInput.disabled = !custom;
  });
  audienceSelect?.addEventListener("change", () => load({ silent: false }));
  markInternalBtn?.addEventListener("click", () => {
    try {
      localStorage.setItem(MARK_KEY, "internal");
      syncMarkUi();
      setStatus("This browser is marked Internal. Public External reports will exclude it. Marker persists after logout.", "ok");
    } catch (_) {
      setStatus("Could not mark this browser Internal (storage blocked).", "error");
    }
  });
  document.getElementById("dash-unmark-internal")?.addEventListener("click", () => {
    try {
      localStorage.removeItem(MARK_KEY);
      syncMarkUi();
      setStatus("Internal mark removed for this browser. New visits are Unknown until classified.", "ok");
    } catch (_) {
      setStatus("Could not clear Internal mark (storage blocked).", "error");
    }
  });
  syncMarkUi();

  document.getElementById("diagnostics-show-zeros")?.addEventListener("click", () => {
    showZeroDiagnostics = !showZeroDiagnostics;
    renderDiagnostics(lastDiagnostics || lastDashboard?.diagnostics || {});
  });

  const diagnosticsPanel = document.getElementById("diagnostics-panel");
  const syncDiagnosticsExpanded = () => {
    if (!diagnosticsPanel) return;
    diagnosticsPanel.setAttribute("aria-expanded", diagnosticsPanel.open ? "true" : "false");
  };
  diagnosticsPanel?.addEventListener("toggle", syncDiagnosticsExpanded);
  syncDiagnosticsExpanded();

  showLoggedOut();
  const saved = restoreSession();
  if (saved.token) {
    showLoggedIn();
    load({ silent: false }).catch(() => {
      logout();
      setLoginStatus("Session expired. Sign in again.", "error");
    });
  }
})();
