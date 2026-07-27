#!/usr/bin/env python3
"""Migrate public HTML pages to the canonical premium shell without reserializing HTML."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SHELL_VERSION = "premium-shell-20260727"
DIV_OPEN = re.compile(r'<div\b[^>]*>', re.I)
CLASS_VALUE = re.compile(r'\bclass\s*=\s*["\']([^"\']*)["\']', re.I)
DIV_TOKEN = re.compile(r'<div\b[^>]*>|</div\s*>', re.I)
FOOTER_OPEN = re.compile(r'<footer\b[^>]*>', re.I)
FOOTER_CLOSE = re.compile(r'</footer\s*>', re.I)
BODY_CLOSE = re.compile(r'</body\s*>', re.I)
FOOTER_MOUNT = '<div data-aics-footer-mount></div>'
DISCLOSURE = re.compile(r'<aside\b[^>]*\bdata-aics-page-disclosure\b[^>]*>.*?</aside\s*>', re.I | re.S)

PAGE_DISCLOSURES = {
    "growth-control-os/index.html": "Safe claim: We use diagnostics, calculators, and owner dashboards to estimate value and track progress. We do not guarantee revenue outcomes or fabricate proof.",
    "healthcare-growthos/index.html": "Safe claim: AICloudStrategist does not guarantee patient bookings or medical outcomes. We improve digital trust, enquiry capture, follow-up discipline, content quality, and owner visibility.",
    "website-digital-presence/index.html": "Safe claim: AICloudStrategist does not guarantee traffic or sales. We build a clearer, more trustworthy website and connect it to lead capture so enquiries are easier to receive and follow up.",
}

FOOTER_HTML = """<footer class="aics-global-footer" data-aics-global-footer>
  <div class="aics-footer-inner">
    <div class="aics-footer-grid">
      <section class="aics-footer-brand-block">
        <a class="aics-footer-brand" href="/" aria-label="AICloudStrategist home"><span class="aics-footer-mark" aria-hidden="true">AI</span><span>AICloudStrategist</span></a>
        <p>Enterprise AI systems, controls, economics and managed operations for business-critical initiatives.</p>
        <a class="aics-footer-primary-link" href="/contact.html?service=enterprise-ai">Discuss your AI initiative<span aria-hidden="true">→</span></a>
      </section>
      <section class="aics-footer-group"><h2>Enterprise AI</h2>
        <a href="/services/ai-mlops/">Production AI Assurance</a><a href="/services/ai-automation/">AI Systems &amp; Agents</a><a href="/services/cloud-finops/">AI FinOps &amp; Economics</a><a href="/services/cloud-security/">AI Security &amp; Sovereignty</a><a href="/services/devops-observability/">Managed AI Operations</a>
      </section>
      <section class="aics-footer-group"><h2>Company</h2>
        <a href="/#why-aics">Why AICloudStrategist</a><a href="/case-studies/">Evidence</a><a href="/#engagement">How we engage</a><a href="/about/">About</a><a href="/contact.html?service=enterprise-ai">Contact</a>
      </section>
      <section class="aics-footer-group aics-footer-practices"><h2>Specialist Practices</h2>
        <a href="/contact.html?service=business-growth-systems">Business Growth Systems</a><a href="/ai-creative-studio/">AI Creative Studio</a><a href="/resources/">Enterprise AI resources</a><a href="/case-studies/">Proof policy</a>
      </section>
      <section class="aics-footer-contact"><h2>Contact</h2>
        <a href="mailto:contact@aicloudstrategist.com">contact@aicloudstrategist.com</a><a href="tel:+918065480898">+91 80654 80898</a><p>Serving enterprises, mid-market companies and scale-ups worldwide.</p>
      </section>
    </div>
    <div class="aics-footer-bottom"><span>© AICloudStrategist</span><span class="aics-footer-legal"><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a></span><span>Enterprise-grade, not enterprise-exclusive.</span></div>
  </div>
</footer>"""


def topbar_range(source: str, start: int) -> tuple[int, int]:
    depth = 0
    for token in DIV_TOKEN.finditer(source, start):
        value = token.group(0).lower()
        if value.startswith('<div') and not value.rstrip().endswith('/>'):
            depth += 1
        elif value.startswith('</div'):
            depth -= 1
            if depth == 0:
                return start, token.end()
    raise ValueError(f'unclosed topbar at offset {start}')


def topbar_openings(source: str):
    openings = []
    for opening in DIV_OPEN.finditer(source):
        class_value = CLASS_VALUE.search(opening.group(0))
        if class_value and 'topbar' in class_value.group(1).split():
            openings.append(opening)
    return openings


def version_shell_assets(source: str) -> str:
    source = re.sub(
        r'(/css/site-navigation\.css)(?:\?[^"\']*)?',
        rf'\1?v={SHELL_VERSION}',
        source,
        flags=re.I,
    )
    return re.sub(
        r'(/js/site-navigation\.js)(?:\?[^"\']*)?',
        rf'\1?v={SHELL_VERSION}',
        source,
        flags=re.I,
    )


def migrate(source: str, rel: str = "") -> tuple[str, int, int]:
    topbars = topbar_openings(source)
    for opening in reversed(topbars):
        start, end = topbar_range(source, opening.start())
        source = source[:start] + source[end:]

    footers = list(FOOTER_OPEN.finditer(source))
    if len(footers) > 1:
        raise ValueError(f'expected at most one footer, found {len(footers)}')

    if footers:
        opening = footers[0]
        closing = FOOTER_CLOSE.search(source, opening.end())
        if not closing:
            raise ValueError('unclosed footer')
        source = source[:opening.start()] + source[closing.end():]

    source = source.replace(FOOTER_MOUNT, '')
    source = DISCLOSURE.sub('', source)
    source = version_shell_assets(source)

    closing = BODY_CLOSE.search(source)
    if not closing:
        raise ValueError('missing closing body tag')

    disclosure = ""
    if rel in PAGE_DISCLOSURES:
        disclosure = (
            '<aside class="aics-page-disclosure" data-aics-page-disclosure '
            'aria-label="Service outcome notice"><p>'
            f'{PAGE_DISCLOSURES[rel]}</p></aside>'
        )
    shell = disclosure + FOOTER_HTML
    source = source[:closing.start()] + shell + source[closing.start():]

    return source, len(topbars), len(footers)


def main() -> None:
    pages = changed = removed_topbars = replaced_footers = 0
    for path in sorted(ROOT.rglob('*.html')):
        if '.git' in path.parts:
            continue
        source = path.read_text(errors='replace')
        if 'data-aics-navigation-mount' not in source:
            continue
        rel = path.relative_to(ROOT).as_posix()
        pages += 1
        migrated, topbars, footers = migrate(source, rel)
        removed_topbars += topbars
        replaced_footers += footers
        if migrated != source:
            path.write_text(migrated)
            changed += 1

    print(
        f'public_pages={pages} changed={changed} '
        f'removed_topbars={removed_topbars} replaced_footers={replaced_footers}'
    )


if __name__ == '__main__':
    main()
