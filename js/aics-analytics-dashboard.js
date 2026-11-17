(() => {
  const TOKEN_KEY = "aics_report_token_v1";
  const statusEl = document.getElementById("dash-status");
  const tokenInput = document.getElementById("dash-token");
  const daysSelect = document.getElementById("dash-days");
  const fromInput = document.getElementById("dash-from");
  const toInput = document.getElementById("dash-to");
  const liveUpdated = document.getElementById("live-updated");

  const charts = {};
  let pollTimer = null;

  const palette = ["#0d7a75", "#0f3350", "#1aa39b", "#4a6075", "#7fd4cf", "#c45c26", "#5b7cfa", "#8a4b12"];

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

  const escapeHtml = (value) =>
    String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");

  const ensureChartJs = () =>
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
    });

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
      charts[key].options = config.options;
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
      legend: {
        position: "bottom",
        labels: { boxWidth: 12, color: "#4a6075" },
      },
      tooltip: {
        backgroundColor: "#0f3350",
        titleColor: "#fff",
        bodyColor: "#e8f2f8",
      },
    },
  };

  const entriesToXY = (items, limit = 12) => {
    const rows = (items || []).slice(0, limit);
    return {
      labels: rows.map((row) => String(row.key || row.path || "—")),
      values: rows.map((row) => Number(row.count ?? row.value ?? row.avg_dwell_seconds ?? 0) || 0),
    };
  };

  const renderRealtime = (rt) => {
    document.getElementById("kpi-live").textContent = fmt(rt.live_visitors);
    document.getElementById("kpi-entering").textContent = fmt(rt.entering_visitors);

    const pages = entriesToXY(rt.pages_in_view || []);
    upsertChart("livePages", "chart-live-pages", {
      type: "bar",
      data: {
        labels: pages.labels,
        datasets: [{ label: "Active on page", data: pages.values, backgroundColor: "#0d7a75" }],
      },
      options: {
        ...baseOptions,
        indexAxis: "y",
        plugins: { ...baseOptions.plugins, legend: { display: false } },
        scales: { x: { beginAtZero: true, ticks: { precision: 0 } }, y: { ticks: { autoSkip: false } } },
      },
    });

    const sources = entriesToXY(rt.traffic_sources || []);
    upsertChart("liveSources", "chart-live-sources", {
      type: "doughnut",
      data: {
        labels: sources.labels,
        datasets: [{ data: sources.values, backgroundColor: palette }],
      },
      options: { ...baseOptions, cutout: "55%" },
    });

    const locations = entriesToXY(rt.locations || []);
    upsertChart("liveLocations", "chart-live-locations", {
      type: "bar",
      data: {
        labels: locations.labels,
        datasets: [{ label: "Active by country", data: locations.values, backgroundColor: "#0f3350" }],
      },
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
    liveUpdated.textContent = `Auto-refresh every ${rt.refresh_hint_seconds || 15}s · window ${rt.window_seconds || 120}s · aggregated only`;
  };

  const renderDashboard = (data) => {
    const ov = data.overview || {};
    const aud = data.audience || {};
    const traf = data.traffic || {};
    const eng = data.engagement || {};
    const leads = data.leads || {};

    document.getElementById("kpi-visitors").textContent = fmt(ov.visitors);
    document.getElementById("kpi-views").textContent = fmt(ov.page_views);
    document.getElementById("kpi-sessions").textContent = fmt(ov.sessions);
    document.getElementById("kpi-conversions").textContent = fmt(ov.conversions);

    const growth = ov.growth || [];
    upsertChart("growth", "chart-growth", {
      type: "line",
      data: {
        labels: growth.map((d) => d.day),
        datasets: [
          {
            label: "Page views",
            data: growth.map((d) => d.page_views || 0),
            borderColor: "#0d7a75",
            backgroundColor: "rgba(13,122,117,0.15)",
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
      options: {
        ...baseOptions,
        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
      },
    });

    const nr = Object.entries(aud.new_vs_returning || {}).map(([key, count]) => ({ key, count }));
    const nrXY = entriesToXY(nr);
    upsertChart("audienceNR", "chart-audience-nr", {
      type: "doughnut",
      data: { labels: nrXY.labels, datasets: [{ data: nrXY.values, backgroundColor: ["#0d7a75", "#0f3350", "#4a6075"] }] },
      options: { ...baseOptions, cutout: "50%" },
    });

    const loc = entriesToXY(aud.locations || []);
    upsertChart("audienceLoc", "chart-audience-locations", {
      type: "bar",
      data: { labels: loc.labels, datasets: [{ label: "Page views", data: loc.values, backgroundColor: "#1aa39b" }] },
      options: {
        ...baseOptions,
        plugins: { ...baseOptions.plugins, legend: { display: false } },
        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
      },
    });

    document.getElementById("age-note").textContent =
      (aud.age && aud.age.note) || "Age is not available from browsers.";

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
      data: { labels: providers.labels, datasets: [{ label: "Page views", data: providers.values, backgroundColor: "#0f3350" }] },
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
            label: "Avg dwell (seconds)",
            data: content.map((row) => row.avg_dwell_seconds || 0),
            backgroundColor: "#0d7a75",
          },
          {
            label: "Page views",
            data: content.map((row) => row.page_views || 0),
            backgroundColor: "#0f3350",
          },
        ],
      },
      options: {
        ...baseOptions,
        indexAxis: "y",
        scales: { x: { beginAtZero: true, ticks: { precision: 0 } } },
      },
    });

    const contentRows = content
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
      await ensureChartJs();
      const response = await fetch(queryUrl(), {
        headers: { Authorization: `Bearer ${auth}` },
        cache: "no-store",
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok || !data.ok) {
        throw new Error(data.error || `Request failed (${response.status})`);
      }
      renderDashboard(data);
      setStatus("Live. Charts and real-time panel auto-refresh.", "ok");
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
    Object.keys(charts).forEach(destroyChart);
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
