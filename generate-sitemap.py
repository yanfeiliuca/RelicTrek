#!/usr/bin/env python3
"""Generate sitemap.xml for RelicTrek static site.
Scans all .html files, writes sitemap.xml to the repo root.
Run: python generate-sitemap.py
"""

import os
import re
from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, ElementTree

BASE_URL = "https://relictrek.com"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Priority by page type (higher = more important for SEO)
PRIORITY_MAP = {
    "home": "1.0",
    "game_hub": "0.9",
    "guide": "0.8",
    "game_index": "0.7",
    "info": "0.5",
    "default": "0.6",
}

CHANGEFREQ_MAP = {
    "home": "weekly",
    "game_hub": "weekly",
    "guide": "monthly",
    "game_index": "monthly",
    "info": "yearly",
    "default": "monthly",
}


def classify(path: str) -> str:
    """Classify a page by its path for priority and changefreq."""
    # /en/ or /zh/ homepages
    if re.match(r"^(en|zh)/index\.html$", path):
        return "home"
    # Game hub pages (e.g. /en/games/windrose/index.html)
    if "/games/" in path and path.endswith("/index.html"):
        parts = path.split("/")
        # /en/games/index.html -> game_index (list of games)
        # /en/games/windrose/index.html -> game_hub (specific game)
        if len([p for p in parts if p and p != "index.html"]) >= 3:
            return "game_hub"
        return "game_index"
    # Game detail pages are guide pages even when they are not under /guides/.
    if "/games/" in path:
        return "guide"
    # Info pages (about, privacy, terms, contact)
    if any(p in path for p in ["about", "privacy", "terms", "contact"]):
        return "info"
    # Blog pages
    if "/blog/" in path:
        return "game_index"
    return "default"


def is_redirect_like(full_path: str) -> bool:
    """Return True for HTML shim pages that only redirect elsewhere."""
    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read(4096).lower()
    return (
        "<title>moved permanently</title>" in html
        or "http-equiv=\"refresh\"" in html
        or "window.location.replace" in html
    )


def find_html_files(root: str) -> list:
    """Recursively find indexable .html files, return relative paths."""
    html_files = []
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith(".html"):
                full = os.path.join(dirpath, f)
                rel = os.path.relpath(full, root).replace("\\", "/")
                # Skip files in .git or scripts directories. Keep root index handled separately.
                if rel.startswith(".") or "scripts/" in rel:
                    continue
                if rel != "index.html" and is_redirect_like(full):
                    continue
                html_files.append(rel)
    return sorted(html_files)


def canonical_path(path: str) -> str:
    """Convert a local HTML path into the public canonical URL path."""
    if path == "index.html":
        return "/"
    if path.endswith("/index.html"):
        return "/" + path[: -len("index.html")]
    if path.endswith(".html"):
        return "/" + path[: -len(".html")]
    return "/" + path


def build_sitemap(files: list) -> Element:
    """Build XML sitemap element tree."""
    urlset = Element("urlset", {
        "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
    })

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for path in files:
        page_type = classify(path)
        priority = PRIORITY_MAP.get(page_type, PRIORITY_MAP["default"])
        changefreq = CHANGEFREQ_MAP.get(page_type, CHANGEFREQ_MAP["default"])

        url_el = SubElement(urlset, "url")
        loc = SubElement(url_el, "loc")
        loc.text = f"{BASE_URL}{canonical_path(path)}"

        lastmod = SubElement(url_el, "lastmod")
        lastmod.text = today

        cf = SubElement(url_el, "changefreq")
        cf.text = changefreq

        pr = SubElement(url_el, "priority")
        pr.text = priority

    return urlset


def main():
    files = find_html_files(ROOT_DIR)
    print(f"Found {len(files)} HTML files")

    # Separate root index (redirect page) — handle specially
    root_idx = "index.html"
    regular_files = [f for f in files if f != root_idx]

    # Root redirect page
    urlset = build_sitemap(regular_files)

    # Add root as special entry
    url_el = SubElement(urlset, "url")
    SubElement(url_el, "loc").text = f"{BASE_URL}/"
    SubElement(url_el, "lastmod").text = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    SubElement(url_el, "changefreq").text = "weekly"
    SubElement(url_el, "priority").text = "1.0"

    # Write
    output_path = os.path.join(ROOT_DIR, "sitemap.xml")
    tree = ElementTree(urlset)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Wrote sitemap.xml ({len(regular_files) + 1} URLs)")


if __name__ == "__main__":
    main()
