#!/usr/bin/env python3
"""
validate-blog-sources.py — Anti-hallucination gate for RelicTrek blog posts.

Checks every blog HTML file passed as an argument.  A file passes only when:
  1. <section class="sources-section"> is present
  2. That section contains ≥ 2 real external URLs (http/https, non-placeholder)
  3. No placeholder URLs remain (URL_1, #, example.com …)
  4. No draft [Source: URL] annotations are left in body text

Usage (from repo root):
    python3 validate-blog-sources.py en/blog/2026-06-29-game-topic.html zh/blog/...

Exit codes:
    0 — all blog files pass (or no blog files were given)
    1 — one or more blog files failed validation

Called automatically by git-push-edit.ps1 and git-push-blog.ps1 before every
commit that touches en/blog/ or zh/blog/ paths.
"""

import re
import sys
from pathlib import Path

# ------------------------------------------------------------------
# Placeholder detection
# ------------------------------------------------------------------
_PLACEHOLDER_RE = re.compile(
    r'^URL_\d+$'           # URL_1, URL_2 …
    r'|^#$'                # bare hash
    r'|^$'                 # empty
    r'|^https?://example\.'    # example.com / example.org
    r'|^https?://placeholder'  # placeholder.com
    r'|^https?://your-',   # your-site.com style
    re.IGNORECASE,
)


def _is_placeholder(url: str) -> bool:
    return bool(_PLACEHOLDER_RE.match(url.strip()))


# ------------------------------------------------------------------
# Per-file validation
# ------------------------------------------------------------------
def validate_file(path: Path) -> list[str]:
    """Return a list of error strings.  Empty list = file passes."""
    errors: list[str] = []
    content = path.read_text(encoding="utf-8", errors="replace")

    # ── 1. sources-section must exist ────────────────────────────
    has_section = (
        'class="sources-section"' in content
        or "class='sources-section'" in content
    )
    if not has_section:
        errors.append(
            'MISSING <section class="sources-section"> — '
            "no sources block found in this blog post"
        )
        return errors  # nothing more to check

    # ── 2. Parse the section ──────────────────────────────────────
    section_match = re.search(
        r'<section[^>]*class=["\']sources-section["\'][^>]*>(.*?)</section>',
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if not section_match:
        errors.append(
            "Found sources-section class but could not parse the <section> block — "
            "check for unclosed tags"
        )
        return errors

    section_html = section_match.group(1)

    # ── 3. Collect all hrefs inside the section ───────────────────
    hrefs = re.findall(
        r'<a\s[^>]*href=["\']([^"\']+)["\']',
        section_html,
        re.IGNORECASE,
    )

    placeholders = [h for h in hrefs if _is_placeholder(h)]
    real_urls    = [h for h in hrefs if h.startswith("http") and not _is_placeholder(h)]

    if placeholders:
        errors.append(
            f"Placeholder URL(s) still in sources-section: {placeholders}\n"
            "        Replace them with real source URLs before pushing."
        )

    if len(real_urls) < 2:
        errors.append(
            f"Need ≥ 2 real external URLs in sources-section, "
            f"found {len(real_urls)}: {real_urls or '(none)'}"
        )

    # ── 4. Draft annotations must not remain in body text ─────────
    # Strip the sources-section itself before searching
    body_without_sources = content.replace(section_match.group(0), "")
    draft_annotations = re.findall(
        r'\[Source:\s*https?://[^\]]{3,}\]',
        body_without_sources,
    )
    if draft_annotations:
        errors.append(
            f"{len(draft_annotations)} draft [Source: URL] annotation(s) still visible "
            "in body text — move them to the <section class=\"sources-section\"> block "
            "and remove the inline markers."
        )

    return errors


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: python3 validate-blog-sources.py <file1.html> [file2.html ...]\n"
            "Only en/blog/ and zh/blog/ paths are validated; others are skipped."
        )
        sys.exit(1)

    all_passed = True
    checked = 0

    print("\n=== RelicTrek Anti-Hallucination Source Validator ===\n")

    for arg in sys.argv[1:]:
        path = Path(arg)
        path_str = str(path).replace("\\", "/")

        # Skip non-blog files silently
        if "/blog/" not in path_str:
            continue

        if not path.exists():
            print(f"  WARN  {arg}  (file not found — skipping)")
            continue

        checked += 1
        errors = validate_file(path)

        if errors:
            print(f"  FAIL  {arg}")
            for e in errors:
                print(f"        ✗ {e}")
            print()
            all_passed = False
        else:
            print(f"  PASS  {arg}")

    print()

    if checked == 0:
        print("No blog files to validate.\n")
        sys.exit(0)

    if not all_passed:
        print("━" * 56)
        print("BLOCKED: blog file(s) failed anti-hallucination checks.")
        print()
        print("Required before any push:")
        print("  1. <section class=\"sources-section\"> with ≥ 2 real")
        print("     external URLs (http/https, not placeholders)")
        print("  2. No placeholder URLs: URL_1, #, example.com …")
        print("  3. No draft [Source: URL] markers left in body text")
        print()
        print("Fix the issues above, then re-run the push script.")
        print("━" * 56)
        sys.exit(1)
    else:
        print("All blog files passed source validation. ✓ Safe to push.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
