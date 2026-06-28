---
name: jfrog-learn-author
description: >-
  Use whenever working on the JFrog Learn site in this repo - adding or expanding
  any JFrog Artifactory or Xray topic, editing page_data.py, building or
  regenerating pages, or shipping content to GitHub Pages and the NotebookLM
  Google Docs mirror. Trigger this even when Tal just says "add a topic on X",
  "explain Y on the site", "expand the Z page", or "I want to learn about W" in
  the context of this project, even if he does not name the build steps. It
  encodes the sourcing, citation, bottom-up writing, build, and deploy workflow
  so content stays correct, Junior-readable, and NotebookLM-safe.
---

# Authoring JFrog Learn content

JFrog Learn is a static, bottom-up knowledge base teaching JFrog Artifactory
and Xray. Tal uses it to learn JFrog: every addition should make it a fuller
learning tool, written so a Junior with no prior knowledge can follow. The
site is the single source of truth; a Google Docs mirror feeds NotebookLM.

This skill is the procedure for changing content. The reasoning lives in
`AGENTS.md` (hard rules), `DECISIONS.md` (rationale), and `DESIGN.md` (UI
system). Read those when a decision is non-obvious; do not duplicate them.

## The one mental model to hold

`page_data.py` is the source. Everything else for the website and the
NotebookLM mirror is generated from it. The order is always:

```
page_data.py  ->  build_pages.py        ->  pages/*.html
              ->  build_search_index.py  ->  search-index.json
(on push to main, CI only:)  pages/*.html -> render_diagrams -> build_docx -> Drive -> Google Docs -> NotebookLM
```

CI does NOT run the page generators. Its path filter is `pages/**`,
`automation/**`, and the workflow file - it never fires on `page_data.py`
alone, and it only runs the Drive sync. So the generators MUST run locally,
and the generated `pages/*.html` and `search-index.json` get committed. If you
edit `page_data.py` and commit only that, the live site shows stale HTML and
the Drive sync may not even trigger.

## Workflow

### 1. Source before writing

Correctness beats recall; JFrog ships fast, so training data goes stale.

- Primary: official JFrog docs at `https://jfrog.com/help/`. Fetch and read the
  relevant page before drafting. Verify version-specific behavior there.
- Supplement: JFrog Community forum, Stack Overflow, official JFrog blog and
  YouTube, where they clarify or give worked examples.
- If you cannot confirm a claim from a source, say so rather than guessing.

### 2. Write it bottom-up and Junior-readable

Default treatment when Tal says "add a topic" without specifying format. Match
the structure of existing pages in `page_data.py`:

1. Concept explanation - define every term before using it; assume nothing.
2. Diagram - CSS/HTML `<figure>` only, using DESIGN.md component classes
   (`.flow`, `.diagram`, `.onion`, `.diag-node`, etc.). There are NO image
   assets on the site; never introduce one.
3. List or table to organize the moving parts (`.datatable`, `.kv-list`,
   pills, chips).
4. Step-by-step how-to (`.lab-steps`, numbered `.ls-n`) for anything actionable.
5. Recap box (`.recap`) summarizing the takeaways.

Apply product semantics from DESIGN.md: green for Artifactory, violet for
Xray, amber for hands-on labs. Use `.callout-*` and `.analogy` blocks to make
hard ideas land for a beginner.

### 3. Cite on the page

- Link key claims inline where it reads naturally (descriptive text, no raw
  URLs).
- End each topic with a "Sources / Further reading" block listing the official
  doc URLs used.

### 4. Respect the hard rules (from AGENTS.md)

- No em-dashes or en-dashes anywhere - hyphens only. This corrupts the .docx
  conversion. Run `python3 automation/convert_dashes.py` to auto-fix.
- Never hand-edit generated files: `pages/*.html`, `search-index.json`,
  `automation/_diagrams/`, `automation/_docx/`.
- Never do anything that recreates a Google Doc from scratch; the sync updates
  in place to preserve Drive file IDs that NotebookLM source links depend on.
  Do not touch the ID-tracking logic in `sync_to_drive.py`.

### 5. Adding a NEW page (extra steps beyond editing prose)

1. Append a dict to `PAGE_LIST` in `page_data.py` with `file`, `title`, `desc`,
   `h1`, `lede`, `sections`, `body`, optional `badges`; use the `chain()`
   helper for `prev`/`next`.
2. Add the filename to `NAV_ORDER` at the top of `page_data.py`.
3. Add the page to the `NAV` structure in `assets/app.js`.

### 6. Build locally, then verify

Run from the repo root after any content edit:

```bash
python3 automation/convert_dashes.py   # auto-fix any dashes that crept in
python3 build_pages.py                 # page_data.py -> pages/*.html
python3 build_search_index.py          # -> search-index.json
```

Verify no dashes leaked (should print nothing):

```bash
grep -rn $'—\|–' --include="*.html" --include="*.py" \
  --include="*.js" --include="*.json" --include="*.md" . \
  | grep -v convert_dashes.py | grep -v AGENTS.md
```

Optionally preview locally: `python3 -m http.server 8000`. Then report what
changed and let Tal review the rendered result.

### 7. Git and deploy

- Commit on local `main` (source + regenerated `pages/*.html` and
  `search-index.json` together).
- NEVER push `main`. Tal pushes. His push triggers the GitHub Pages deploy and
  the Drive/NotebookLM sync.
- After Tal pushes, an updated existing Doc keeps its ID (he refreshes the
  source in NotebookLM); a brand-new page becomes a new Doc he adds as a new
  NotebookLM source.

## The NotebookLM pipeline (for reference when asked)

All under `automation/`, orchestrated by `sync_to_drive.py` in CI:

1. `render_diagrams.py` - screenshots each page's CSS `<figure>` to a high-DPI
   PNG via headless Chromium (the site has no image files).
2. `build_docx.py` - turns each page's HTML into a native `.docx` with those
   PNGs embedded - this is what produces the Doc-compatible format.
3. `sync_to_drive.py` - uploads each `.docx` with the Google Doc mimeType so
   Google Drive performs the final conversion to a native Google Doc, updating
   in place by exact name to preserve file IDs.

## Key files

- `page_data.py` - all content; edit here to change any page (SOURCE).
- `build_pages.py` - page generator + HTML shell template.
- `build_search_index.py` - search index generator.
- `assets/app.js` - NAV structure, theme, search, tabs.
- `assets/style.css` - design system; `DESIGN.md` documents it.
- `AGENTS.md` - hard rules. `DECISIONS.md` - rationale. `automation/SETUP.md` -
  OAuth/Drive setup and preserved Doc IDs.
