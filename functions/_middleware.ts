const blockedExact = new Set([
  "/CLAUDE.md",
  "/DEPLOYMENT.md",
  "/contact-channels.json",
  "/gtm.csv",
  "/prospects.csv",
  "/internal.html",
]);

const blockedPrefixes = [
  "/reports/",
  "/_workspace/",
  "/.workspace-snapshots/",
  "/week1-brief/",
  "/week2-brief/",
  "/preview/",
];

export const onRequest: PagesFunction = async (context) => {
  const pathname = new URL(context.request.url).pathname;
  const blocked = blockedExact.has(pathname) || blockedPrefixes.some((prefix) => pathname.startsWith(prefix));

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
