#!/usr/bin/env python3
"""Migrate public HTML pages to the canonical premium shell without reserializing HTML."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DIV_OPEN = re.compile(r'<div\b[^>]*>', re.I)
CLASS_VALUE = re.compile(r'\bclass\s*=\s*["\']([^"\']*)["\']', re.I)
DIV_TOKEN = re.compile(r'<div\b[^>]*>|</div\s*>', re.I)
FOOTER_OPEN = re.compile(r'<footer\b[^>]*>', re.I)
FOOTER_CLOSE = re.compile(r'</footer\s*>', re.I)
BODY_CLOSE = re.compile(r'</body\s*>', re.I)
FOOTER_MOUNT = '<div data-aics-footer-mount></div>'


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


def migrate(source: str) -> tuple[str, int, int]:
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

    # The canonical footer must be a direct body child, never nested in page-specific wrappers.
    source = source.replace(FOOTER_MOUNT, '')
    closing = BODY_CLOSE.search(source)
    if not closing:
        raise ValueError('missing closing body tag')
    source = source[:closing.start()] + FOOTER_MOUNT + source[closing.start():]

    return source, len(topbars), len(footers)


def main() -> None:
    pages = changed = removed_topbars = replaced_footers = 0
    for path in sorted(ROOT.rglob('*.html')):
        if '.git' in path.parts:
            continue
        source = path.read_text(errors='replace')
        if 'data-aics-navigation-mount' not in source:
            continue
        pages += 1
        migrated, topbars, footers = migrate(source)
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
