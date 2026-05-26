export const onRequest: PagesFunction = async (context) => {
  const url = new URL(context.request.url);
  if (url.pathname.startsWith("/_workspace/")) {
    return new Response("Not found", {
      status: 404,
      headers: {
        "Cache-Control": "no-store",
        "X-Robots-Tag": "noindex, nofollow, noarchive",
      },
    });
  }
  return context.next();
};
