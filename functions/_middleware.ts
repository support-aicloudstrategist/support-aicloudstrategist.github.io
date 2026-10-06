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
  "/", "/about", "/pricing", "/free-business-review", "/portfolio",
  "/portfolio/production-ai-readiness-sample", "/portfolio/cloud-ai-economics-sample",
  "/services/production-ai-readiness", "/services/cloud-ai-economics",
  "/visibility-methodology", "/resources", "/privacy", "/terms",
  "/resources/global-ai-pilot-production-go-no-go-decision-record-template",
  "/resources/global-ai-pilot-model-evaluation-regression-drift-faq",
  "/resources/global-ai-pilot-human-override-escalation-matrix",
  "/resources/global-enterprise-ai-agent-access-review-evidence-checklist",
  "/resources/global-ai-pilot-rollback-readiness-checklist",
  "/resources/cloud-ai-economics-decision-pack",
  "/resources/ai-cost-savings-claim-boundary-worksheet",
  "/resources/global-ai-agent-cost-overrun-owner-evidence-checklist",
  "/resources/global-enterprise-ai-cost-anomaly-approval-runbook",
  "/resources/kubernetes-namespace-cost-owner-dashboard-demo",
  "/resources/uae-healthtech-cloud-trust-executive-summary",
  "/resources/europe-saas-ai-governance-evidence-diagnostic-package",
]);

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
  const method = context.request.method.toUpperCase();
  const accept = context.request.headers.get("Accept") || "";
  const extension = pathname && pathname.split("/").pop()?.includes(".");
  const isDocument = method === "GET" && (!extension || accept.includes("text/html"));
  if (!pathname || !isDocument || indexableExact.has(pathname)) return response;

  const headers = new Headers(response.headers);
  headers.set("X-Robots-Tag", "noindex, follow, noarchive");
  return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
};
