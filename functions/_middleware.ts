export const onRequest: PagesFunction = async (context) => {
  const pathname = new URL(context.request.url).pathname;
  if (pathname.startsWith("/.workspace-snapshots/") || pathname.startsWith("/_workspace/")) {
    return new Response("Not found", {
      status: 404,
      headers: {
        "Cache-Control": "no-store",
        "X-Robots-Tag": "noindex, nofollow, noarchive",
      },
    });
  }
  return await context.next();
};
