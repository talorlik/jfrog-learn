#!/usr/bin/env python3
"""Build search-index.json by parsing index.html + every page in pages/.

Each entry has the fields app.js expects:
  url       - path relative to site root (e.g. "pages/frogbot.html")
  page      - short display label for the result
  title     - page <h1> (or <title> fallback)
  body      - plain-text body for snippets
  _title    - lowercase title (score())
  _headings - lowercase concatenation of all h1/h2/h3 (score())
  _body     - lowercase body (score())
"""
import os, re, json
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(ROOT, "pages")

# Short display labels per file (matches sidebar phrasing)
LABELS = {
    "index.html": "Home",
    "fundamentals.html": "Fundamentals",
    "replication-federation.html": "Replication & Federation",
    "build-promotion.html": "Build promotion",
    "release-bundles.html": "Release Bundles & Distribution",
    "rest-api.html": "Artifactory REST API",
    "frogbot.html": "Frogbot & IDE",
    "pipelines.html": "JFrog Pipelines",
    "access-tokens.html": "Access tokens & permissions",
    "kubernetes-helm.html": "Kubernetes / Helm setup",
}

SKIP_TAGS = {"script", "style", "svg", "head"}


class Extractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.cur_tag = None
        self.title = ""
        self.h1 = ""
        self.headings = []
        self.text_parts = []
        self._buf = []
        self._capture_title = False

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.skip += 1
        if tag == "title":
            self._capture_title = True
        self.cur_tag = tag
        if tag in ("h1", "h2", "h3"):
            self._buf = []

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self.skip:
            self.skip -= 1
        if tag == "title":
            self._capture_title = False
        if tag in ("h1", "h2", "h3"):
            txt = " ".join("".join(self._buf).split())
            if txt:
                self.headings.append(txt)
                if tag == "h1" and not self.h1:
                    self.h1 = txt
            self._buf = []
        self.cur_tag = None

    def handle_data(self, data):
        if self._capture_title:
            self.title += data
            return
        if self.skip:
            return
        if self.cur_tag in ("h1", "h2", "h3"):
            self._buf.append(data)
        self.text_parts.append(data)


def clean(s):
    return " ".join(s.split())


def extract(path, url, label):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    p = Extractor()
    p.feed(html)
    title = clean(p.h1) or clean(p.title).split("—")[0].strip() or label
    body = clean(" ".join(p.text_parts))
    headings = clean(" ".join(p.headings))
    return {
        "url": url,
        "page": label,
        "title": title,
        "body": body,
        "_title": title.lower(),
        "_headings": headings.lower(),
        "_body": body.lower(),
    }


def main():
    entries = []
    # home
    home = os.path.join(ROOT, "index.html")
    if os.path.exists(home):
        e = extract(home, "index.html", LABELS["index.html"])
        e["title"] = "JFrog Learn — Home"
        e["_title"] = e["title"].lower()
        entries.append(e)
    # topic pages
    for fn in sorted(os.listdir(PAGES)):
        if not fn.endswith(".html"):
            continue
        label = LABELS.get(fn, fn.replace("-", " ").replace(".html", "").title())
        entries.append(extract(os.path.join(PAGES, fn), f"pages/{fn}", label))

    out = os.path.join(ROOT, "search-index.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, separators=(",", ":"))
    print(f"wrote search-index.json with {len(entries)} entries")
    for e in entries:
        print(f"  {e['url']:42s} {len(e['body']):6d} chars  '{e['title']}'")


if __name__ == "__main__":
    main()
