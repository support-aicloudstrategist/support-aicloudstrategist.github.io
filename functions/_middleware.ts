// AICloudStrategist edge middleware.
// Runs on every route (_routes.json include "/*"). Because Functions intercept
// all requests, Cloudflare's _redirects file is bypassed — so retirement
// redirects are handled here to guarantee they apply.

const EXACT: Record<string, string> = {
  "/about.html": "/about/",
  "/pricing.html": "/pricing/",
  "/contact.html": "/contact/",
  "/free-business-review": "/cost-teardown/",
  "/free-business-review/": "/cost-teardown/",
  "/free-business-review.html": "/cost-teardown/",
  "/advisory.html": "/ai-cloud-cost/",
  "/audit.html": "/cost-teardown/",
  "/book.html": "/cost-teardown/",
  "/industries.html": "/web-seo/",
  "/products.html": "/web-seo/",
  "/factory-website-development-india.html": "/web-seo/",
  "/local-business-website-india.html": "/web-seo/",
  "/small-business-automation-india.html": "/web-seo/",
  "/smb-website-checklist-india.html": "/web-seo/",
  "/whatsapp-lead-management-india.html": "/web-seo/",
  "/whatsapp-link-generator.html": "/web-seo/",
  "/operations-automation-sprint.html": "/web-seo/",
  "/website-lead-capture-sprint.html": "/web-seo/",
  "/lead-follow-up-checklist-india.html": "/web-seo/",
  "/lead-leakage-calculator.html": "/web-seo/",
  "/client-desk.html": "/",
  "/resources.html": "/",
  "/local.html": "/",
  "/payments.html": "/",
  "/policykart.html": "/",
  "/thank-you.html": "/",
  "/dpdp-breach-readiness-checklist.html": "/",
  "/dpdp-compliance-checklist-india.html": "/",
  "/dpdp-compliance-consultant-india.html": "/",
  "/dpdp-compliance-for-d2c-brands.html": "/",
  "/dpdp-compliance-for-saas-india.html": "/",
  "/dpdp-consent-flow-checklist.html": "/",
  "/dpdp-readiness-assessment.html": "/",
  "/dpdp-vendor-register-template.html": "/",
  "/dpdp-website-compliance-sprint.html": "/",
};

// Prefix → destination. Matches the path or any sub-path.
const PREFIX: Array<[string, string]> = [
  ["/cloud-trust-finops", "/ai-cloud-cost/"],
  ["/roi-calculator", "/ai-cloud-cost/"],
  ["/blog", "/ai-cloud-cost/"],
  ["/papers", "/ai-cloud-cost/"],
  ["/website-digital-presence", "/web-seo/"],
  ["/services", "/web-seo/"],
  ["/lead-capture-follow-up", "/web-seo/"],
  ["/trust-compliance", "/web-seo/"],
  ["/ai-creative-studio", "/web-seo/"],
  ["/growth-control-os", "/web-seo/"],
  ["/how-we-work", "/web-seo/"],
  ["/partners", "/web-seo/"],
  ["/case-studies", "/web-seo/"],
  ["/healthcare-growthos", "/"],
  ["/healthcare-roi-leakage-calculator", "/"],
  ["/aesthetic-clinics", "/"],
  ["/dpdp-for-clinics", "/"],
  ["/dpdp-for-diagnostic-labs", "/"],
  ["/webinars", "/"],
  ["/resources", "/"],
];

function resolveRedirect(pathname: string): string | null {
  if (EXACT[pathname]) return EXACT[pathname];
  for (const [prefix, dest] of PREFIX) {
    if (pathname === prefix || pathname.startsWith(prefix + "/")) return dest;
  }
  return null;
}

export const onRequest: PagesFunction = async (context) => {
  const url = new URL(context.request.url);
  const p = url.pathname;

  // Block internal / sensitive artifacts.
  if (
    p.startsWith("/.workspace-snapshots/") ||
    p.startsWith("/_workspace/") ||
    p.startsWith("/scripts/") ||
    p.startsWith("/preview/") ||
    p === "/contact-channels.json" ||
    p === "/payment-config.json"
  ) {
    return new Response("Not found", {
      status: 404,
      headers: {
        "Cache-Control": "no-store",
        "X-Robots-Tag": "noindex, nofollow, noarchive",
      },
    });
  }

  // Retirement redirects (301).
  const dest = resolveRedirect(p);
  if (dest) {
    return Response.redirect(url.origin + dest, 301);
  }

  return await context.next();
};
