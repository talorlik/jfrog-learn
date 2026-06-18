#!/usr/bin/env python3
"""Generate topic pages from a shared shell. Bodies live in pages_content/."""
import os, json

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(ROOT, "pages")

SHELL = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} — JFrog Learn</title>
<meta name="description" content="{desc}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;450;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="../assets/style.css" />
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%2340b14e'/%3E%3Cpath d='M9 21V11l7 4 7-4v10' fill='none' stroke='%230f1410' stroke-width='2.4' stroke-linejoin='round' stroke-linecap='round'/%3E%3C/svg%3E" />
<script>window.__BASE='../';</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<aside class="sidebar" id="sidebar"></aside>

<div id="onThisPage" hidden>
  <p class="nav-group">On this page</p>
  {onthispage}
</div>

<button class="menu-btn" id="menuBtn" aria-label="Open navigation"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
<div class="scrim" id="scrim"></div>

<main id="main">
  <button class="theme-toggle" data-theme-toggle aria-label="Switch theme"></button>

  <header class="page-head">
    <nav class="breadcrumb"><a href="../index.html">Home</a><span class="sep">/</span><span>{title}</span></nav>
    <div class="page-badges">{badges}</div>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </header>

{body}

  <nav class="page-nav" aria-label="Page navigation">
    <a href="{prev_href}"><span class="pn-dir">← {prev_dir}</span><span class="pn-title">{prev_title}</span></a>
    <a class="pn-next" href="{next_href}"><span class="pn-dir">{next_dir} →</span><span class="pn-title">{next_title}</span></a>
  </nav>

  <footer class="footer">
    <p>All facts link to primary JFrog documentation, current as of June 2026. Product names belong to JFrog Ltd.</p>
  </footer>
</main>

<div class="search-overlay" id="searchOverlay" role="dialog" aria-modal="true" aria-label="Search">
  <div class="search-box">
    <div class="search-input-row">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
      <input id="searchInput" type="text" placeholder="Search concepts, commands, CLI…" autocomplete="off" spellcheck="false" />
      <span class="search-esc">esc</span>
    </div>
    <div class="search-results" id="searchResults"></div>
    <div class="search-foot">
      <span><kbd>&uarr;</kbd><kbd>&darr;</kbd> navigate</span><span><kbd>&crarr;</kbd> open</span><span><kbd>/</kbd> or <kbd>&#8984;K</kbd> to search</span>
    </div>
  </div>
</div>

<script src="../assets/app.js"></script>
</body>
</html>
"""

def render(p):
    onthis = "\n  ".join(
        f'<a href="#{s["id"]}" class="nav-link">{s["label"]}</a>' for s in p["sections"]
    )
    return SHELL.format(
        title=p["title"], desc=p["desc"], onthispage=onthis,
        badges=p["badges"], h1=p["h1"], lede=p["lede"], body=p["body"],
        prev_href=p["prev"][0], prev_dir=p["prev"][1], prev_title=p["prev"][2],
        next_href=p["next"][0], next_dir=p["next"][1], next_title=p["next"][2],
    )

if __name__ == "__main__":
    from page_data import PAGE_LIST
    for p in PAGE_LIST:
        out = os.path.join(PAGES, p["file"])
        with open(out, "w") as f:
            f.write(render(p))
        print("wrote", p["file"])
