# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

JFrog Learn is a static multi-page educational site (no backend, no JS framework) teaching
Artifactory and Xray. Content lives in a Python data file; Python scripts generate static HTML.
Vanilla JS handles all interactivity. A separate Python/Playwright pipeline syncs pages to
Google Drive as native Google Docs (for NotebookLM).

## Build Commands

```bash
python3 build_pages.py           # Regenerate pages/*.html from page_data.py
python3 build_search_index.py    # Regenerate search-index.json from all .html files
python3 -m http.server 8000      # Local dev server at http://localhost:8000

python3 automation/convert_dashes.py   # Auto-fix em/en-dashes -> hyphens in page_data.py
```

There is no npm, no TypeScript compilation, and no test suite. Generated files (`pages/*.html`,
`search-index.json`) are committed to git - they are not gitignored.

## Architecture

**Content pipeline:** `page_data.py` is the single source of truth. It contains a `PAGE_LIST`
of Python dicts, each with `file`, `title`, `body` (raw HTML string), `sections` (sidebar
anchors), and nav chain pointers. `build_pages.py` reads this and stamps each dict into an
HTML shell template. `build_search_index.py` parses the generated HTML files to build the
flat-array `search-index.json`.

**Frontend (`assets/app.js`):** A single vanilla JS file that handles sidebar injection from
an in-file `NAV` data structure, theme toggle (CSS `data-theme` attribute + localStorage),
off-canvas mobile nav, command-palette search modal (reads `search-index.json` via fetch),
tab switching, scrollspy, and related-topics cards.

**Design system (`assets/style.css`):** CSS variables for all tokens; `data-theme` drives
light/dark mode. All diagrams are pure CSS/HTML `<figure>` elements - there are no image
files. Component classes (`.flow`, `.diag-grid`, `.onion`, `.callout-*`, etc.) are documented
in `DESIGN.md`.

**Automation pipeline (`automation/`):** On every push to `main`, GitHub Actions runs
`sync_to_drive.py`. It uses Playwright (headless Chromium) to screenshot each CSS diagram to
PNG, then `build_docx.py` assembles a `.docx` per page with embedded PNGs, then uploads to
Google Drive with the DOCX-to-Docs conversion API. Existing Docs are updated in place by
stable file ID (preserving NotebookLM source links). OAuth credentials live in the
`GOOGLE_OAUTH_CREDENTIALS` repo secret.

## Adding a New Page

1. Append a dict to `PAGE_LIST` in `page_data.py` with `file`, `title`, `desc`, `h1`,
   `lede`, `sections`, `body`, and optionally `badges`. Use the `chain()` helper for
   `prev`/`next` links.
2. Add the filename to `NAV_ORDER` at the top of `page_data.py`.
3. Add the page to the `NAV` data structure in `assets/app.js`.
4. Run both generators (`build_pages.py`, `build_search_index.py`).

## Hard Rules (from AGENTS.md)

**No em-dashes or en-dashes.** Use hyphens (`-`) only. Em/en-dashes corrupt the `.docx`
conversion. Run `python3 automation/convert_dashes.py` to auto-fix before committing.

**Preserve Google Doc file IDs.** The sync always updates an existing Doc in place rather
than deleting and recreating it. NotebookLM source links are bound to those Drive file IDs.
Do not delete Docs manually or change the ID-tracking logic in `sync_to_drive.py`.

## Key Files

- `page_data.py` - all content; edit here to change any page
- `build_pages.py` - page generator; contains the HTML shell template
- `assets/app.js` - all frontend logic including the `NAV` data structure
- `assets/style.css` - full design system
- `DESIGN.md` - component/class catalog and responsive breakpoints; read before touching UI
- `DECISIONS.md` - rationale for architectural choices; read before proposing changes
- `AGENTS.md` - operational rules for contributors and AI agents
- `automation/SETUP.md` - one-time OAuth setup for the Drive sync
