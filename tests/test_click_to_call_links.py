import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEL_RE = re.compile(r'href=["\']tel:([^"\']+)["\']', re.I)


def public_contact_files():
    skip = {".git", ".pytest_cache", "__pycache__", ".venv", "node_modules", "tests"}
    extensionless_pages = {"guarantee", "payments", "terms", "privacy", "local", "advisory", "policykart"}
    for path in ROOT.rglob("*"):
        if path.is_dir() or set(path.relative_to(ROOT).parts) & skip:
            continue
        if path.suffix.lower() not in {".html", ".js"} and path.name not in extensionless_pages:
            continue
        yield path


def test_tel_links_are_clickable_digits_not_masked():
    broken = []
    for path in public_contact_files():
        source = path.read_text(encoding="utf-8", errors="ignore")
        for value in TEL_RE.findall(source):
            if "*" in value or not re.fullmatch(r"\+?[0-9][0-9\-() ]{6,}[0-9]", value):
                broken.append(f"{path.relative_to(ROOT)} -> tel:{value}")
    assert broken == []


def test_shared_navigation_has_a_click_to_call_route_for_visible_number():
    nav = (ROOT / "js" / "site-navigation.js").read_text(encoding="utf-8")
    assert "+91 80654 80898" in nav
    assert any(value == "+918065480898" for value in TEL_RE.findall(nav))
