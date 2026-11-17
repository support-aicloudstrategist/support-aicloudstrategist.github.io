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
  "/services",
  "/request-fit-review",
  "/resources",
  "/resources/what-is-cloud-cost-ownership",
  "/resources/why-fixed-fee-diagnostics-beat-savings-share",
  "/resources/how-to-read-a-cloud-bill",
  "/resources/sample-diagnostic-deliverable",
  "/resources/gpu-and-llm-inference-cost-governance",
  "/resources/ai-agent-and-cloud-automation-cost-checklist",
  "/resources/europe-saas-ai-finops-vs-cloud-cost-tools-comparison",
  "/resources/cloud-cogs-for-the-board-and-saas-gross-margin",
  "/resources/kubernetes-eks-aks-gke-cost-allocation-guide",
  "/why",
  "/why/finance",
  "/why/engineering",
  "/why/operations",
  "/why/minimize-waste",
  "/why/reduce-risk",
  "/privacy",
  "/terms",
  "/40e44a58612d3ad782ec35d292fa20ce.txt",
]);

/** Private HTML routes served with noindex (token-gated dashboards, etc.). */
const privateExact = new Set(["/analytics"]);

const legacyRedirects = new Map<string, string>([
  ["/index.html", "/"],
  ["/about.html", "/about/"],
  ["/resources.html", "/resources/"],
  ["/privacy.html", "/privacy"],
  ["/terms.html", "/terms"],
  ["/pricing.html", "/pricing/"],
  ["/contact", "/request-fit-review/"],
  ["/contact.html", "/request-fit-review/"],
  ["/book", "/request-fit-review/"],
  ["/book.html", "/request-fit-review/"],
  ["/free-business-review", "/request-fit-review/"],
  ["/free-business-review.html", "/request-fit-review/"],
  ["/services/cloud-ai-economics", "/services/"],
  ["/services/cloud-finops", "/services/"],
  ["/cloud-trust-finops", "/services/"],
  ["/cloud-ai-cost-governance-diagnostic", "/services/"],
  ["/cloud-cost-optimization", "/services/"],
  ["/finops-consulting", "/services/"],
  ["/reduce-cloud-spend", "/services/"],
  ["/aws-cost-optimization", "/services/"],
  ["/azure-cost-optimization", "/services/"],
  ["/gcp-cost-optimization", "/services/"],
  ["/kubernetes-cost-optimization", "/services/"],
  ["/gpu-ai-cost-optimization", "/services/"],
  ["/cloud-cost-audit", "/services/"],
  ["/cloud-cost-governance", "/services/"],
  ["/hi/cloud-cost-optimization", "/services/"],
  ["/resources/cloud-ai-economics-decision-pack", "/services/"],
  ["/trust-data-handling", "/privacy"],
  ["/company-details", "/about/"],
  ["/cloud-cost", "/services/"],
  ["/finops", "/services/"],
  ["/ai-cloud-cost-review", "/services/"],
  ["/ai-cloud-cost-efficiency", "/services/"],
  ["/portfolio/cloud-ai-economics-sample", "/services/"],
  ["/resources/ai-cost-savings-claim-boundary-worksheet", "/services/"],
  ["/resources/global-ai-agent-cost-overrun-owner-evidence-checklist", "/services/"],
  ["/resources/global-enterprise-ai-cost-anomaly-approval-runbook", "/services/"],
  ["/resources/kubernetes-namespace-cost-owner-dashboard-demo", "/services/"],
  ["/cloud-waste-reduction", "/services/"],
  ["/cloud-bill-shock", "/services/"],
  ["/cloud-overspending", "/services/"],
  ["/cloud-rightsizing", "/services/"],
  ["/cloud-tco", "/services/"],
  ["/multi-cloud-cost-management", "/services/"],
  ["/cloud-financial-management", "/services/"],
  ["/cloud-showback", "/services/"],
  ["/cloud-chargeback", "/services/"],
  ["/cloud-tagging-strategy", "/services/"],
  ["/cloud-cost-allocation", "/services/"],
  ["/cloud-spend-analysis", "/services/"],
  ["/cloud-anomaly-detection", "/services/"],
  ["/cloud-cost-monitoring", "/services/"],
  ["/reduce-aws-bill", "/services/"],
  ["/cut-azure-spend", "/services/"],
  ["/gcp-cost-savings", "/services/"],
  ["/container-cost-optimization", "/services/"],
  ["/serverless-cost-optimization", "/services/"],
  ["/ai-infrastructure-cost", "/services/"],
  ["/llm-cost-optimization", "/services/"],
  ["/advisory", "/services/"],
  ["/advisory.html", "/services/"],
  ["/case-studies", "/resources/sample-diagnostic-deliverable/"],
  ["/services/production-ai-readiness", "/resources/ai-agent-and-cloud-automation-cost-checklist/"],
  ["/ai-automation-agency", "/resources/ai-agent-and-cloud-automation-cost-checklist/"],
  ["/resources/dpdp-compliance-checklist-dental-clinics-india", "/resources/"],
  ["/resources/global-b2b-saas-trial-to-paid-conversion-follow-up-evidence-checklist", "/resources/"],
  ["/resources/india-coaching-centre-admission-follow-up-checklist", "/resources/"],
  ["/resources/italy-whatsapp-crm-ai-automation-diagnostic-package", "/resources/"],
]);

const legacyPrefixRedirects: Array<[string, string]> = [
  ["/services/cloud-ai-economics/", "/services/"],
  ["/services/cloud-finops/", "/services/"],
  ["/services/production-ai-readiness/", "/resources/ai-agent-and-cloud-automation-cost-checklist/"],
  ["/ai-automation-agency-", "/resources/ai-agent-and-cloud-automation-cost-checklist/"],
  ["/ai-automation-agency/", "/resources/ai-agent-and-cloud-automation-cost-checklist/"],
  ["/case-studies/", "/resources/sample-diagnostic-deliverable/"],
  ["/advisory/", "/services/"],
  ["/dpdp-", "/services/"],
  ["/resources/uae-saas-cloud-finops", "/resources/europe-saas-ai-finops-vs-cloud-cost-tools-comparison/"],
  ["/resources/finops-cloud-cost-management-tools", "/resources/europe-saas-ai-finops-vs-cloud-cost-tools-comparison/"],
  ["/resources/", "/resources/"],
  ["/resources/dpdp-compliance-checklist-dental-clinics-india/", "/resources/"],
  ["/resources/global-b2b-saas-trial-to-paid-conversion-follow-up-evidence-checklist/", "/resources/"],
  ["/resources/india-coaching-centre-admission-follow-up-checklist/", "/resources/"],
  ["/resources/italy-whatsapp-crm-ai-automation-diagnostic-package/", "/resources/"],
  ["/cloud-ai-cost-governance-diagnostic/", "/services/"],
  ["/cloud-cost-optimization/", "/services/"],
  ["/finops-consulting/", "/services/"],
  ["/reduce-cloud-spend/", "/services/"],
  ["/aws-cost-optimization/", "/services/"],
  ["/azure-cost-optimization/", "/services/"],
  ["/gcp-cost-optimization/", "/services/"],
  ["/kubernetes-cost-optimization/", "/services/"],
  ["/gpu-ai-cost-optimization/", "/services/"],
  ["/cloud-cost-audit/", "/services/"],
  ["/cloud-cost-governance/", "/services/"],
  ["/hi/", "/services/"],
  ["/trust-data-handling/", "/privacy"],
  ["/company-details/", "/about/"],
  ["/cloud-cost/", "/services/"],
  ["/finops/", "/services/"],
  ["/book/", "/request-fit-review/"],
  ["/free-business-review/", "/request-fit-review/"],
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

const GA4_MEASUREMENT_ID = "G-5F6Y7JZFB5";

function injectGeoScript(response: Response, geo: { country: string; currency: "INR" | "USD" }, headers: Headers): Response {
  const payload = JSON.stringify(geo).replace(/</g, "\\u003c");
  let sawGaTag = false;
  const transformed = new HTMLRewriter()
    .on('script[src*="googletagmanager.com/gtag/js"]', {
      element() {
        sawGaTag = true;
      },
    })
    .on("head", {
      element(element) {
        element.append(
          `<script>window.__AICS_GEO__=${payload};</script>`,
          { html: true },
        );
        element.onEndTag((endTag) => {
          if (!sawGaTag) {
            endTag.before(
              `<script async src="https://www.googletagmanager.com/gtag/js?id=${GA4_MEASUREMENT_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}window.__AICS_GA4_INITIALIZED__=true;gtag('js',new Date());gtag('config','${GA4_MEASUREMENT_ID}',{transport_type:'beacon'});</script>`,
              { html: true },
            );
          }
        });
      },
    })
    .transform(response);

  return new Response(transformed.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

/** Canonical public sitemap. Served from middleware so a stuck static/edge copy cannot pin 7 URLs. */
const sitemapEntries: Array<{ loc: string; lastmod: string }> = [
  { loc: "/", lastmod: "2026-11-17" },
  { loc: "/services/", lastmod: "2026-11-17" },
  { loc: "/pricing/", lastmod: "2026-11-15" },
  { loc: "/request-fit-review/", lastmod: "2026-11-17" },
  { loc: "/why/", lastmod: "2026-11-13" },
  { loc: "/why/finance/", lastmod: "2026-11-13" },
  { loc: "/why/engineering/", lastmod: "2026-11-13" },
  { loc: "/why/operations/", lastmod: "2026-11-13" },
  { loc: "/why/minimize-waste/", lastmod: "2026-11-13" },
  { loc: "/why/reduce-risk/", lastmod: "2026-11-13" },
  { loc: "/resources/", lastmod: "2026-11-17" },
  { loc: "/resources/what-is-cloud-cost-ownership/", lastmod: "2026-11-17" },
  { loc: "/resources/why-fixed-fee-diagnostics-beat-savings-share/", lastmod: "2026-11-17" },
  { loc: "/resources/how-to-read-a-cloud-bill/", lastmod: "2026-11-17" },
  { loc: "/resources/sample-diagnostic-deliverable/", lastmod: "2026-11-17" },
  { loc: "/resources/gpu-and-llm-inference-cost-governance/", lastmod: "2026-11-17" },
  { loc: "/resources/ai-agent-and-cloud-automation-cost-checklist/", lastmod: "2026-11-17" },
  { loc: "/resources/europe-saas-ai-finops-vs-cloud-cost-tools-comparison/", lastmod: "2026-11-17" },
  { loc: "/resources/cloud-cogs-for-the-board-and-saas-gross-margin/", lastmod: "2026-11-17" },
  { loc: "/resources/kubernetes-eks-aks-gke-cost-allocation-guide/", lastmod: "2026-11-17" },
  { loc: "/about/", lastmod: "2026-11-14" },
  { loc: "/privacy", lastmod: "2026-11-10" },
  { loc: "/terms", lastmod: "2026-11-10" },
];

function buildSitemapXml(origin: string): string {
  const urls = sitemapEntries
    .map((entry) => `  <url><loc>${origin}${entry.loc}</loc><lastmod>${entry.lastmod}</lastmod></url>`)
    .join("\n");
  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>
`;
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

  // Bypass any stuck static/edge sitemap.xml (observed live loc count=7 while git has 17).
  if (pathname === "/sitemap.xml") {
    const origin = "https://aicloudstrategist.com";
    const body = buildSitemapXml(origin);
    return new Response(body, {
      status: 200,
      headers: {
        "Content-Type": "application/xml; charset=utf-8",
        "Cache-Control": "public, max-age=0, must-revalidate",
        "X-AICS-Sitemap": "middleware-17",
      },
    });
  }

  const response = await context.next();
  const requestUrl = new URL(context.request.url);
  const method = context.request.method.toUpperCase();
  // API/functions responses must pass through unchanged (pathnames like /api/chat
  // look "extensionless" and would otherwise be treated as HTML documents).
  if (pathname === "/api" || pathname.startsWith("/api/")) return response;
  if (
    pathname === "/robots.txt"
    || pathname === "/llms.txt"
    || pathname === "/llms-full.txt"
    || pathname === "/40e44a58612d3ad782ec35d292fa20ce.txt"
  ) {
    return response;
  }
  const filename = pathname?.split("/").pop() || "";
  const isHtmlPath = !filename.includes(".") || filename.toLowerCase().endsWith(".html");
  const isDocument = (method === "GET" || method === "HEAD") && isHtmlPath;
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

  if (privateExact.has(pathname)) {
    const headers = withGeoHeaders(response.headers, geo);
    headers.set("Content-Type", "text/html; charset=utf-8");
    headers.set("Cache-Control", "no-store");
    headers.set("X-Robots-Tag", "noindex, nofollow, noarchive");
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
