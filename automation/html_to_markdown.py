#!/usr/bin/env python3
"""
html_to_markdown.py — Convert a JFrog Learn page (HTML) into clean Markdown that
preserves structure (headings, lists, tables, code, callouts) and converts the
site's CSS/HTML diagrams into Mermaid flowcharts (with an image fallback hook for
any future diagram that can't be expressed as Mermaid).

The Markdown is later uploaded to Google Drive and converted to a Google Doc, then
used as a NotebookLM source. NotebookLM reads text, so Mermaid (text) > images.

Stdlib + BeautifulSoup only. No site JS/CSS needed.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

# ---------------------------------------------------------------------------
# Inline rendering (bold, italic, code, links) for text-bearing elements
# ---------------------------------------------------------------------------

INLINE_TAGS = {"strong", "b", "em", "i", "code", "a", "span", "small", "sup", "sub", "br", "kbd"}


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def render_inline(node) -> str:
    """Render an element's children to inline Markdown (recursive)."""
    out = []
    for child in node.children:
        if isinstance(child, Comment):
            continue
        if isinstance(child, NavigableString):
            out.append(str(child))
            continue
        if not isinstance(child, Tag):
            continue
        name = child.name.lower()
        inner = render_inline(child)
        if name in ("strong", "b"):
            inner = inner.strip()
            out.append(f"**{inner}**" if inner else "")
        elif name in ("em", "i"):
            inner = inner.strip()
            out.append(f"*{inner}*" if inner else "")
        elif name in ("code", "kbd"):
            inner = inner.strip()
            out.append(f"`{inner}`" if inner else "")
        elif name == "a":
            href = child.get("href", "").strip()
            label = inner.strip() or href
            if href and not href.startswith("#"):
                out.append(f"[{label}]({href})")
            else:
                out.append(label)
        elif name == "br":
            out.append("  \n")
        elif name in ("span", "small", "sup", "sub"):
            # small/sup/sub: keep text, drop styling; add a space so glued labels separate
            out.append(inner)
        else:
            out.append(inner)
    text = "".join(out)
    # Collapse internal whitespace but keep explicit line breaks
    parts = text.split("  \n")
    parts = [re.sub(r"[ \t]+", " ", p).strip() for p in parts]
    return "  \n".join(p for p in parts if p is not None)


# ---------------------------------------------------------------------------
# Diagram detection + Mermaid conversion
# ---------------------------------------------------------------------------

def _node_text(el: Tag) -> str:
    """Readable label for a diagram node: main text + a small sub-label if present."""
    small = el.find("small")
    small_txt = _clean(small.get_text(" ")) if small else ""
    if small:
        small.extract()
    main = _clean(el.get_text(" "))
    if small_txt:
        return f"{main} — {small_txt}" if main else small_txt
    return main


def _mm_id(counter: list[int]) -> str:
    counter[0] += 1
    return f"n{counter[0]}"


def _mm_label(text: str) -> str:
    """Escape a label for a Mermaid node."""
    text = text.replace('"', "'").replace("\n", " ")
    return _clean(text)


def flow_to_mermaid(fig: Tag) -> str | None:
    """Convert a stack of .flow-row blocks into a top-down Mermaid flowchart."""
    rows = fig.find_all("div", class_="flow-row", recursive=True)
    if not rows:
        return None
    counter = [0]
    lines = ["flowchart TD"]
    prev_ids: list[str] = []
    for row in rows:
        steps = row.find_all("div", class_="flow-step", recursive=False)
        if steps:
            ids = []
            for st in steps:
                nid = _mm_id(counter)
                label = _mm_label(_node_text(st))
                lines.append(f'    {nid}["{label}"]')
                ids.append(nid)
            # chain steps left-to-right within a row
            for a, b in zip(ids, ids[1:]):
                lines.append(f"    {a} --> {b}")
            # connect previous row's last to this row's first
            if prev_ids and ids:
                lines.append(f"    {prev_ids[-1]} --> {ids[0]}")
            prev_ids = ids
        else:
            # a connector/annotation row (e.g. "↓ every artifact is indexed")
            ann = _clean(row.get_text(" "))
            ann = re.sub(r"^[↓→▸\s]+|[↓→▸\s]+$", "", ann)
            if ann and prev_ids:
                # carry annotation onto the next edge by stashing it
                row["_ann"] = ann  # type: ignore
    return "\n".join(lines)


def diag_grid_to_mermaid(fig: Tag) -> str | None:
    """Convert a .diag-grid (columns of nodes joined by arrows) to Mermaid LR."""
    grid = fig.find("div", class_="diag-grid")
    if not grid:
        return None
    counter = [0]
    lines = ["flowchart LR"]
    col_last_ids: list[str] = []  # last node id of each column, in order
    arrows: list[str] = []
    for child in grid.find_all(["div"], recursive=False):
        cls = child.get("class", [])
        if "diag-col" in cls:
            ids = []
            label_el = child.find("p", class_="diag-label")
            col_label = _clean(label_el.get_text(" ")) if label_el else ""
            nodes = child.find_all("div", class_=re.compile(r"diag-node|diag-bracket"))
            for nd in nodes:
                if "diag-bracket" in nd.get("class", []):
                    continue
                nid = _mm_id(counter)
                label = _mm_label(_node_text(nd))
                lines.append(f'    {nid}["{label}"]')
                ids.append(nid)
            # vertical relation inside a column (stacked nodes)
            for a, b in zip(ids, ids[1:]):
                lines.append(f"    {a} -.-> {b}")
            if ids:
                if col_label:
                    lines.append(f"    %% column: {col_label}")
                col_last_ids.append(ids[0])
        elif "diag-arrow" in cls:
            arrows.append(_clean(child.get_text(" ")))
    # connect columns in sequence using captured arrow labels
    for i, (a, b) in enumerate(zip(col_last_ids, col_last_ids[1:])):
        lab = arrows[i] if i < len(arrows) else ""
        lab = re.sub(r"[→\s]+$", "", lab).strip()
        if lab:
            lines.append(f'    {a} -->|"{_mm_label(lab)}"| {b}')
        else:
            lines.append(f"    {a} --> {b}")
    return "\n".join(lines)


def bm_to_mermaid(fig: Tag) -> str | None:
    """Convert a .bm-box / .bm-band 'mental model' diagram to Mermaid TD."""
    boxes = fig.find_all("div", class_="bm-box")
    core = fig.find("div", class_="bm-core") or fig.find("div", class_="bm-band")
    if not boxes and not core:
        return None
    counter = [0]
    lines = ["flowchart TD"]
    src_ids = []
    for bx in boxes:
        nid = _mm_id(counter)
        lines.append(f'    {nid}["{_mm_label(_node_text(bx))}"]')
        src_ids.append(nid)
    core_id = None
    if core:
        titles = [
            _clean(t.get_text(" "))
            for t in core.find_all(class_=re.compile(r"bm-title"))
        ]
        core_label = " / ".join(titles) if titles else "Core"
        pills = [
            _clean(p.get_text(" "))
            for p in core.find_all(class_=re.compile(r"^pill"))
        ]
        if pills:
            core_label += " — " + ", ".join(pills)
        core_id = _mm_id(counter)
        lines.append(f'    {core_id}["{_mm_label(core_label)}"]')
        for sid in src_ids:
            lines.append(f"    {sid} --> {core_id}")
    # outputs band (e.g. consumers/production) if present
    out_band = fig.find("div", class_="bm-out")
    if out_band is not None and core_id:
        out_boxes = out_band.find_all("div", class_="bm-box")
        for ob in out_boxes:
            oid = _mm_id(counter)
            lines.append(f'    {oid}["{_mm_label(_node_text(ob))}"]')
            lines.append(f"    {core_id} --> {oid}")
    return "\n".join(lines)


def convert_diagram(fig: Tag) -> tuple[str | None, str]:
    """
    Try each diagram converter. Returns (mermaid_or_none, caption).
    Caller renders Mermaid as a fenced ```mermaid block, or falls back to a text
    description / image if mermaid is None.
    """
    cap_el = fig.find("figcaption")
    caption = _clean(cap_el.get_text(" ")) if cap_el else ""
    if not caption:
        caption = _clean(fig.get("aria-label", "")) if fig.has_attr("aria-label") else ""

    for converter in (flow_to_mermaid, diag_grid_to_mermaid, bm_to_mermaid):
        try:
            mm = converter(fig)
        except Exception:
            mm = None
        if mm and len(mm.splitlines()) > 1:
            return mm, caption
    return None, caption


def diagram_text_fallback(fig: Tag) -> str:
    """Linearize an un-convertible diagram into readable text so NotebookLM can use it."""
    lines = []
    for el in fig.find_all(["div", "span", "p"], recursive=True):
        if el.find(["div", "span", "p"], recursive=False):
            continue  # only leaf-ish blocks
        t = _clean(el.get_text(" "))
        if t:
            lines.append(f"- {t}")
    # dedupe consecutive
    out, prev = [], None
    for l in lines:
        if l != prev:
            out.append(l)
        prev = l
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------

def table_to_markdown(table: Tag) -> str:
    rows = []
    head = table.find("thead")
    body = table.find("tbody") or table
    headers = []
    if head:
        headers = [render_inline(th) or _clean(th.get_text(" ")) for th in head.find_all("th")]
    if not headers:
        first = body.find("tr")
        if first and first.find("th"):
            headers = [render_inline(th) for th in first.find_all("th")]
    md = []
    if headers:
        headers = [h.replace("|", "\\|").replace("\n", " ") or " " for h in headers]
        md.append("| " + " | ".join(headers) + " |")
        md.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for tr in body.find_all("tr"):
        cells = tr.find_all(["td"])
        if not cells:
            continue
        vals = [(render_inline(td) or _clean(td.get_text(" "))).replace("|", "\\|").replace("\n", " ") or " " for td in cells]
        md.append("| " + " | ".join(vals) + " |")
    return "\n".join(md)


# ---------------------------------------------------------------------------
# List rendering (nested)
# ---------------------------------------------------------------------------

def list_to_markdown(lst: Tag, depth: int = 0) -> str:
    ordered = lst.name.lower() == "ol"
    indent = "    " * depth
    out = []
    idx = 1
    for li in lst.find_all("li", recursive=False):
        # drop decorative step-number spans (the markdown ordinal already numbers)
        for n in li.find_all(class_=re.compile(r"ls-n|step-n|card-num")):
            n.decompose()
        # split nested lists out first
        nested = []
        for sub in li.find_all(["ul", "ol"], recursive=False):
            nested.append(sub.extract())
        marker = f"{idx}." if ordered else "-"
        # If the li wraps a single content div (lab-steps pattern), render its
        # block children so a bold title, code, and notes separate cleanly.
        inner_div = None
        div_children = [c for c in li.children if isinstance(c, Tag)]
        if len(div_children) == 1 and div_children[0].name == "div":
            inner_div = div_children[0]
        if inner_div is not None and inner_div.find(["pre", "p", "ul", "ol"]):
            body = render_block_children(inner_div).strip()
            body_lines = body.split("\n\n")
            first = body_lines[0] if body_lines else ""
            out.append(f"{indent}{marker} {first}")
            for extra in body_lines[1:]:
                for ln in extra.split("\n"):
                    out.append(f"{indent}    {ln}" if ln else "")
            for sub in nested:
                out.append(list_to_markdown(sub, depth + 1))
            idx += 1
            continue
        text = render_inline(li).strip()
        out.append(f"{indent}{marker} {text}" if text else f"{indent}{marker}")
        for sub in nested:
            out.append(list_to_markdown(sub, depth + 1))
        idx += 1
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Callouts / cards
# ---------------------------------------------------------------------------

CALLOUT_PREFIX = {
    "callout-tip": "💡 Tip",
    "callout-q": "❓",
    "callout-warn": "⚠️ Warning",
    "callout-note": "📝 Note",
}


def callout_to_markdown(div: Tag) -> str:
    cls = div.get("class", [])
    title_el = div.find(class_="callout-title")
    title = _clean(title_el.get_text(" ")) if title_el else ""
    if title_el:
        title_el.extract()
    prefix = ""
    for c in cls:
        if c in CALLOUT_PREFIX:
            prefix = CALLOUT_PREFIX[c]
            break
    lines = []
    head = " ".join(x for x in [prefix, f"**{title}**" if title else ""] if x).strip()
    if head:
        lines.append(f"> {head}")
    body = render_block_children(div).strip()
    for bl in body.split("\n"):
        lines.append(f"> {bl}" if bl else ">")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Generic block walker
# ---------------------------------------------------------------------------

SKIP_CLASSES = {"nav-link", "sidebar", "search", "tab-bar", "kicker"}


def _guess_lang(text: str) -> str:
    low = text.lstrip()[:80].lower()
    # scan all lines for a strong shell signal (handles comment-first blocks)
    for ln in text.splitlines():
        s = ln.strip().lower()
        if s.startswith(("curl", "jf ", "jfrog", "docker ", "helm ", "kubectl ",
                         "git ", "brew ", "npm ", "pip ", "mvn ", "export ")):
            return "bash"
    if low.startswith((
        "curl", "jf ", "jfrog", "docker", "helm", "kubectl", "git ", "export ",
        "cd ", "$ ", "sudo", "brew", "npm", "pip", "apt", "yum", "mvn", "go ",
        "chmod", "tar ", "wget", "bash", "sh ", "./",
    )):
        return "bash"
    if low.startswith(("{", "[")):
        return "json"
    if re.match(r"^[a-z_]+:\s", low) or low.startswith((
        "apiversion", "kind:", "resources:", "pipelines:", "name:", "steps:",
        "on:", "jobs:", "version:",
    )):
        return "yaml"
    if low.startswith(("<", "<!")):
        return "xml"
    return ""
HEADING_LEVEL = {"h1": "#", "h2": "##", "h3": "###", "h4": "####", "h5": "#####", "h6": "######"}


BLOCK_TAGS = {
    "p", "div", "section", "article", "main", "aside", "header", "footer",
    "ul", "ol", "li", "table", "pre", "figure", "blockquote", "details",
    "h1", "h2", "h3", "h4", "h5", "h6", "hr", "dl",
}


def render_block_children(parent: Tag) -> str:
    """Render children, coalescing runs of inline-level nodes into single paragraphs."""
    blocks = []
    inline_buf = []  # accumulates inline nodes between block elements

    def flush():
        if inline_buf:
            text = "".join(inline_buf).strip()
            text = re.sub(r"[ \t]+", " ", text)
            if text:
                blocks.append(text)
            inline_buf.clear()

    for child in parent.children:
        if isinstance(child, Comment):
            continue
        if isinstance(child, NavigableString):
            inline_buf.append(str(child))
            continue
        if not isinstance(child, Tag):
            continue
        name = child.name.lower()
        cls = set(child.get("class", []))
        is_block = (
            name in BLOCK_TAGS
            or bool(cls & {"callout", "gloss", "analogy", "card", "split-item",
                            "diagram", "diag-grid", "table-wrap", "flow-row", "bm-box",
                            "codeblock", "code-label"})
        )
        if is_block:
            flush()
            rendered = render_block(child)
            if rendered and rendered.strip():
                blocks.append(rendered)
        else:
            # skip decorative eyebrow labels even when they are inline spans
            if cls & {"kicker"}:
                continue
            # inline-level tag (b, em, code, a, span, small, kbd, sup, sub, ...)
            inline_buf.append(render_inline_tag(child))
    flush()
    return "\n\n".join(b for b in blocks if b.strip())


def render_inline_tag(el: Tag) -> str:
    """Render a single inline tag (with its children) to inline Markdown."""
    name = el.name.lower()
    inner = render_inline(el)
    if name in ("strong", "b"):
        inner = inner.strip()
        return f"**{inner}**" if inner else ""
    if name in ("em", "i"):
        inner = inner.strip()
        return f"*{inner}*" if inner else ""
    if name in ("code", "kbd"):
        inner = inner.strip()
        return f"`{inner}`" if inner else ""
    if name == "a":
        href = el.get("href", "").strip()
        label = inner.strip() or href
        if href and not href.startswith("#"):
            return f"[{label}]({href})"
        return label
    if name == "br":
        return "  \n"
    return inner


def render_block(el: Tag) -> str:
    name = el.name.lower()
    cls = set(el.get("class", []))

    if cls & SKIP_CLASSES:
        return ""

    if name in HEADING_LEVEL:
        txt = render_inline(el).strip()
        return f"{HEADING_LEVEL[name]} {txt}" if txt else ""

    if name == "figure" or "diagram" in cls or "diag-grid" in cls or el.find("div", class_="flow-row") or el.find("div", class_="bm-box"):
        # treat as a diagram if it contains diagram structures
        if name == "figure" or (cls & {"diagram"}) or el.find(class_=re.compile(r"flow-row|diag-grid|bm-box")):
            mm, caption = convert_diagram(el)
            parts = []
            if caption:
                parts.append(f"**Diagram: {caption}**")
            if mm:
                parts.append("```mermaid\n" + mm + "\n```")
            else:
                parts.append(diagram_text_fallback(el))
            return "\n\n".join(parts)

    if name == "table" or "datatable" in cls:
        tbl = el if name == "table" else el.find("table")
        if tbl:
            return table_to_markdown(tbl)

    if name in ("ul", "ol"):
        return list_to_markdown(el)

    if name == "pre" or "codeblock" in cls:
        code = el.find("code") or el
        text = code.get_text()  # preserves newlines and inline comment spans
        text = text.replace("\xa0", " ").rstrip("\n")
        lang = _guess_lang(text)
        return f"```{lang}\n{text}\n```"

    # caption line above a code block
    if "code-label" in cls:
        txt = render_inline(el).strip()
        return txt

    if "callout" in cls:
        return callout_to_markdown(el)

    # Glossary entry: <div class="gloss"><dt>term</dt><dd>def</dd></div>
    if "gloss" in cls:
        dt = el.find("dt")
        dd = el.find("dd")
        term = render_inline(dt).strip() if dt else ""
        definition = render_inline(dd).strip() if dd else ""
        if term and definition:
            return f"- **{term}** — {definition}"
        return f"- **{term}**" if term else definition

    # Analogy box: icon + title + body — render like a tip callout
    if "analogy" in cls:
        title_el = el.find(class_="analogy-title")
        title = _clean(title_el.get_text(" ")) if title_el else ""
        if title_el:
            title_el.extract()
        for ic in el.find_all(class_=re.compile(r"analogy-icon")):
            ic.decompose()
        body = render_block_children(el).strip()
        lines = []
        if title:
            lines.append(f"> **{title}**")
        for bl in body.split("\n"):
            lines.append(f"> {bl}" if bl else ">")
        return "\n".join(lines)

    # Card: numbered concept card — drop the decorative number, keep heading + body
    if "card" in cls and "cards" not in cls:
        for num in el.find_all(class_=re.compile(r"card-num")):
            num.decompose()
        return render_block_children(el)

    # Split item: a tag/label span followed by a paragraph
    if "split-item" in cls:
        tag = el.find(class_=re.compile(r"\btag\b"))
        label = _clean(tag.get_text(" ")) if tag else ""
        if tag:
            tag.extract()
        body = render_block_children(el).strip()
        if label and body:
            return f"**{label}** — {body}"
        return body or (f"**{label}**" if label else "")

    if "table-wrap" in cls:
        return render_block_children(el)

    if name == "blockquote":
        body = render_block_children(el)
        return "\n".join(f"> {l}" for l in body.split("\n"))

    if name in ("p",) or "prose" in cls or "panel-intro" in cls or "subhead" in cls:
        txt = render_inline(el).strip()
        if "subhead" in cls and txt:
            return f"**{txt}**"
        return txt

    # generic container — recurse
    if name in ("div", "section", "article", "main", "aside", "details"):
        return render_block_children(el)

    # fallback: inline text
    txt = render_inline(el).strip()
    return txt


# ---------------------------------------------------------------------------
# Top-level page conversion
# ---------------------------------------------------------------------------

def convert_page(html: str) -> tuple[str, str]:
    """Return (title, markdown) for a page's content area (excludes nav/search/footer)."""
    soup = BeautifulSoup(html, "lxml")

    # Title: <h1> in content, fall back to <title>
    h1 = soup.find("h1")
    title = _clean(h1.get_text(" ")) if h1 else ""
    if not title and soup.title:
        title = _clean(soup.title.get_text()).replace(" — JFrog Learn", "")

    # Locate the main content container; the site uses <main> for page body.
    content = soup.find("main") or soup.find("article") or soup.body

    # Remove non-content chrome
    for sel in ["nav", "aside", "header", "footer", "script", "style", "form"]:
        for t in content.find_all(sel):
            t.decompose()
    for t in content.find_all(class_=re.compile(r"sidebar|search|tab-bar|theme-toggle|page-nav|breadcrumb|pagenav|prevnext")):
        t.decompose()

    md = render_block_children(content)

    # tidy: collapse 3+ blank lines, strip trailing spaces
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    md = "\n".join(line.rstrip() for line in md.split("\n"))
    return title or "Untitled", md


def main():
    if len(sys.argv) < 2:
        print("usage: html_to_markdown.py <page.html> [out.md]", file=sys.stderr)
        sys.exit(1)
    src = Path(sys.argv[1])
    title, md = convert_page(src.read_text(encoding="utf-8"))
    doc = f"# {title}\n\n{md}\n"
    if len(sys.argv) >= 3:
        Path(sys.argv[2]).write_text(doc, encoding="utf-8")
        print(f"wrote {sys.argv[2]} (title={title!r}, {len(doc)} chars)", file=sys.stderr)
    else:
        print(doc)


if __name__ == "__main__":
    main()
