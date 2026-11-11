# Cost-keyword SEO plan (non-branded)

Updated: 2026-11-11  
Inventory: `seo/cost-keyword-inventory.csv` (121+ mapped queries)  
Goal: rank for problem/solution queries (not company-name searches) on Google, Bing, and AI assistants.

## Priority tiers

| Tier | Intent | Examples | Primary targets |
|---|---|---|---|
| P0 | Transactional / high volume | cloud cost optimization, reduce cloud spend, FinOps consulting, reduce AWS bill, Kubernetes cost management, GPU cost optimization | Hub pages + homepage |
| P1 | Problem / mid volume | bill shock, overspending, anomaly, budget overrun, rightsizing, Savings Plans/RI, showback | Hubs + FAQ schema |
| P2 | Long-tail / niche | serverless cost, unattached EBS, showback vs chargeback, Hindi variants | Alias redirects → hubs / Hindi page |

## Keyword → page map (clusters)

| Cluster | Target URL | Alias redirects (examples) |
|---|---|---|
| Optimization / multi-cloud / TCO / ROI / rightsizing / serverless / migration cost | `/cloud-cost-optimization/` | `/cloud-rightsizing`, `/cloud-tco`, `/multi-cloud-cost-management`, `/serverless-cost-optimization` |
| Reduce / cut / waste / bill shock / overspend | `/reduce-cloud-spend/` | `/cloud-waste-reduction`, `/cloud-bill-shock`, `/cloud-overspending` |
| FinOps / financial management / showback / chargeback / best practices | `/finops-consulting/` | `/finops`, `/cloud-financial-management`, `/cloud-showback`, `/cloud-chargeback` |
| AWS bill / SP / RI / EC2 | `/aws-cost-optimization/` | `/reduce-aws-bill` |
| Azure spend | `/azure-cost-optimization/` | `/cut-azure-spend` |
| GCP / CUD | `/gcp-cost-optimization/` | `/gcp-cost-savings` |
| Kubernetes / container / EKS AKS GKE | `/kubernetes-cost-optimization/` | `/container-cost-optimization` |
| GPU / AI infra / LLM / inference | `/gpu-ai-cost-optimization/` | `/ai-infrastructure-cost`, `/llm-cost-optimization` |
| Audit / spend analysis / monitoring / anomaly / calculator intent | `/cloud-cost-audit/` | `/cloud-spend-analysis`, `/cloud-anomaly-detection`, `/cloud-cost-monitoring` |
| Governance / tagging / allocation / ownership | `/cloud-cost-governance/` | `/cloud-tagging-strategy`, `/cloud-cost-allocation` |
| Hindi queries | `/hi/cloud-cost-optimization/` | — |
| Service mechanics | `/cloud-ai-cost-governance-diagnostic/` | — |
| Fees | `/pricing/` | — |
| Conversion | `/request-fit-review/` | — |

## Why hubs + aliases (not 100 thin pages)

Creating one URL per synonym triggers doorway-page risk and dilutes crawl budget. Each hub is substantive (problem → method → FAQ → CTA) and aliases 301 to the hub. Full synonym coverage lives in the CSV + FAQ copy + `llms.txt` for AI citation.

## On-page rules

1. Titles/H1s lead with the problem keyword; brand is secondary or omitted.
2. Every hub has FAQPage + Service JSON-LD.
3. Internal links use keyword anchors between hubs, diagnostic, pricing, Decision Pack.
4. India fee band stays independent (INR); international USD—never invent savings %.
5. `functions/_middleware.ts` `indexableExact` must list every new indexable path or Cloudflare returns 404.

## Measurement (manual)

1. Google Search Console + Bing Webmaster: submit `sitemap.xml`.
2. Track impressions for P0 queries weekly.
3. Ask ChatGPT/Claude/Gemini cost questions and check citation of hub URLs after crawl.
