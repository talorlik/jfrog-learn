#!/usr/bin/env python3
"""
render_diagrams.py - Render each JFrog Learn page's CSS/HTML <figure> diagrams to
high-DPI PNG images using headless Chromium (Playwright) + the site's real
assets/style.css, so the diagrams look exactly like the live website.

The site draws its diagrams with HTML + CSS (no image files), so the only way to
get faithful diagram images for the Google Docs is to render them in a browser and
screenshot each <figure> element.

Output: PNGs written to automation/_diagrams/<slug>/fig_<n>.png, plus a JSON
manifest mapping (slug -> [ {index, path, caption, width, height} ]).

Usage:
    python render_diagrams.py                 # all pages
    python render_diagrams.py fundamentals    # one slug
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

from bs4 import BeautifulSoup

REPO_ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = REPO_ROOT / "pages"
CSS_PATH = REPO_ROOT / "assets" / "style.css"
OUT_DIR = Path(__file__).resolve().parent / "_diagrams"

# Allow overriding the Chromium path (the sandbox needs an explicit binary).
CHROME_PATH = os.environ.get("PLAYWRIGHT_CHROMIUM_PATH", "").strip() or None

EXCLUDE = {"search"}
# Render at 2x for crisp images in the Doc.
DEVICE_SCALE = 2
# A comfortable viewport; figures size themselves, we screenshot the element.
VIEWPORT = {"width": 1100, "height": 900}


def page_slugs(argv: list[str]) -> list[str]:
    if len(argv) > 1:
        return [argv[1]]
    return sorted(
        p.stem for p in PAGES_DIR.glob("*.html") if p.stem not in EXCLUDE
    )


def figure_caption(fig) -> str:
    cap = fig.find("figcaption")
    if cap:
        return " ".join(cap.get_text(" ").split())
    al = fig.get("aria-label", "")
    return " ".join(al.split())


def build_doc_html(page_html: str, css: str) -> tuple[str, list[str]]:
    """Wrap the page's <main> content in a minimal HTML doc with the site CSS so
    figures render identically. Returns (html, captions[]) where captions align
    with figure order."""
    soup = BeautifulSoup(page_html, "lxml")
    content = soup.find("main") or soup.find("article") or soup.body
    figs = content.find_all("figure")
    captions = [figure_caption(f) for f in figs]

    # Build a standalone page: site CSS + the content. We give body a white
    # background and some padding so screenshots aren't clipped or transparent.
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<style>{css}</style>
<style>
  html,body {{ background:#fff !important; margin:0; padding:0; }}
  main {{ padding:24px; }}
  /* Ensure figures are fully visible and not constrained by layout chrome */
  figure {{ break-inside: avoid; }}
</style>
</head><body><main>{''.join(str(f) for f in figs)}</main></body></html>"""
    return doc, captions


async def render_slug(browser, slug: str, css: str) -> list[dict]:
    page_file = PAGES_DIR / f"{slug}.html"
    if not page_file.exists():
        return []
    html = page_file.read_text(encoding="utf-8")
    doc_html, captions = build_doc_html(html, css)
    if not captions:
        return []

    out_sub = OUT_DIR / slug
    out_sub.mkdir(parents=True, exist_ok=True)

    page = await browser.new_page(
        viewport=VIEWPORT, device_scale_factor=DEVICE_SCALE
    )
    await page.set_content(doc_html, wait_until="networkidle")
    # Give CSS/layout a beat to settle (fonts, flex, etc.)
    await page.wait_for_timeout(300)

    figs = await page.query_selector_all("figure")
    results = []
    for i, el in enumerate(figs):
        png_path = out_sub / f"fig_{i}.png"
        try:
            box = await el.bounding_box()
            await el.screenshot(path=str(png_path))
            results.append({
                "index": i,
                "path": str(png_path.relative_to(REPO_ROOT)),
                "abs_path": str(png_path),
                "caption": captions[i] if i < len(captions) else "",
                "width": round(box["width"]) if box else None,
                "height": round(box["height"]) if box else None,
            })
            print(f"  {slug} fig {i}: {png_path.name} "
                  f"({results[-1]['width']}x{results[-1]['height']})")
        except Exception as e:
            print(f"  {slug} fig {i}: FAILED {e!r}")
    await page.close()
    return results


async def main_async(slugs: list[str]) -> dict:
    css = CSS_PATH.read_text(encoding="utf-8") if CSS_PATH.exists() else ""
    from playwright.async_api import async_playwright

    manifest: dict[str, list[dict]] = {}
    async with async_playwright() as p:
        launch_kwargs = {"args": ["--no-sandbox", "--disable-gpu",
                                  "--force-color-profile=srgb"]}
        if CHROME_PATH:
            launch_kwargs["executable_path"] = CHROME_PATH
        browser = await p.chromium.launch(**launch_kwargs)
        for slug in slugs:
            print(f"rendering {slug} ...")
            manifest[slug] = await render_slug(browser, slug, css)
        await browser.close()
    return manifest


def main():
    slugs = page_slugs(sys.argv)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = asyncio.run(main_async(slugs))
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    total = sum(len(v) for v in manifest.values())
    print(f"\nDone. Rendered {total} diagram(s) across {len(slugs)} page(s).")
    print(f"Manifest: {OUT_DIR / 'manifest.json'}")


if __name__ == "__main__":
    main()
