const blockedExact = new Set([
  "/.gitattributes",
  "/.gitignore",
  "/.nojekyll",
  "/_headers",
  "/_redirects",
  "/_routes.json",
  "/CLAUDE.md",
  "/DEPLOYMENT.md",
  "/contact-channels.json",
  "/client-desk",
  "/client-desk.html",
  "/gtm.csv",
  "/prospects.csv",
  "/internal",
  "/internal.html",
  "/tools/brand_trust_monitor.py",
  "/tools/layman_problem_search_score.py",
]);

const blockedPrefixes = [
  "/.github/",
  "/.hermes/",
  "/.workspace-snapshots/",
  "/.venv/",
  "/docs/",
  "/node_modules/",
  "/phase-",
  "/reports/",
  "/scripts/",
  "/seo/",
  "/tests/",
  "/_workspace/",
  "/week1-brief/",
  "/week2-brief/",
  "/preview/",
];

const indexableExact = new Set([
  "/",
  "/about",
  "/pricing",
  "/cloud-ai-cost-governance-diagnostic",
  "/cloud-cost-optimization",
  "/finops-consulting",
  "/reduce-cloud-spend",
  "/aws-cost-optimization",
  "/azure-cost-optimization",
  "/gcp-cost-optimization",
  "/kubernetes-cost-optimization",
  "/gpu-ai-cost-optimization",
  "/cloud-cost-audit",
  "/cloud-cost-governance",
  "/hi/cloud-cost-optimization",
  "/resources",
  "/resources/cloud-ai-economics-decision-pack",
  "/trust-data-handling",
  "/request-fit-review",
  "/company-details",
  "/privacy",
  "/terms",
]);

const legacyRedirects = new Map<string, string>([
  ["/contact", "/request-fit-review/"],
  ["/contact.html", "/request-fit-review/"],
  ["/free-business-review", "/request-fit-review/"],
  ["/free-business-review.html", "/request-fit-review/"],
  ["/pricing.html", "/pricing/"],
  ["/services/cloud-ai-economics", "/cloud-ai-cost-governance-diagnostic/"],
  ["/services/cloud-finops", "/cloud-ai-cost-governance-diagnostic/"],
  ["/cloud-trust-finops", "/cloud-ai-cost-governance-diagnostic/"],
  ["/cloud-cost", "/cloud-cost-optimization/"],
  ["/finops", "/finops-consulting/"],
  ["/ai-cloud-cost-review", "/gpu-ai-cost-optimization/"],
  ["/ai-cloud-cost-efficiency", "/gpu-ai-cost-optimization/"],
  ["/portfolio/cloud-ai-economics-sample", "/resources/cloud-ai-economics-decision-pack/"],
  ["/resources/ai-cost-savings-claim-boundary-worksheet", "/resources/cloud-ai-economics-decision-pack/"],
  ["/resources/global-ai-agent-cost-overrun-owner-evidence-checklist", "/gpu-ai-cost-optimization/"],
  ["/resources/global-enterprise-ai-cost-anomaly-approval-runbook", "/cloud-cost-audit/"],
  ["/resources/kubernetes-namespace-cost-owner-dashboard-demo", "/kubernetes-cost-optimization/"],
  ["/cloud-waste-reduction", "/reduce-cloud-spend/"],
  ["/cloud-bill-shock", "/reduce-cloud-spend/"],
  ["/cloud-overspending", "/reduce-cloud-spend/"],
  ["/cloud-rightsizing", "/cloud-cost-optimization/"],
  ["/cloud-tco", "/cloud-cost-optimization/"],
  ["/multi-cloud-cost-management", "/cloud-cost-optimization/"],
  ["/cloud-financial-management", "/finops-consulting/"],
  ["/cloud-showback", "/finops-consulting/"],
  ["/cloud-chargeback", "/finops-consulting/"],
  ["/cloud-tagging-strategy", "/cloud-cost-governance/"],
  ["/cloud-cost-allocation", "/cloud-cost-governance/"],
  ["/cloud-spend-analysis", "/cloud-cost-audit/"],
  ["/cloud-anomaly-detection", "/cloud-cost-audit/"],
  ["/cloud-cost-monitoring", "/cloud-cost-audit/"],
  ["/reduce-aws-bill", "/aws-cost-optimization/"],
  ["/cut-azure-spend", "/azure-cost-optimization/"],
  ["/gcp-cost-savings", "/gcp-cost-optimization/"],
  ["/container-cost-optimization", "/kubernetes-cost-optimization/"],
  ["/serverless-cost-optimization", "/cloud-cost-optimization/"],
  ["/ai-infrastructure-cost", "/gpu-ai-cost-optimization/"],
  ["/llm-cost-optimization", "/gpu-ai-cost-optimization/"],
]);

const legacyPrefixRedirects: Array<[string, string]> = [
  ["/services/cloud-ai-economics/", "/cloud-ai-cost-governance-diagnostic/"],
  ["/services/cloud-finops/", "/cloud-ai-cost-governance-diagnostic/"],
  ["/cloud-cost/", "/cloud-cost-optimization/"],
  ["/finops/", "/finops-consulting/"],
];

function canonicalizePathname(pathname: string): string | null {
  let decoded = pathname;

  try {
    // Cloudflare's asset resolver decodes paths after middleware. Mirror that
    // behavior so encoded and double-encoded names cannot bypass the denylist.
    for (let pass = 0; pass < 4; pass += 1) {
      const next = decodeURIComponent(decoded);
      if (next === decoded) break;
      decoded = next;
    }
  } catch {
    return null;
  }

  decoded = decoded.replace(/\\/g, "/").replace(/\/{2,}/g, "/");

  const segments: string[] = [];
  for (const segment of decoded.split("/")) {
    if (!segment || segment === ".") continue;
    if (segment === "..") {
      segments.pop();
      continue;
    }
    segments.push(segment);
  }

  return `/${segments.join("/")}`;
}

function isBlockedPath(pathname: string): boolean {
  if (blockedExact.has(pathname)) return true;

  return blockedPrefixes.some((prefix) => {
    if (prefix.endsWith("/")) {
      return pathname === prefix.slice(0, -1) || pathname.startsWith(prefix);
    }
    return pathname.startsWith(prefix);
  });
}

/** Geo display currency from Cloudflare edge country. India → INR fee band; all others → USD.
 * Optional `?geo=US` / `?geo=IN` (or any ISO country) overrides CF-IPCountry for QA; not for SEO. */
function geoCurrency(request: Request): { country: string; currency: "INR" | "USD" } {
  const url = new URL(request.url);
  const geoParam = (url.searchParams.get("geo") || "").toUpperCase();
  const cfCountry = (request.headers.get("CF-IPCountry") || "").toUpperCase();
  const country = (geoParam || cfCountry || "XX").replace(/[^A-Z]/g, "").slice(0, 2) || "XX";
  const currency = country === "IN" ? "INR" : "USD";
  return { country, currency };
}

function withGeoHeaders(headers: Headers, geo: { country: string; currency: "INR" | "USD" }): Headers {
  const next = new Headers(headers);
  // Personalized currency must not be shared across countries at the edge.
  next.set("Cache-Control", "private, no-store");
  next.set("Set-Cookie", `aics_currency=${geo.currency}; Path=/; Max-Age=86400; SameSite=Lax`);
  next.set("X-AICS-Currency", geo.currency);
  next.set("X-AICS-Country", geo.country);
  next.append("Vary", "CF-IPCountry");
  return next;
}

function injectGeoScript(response: Response, geo: { country: string; currency: "INR" | "USD" }, headers: Headers): Response {
  const payload = JSON.stringify(geo).replace(/</g, "\\u003c");
  const transformed = new HTMLRewriter()
    .on("head", {
      element(element) {
        element.append(
          `<script>window.__AICS_GEO__=${payload};</script>`,
          { html: true },
        );
      },
    })
    .transform(response);

  return new Response(transformed.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

export const onRequest: PagesFunction = async (context) => {
  const pathname = canonicalizePathname(new URL(context.request.url).pathname);
  const blocked = pathname === null || isBlockedPath(pathname);

  if (blocked) {
    return new Response("Not Found", {
      status: 404,
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "no-store",
        "X-Robots-Tag": "noindex, nofollow, noarchive",
      },
    });
  }

  const response = await context.next();
  const requestUrl = new URL(context.request.url);
  const method = context.request.method.toUpperCase();
  const accept = context.request.headers.get("Accept") || "";
  const filename = pathname?.split("/").pop() || "";
  const isHtmlPath = !filename.includes(".") || filename.toLowerCase().endsWith(".html");
  const isDocument = (method === "GET" || method === "HEAD") && (isHtmlPath || accept.includes("text/html"));
  if (!pathname || !isDocument) return response;

  const geo = geoCurrency(context.request);

  if (indexableExact.has(pathname)) {
    const headers = withGeoHeaders(response.headers, geo);
    headers.set("Content-Type", "text/html; charset=utf-8");
    if (requestUrl.hostname.endsWith(".pages.dev")) headers.set("X-Robots-Tag", "noindex, follow, noarchive");
    else headers.delete("X-Robots-Tag");
    return injectGeoScript(
      new Response(response.body, { status: response.status, statusText: response.statusText, headers }),
      geo,
      headers,
    );
  }

  const legacyTarget = legacyRedirects.get(pathname)
    || legacyPrefixRedirects.find(([prefix]) => pathname.startsWith(prefix))?.[1];
  if (legacyTarget) {
    return new Response(null, {
      status: 301,
      headers: {
        Location: new URL(legacyTarget, requestUrl).toString(),
        "Cache-Control": "public, max-age=300",
        "X-Robots-Tag": "noindex, follow, noarchive",
      },
    });
  }

  if (response.status >= 400) {
    const headers = new Headers(response.headers);
    headers.set("Cache-Control", "no-store");
    headers.set("X-Robots-Tag", "noindex, nofollow, noarchive");
    return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
  }

  return new Response("Not Found", {
    status: 404,
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "no-store",
      "X-Robots-Tag": "noindex, nofollow, noarchive",
    },
  });
};
