# Contributor & agent rules

Rules and orientation for anyone (human or AI) working in this repository.
Read this top to bottom before making any change. For the reasoning behind the
major design choices, see [DECISIONS.md](DECISIONS.md). For the user-facing
overview, see [README.md](README.md).

---

## 1. What this project is

JFrog Learn is a static, multi-page knowledge base that teaches JFrog
Artifactory and Xray from first principles. It has two faces:

1. A website published with GitHub Pages at
   https://talorlik.github.io/jfrog-learn/ with client-side full-text search.
2. A set of native Google Docs (one per topic page, plus an index Doc) that are
   automatically mirrored from the site into a Google Drive folder so they can be
   used as NotebookLM sources.

The site is the single source of truth. The Google Docs are a generated mirror,
rebuilt from the site content by the automation pipeline. Never edit the Docs by
hand; edit the site source and let the pipeline regenerate them.

---

## 2. Hard rules (non-negotiable)

### 2.1 No em-dashes or en-dashes. Use hyphens (minus) instead.

This is a hard, non-negotiable rule. It applies to **all** content:

- The website (HTML pages, page bodies in `page_data.py`, the SHELL template in
  `build_pages.py`, `index.html`, JS in `assets/`).
- The generated Google Docs (the DOCX pipeline in `automation/`).
- File names.
- Documentation (`README.md`, `DECISIONS.md`, `automation/SETUP.md`, etc.).

Specifically, never use any of these:

| Forbidden                          | Use instead |
| ---------------------------------- | ----------- |
| em-dash (U+2014)                   | `-` hyphen  |
| en-dash (U+2013)                   | `-` hyphen  |
| `&mdash;` / `&ndash;` HTML entity  | `-` hyphen  |
| `\u2014` / `\u2013` escape         | `-` hyphen  |

Spacing: a spaced em-dash becomes a spaced hyphen (` - `); an unspaced dash in a
numeric range (`1-10`) becomes a plain hyphen with no spaces.

A one-shot converter that enforces this lives at `automation/convert_dashes.py`.
Run it from the repo root if dashes ever creep back in. It rewrites the literal
characters, the HTML entities, AND the Python/JSON unicode-escape forms (the
content in `page_data.py` is stored with `\u2014`-style escapes, so the escape
handling matters):

```
python3 automation/convert_dashes.py
python3 build_pages.py            # regenerate pages/*.html from page_data.py
python3 build_search_index.py     # regenerate search-index.json
```

Verify with:

```
grep -rn "<EM>\|<EN>" --include="*.html" --include="*.py" --include="*.js" \
  --include="*.json" --include="*.md" . | grep -v convert_dashes.py | grep -v AGENTS.md
```

(Replace `<EM>` / `<EN>` with the literal em-dash and en-dash characters. The
command should print nothing. `convert_dashes.py` documents the characters on
purpose, and this file shows them in the forbidden table, so both are excluded.)

### 2.2 Preserve Google Doc file IDs.

Each generated Google Doc keeps a stable Drive file ID. NotebookLM source links
point at those IDs, and the user refreshes NotebookLM sources manually (there is
no NotebookLM API). If a Doc ID changes, the user's NotebookLM source breaks.
Therefore the sync ALWAYS updates an existing Doc in place (same file id) rather
than deleting and recreating it. Never do anything that recreates a Doc from
scratch when one already exists. The current preserved IDs are listed in
`automation/SETUP.md` and were reconciled once already (see DECISIONS.md).

---

## 3. Repository layout

```
index.html              # home / landing page with the topic grid
pages/*.html            # one page per topic - GENERATED, do not hand-edit
assets/style.css        # design system (light/dark, responsive)
assets/app.js           # sidebar, theme toggle, mobile nav, tabs, scrollspy, search
search-index.json       # GENERATED static full-text index for in-browser search
build_pages.py          # generator: SHELL template + page_data.py -> pages/*.html
page_data.py            # content bodies + nav order for each topic page (SOURCE)
build_search_index.py   # parses index.html + pages/*.html -> search-index.json
AGENTS.md               # this file
DECISIONS.md            # key design decisions and their rationale
README.md               # user-facing overview
LICENSE                 # MIT

automation/             # the Google Docs sync pipeline
  sync_to_drive.py      # entrypoint: orchestrates render -> docx -> upload/convert
  render_diagrams.py    # renders each page's CSS/HTML <figure> to a PNG (Playwright)
  build_docx.py         # converts a page's HTML into a high-fidelity .docx
  html_to_markdown.py   # legacy/aux HTML parsing helpers
  convert_dashes.py     # one-shot em/en-dash -> hyphen converter
  get_oauth_token.py    # one-time helper to mint the OAuth refresh token
  requirements.txt      # python deps for the pipeline
  SETUP.md              # one-time setup: OAuth, secrets, preserved Doc IDs
  _diagrams/  _docx/    # generated artifacts (gitignored)

.github/workflows/sync-to-drive.yml   # CI that runs the sync on push to main
```

Generated files you must never hand-edit: `pages/*.html`, `search-index.json`,
everything under `automation/_diagrams/` and `automation/_docx/`.

---

## 4. The website build

`pages/*.html` are generated from `page_data.py` (the content) plus the SHELL
template in `build_pages.py`. To change a page, edit `page_data.py`, then:

```bash
python3 build_pages.py          # rebuild pages/*.html from page_data.py
python3 build_search_index.py   # rebuild search-index.json
```

Search runs entirely in the browser: a static JSON index fetched and ranked
client-side, so it works on GitHub Pages with no backend.

Diagrams on the site are pure CSS/HTML `<figure>` elements (classes include
`diag-grid`, `flow-row`, `bm-box`, `onion`). The site contains ZERO image files;
every diagram is drawn with markup and CSS. This matters for the Docs pipeline
(section 5), which has to rasterize those figures.

### Run the site locally

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

### Adding a new topic

1. Append a page dict to `PAGE_LIST` in `page_data.py` (and add it to
   `NAV_ORDER`).
2. Add the link to the `NAV` model in `assets/app.js` and a label in
   `build_search_index.py`.
3. Run `build_pages.py` then `build_search_index.py`.
4. The Docs sync picks the new page up automatically on the next push to main
   (it creates a new Doc and adds it to the index Doc). The `search` page is
   excluded from the sync.
5. Commit and push.

---

## 5. The Google Docs sync pipeline (`automation/`)

Purpose: mirror every content page into the `jfrog-learning` Google Drive folder
as a native Google Doc, one Doc per page plus an auto-rebuilt index Doc, so they
can be added as NotebookLM sources.

Pipeline (entrypoint `automation/sync_to_drive.py`):

1. `render_diagrams.py` renders each page's CSS/HTML `<figure>` to a high-DPI PNG
   using headless Chromium via Playwright (DEVICE_SCALE=2). `main_async(slugs)`
   returns a manifest dict; `main()` also writes
   `automation/_diagrams/manifest.json`. It respects the
   `PLAYWRIGHT_CHROMIUM_PATH` env var for the browser executable.
2. `build_docx.py` converts each page's HTML into a `.docx` with those PNGs
   embedded and native Word structure (headings, lists, tables, code blocks,
   inline code, callouts, links). Public functions: `page_title(html)`,
   `build_page_docx(html, diagrams, out_path, title, source_url)`, and
   `_add_hyperlink(para, url, text)`.
3. `sync_to_drive.py` uploads each `.docx` to Drive with the Google Doc
   mimeType, so Drive CONVERTS it to a native Google Doc. It looks up each Doc by
   exact name and updates it IN PLACE (same file id) if it exists, or creates it
   if not. It also reconciles any legacy doc names (see DECISIONS.md) and
   rebuilds the index Doc.

Auth and scope: OAuth user credentials with the non-sensitive
`https://www.googleapis.com/auth/drive.file` scope. The app acts as the user
(Docs count against the user's own Drive quota) and can only see/manage files it
created, so it manages its own `jfrog-learning` folder. Credentials come from a
single env var / GitHub secret `GOOGLE_OAUTH_CREDENTIALS` (JSON with client_id,
client_secret, refresh_token). The Google Docs API and the `documents` scope are
NOT used; images are embedded in the `.docx` before upload. Full one-time setup
is in `automation/SETUP.md`.

### Run the sync locally (dry run)

```bash
cd automation
PLAYWRIGHT_CHROMIUM_PATH=/home/user/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome \
  python3 sync_to_drive.py --dry-run
```

In this sandbox, Playwright's auto-install fails, so the Chromium path must be
passed explicitly. In CI (ubuntu-latest) Chromium installs cleanly via
`python -m playwright install --with-deps chromium`.

LibreOffice can be used for visual QA of a built `.docx`:
`soffice --headless --convert-to pdf <file>.docx`.

---

## 6. Document styling (colors)

These apply only to the generated Google Docs, not the website or the diagram
images. Do not change colors inside images, diagrams, or code blocks unless the
user asks.

- Code BLOCKS (fenced/multi-line): dark theme matching the site. Background
  `#0A0D0B`, text green `#9FE6AD`, border `#24302A`. Rendered as a single-cell
  table for a solid background.
- INLINE code (single backticks): dark slate text `#242A33` on a light gray chip
  `#EDEDF2`. This replaced an earlier faint green that was hard to read on light
  backgrounds.
- Links: `#1A57B7`.
- Callout backgrounds: tip `#EAF6EC`, warn `#FCEFE3`, note `#EAF0FA`,
  question `#F1ECF8`, analogy/amber box `#FFF6E6`.
- Table header fill: `#E8E8EC`.

Relevant helpers in `build_docx.py`: `_run_shade()`, and `_set_cell_border()`
which honors a `color=` kwarg.

---

## 7. CI workflow

`.github/workflows/sync-to-drive.yml` runs the sync on every push to `main` that
touches `pages/**`, `automation/**`, or the workflow file itself, and can also be
run manually (`workflow_dispatch`). It checks out the repo, sets up Python 3.12,
installs `automation/requirements.txt`, installs Chromium for Playwright, then
runs `python sync_to_drive.py` from the `automation/` directory. A
`concurrency` group prevents overlapping runs from racing on the same Docs.

Note the path filters: a commit that changes ONLY documentation
(`README.md`, `AGENTS.md`, `DECISIONS.md`, `LICENSE`) does NOT trigger the sync,
which is correct - doc-only changes do not affect the Docs mirror. To force a
run, use the Actions tab (`workflow_dispatch`) or touch a file under `pages/**`
or `automation/**`.

---

## 8. Git conventions

- Commit identity:
  `git -c user.name="Tal Orlik" -c user.email="talorlik@gmail.com" commit ...`
- Push to main: `git push origin main`. In this environment the push needs
  GitHub credentials supplied via the tool's `api_credentials=["github"]`; a
  plain push fails with "could not read Username".
- The `gh` CLI is available (also with `api_credentials=["github"]`) for
  inspecting workflow runs: `gh run list`, `gh run view`, `gh run watch`.
- Before pushing site/content changes, run `build_pages.py` and
  `build_search_index.py` so the generated files in the commit are current, and
  run the no-dash verify grep from section 2.1.
