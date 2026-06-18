# JFrog Learn — Artifactory & Xray, Bottom-Up

An interactive, self-paced **knowledge base** that teaches **JFrog Artifactory** and **JFrog Xray** from first principles — no prior knowledge assumed. It grows over time: each new topic becomes its own page with full-text search across everything.

🔗 **Live site:** https://talorlik.github.io/jfrog-learn/

## What's inside

A multi-page knowledge base with client-side search (press `/` or `⌘K` / `Ctrl-K` on any page):

**Core concepts**
- **Fundamentals** — the problem these tools solve, a vocabulary primer (artifact, CVE, SCA, SBOM, JPD, build-info, promotion), the 4 repository types (local/remote/virtual/federated), the Xray scan lifecycle, the Policy vs. Watch model, three hands-on lab tracks (JFrog Cloud free tier, local Docker, Concepts + CLI), and a `jf` CLI cheat sheet.
- **Replication & Federation** — keeping artifacts in sync across sites: push/pull replication vs. federated repositories.
- **Build promotion in practice** — moving a build dev → staging → release without rebuilding, via `build-info`, the CLI, and the REST API.

**Distribution**
- **Release Bundles & Distribution** — immutable signed artifact manifests and shipping them to edge nodes / air-gapped sites.

**Automation & security**
- **Artifactory REST API** — auth methods, key endpoints, and driving them from `curl` and `jf api`.
- **Frogbot & IDE integration** — PR/repo scanning with Xray and inline editor findings.
- **JFrog Pipelines** — the YAML CI/CD engine: integrations, resources, steps, and a Hello-World walkthrough.
- **Access tokens & permissions** — tokens, and the Users → Groups → Permission Targets model.

**Platform operations**
- **Kubernetes / Helm setup** — installing Artifactory on a cluster via Helm, and using Artifactory as a Helm/OCI chart registry.

## Project structure

```
index.html              # home / landing page with the topic grid
pages/*.html            # one page per topic (generated from page_data.py)
assets/style.css        # design system (light/dark, responsive)
assets/app.js           # sidebar injection, theme toggle, mobile nav, tabs, scrollspy, search
search-index.json       # static full-text index consumed by the in-browser search
build_pages.py          # generator: shared HTML shell + page_data.py → pages/*.html
page_data.py            # content bodies + nav order for each topic page
build_search_index.py   # parses index.html + pages/*.html → search-index.json
```

### Regenerating after a content change

```bash
python3 build_pages.py          # rebuild pages/*.html from page_data.py
python3 build_search_index.py   # rebuild search-index.json
```

Search runs entirely in the browser (a static JSON index fetched and ranked client-side), so it works on GitHub Pages with no backend.

## Run locally

It's a static site — serve the folder so `fetch()` of the search index works:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Adding a new topic

1. Append a page dict to `PAGE_LIST` in `page_data.py` (and add it to `NAV_ORDER`).
2. Add the link to the `NAV` model in `assets/app.js` and a label in `build_search_index.py`.
3. Run `build_pages.py` then `build_search_index.py`, and commit.

All facts link to primary JFrog documentation. Product names belong to JFrog Ltd.

## License

[MIT](LICENSE) © 2026 Tal Orlik
