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
  "/cloud-ai-cost-governance-diagnostic",
  "/resources",
  "/resources/cloud-ai-economics-decision-pack",
  "/trust-data-handling",
  "/request-fit-review",
  "/company-details",
  "/privacy",
  "/terms",
]);

const utilityExact = new Set(["/lead-desk"]);

const legacyRedirects = new Map<string, string>([
  ["/contact", "/request-fit-review/"],
  ["/contact.html", "/request-fit-review/"],
  ["/free-business-review", "/request-fit-review/"],
  ["/free-business-review.html", "/request-fit-review/"],
  ["/pricing", "/cloud-ai-cost-governance-diagnostic/"],
  ["/pricing.html", "/cloud-ai-cost-governance-diagnostic/"],
  ["/services/cloud-ai-economics", "/cloud-ai-cost-governance-diagnostic/"],
  ["/services/cloud-finops", "/cloud-ai-cost-governance-diagnostic/"],
  ["/cloud-trust-finops", "/cloud-ai-cost-governance-diagnostic/"],
  ["/cloud-cost", "/cloud-ai-cost-governance-diagnostic/"],
  ["/finops", "/cloud-ai-cost-governance-diagnostic/"],
  ["/ai-cloud-cost-review", "/cloud-ai-cost-governance-diagnostic/"],
  ["/ai-cloud-cost-efficiency", "/cloud-ai-cost-governance-diagnostic/"],
  ["/portfolio/cloud-ai-economics-sample", "/resources/cloud-ai-economics-decision-pack/"],
  ["/resources/ai-cost-savings-claim-boundary-worksheet", "/resources/cloud-ai-economics-decision-pack/"],
  ["/resources/global-ai-agent-cost-overrun-owner-evidence-checklist", "/cloud-ai-cost-governance-diagnostic/"],
  ["/resources/global-enterprise-ai-cost-anomaly-approval-runbook", "/cloud-ai-cost-governance-diagnostic/"],
  ["/resources/kubernetes-namespace-cost-owner-dashboard-demo", "/resources/cloud-ai-economics-decision-pack/"],
]);

const legacyPrefixRedirects: Array<[string, string]> = [
  ["/services/cloud-ai-economics/", "/cloud-ai-cost-governance-diagnostic/"],
  ["/services/cloud-finops/", "/cloud-ai-cost-governance-diagnostic/"],
  ["/cloud-cost/", "/cloud-ai-cost-governance-diagnostic/"],
  ["/finops/", "/cloud-ai-cost-governance-diagnostic/"],
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
  const isApiPath = Boolean(pathname && pathname.startsWith("/api/"));
  if (isApiPath) return response;
  const method = context.request.method.toUpperCase();
  const accept = context.request.headers.get("Accept") || "";
  const filename = pathname?.split("/").pop() || "";
  const isHtmlPath = !filename.includes(".") || filename.toLowerCase().endsWith(".html");
  const isDocument = (method === "GET" || method === "HEAD") && (isHtmlPath || accept.includes("text/html"));
  if (!pathname || !isDocument) return response;

  if (indexableExact.has(pathname)) {
    const headers = new Headers(response.headers);
    headers.set("Content-Type", "text/html; charset=utf-8");
    if (requestUrl.hostname.endsWith(".pages.dev")) headers.set("X-Robots-Tag", "noindex, follow, noarchive");
    else headers.delete("X-Robots-Tag");
    return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
  }

  if (utilityExact.has(pathname)) {
    const headers = new Headers(response.headers);
    headers.set("Content-Type", "text/html; charset=utf-8");
    headers.set("Cache-Control", "no-store");
    headers.set("X-Robots-Tag", "noindex, nofollow, noarchive");
    return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
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
