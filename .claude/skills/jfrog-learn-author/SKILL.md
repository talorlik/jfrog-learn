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

## Decisions I make without asking

Tal does not want to re-answer settled questions. Decide these yourself from the
defaults below and state the decision in your response; only ask when the
situation is genuinely ambiguous or the choice is hard to reverse.

- **Scope.** Default to ONE new page for a new topic. If the audit (step 0)
  shows an existing page already owns the topic, extend that page and
  cross-link instead of duplicating. Only ask about scope when the topic is
  large enough to plausibly be a multi-page track AND the audit does not settle
  it.
- **Format.** Always the full bottom-up treatment in step 2. Do not ask.
- **Nav placement.** Recommend it yourself and state why. Put a page in the
  sidebar group that matches its theme (security -> "Automation & security",
  etc.) and order it bottom-up (teach the model before the pages that reference
  it). Insert into `NAV_ORDER`, `assets/app.js` NAV, `GROUPS`, and `RELATED`
  consistently. Only ask if two placements are equally defensible and the
  choice materially changes the learning flow.
- **Sourcing depth.** Always fetch official docs first (step 1). Do not ask
  whether to cite - always cite inline plus a Sources block.
- **Cross-links.** When a new page overlaps an existing one, add minimal
  forward-links from the existing page to the new canonical page. Do not restate
  content. No need to ask.

Things that DO warrant a question: a large delicate change that could lose
existing bespoke work (e.g. migrating a hand-authored page), a request that
contradicts an existing page, or anything you cannot confirm from a source.

## Workflow

### 0. Audit existing content FIRST (anti-duplication)

Before sourcing or writing, find out what the site already teaches. The pages
overlap: Xray basics, scanning, the Policy-vs-Watch concept, CVEs, secrets, and
build gating are already scattered across `fundamentals.html`, `frogbot.html`,
and `build-promotion.html`. Duplicating them is the most common failure mode.

- Scan `page_data.py` for the topic's key terms to see which pages mention it
  and how heavily. Use `ctx_execute_file` so the file bytes stay out of context:
  count term hits per page, then read only the relevant sections.
- `fundamentals.html` is the big one: it already has sections for what Xray is
  (`#xray`), how scanning works (`#xray-how`), and a Policies & Watches primer
  (`#policies`), plus reusable diagram components - the Xray onion, severity
  chips (`.sev sev-crit` ... `sev-unknown`), `.analogy`/`.analogy-x`, and the
  `.bigmodel` mental-model diagram. Reference these and link to them; do not
  rebuild them.
- Decide per the audit: new page for a genuine gap, or extend an existing page.
  A new page should recap shared concepts in one line with a link, then go deep
  on what is actually missing.

### 1. Source before writing

Correctness beats recall; JFrog ships fast, so training data goes stale.

- Primary: official JFrog docs. Verify version-specific behavior there before
  drafting.
- Fetch mechanics that work: the `jfrog.com/help/...` help-center URLs are
  JS-rendered SPAs that redirect and defeat a plain fetch. Use the
  `docs.jfrog.com/...` mirrors, which render to static HTML, and fetch them with
  `ctx_fetch_and_index` (handles redirects, keeps raw bytes out of context),
  then `ctx_search` the indexed sources for the exact mechanics. `WebSearch`
  scoped to `jfrog.com` is the fastest way to find the right `docs.jfrog.com`
  page. `https://docs.jfrog.com/llms.txt` indexes the docs as markdown.
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

- No em-dashes or en-dashes anywhere in site content - hyphens only. This
  corrupts the .docx conversion. Run `python3 automation/convert_dashes.py` to
  auto-fix. That script excludes `.claude/` (and `.git`, `_diagrams`, `_docx`),
  so it will never rewrite this skill - keep that exclusion in place. The skill
  is self-protecting too: it documents the forbidden dash forms only via
  codepoints (`chr(0x2014)`, string concatenation), never as literal characters,
  entities, or escapes, so neither the converter nor a markdown linter can
  corrupt the verification block. If you add dash documentation here, follow the
  same codepoint pattern.
- Never hand-edit generated files: `pages/*.html`, `search-index.json`,
  `automation/_diagrams/`, `automation/_docx/`.
- Never do anything that recreates a Google Doc from scratch; the sync updates
  in place to preserve Drive file IDs that NotebookLM source links depend on.
  Do not touch the ID-tracking logic in `sync_to_drive.py`.

### 5. Adding a NEW page (extra steps beyond editing prose)

1. Append a dict to `PAGE_LIST` in `page_data.py` with `file`, `title`, `desc`,
   `h1`, `lede`, `sections`, `body`, optional `badges`; use the `chain()`
   helper for `prev`/`next`. End with `_p["prev"], _p["next"] = chain(_p["file"])`
   then `PAGE_LIST.append(_p)`.
2. Add the filename to `NAV_ORDER` at the top of `page_data.py` (this drives the
   prev/next chain; position it bottom-up).
3. Add the page to the `NAV` structure in `assets/app.js`, in the matching group.
4. Add the page to the `GROUPS` map AND the `RELATED` map near the bottom of
   `page_data.py` - both feed `build_search_index.py`. Skipping `GROUPS` leaves
   the page ungrouped in search; add it to neighbors' `RELATED` lists too so
   cross-page discovery works both ways.
5. Verify any in-page anchor you link to actually exists on the target page
   (e.g. `build-promotion.html#pattern`), and that the rule "no image assets,
   CSS diagrams only" holds.

### 6. Build locally, then verify

Run from the repo root after any content edit:

```bash
python3 automation/convert_dashes.py   # auto-fix any dashes that crept in
python3 build_pages.py                 # page_data.py -> pages/*.html
python3 build_search_index.py          # -> search-index.json
```

Verify no dashes leaked (should print nothing). Do NOT write the check with
literal em/en-dash characters, HTML dash entities, or unicode dash escapes in
this file - both a markdown linter and `convert_dashes.py` will rewrite them and
the check rots. Build every forbidden form from codepoints, as below. Prefer
this Python check: it is portable (macOS default grep lacks `-P`) and also
catches the dash HTML entities and the unicode escape forms that `page_data.py`
stores:

```bash
python3 - <<'PY'
import pathlib
# Every forbidden form is built from codepoints, never written literally, so
# that neither a markdown linter nor convert_dashes.py can rewrite this block.
EM, EN = chr(0x2014), chr(0x2013)
bad = [EM, EN,
       '&mdash' + ';', '&ndash' + ';',           # HTML entities
       '\\u' + '2014', '\\u' + '2013']            # python/json escape forms
exts = ('.html', '.py', '.js', '.json', '.md')
skip = {'convert_dashes.py', 'AGENTS.md'}
hits = 0
for p in pathlib.Path('.').rglob('*'):
    if p.suffix not in exts or not p.is_file():
        continue
    if '.venv' in p.parts or '.git' in p.parts or p.name in skip:
        continue
    try:
        t = p.read_text(encoding='utf-8')
    except Exception:
        continue
    for b in bad:
        if b in t:
            print(f"{p}: contains {b!r}")
            hits += 1
print('CLEAN' if not hits else f'{hits} file(s) with dashes')
PY
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
