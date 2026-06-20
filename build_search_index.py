#!/usr/bin/env python3
"""Build search-index.json - a SECTION-LEVEL index over the whole site.

The consolidated results page (search.html) and the command-palette overlay
(assets/app.js) both read this file. It produces two kinds of entries:

  kind="page"     one summary entry per page (whole-page body, no anchor)
  kind="section"  one entry per <section id="..."> (deep-linkable heading)

Every entry has the fields the front-end expects:
  url        path relative to site root (e.g. "pages/frogbot.html")
  anchor     "#setup" for sections, "" for page entries
  kind       "page" | "section"
  page       short sidebar label for the owning page
  group      sidebar group the page lives in
  pageTitle  the owning page's <h1>
  title      section heading (or page title for page entries)
  body       plain-text body for snippets
  howto      bool - is this a how-to / step / command section?
  _title / _headings / _body   lowercase fields used by score()

It also appends a single meta record (kind="meta") carrying the curated
RELATED cross-page map and the prev/next learning chain, so the front-end
can render "related information" links without re-deriving them.
"""
import os, re, json
from html.parser import HTMLParser

import page_data as P

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(ROOT, "pages")

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

# A section counts as "how-to" if its anchor id or heading signals action.
HOWTO_IDS = {"howto", "cli", "create", "setup", "install", "steps", "curl",
             "yaml", "rest", "jfapi", "oci", "example", "labs"}
HOWTO_RE = re.compile(r"\b(how to|set up|setting up|create|creating|install|"
                      r"configure|configuring|wire|wiring|run|running|step|"
                      r"calling|build a|first)\b", re.I)


class SectionExtractor(HTMLParser):
    """Splits a page into the <h1> title plus a list of sections.

    Each section = {id, heading, body}. Content before the first
    <section id> (the page <h1>/lede) is folded into the page summary.
    """

    def __init__(self):
        super().__init__()
        self.skip = 0
        self.title = ""           # <title>
        self.h1 = ""
        self._cap_title = False
        self._cap_h1 = False
        self._in_heading = None   # h2/h3 currently open within a section
        self.sections = []        # [{id, heading, body_parts}]
        self._cur = None          # current section dict
        self.preface = []         # text before first section (h1/lede)

    def handle_starttag(self, tag, attrs):
        ad = dict(attrs)
        if tag in SKIP_TAGS:
            self.skip += 1
            return
        if tag == "title":
            self._cap_title = True
        if tag == "h1":
            self._cap_h1 = True
        if tag == "section" and "id" in ad:
            self._cur = {"id": ad["id"], "heading": "", "body": [], "_locked": False}
            self.sections.append(self._cur)
            self._in_heading = None
        if tag in ("h2", "h3") and self._cur is not None and not self._cur["_locked"]:
            self._in_heading = tag

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self.skip:
            self.skip -= 1
            return
        if tag == "title":
            self._cap_title = False
        if tag == "h1":
            self._cap_h1 = False
        if tag in ("h2", "h3"):
            if self._in_heading and self._cur is not None:
                self._cur["_locked"] = True  # capture only the first heading
            self._in_heading = None

    def handle_data(self, data):
        if self._cap_title:
            self.title += data
            return
        if self.skip:
            return
        if self._cap_h1:
            self.h1 += data
        if self._in_heading and self._cur is not None and not self._cur["_locked"]:
            # accumulate ALL text inside the section's first h2/h3,
            # including text nested in <code>, <em>, etc.
            self._cur["heading"] += data
        if self._cur is not None:
            self._cur["body"].append(data)
        else:
            self.preface.append(data)


def clean(s):
    return " ".join((s or "").split())


def is_howto(sec_id, heading):
    return sec_id in HOWTO_IDS or bool(HOWTO_RE.search(heading or ""))


def parse_page(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    p = SectionExtractor()
    p.feed(html)
    h1 = clean(p.h1) or clean(p.title).split("-")[0].strip()
    preface = clean(" ".join(p.preface))
    secs = []
    for s in p.sections:
        secs.append({
            "id": s["id"],
            "heading": clean(s["heading"]),
            "body": clean(" ".join(s["body"])),
        })
    return h1, preface, secs


def entry(url, anchor, kind, page, group, page_title, title, body, howto):
    return {
        "url": url,
        "anchor": anchor,
        "kind": kind,
        "page": page,
        "group": group,
        "pageTitle": page_title,
        "title": title,
        "body": body,
        "howto": howto,
        "_title": title.lower(),
        "_headings": (title + " " + page_title).lower(),
        "_body": body.lower(),
    }


def build_for_file(fn, url):
    label = LABELS.get(fn, fn.replace("-", " ").replace(".html", "").title())
    group = P.GROUPS.get(fn, "")
    path = os.path.join(ROOT, "index.html") if fn == "index.html" \
        else os.path.join(PAGES, fn)
    h1, preface, secs = parse_page(path)
    page_title = h1 or label
    out = []

    # page summary entry (whole-page body so broad queries still match)
    whole = clean(preface + " " + " ".join(s["heading"] + " " + s["body"] for s in secs))
    out.append(entry(url, "", "page", label, group, page_title,
                     page_title, whole, False))

    # one entry per section (deep-linkable)
    for s in secs:
        if not s["heading"] and not s["body"]:
            continue
        heading = s["heading"] or label
        out.append(entry(url, "#" + s["id"], "section", label, group,
                         page_title, heading, s["body"],
                         is_howto(s["id"], heading)))
    return out


def main():
    entries = []

    # Home (page-level only)
    home = build_for_file("index.html", "index.html")
    home[0]["title"] = "JFrog Learn - Home"
    home[0]["pageTitle"] = "JFrog Learn - Home"
    home[0]["_title"] = home[0]["title"].lower()
    entries.extend(home[:1])  # home has no real <section id>, keep summary only

    # Topic pages (search.html is the results UI itself, not content)
    for fn in sorted(os.listdir(PAGES)):
        if not fn.endswith(".html") or fn == "search.html":
            continue
        entries.extend(build_for_file(fn, f"pages/{fn}"))

    # Meta record: related map + prev/next chain + page labels/groups
    chain = {}
    for f, _ in P.NAV_ORDER:
        prev, nxt = P.chain(f)
        chain[f] = {"prev": list(prev), "next": list(nxt)}
    meta = {
        "kind": "meta",
        "related": P.RELATED,
        "chain": chain,
        "labels": LABELS,
        "groups": P.GROUPS,
    }
    entries.append(meta)

    out = os.path.join(ROOT, "search-index.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, separators=(",", ":"))

    n_page = sum(1 for e in entries if e.get("kind") == "page")
    n_sec = sum(1 for e in entries if e.get("kind") == "section")
    n_how = sum(1 for e in entries if e.get("howto"))
    print(f"wrote search-index.json: {n_page} page + {n_sec} section entries "
          f"({n_how} how-to) + 1 meta")
    for e in entries:
        if e.get("kind") == "section":
            flag = " [how-to]" if e["howto"] else ""
            print(f"  {e['url']}{e['anchor']:14s} {e['title']!r}{flag}")


if __name__ == "__main__":
    main()
