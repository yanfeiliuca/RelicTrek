# Repository Guidelines

## Project Structure & Module Organization
RelicTrek is a static bilingual guide site. Root-level pages include `index.html`, `robots.txt`, and `sitemap.xml`. English content lives under `en/`; Chinese content lives under `zh/`. Game guide pages are grouped by title, for example `en/games/tw3/` and `zh/games/tw3/`. Blog entries live in `en/blog/` and `zh/blog/`, using date-prefixed filenames such as `2026-06-16-tw3-starry-night-painting.html`. Planning and reference notes are kept in `daily_plans/` and `workdocs/`; do not treat those as public site pages.

## Build, Test, and Development Commands
There is no package manager or compiled build step. Useful commands:

- `python3 -m http.server 8765` - serve the static site locally from the repository root.
- `python3 normalize-extensionless-urls.py` - remove `.html` from internal HTML URLs and SEO metadata.
- `python3 generate-sitemap.py` - regenerate `sitemap.xml` from indexable HTML files.
- `git status --short` - review changed files before committing.

GitHub Actions runs the URL normalizer and sitemap generator on pushes to `main` that change HTML or related scripts.

## Coding Style & Naming Conventions
Use UTF-8 HTML. Match nearby page structure, metadata, navigation, and inline CSS conventions before introducing new patterns. Keep canonical links and internal navigation extensionless, for example `/en/games/tw3/iris-steel-sword`. Name guide files with lowercase, hyphen-separated slugs. Blog posts should keep the `YYYY-MM-DD-topic.html` pattern and appear in both language trees when translated.

## Testing Guidelines
No automated unit test suite is present. For content or template changes, run the normalizer and sitemap generator, then serve locally and inspect affected pages in a browser. Verify language alternates, canonical URLs, navigation links, and mobile layout. For SEO-sensitive edits, confirm `sitemap.xml` includes the expected canonical path.

## Commit & Pull Request Guidelines
Recent commits use concise imperative summaries, such as `Fix TW3 Manticore gear facts` or `Tighten blog index route wording`. Keep commits focused on one content or maintenance task. Pull requests should describe the pages changed, note fact-checking sources or rationale, mention generated sitemap changes, and include screenshots when layout or visual presentation changes.

## Security & Configuration Tips
Do not commit secrets, analytics credentials beyond existing public IDs, or private research notes from `workdocs/`. Preserve existing Google Analytics and AdSense snippets unless the task explicitly requires changing them.
