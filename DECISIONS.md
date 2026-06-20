# Decisions

A running log of the key decisions made on this project and, more importantly,
WHY. The goal is that any future contributor (human or AI) can understand the
current shape of the system without re-deriving it. For the operational rules
that follow from these decisions, see [AGENTS.md](AGENTS.md).

Each entry records the decision, the rationale, and any alternatives that were
considered and rejected.

---

## 1. Static, generated multi-page site over a CMS or framework

Decision: build the knowledge base as plain static HTML/CSS/JS, with each topic
page generated from a single content source (`page_data.py`) plus a shared HTML
shell (`build_pages.py`).

Rationale:
- It hosts for free on GitHub Pages with no backend to run or pay for.
- One content source plus one template keeps every page visually consistent and
  makes site-wide changes a single edit.
- It stays simple and fully inspectable, which matters for a learning resource.

Rejected alternatives: a static-site generator (Hugo, Eleventy) or a JS
framework (Next, Astro) added build tooling and dependencies out of proportion to
a content site this small.

Consequence: `pages/*.html` and `search-index.json` are GENERATED. They are never
hand-edited; the source is `page_data.py`.

---

## 2. Client-side full-text search over a hosted search service

Decision: ship a static `search-index.json` built at generation time and rank it
in the browser (`assets/app.js`), triggered by `/` or Cmd/Ctrl-K.

Rationale: works on GitHub Pages with zero backend, no API keys, no per-query
cost, and no privacy concerns. The corpus is small enough that a client-side
index is fast.

Rejected alternative: a hosted search service (Algolia and similar) added
external dependencies, accounts, and cost for no real benefit at this scale.

---

## 3. Diagrams as pure CSS/HTML, not image files

Decision: every diagram on the site is drawn with HTML markup and CSS (figures
with classes like `diag-grid`, `flow-row`, `bm-box`, `onion`). The repository
contains zero diagram image files.

Rationale: CSS/HTML diagrams stay crisp at any zoom, adapt to light/dark themes,
are diffable in version control, and need no image-editing workflow.

Consequence: the Google Docs pipeline cannot just copy image files - there are
none. It has to rasterize the live figures (see decision 5).

---

## 4. Mirror the content into Google Docs for NotebookLM

Decision: automatically mirror every content page into a Google Drive folder
(`jfrog-learning`) as native Google Docs, one Doc per page plus an auto-rebuilt
index Doc.

Rationale: the user wants to study the material in NotebookLM, which ingests
Google Docs as sources. Keeping the Docs in sync with the site by hand would be
tedious and error-prone, so it is automated in CI.

---

## 5. The DOCX upload-and-convert pipeline (over Markdown or the Docs API)

Decision: to produce each Google Doc, build a `.docx` locally (with diagrams
rendered to embedded PNGs and native Word structure), upload it to Drive with the
Google Doc mimeType, and let Drive convert it.

Rationale and rejected alternatives:
- Uploading Markdown was tried first and rejected: Drive's Markdown importer
  mangles tables and code, and code fences (including Mermaid) never render as
  diagrams.
- Driving the Google Docs API directly was rejected: it cannot embed local image
  bytes easily and would require the broader `documents` OAuth scope.
- The DOCX path wins: Drive's DOCX importer is its highest-fidelity converter, so
  headings, lists, tables, code, callouts, and embedded images survive well; the
  diagrams (rasterized to PNG via headless Chromium, decision 3) finally render;
  and it needs only the narrow `drive.file` scope (decision 6).

Caveat: conversion is high-fidelity but not 100 percent pixel-perfect. That is an
accepted trade-off.

---

## 6. OAuth with the narrow `drive.file` scope, acting as the user

Decision: authenticate the sync with OAuth user credentials using only the
non-sensitive `https://www.googleapis.com/auth/drive.file` scope, supplied via a
single env var / GitHub secret `GOOGLE_OAUTH_CREDENTIALS` (client_id,
client_secret, refresh_token).

Rationale:
- `drive.file` is non-sensitive, so it avoids Google's app-verification friction
  while letting the app see and manage only the files it creates - which is
  exactly the `jfrog-learning` folder and its Docs.
- Acting as the user means the Docs live in the user's own Drive and count
  against the user's own quota, and they own the NotebookLM sources.
- Because no image is uploaded via the Docs API (images are embedded in the
  `.docx` before upload), the `documents` scope is not needed.

Note: a service account would only work on Workspace/Shared Drives, so it is not
used for this personal-Drive setup.

---

## 7. Idempotent in-place upsert that preserves Doc file IDs

Decision: the sync treats the Drive folder as the source of truth. Each run looks
up a Doc by exact name; if it exists, it UPDATES that Doc in place by uploading
new `.docx` media (same file id); if not, it CREATES one. It never deletes and
recreates an existing Doc.

Rationale: NotebookLM source links point at Drive file IDs, and the user
refreshes NotebookLM sources manually (there is no NotebookLM API). If a Doc's ID
changed, the user's NotebookLM source would break. Preserving the ID keeps every
existing source link valid across every sync. The preserved IDs are recorded in
`automation/SETUP.md`.

---

## 8. No em-dashes or en-dashes anywhere; hyphens only

Decision: ban em-dashes (U+2014) and en-dashes (U+2013) across the entire
project - website, generated Docs, file names, and documentation - and use plain
hyphens instead. Enforced by a one-shot converter `automation/convert_dashes.py`
and a verify grep.

Rationale: a deliberate, consistent typographic style the user wants applied
everywhere. It is now a permanent project rule.

Implementation note: the content in `page_data.py` stores dashes as
unicode-escape sequences (`\u2014`-style), not literal characters, so the
converter had to handle the literal characters, the HTML entities
(`&mdash;` / `&ndash;`), AND the escape forms. An early version that only caught
literals missed the escaped ones.

---

## 9. Self-healing reconciliation of legacy Doc names

Decision: when the Doc-name template changed (the prefix went from an em-dash
form to the hyphen form `"JFrog Learn - "` under decision 8), add a
`reconcile_legacy_name()` step that runs before each upsert: it finds any Doc
under the old em-dash name, renames it in place to the new name (preserving its
file id), and trashes any duplicate that a prior run created under the new name.

Rationale: a naive rename of the name template caused one sync run to fail to
find the existing (old-named) Docs, so it CREATED 10 duplicate Docs under the new
names. That would have orphaned the original Doc IDs and broken NotebookLM links
(violating decision 7). The reconciliation step recovers automatically: it
reclaimed all 10 originals by renaming them in place and removed the duplicates,
and it makes future name migrations safe.

---

## 10. Document color scheme: dark code blocks, readable inline code

Decision: in the generated Docs, render fenced code BLOCKS in a dark theme
matching the site (background `#0A0D0B`, green text `#9FE6AD`, border `#24302A`,
drawn as a single-cell table). Render INLINE code as dark slate text `#242A33` on
a light gray chip `#EDEDF2`.

Rationale:
- Dark code blocks were the user's explicit preference ("Dark, matching the
  site").
- The original inline code used a faint green that was hard to read on light and
  shaded backgrounds. The user asked for a color that looks good on white or any
  shaded background, while leaving images, diagrams, and code blocks untouched.
  Dark slate on a light chip satisfies that.

Scope guard: these color choices apply ONLY to the generated documents. Colors
inside images, diagrams, and code blocks are left as-is per the user's
instruction.
