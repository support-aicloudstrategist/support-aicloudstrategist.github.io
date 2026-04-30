# Deployment

## Source of Truth

This repository is the GitHub source of truth for the public AICloudStrategist website. Cloudflare Pages is connected to this repository and deploys new commits from `main`.

- Repository: `support-aicloudstrategist/support-aicloudstrategist.github.io`
- Production branch: `main`
- Cloudflare Pages project: `aicloudstrategist-site`
- Cloudflare Pages URL: `https://aicloudstrategist-site.pages.dev/`
- Custom domains: `https://aicloudstrategist.com/` and `https://www.aicloudstrategist.com/`

Any committed change pushed to `main` is deployed by Cloudflare Pages automatically.

## Current Custom Domain Status

Cloudflare Pages is connected to GitHub with repository access limited to `support-aicloudstrategist/support-aicloudstrategist.github.io`.

Cloudflare DNS was updated on April 30, 2026 to route `aicloudstrategist.com` and `www.aicloudstrategist.com` to the Cloudflare Pages project. Cloudflare handles public HTTPS for both domains.

## Required Cloudflare DNS Records

Cloudflare should keep these proxied DNS records:

```text
Type   Name  Value                           Proxy
CNAME  @     aicloudstrategist-site.pages.dev Proxied
CNAME  www   aicloudstrategist-site.pages.dev Proxied
```

Security settings enabled in Cloudflare:

- Always Use HTTPS: on
- Automatic HTTPS Rewrites: on
- Minimum TLS version: 1.2
- TLS 1.3: on
- HSTS: on for the apex hostname, without `includeSubDomains`

Do not re-add a root `CNAME` file for GitHub Pages. The custom domain belongs to Cloudflare Pages.
