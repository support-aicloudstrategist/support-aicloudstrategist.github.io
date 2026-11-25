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
  "/resources/cloud-ai-cost-governance-before-you-cut",
  "/resources/ai-cost-governance-diagnostic",
  "/resources/why-fixed-fee-diagnostics-beat-savings-share",
  "/resources/how-to-read-a-cloud-bill",
  "/resources/sample-diagnostic-deliverable",
  "/resources/gpu-and-llm-inference-cost-governance",
  "/resources/ai-agent-and-cloud-automation-cost-checklist",
  "/resources/ai-workflow-auto-act-or-ask-first",
  "/resources/whatsapp-lead-follow-up-owner-path",
  "/resources/small-business-ai-automation-owner-path",
  "/resources/saas-exit-readiness-owner-path",
  "/resources/ai-automation-vs-msp-vs-in-house",
  "/resources/ai-tool-pilot-brief",
  "/resources/australia-nz-clinic-patient-growthos-readiness-checklist",
  "/resources/brand-trust-monitoring",
  "/resources/cloud-cost-owner-path",
  "/resources/customer-problem-search/aws-cloud-bill-too-high",
  "/resources/europe-healthtech-ai-trust-finops-readiness-map",
  "/resources/europe-healthtech-procurement-response-readiness-checklist",
  "/resources/global-whatsapp-lead-follow-up-vs-crm-automation-comparison",
  "/resources/ivf-clinic-lead-leakage-owner-map",
  "/resources/india-healthcare-dpdp-patient-growthos-owner-path",
  "/resources/missed-patient-calls-owner-path",
  "/resources/manual-work-automation-owner-path",
  "/resources/manual-data-entry-owner-path",
  "/resources/middle-east-healthcare-growthos-cloud-trust-readiness-map",
  "/resources/middle-east-healthcare-vendor-evidence-checklist",
  "/resources/north-america-healthtech-ai-trust-finops-submission-gate",
  "/resources/singapore-clinic-pdpa-cloud-trust-finops-intake",
  "/publications/2026-11-21",
  "/publications/2026-11-21/ai-tool-pilot-brief",
  "/publications/2026-11-21/ai-workflow-auto-act-or-ask-first",
  "/publications/2026-11-21/ai-tool-pilot-brief.html",
  "/publications/2026-11-21/ai-workflow-auto-act-or-ask-first.html",
  "/publications/2026-11-23",
  "/publications/2026-11-23/ai-tool-access-review",
  "/publications/2026-11-23/ai-tool-access-review.html",
  "/publications/2026-11-24",
  "/publications/2026-11-24/ai-output-verification-loop.html",
  "/publications/2026-11-25",
  "/publications/2026-11-25/recurring-report-automation-handoff",
  "/publications/2026-11-25/recurring-report-automation-handoff.html",
  "/why",
  "/why/finance",
  "/why/engineering",
  "/why/operations",
  "/why/minimize-waste",
  "/why/reduce-risk",
  "/how-we-work",
  "/data-handling",
  "/scope-and-limits",
  "/company",
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
  ["/trust-data-handling", "/data-handling/"],
  ["/company-details", "/company/"],
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
  ["/services/production-ai-readiness", "/services/"],
  ["/ai-automation-agency", "/services/"],
  ["/resources/europe-saas-ai-finops-vs-cloud-cost-tools-comparison", "/resources/why-fixed-fee-diagnostics-beat-savings-share/"],
  ["/resources/dpdp-compliance-checklist-dental-clinics-india", "/resources/"],
  ["/resources/global-b2b-saas-trial-to-paid-conversion-follow-up-evidence-checklist", "/resources/"],
  ["/resources/india-coaching-centre-admission-follow-up-checklist", "/resources/"],
  ["/resources/italy-whatsapp-crm-ai-automation-diagnostic-package", "/resources/"],
  // Buyer-POV cleanup: retire SMB / WhatsApp / DPDP / automation package lanes
  ["/small-business-automation-india", "/services/"],
  ["/small-business-automation-india.html", "/services/"],
  ["/industries", "/services/"],
  ["/industries.html", "/services/"],
  ["/growth-control-os", "/services/"],
  ["/healthcare-enquiry-leakage-scorecard", "/services/"],
  ["/whatsapp-link-generator", "/services/"],
  ["/whatsapp-link-generator.html", "/services/"],
  ["/whatsapp-lead-management-india", "/services/"],
  ["/whatsapp-lead-management-india.html", "/services/"],
  ["/dpdp-website-compliance-sprint", "/services/"],
  ["/dpdp-website-compliance-sprint.html", "/services/"],
  ["/dpdp-vendor-register-template", "/services/"],
  ["/dpdp-vendor-register-template.html", "/services/"],
  ["/dpdp-readiness-assessment", "/services/"],
  ["/dpdp-readiness-assessment.html", "/services/"],
  ["/dpdp-consent-flow-checklist", "/services/"],
  ["/dpdp-consent-flow-checklist.html", "/services/"],
  ["/dpdp-compliance-for-saas-india", "/services/"],
  ["/dpdp-compliance-for-saas-india.html", "/services/"],
  ["/dpdp-compliance-for-d2c-brands", "/services/"],
  ["/dpdp-compliance-for-d2c-brands.html", "/services/"],
  ["/dpdp-compliance-consultant-india", "/services/"],
  ["/dpdp-compliance-consultant-india.html", "/services/"],
  ["/dpdp-compliance-checklist-india", "/services/"],
  ["/dpdp-compliance-checklist-india.html", "/services/"],
  ["/dpdp-breach-readiness-checklist", "/services/"],
  ["/dpdp-breach-readiness-checklist.html", "/services/"],
  ["/operations-automation-sprint", "/services/"],
  ["/operations-automation-sprint.html", "/services/"],
  ["/website-lead-capture-sprint", "/request-fit-review/"],
  ["/website-lead-capture-sprint.html", "/request-fit-review/"],
  ["/audit", "/request-fit-review/"],
  ["/audit.html", "/request-fit-review/"],
  ["/guarantee", "/scope-and-limits/"],
  ["/guarantee.html", "/scope-and-limits/"],
  ["/local-business-website-india", "/services/"],
  ["/local-business-website-india.html", "/services/"],
  ["/factory-website-development-india", "/services/"],
  ["/factory-website-development-india.html", "/services/"],
  ["/lead-follow-up-checklist-india", "/services/"],
  ["/lead-follow-up-checklist-india.html", "/services/"],
  ["/lead-leakage-calculator", "/services/"],
  ["/lead-leakage-calculator.html", "/services/"],
  ["/smb-website-checklist-india", "/services/"],
  ["/smb-website-checklist-india.html", "/services/"],
  ["/products", "/services/"],
  ["/products.html", "/services/"],
  ["/policykart", "/services/"],
  ["/policykart.html", "/services/"],
  ["/client-desk", "/request-fit-review/"],
  ["/client-desk.html", "/request-fit-review/"],
  ["/ai-creative-studio", "/services/"],
  ["/webinars/dpdp-for-clinics-2026", "/services/"],
  ["/local", "/services/"],
  ["/local.html", "/services/"],
  ["/payments", "/request-fit-review/"],
  ["/payments.html", "/request-fit-review/"],
  ["/demos/clinic-growthos-dashboard", "/services/"],
]);

const legacyPrefixRedirects: Array<[string, string]> = [
  ["/services/cloud-ai-economics/", "/services/"],
  ["/services/cloud-finops/", "/services/"],
  ["/services/production-ai-readiness/", "/services/"],
  ["/ai-automation-agency-", "/services/"],
  ["/ai-automation-agency/", "/services/"],
  ["/case-studies/", "/resources/sample-diagnostic-deliverable/"],
  ["/advisory/", "/services/"],
  ["/resources/europe-saas-ai-finops-vs-cloud-cost-tools-comparison/", "/resources/why-fixed-fee-diagnostics-beat-savings-share/"],
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
  ["/trust-data-handling/", "/data-handling/"],
  ["/company-details/", "/company/"],
  ["/cloud-cost/", "/services/"],
  ["/finops/", "/services/"],
  ["/book/", "/request-fit-review/"],
  ["/free-business-review/", "/request-fit-review/"],
  ["/industries/", "/services/"],
  ["/small-business-automation-india/", "/services/"],
  ["/growth-control-os/", "/services/"],
  ["/whatsapp-link-generator/", "/services/"],
  ["/whatsapp-lead-management-india/", "/services/"],
  ["/dpdp-website-compliance-sprint/", "/services/"],
  ["/dpdp-vendor-register-template/", "/services/"],
  ["/dpdp-readiness-assessment/", "/services/"],
  ["/dpdp-consent-flow-checklist/", "/services/"],
  ["/dpdp-compliance-for-saas-india/", "/services/"],
  ["/dpdp-compliance-for-d2c-brands/", "/services/"],
  ["/dpdp-compliance-consultant-india/", "/services/"],
  ["/dpdp-compliance-checklist-india/", "/services/"],
  ["/dpdp-breach-readiness-checklist/", "/services/"],
  ["/operations-automation-sprint/", "/services/"],
  ["/website-lead-capture-sprint/", "/request-fit-review/"],
  ["/audit/", "/request-fit-review/"],
  ["/guarantee/", "/scope-and-limits/"],
  ["/local-business-website-india/", "/services/"],
  ["/factory-website-development-india/", "/services/"],
  ["/lead-follow-up-checklist-india/", "/services/"],
  ["/lead-leakage-calculator/", "/services/"],
  ["/smb-website-checklist-india/", "/services/"],
  ["/products/", "/services/"],
  ["/policykart/", "/services/"],
  ["/client-desk/", "/request-fit-review/"],
  ["/ai-creative-studio/", "/services/"],
  ["/webinars/dpdp-for-clinics-2026/", "/services/"],
  ["/local/", "/services/"],
  ["/payments/", "/request-fit-review/"],
  ["/demos/clinic-growthos-dashboard/", "/services/"],
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
  { loc: "/resources/", lastmod: "2026-11-23" },
  { loc: "/resources/cloud-ai-cost-governance-before-you-cut/", lastmod: "2026-11-24" },
  { loc: "/resources/what-is-cloud-cost-ownership/", lastmod: "2026-11-17" },
  { loc: "/resources/why-fixed-fee-diagnostics-beat-savings-share/", lastmod: "2026-11-17" },
  { loc: "/resources/how-to-read-a-cloud-bill/", lastmod: "2026-11-17" },
  { loc: "/resources/sample-diagnostic-deliverable/", lastmod: "2026-11-17" },
  { loc: "/resources/gpu-and-llm-inference-cost-governance/", lastmod: "2026-11-17" },
  { loc: "/resources/ai-agent-and-cloud-automation-cost-checklist/", lastmod: "2026-11-17" },
  { loc: "/resources/ai-workflow-auto-act-or-ask-first/", lastmod: "2026-11-21" },
  { loc: "/resources/ai-automation-vs-msp-vs-in-house/", lastmod: "2026-11-23" },
  { loc: "/resources/ai-tool-pilot-brief/", lastmod: "2026-11-23" },
  { loc: "/resources/australia-nz-clinic-patient-growthos-readiness-checklist/", lastmod: "2026-11-21" },
  { loc: "/resources/brand-trust-monitoring/", lastmod: "2026-11-20" },
  { loc: "/resources/cloud-cost-owner-path/", lastmod: "2026-11-20" },
  { loc: "/resources/customer-problem-search/aws-cloud-bill-too-high/", lastmod: "2026-11-20" },
  { loc: "/resources/europe-healthtech-ai-trust-finops-readiness-map/", lastmod: "2026-11-23" },
  { loc: "/resources/europe-healthtech-procurement-response-readiness-checklist/", lastmod: "2026-11-23" },
  { loc: "/resources/global-whatsapp-lead-follow-up-vs-crm-automation-comparison/", lastmod: "2026-11-20" },
  { loc: "/resources/ivf-clinic-lead-leakage-owner-map/", lastmod: "2026-11-23" },
  { loc: "/resources/india-healthcare-dpdp-patient-growthos-owner-path/", lastmod: "2026-11-25" },
  { loc: "/resources/manual-work-automation-owner-path/", lastmod: "2026-11-20" },
  { loc: "/resources/middle-east-healthcare-growthos-cloud-trust-readiness-map/", lastmod: "2026-11-20" },
  { loc: "/resources/middle-east-healthcare-vendor-evidence-checklist/", lastmod: "2026-11-21" },
  { loc: "/resources/north-america-healthtech-ai-trust-finops-submission-gate/", lastmod: "2026-11-23" },
  { loc: "/resources/singapore-clinic-pdpa-cloud-trust-finops-intake/", lastmod: "2026-11-20" },
  { loc: "/resources/whatsapp-lead-follow-up-owner-path/", lastmod: "2026-11-21" },
  { loc: "/resources/small-business-ai-automation-owner-path/", lastmod: "2026-11-23" },
  { loc: "/resources/saas-exit-readiness-owner-path/", lastmod: "2026-11-24" },
  { loc: "/publications/2026-11-21/", lastmod: "2026-11-21" },
  { loc: "/publications/2026-11-21/ai-tool-pilot-brief.html", lastmod: "2026-11-21" },
  { loc: "/publications/2026-11-21/ai-tool-pilot-brief.png", lastmod: "2026-11-21" },
  { loc: "/publications/2026-11-21/ai-tool-pilot-brief.svg", lastmod: "2026-11-21" },
  { loc: "/publications/2026-11-21/ai-tool-pilot-brief.csv", lastmod: "2026-11-21" },
  { loc: "/publications/2026-11-21/ai-tool-pilot-brief-answer-card.json", lastmod: "2026-11-21" },
  { loc: "/publications/2026-11-21/ai-workflow-auto-act-or-ask-first.html", lastmod: "2026-11-21" },
  { loc: "/publications/2026-11-21/ai-workflow-auto-act-or-ask-first.png", lastmod: "2026-11-21" },
  { loc: "/publications/2026-11-21/ai-workflow-auto-act-or-ask-first.svg", lastmod: "2026-11-21" },
  { loc: "/publications/2026-11-21/ai-workflow-auto-act-or-ask-first.csv", lastmod: "2026-11-21" },
  { loc: "/publications/2026-11-21/ai-workflow-auto-act-or-ask-first-answer-card.json", lastmod: "2026-11-21" },
  { loc: "/publications/2026-11-23/", lastmod: "2026-11-23" },
  { loc: "/publications/2026-11-23/ai-tool-access-review.html", lastmod: "2026-11-23" },
  { loc: "/publications/2026-11-23/ai-tool-access-review.png", lastmod: "2026-11-23" },
  { loc: "/publications/2026-11-23/ai-tool-access-review.svg", lastmod: "2026-11-23" },
  { loc: "/publications/2026-11-23/ai-tool-access-review.csv", lastmod: "2026-11-23" },
  { loc: "/publications/2026-11-23/ai-tool-access-review-answer-card.json", lastmod: "2026-11-23" },
  { loc: "/publications/2026-11-24/", lastmod: "2026-11-24" },
  { loc: "/publications/2026-11-24/ai-output-verification-loop.html", lastmod: "2026-11-24" },
  { loc: "/publications/2026-11-24/ai-output-verification-loop.csv", lastmod: "2026-11-24" },
  { loc: "/publications/2026-11-24/ai-output-verification-loop-answer-card.json", lastmod: "2026-11-24" },
  { loc: "/publications/2026-11-25/", lastmod: "2026-11-25" },
  { loc: "/publications/2026-11-25/recurring-report-automation-handoff/", lastmod: "2026-11-25" },
  { loc: "/publications/2026-11-25/recurring-report-automation-handoff.html", lastmod: "2026-11-25" },
  { loc: "/publications/2026-11-25/recurring-report-automation-handoff.png", lastmod: "2026-11-25" },
  { loc: "/publications/2026-11-25/recurring-report-automation-handoff.svg", lastmod: "2026-11-25" },
  { loc: "/publications/2026-11-25/recurring-report-automation-handoff.csv", lastmod: "2026-11-25" },
  { loc: "/publications/2026-11-25/recurring-report-automation-handoff-proof-boundary.json", lastmod: "2026-11-25" },
  { loc: "/publications/2026-11-25/recurring-report-automation-handoff-answer-card.json", lastmod: "2026-11-25" },
  { loc: "/about/", lastmod: "2026-11-18" },
  { loc: "/how-we-work/", lastmod: "2026-11-18" },
  { loc: "/data-handling/", lastmod: "2026-11-18" },
  { loc: "/scope-and-limits/", lastmod: "2026-11-18" },
  { loc: "/company/", lastmod: "2026-11-18" },
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
        "X-AICS-Sitemap": "middleware-21",
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
  const accept = context.request.headers.get("Accept") || "";
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
