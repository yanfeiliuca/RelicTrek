#!/usr/bin/env python3
"""Normalize RelicTrek HTML SEO signals and internal links to extensionless URLs."""

from __future__ import annotations

import codecs
import os
import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent

URL_ATTR_RE = re.compile(
    r'(?P<attr>\b(?:href|content)=["\'])'
    r'(?P<base>(?:https://relictrek\.com)?/[^"\'?#]+)'
    r'\.html'
    r'(?P<tail>[?#][^"\']*)?'
    r'(?P<quote>["\'])'
)


def should_skip(path: Path) -> bool:
    parts = set(path.relative_to(ROOT_DIR).parts)
    return ".git" in parts or "daily_plans" in parts or "workdocs" in parts


def read_text(path: Path) -> tuple[str, bool]:
    data = path.read_bytes()
    has_bom = data.startswith(codecs.BOM_UTF8)
    return data.decode("utf-8-sig"), has_bom


def write_text(path: Path, text: str, has_bom: bool) -> None:
    data = text.encode("utf-8")
    if has_bom:
        data = codecs.BOM_UTF8 + data
    path.write_bytes(data)


def normalize_html(text: str) -> str:
    return URL_ATTR_RE.sub(
        lambda match: (
            f"{match.group('attr')}{match.group('base')}"
            f"{match.group('tail') or ''}{match.group('quote')}"
        ),
        text,
    )


def main() -> int:
    changed: list[str] = []
    for dirpath, _, filenames in os.walk(ROOT_DIR):
        for filename in filenames:
            if not filename.endswith(".html"):
                continue
            path = Path(dirpath) / filename
            if should_skip(path):
                continue
            text, has_bom = read_text(path)
            normalized = normalize_html(text)
            if normalized != text:
                write_text(path, normalized, has_bom)
                changed.append(str(path.relative_to(ROOT_DIR)))

    if changed:
        print("Normalized extensionless URLs in:")
        for path in changed:
            print(f"- {path}")
    else:
        print("No extensionless URL changes needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
