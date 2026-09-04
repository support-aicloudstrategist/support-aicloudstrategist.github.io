import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEL_RE = re.compile(r'href=["\']tel:([^"\']+)["\']', re.I)


def html_files():
    for path in ROOT.rglob("*.html"):
        if ".git" not in path.parts:
            yield path


def test_tel_links_are_clickable_digits_not_masked():
    broken = []
    for path in html_files():
        source = path.read_text(encoding="utf-8", errors="ignore")
        for value in TEL_RE.findall(source):
            if "*" in value or not re.fullmatch(r"\+?[0-9][0-9\-() ]{6,}[0-9]", value):
                broken.append(f"{path.relative_to(ROOT)} -> tel:{value}")
    assert broken == []
