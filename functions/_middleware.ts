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

  return context.next();
};
