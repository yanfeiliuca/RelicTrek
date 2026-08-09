# Repository Guidelines

Guidance for AI coding agents working in this repository. The reader is assumed to know nothing about the project.

## Project Overview

RelicTrek (`relictrek.com`) is a bilingual (English/Chinese) **pure static HTML** website of SEO-optimized game guides. Each page targets a long-tail keyword around hidden items, weapons, quest routes, and missable content. The site is monetized with Google AdSense (`ca-pub-1971262808837870`) and tracked with Google Analytics (`G-5VH076R049`).

- **Repo:** `github.com/yanfeiliuca/RelicTrek`, branch `main`.
- **No build step, no framework, no package manager.** There is no `package.json`, `pyproject.toml`, or similar manifest. Every page is a self-contained `.html` file with inline CSS and JS. The only external dependencies are Google Fonts, Google Analytics, and Google AdSense.
- The Python scripts at the repo root use only the standard library (Python 3).

## Project Structure & Module Organization

```
index.html                      # Root redirect shim: meta-refresh + JS language
                                #   detection (zh -> /zh/, otherwise /en/)
en/  zh/                        # English and Chinese content trees (mirrored)
  index.html                    # Language homepage
  about.html contact.html privacy.html terms.html
  games/index.html              # Hub listing all game sections
  games/{game}/index.html       # Per-game hub page
  games/{game}/{slug}.html      # Individual guide pages
  blog/index.html               # Blog listing page
  blog/index.json               # Blog metadata consumed by the listing page
  blog/YYYY-MM-DD-{game}-{topic}.html   # Dated blog articles
```

Game slugs currently in use: `bg3`, `bmw` (Black Myth: Wukong), `coe33` (Clair Obscur: Expedition 33), `er` (Elden Ring), `lop` (Lies of P), `mhwilds` (Monster Hunter Wilds), `tw3` (The Witcher 3), `windrose` (Early Access).

Root-level tooling:

- `generate-sitemap.py` — rebuilds `sitemap.xml` by scanning all indexable HTML files.
- `normalize-extensionless-urls.py` — strips `.html` from internal `href`/`content` URLs.
- `validate-blog-sources.py` — anti-hallucination gate for blog posts (see below).
- `git-push-blog.ps1`, `git-push-edit.ps1` — PowerShell publish helpers (Windows-oriented; `git-push-edit.ps1` is dry-run by default). Both run the blog validator before committing.
- `robots.txt` — allows search indexing, disallows AI-training crawlers (GPTBot, ClaudeBot, CCBot, etc.).
- `.autoblog-tracker.json` — list of already-generated auto-blog topics; do not hand-edit casually.

Local-only, **gitignored** directories (never commit or push them): `workdocs/` (planning, `Reference.md` source log, `seo/` keyword matrix), `daily_plans/`, `PROGRESS.md`, `CLAUDE.md`, `.learnings/`. The empty `RelicTrek.com/` directory is a leftover placeholder — ignore it.

## Build, Test, and Development Commands

```bash
# Serve the site locally from the repo root
python3 -m http.server 8765

# Regenerate sitemap.xml (after adding/removing pages)
python3 generate-sitemap.py

# Bulk-normalize internal links to extensionless URLs
python3 normalize-extensionless-urls.py

# Validate blog posts before any commit touching en/blog/ or zh/blog/
python3 validate-blog-sources.py en/blog/<file>.html zh/blog/<file>.html

# Pre-commit checks
git status --short
git diff --check
```

### CI / automation

`.github/workflows/auto-sitemap.yml` runs on every push to `main` that changes `**.html` or either Python script: it runs the normalizer, regenerates `sitemap.xml`, commits the result as `[sitemap] Auto-update sitemap.xml` (skipping if the last commit was by itself), and pings Google and Bing. Because of this, **do not hand-edit `sitemap.xml`** — it will be overwritten.

Deployment is a plain static file host behind `https://relictrek.com`; no deployment configuration lives in this repo. Publishing = push to `main`.

## Critical Content Rules

### Extensionless URLs — mandatory everywhere

Every URL in SEO signals and internal links must omit `.html`:

- Correct: `https://relictrek.com/en/games/tw3/aerondight`
- Incorrect: `https://relictrek.com/en/games/tw3/aerondight.html`

This applies to `canonical` href, `hreflang` hrefs, `og:url`, internal `<a href>`, and sitemap `<loc>` (the generator already emits extensionless URLs). Use `normalize-extensionless-urls.py` for bulk fixes.

### Bilingual page parity

Every guide and blog page must exist in both `en/` and `zh/` trees with the **same filename**. Each page must include:

- `<link rel="canonical">` pointing to its own extensionless URL
- `<link rel="alternate" hreflang="en">` and `hreflang="zh">` cross-references
- `<link rel="alternate" hreflang="x-default">` pointing to the EN version
- `<meta property="og:url">` matching the canonical
- A language switcher in the nav linking the two versions

### Never push local planning docs

`workdocs/`, `daily_plans/`, `PROGRESS.md`, and `.learnings/` are gitignored and must stay that way. When committing, stage only the exact site files involved — do not blindly `git add .` on a dirty tree.

### Reference.md before factual edits

Before editing any guide page for factual accuracy, append an entry to `workdocs/Reference.md` recording which pages were edited, what claims changed, and the source URLs used to verify each claim (Fandom, Fextralife, PowerPyx, official patch notes, etc.). Mark uncertain facts as `待确认`. This file is append-only.

## Coding Style & Naming Conventions

- UTF-8 HTML throughout; match the existing page structure, metadata, navigation, and inline CSS conventions before introducing new patterns.
- Guide filenames: lowercase, hyphen-separated slugs (e.g. `iris-steel-sword.html`). Blog filenames: `YYYY-MM-DD-{game}-{topic}.html`.
- Each page is self-contained: all CSS lives in an inline `<style>` block using the shared design tokens (dark theme `--bg-void: #060708`, gold accents `--gold: #f5b945`; fonts Cinzel for headings, Rajdhani for UI, Inter for body). GA and AdSense snippets appear in every page's `<head>` — preserve them.
- Guide pages follow a 9-section intent-first layout: quick answer, requirements, location/route, step-by-step acquisition, missable warnings, rewards/stats (tables), common mistakes, related guides (internal links), FAQ (with JSON-LD FAQ schema).
- When adding or removing pages, also update the relevant hub/index pages and `en/blog/index.json` + `zh/blog/index.json` for blog posts.

## Blog Content Anti-Hallucination Rules

Every blog post must satisfy all of the following **before** the HTML file is written:

1. **Search first.** Execute at least three web searches covering: (a) official wiki / Fandom, (b) Reddit or forum player reports, (c) press coverage (IGN, Fextralife, GameFAQs). No body content may be written before these searches complete.
2. **Source every claim.** Each factual paragraph in the draft carries an inline `[Source: URL]` annotation. Claims with no traceable source are removed or marked `待确认`.
3. **Embed a visible sources section.** The finished HTML must contain `<section class="sources-section">` immediately before `<footer>`, listing every URL used as real links. An HTML comment is not a substitute.
4. **Banned sources.** Never use AI training memory, logical inference, or RelicTrek's own existing pages as evidence for new claims. Only URLs retrieved during the current writing session count.
5. **Early Access caveat.** For Early Access games (e.g., Windrose), numerical values and route details must be marked `待确认` unless confirmed by a source dated after the most recent patch.
6. **Validator must pass.** Run `python3 validate-blog-sources.py <en-file> <zh-file>` before committing. It checks: `<section class="sources-section">` present; ≥ 2 real external URLs inside it (no `URL_1`, `#`, or `example.com` placeholders); no draft `[Source: URL]` markers left in body text. Exit 0 = safe; exit 1 = blocked. It is also wired into `git-push-edit.ps1` and `git-push-blog.ps1` and will block those scripts automatically.

## Testing Guidelines

There is no automated unit test suite. For content or template changes:

1. Run the normalizer and sitemap generator if URLs or pages changed.
2. Serve locally (`python3 -m http.server 8765`) and inspect affected pages in a browser, including mobile layout (the project QA convention is a real 390 × 844 viewport check).
3. Verify language alternates, canonical URLs, breadcrumb/nav links, and the EN/ZH language switcher.
4. For SEO-sensitive edits, confirm `sitemap.xml` includes the expected canonical path.
5. `git diff --check` before committing.

## Commit & Pull Request Guidelines

- Commit messages are concise imperative summaries, e.g. `Fix TW3 Manticore gear facts`, `Improve TW3 potion CTR metadata`. Auto-generated commits look like `auto-blog: 2026-08-06 [mhwilds] death-stench-armor` or `[sitemap] Auto-update sitemap.xml`.
- Keep commits focused on one content or maintenance task.
- PRs should describe the pages changed, note fact-checking sources or rationale, mention generated sitemap changes, and include screenshots when layout changes.

## Security Considerations

- Do not commit secrets, analytics credentials beyond the existing public IDs, or private research notes from `workdocs/`.
- Preserve the existing Google Analytics and AdSense snippets unless the task explicitly requires changing them.
- `robots.txt` deliberately blocks AI-training crawlers while allowing search indexing — keep that distinction intact.
