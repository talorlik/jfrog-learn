/* ============================================================
   JFrog Learn - shared app script (multi-page)
   - injects sidebar + brand + search trigger
   - theme toggle, mobile nav, tabs, in-page scrollspy
   - command-palette style search over search-index.json
   ============================================================ */

/* Resolve a path relative to site root regardless of page depth.
   Pages in /pages/ set window.__BASE = '../'; home leaves it ''. */
const BASE = (typeof window.__BASE === 'string') ? window.__BASE : '';
const HERE = location.pathname.split('/').pop() || 'index.html';

/* ---- Navigation model (single source of truth) ---- */
const NAV = [
  { group: 'Overview', links: [
    { href: 'index.html', label: 'Home', root: true },
  ]},
  { group: 'Core concepts', links: [
    { href: 'pages/fundamentals.html', label: 'Fundamentals' },
    { href: 'pages/replication-federation.html', label: 'Replication & Federation' },
    { href: 'pages/build-promotion.html', label: 'Build promotion' },
  ]},
  { group: 'Distribution', links: [
    { href: 'pages/release-bundles.html', label: 'Release Bundles & Distribution' },
  ]},
  { group: 'Automation & security', links: [
    { href: 'pages/xray-policies-watches.html', label: 'Xray Policies & Watches' },
    { href: 'pages/rest-api.html', label: 'Artifactory REST API' },
    { href: 'pages/frogbot.html', label: 'Frogbot & IDE' },
    { href: 'pages/pipelines.html', label: 'JFrog Pipelines' },
    { href: 'pages/access-tokens.html', label: 'Access tokens & permissions' },
  ]},
  { group: 'Platform ops', links: [
    { href: 'pages/kubernetes-helm.html', label: 'Kubernetes / Helm setup' },
  ]},
];

const BRAND_SVG = '<svg width="30" height="30" viewBox="0 0 32 32" fill="none"><rect width="32" height="32" rx="7" fill="#43c75a"/><rect x="8" y="8" width="16" height="5" rx="1.4" fill="#0d100e"/><rect x="8" y="15" width="16" height="5" rx="1.4" fill="#0d100e" opacity="0.65"/><rect x="8" y="22" width="16" height="2.6" rx="1.1" fill="#0d100e" opacity="0.35"/></svg>';

/* Is link the current page? */
function isCurrent(href) {
  const file = href.split('/').pop();
  return file === HERE;
}

/* ---- Build sidebar ---- */
function buildSidebar() {
  const sb = document.getElementById('sidebar');
  if (!sb) return;

  let html = '';
  // brand
  html += `<a class="brand" href="${BASE}index.html" aria-label="JFrog Learn home">
    <span class="brand-mark" aria-hidden="true">${BRAND_SVG}</span>
    <span class="brand-text">JFrog <span class="brand-sub">Learn</span></span>
  </a>`;

  // search trigger
  html += `<button class="search-trigger" id="searchTrigger" aria-label="Search the knowledge base">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
    <span class="st-label">Search…</span><kbd>/</kbd>
  </button>`;

  // ask-the-docs (opens the NotebookLM notebook in a new tab)
  html += `<a class="ask-docs" href="https://notebooklm.google.com/notebook/754de000-7dd1-47ce-905a-9eb659951264/preview" target="_blank" rel="noopener noreferrer" aria-label="Ask the docs (opens NotebookLM in a new tab)">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.7"/><path d="M12 16.5h.01"/></svg>
    <span class="ask-docs-label">Ask the docs</span>
  </a>`;

  // nav groups
  html += '<nav class="nav" aria-label="Knowledge base navigation">';
  for (const g of NAV) {
    html += `<p class="nav-group">${g.group}</p>`;
    for (const l of g.links) {
      const cur = isCurrent(l.href);
      html += `<a href="${BASE}${l.href}" class="nav-link${cur ? ' current' : ''}"${cur ? ' aria-current="page"' : ''}>${l.label}</a>`;
    }
  }
  html += '</nav>';

  // in-page anchors (only when the page declares them)
  const onThis = document.getElementById('onThisPage');
  sb.innerHTML = html;
  if (onThis) sb.appendChild(onThis);
}

/* ---- Safe storage (degrades gracefully where storage is blocked, e.g. sandboxed iframes) ---- */
const safeStore = {
  get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* no-op */ } },
};

/* ---- Theme toggle ---- */
function initTheme() {
  const t = document.querySelector('[data-theme-toggle]');
  const r = document.documentElement;
  const saved = safeStore.get('jf-theme');
  let d = saved || (matchMedia('(prefers-color-scheme:dark)').matches ? 'dark' : 'light');
  r.setAttribute('data-theme', d);
  if (!t) return;
  const sun = '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>';
  const moon = '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  const render = () => {
    t.setAttribute('aria-label', 'Switch to ' + (d === 'dark' ? 'light' : 'dark') + ' mode');
    t.innerHTML = d === 'dark' ? sun : moon;
  };
  render();
  t.addEventListener('click', () => {
    d = d === 'dark' ? 'light' : 'dark';
    r.setAttribute('data-theme', d);
    safeStore.set('jf-theme', d);
    render();
  });
}

/* ---- Mobile sidebar ---- */
function initMobileNav() {
  const sb = document.getElementById('sidebar');
  const btn = document.getElementById('menuBtn');
  const scrim = document.getElementById('scrim');
  if (!sb || !btn || !scrim) return;
  const close = () => { sb.classList.remove('open'); scrim.classList.remove('show'); };
  btn.addEventListener('click', () => { sb.classList.toggle('open'); scrim.classList.toggle('show'); });
  scrim.addEventListener('click', close);
  sb.addEventListener('click', (e) => {
    if (e.target.closest('.nav-link') && innerWidth <= 980) close();
  });
}

/* ---- Tabs (labs) ---- */
function initTabs() {
  const tabs = document.querySelectorAll('.tab');
  const panels = document.querySelectorAll('.tab-panel');
  if (!tabs.length) return;
  tabs.forEach(tab => tab.addEventListener('click', () => {
    const id = tab.dataset.tab;
    tabs.forEach(t => { t.classList.toggle('active', t === tab); t.setAttribute('aria-selected', t === tab); });
    panels.forEach(p => p.classList.toggle('active', p.dataset.panel === id));
  }));
}

/* ---- In-page scrollspy (uses #onThisPage anchors) ---- */
function initScrollspy() {
  const links = [...document.querySelectorAll('#onThisPage .nav-link')];
  if (!links.length) return;
  const map = new Map(links.map(l => [l.getAttribute('href').slice(1), l]));
  const sections = [...map.keys()].map(id => document.getElementById(id)).filter(Boolean);
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        links.forEach(l => l.classList.remove('active'));
        const link = map.get(e.target.id);
        if (link) link.classList.add('active');
      }
    });
  }, { rootMargin: '-15% 0px -75% 0px', threshold: 0 });
  sections.forEach(s => obs.observe(s));
}

/* ---- Search (command palette) ---- */
let SEARCH_DATA = null;   // array of page/section entries (meta filtered out)
let SEARCH_META = null;   // { related, chain, labels, groups }
let searchLoading = false;
let searchLoadPromise = null;

/* Fetch + split the index once; shared by the overlay and the results page. */
function fetchIndex() {
  if (searchLoadPromise) return searchLoadPromise;
  searchLoadPromise = fetch(`${BASE}search-index.json`)
    .then(r => r.json())
    .then(all => {
      SEARCH_META = all.find(e => e && e.kind === 'meta') || {};
      SEARCH_DATA = all.filter(e => e && e.kind !== 'meta');
    })
    .catch(() => { SEARCH_META = {}; SEARCH_DATA = []; });
  return searchLoadPromise;
}

/* Shared scoring used by both overlay and results page. */
function termsOf(q) {
  return q.toLowerCase().split(/\s+/).filter(Boolean)
    // drop tiny stop-words so "how to create a token" focuses on real terms
    .filter(t => !['a', 'an', 'the', 'to', 'of', 'is', 'do', 'i', 'my'].includes(t));
}
/* Words that should never, on their own, qualify a result. They carry
   intent (how-to boosting) but no topical meaning. */
const INTENT_WORDS = new Set(['how', 'set', 'setup', 'set-up', 'create', 'creating',
  'install', 'installing', 'configure', 'configuring', 'use', 'using', 'make',
  'get', 'add', 'enable', 'run', 'running', 'with', 'via', 'for', 'and', 'or',
  'what', 'why', 'when', 'where', 'in', 'on', 'up']);

function scoreEntry(item, terms, q) {
  let s = 0;
  let contentHits = 0;        // real (non-intent) term matches
  const t = item._title || '', h = item._headings || '', b = item._body || '';
  terms.forEach(term => {
    const intent = INTENT_WORDS.has(term);
    let hit = false;
    if (t.includes(term)) { s += 12; hit = true; }
    if (h.includes(term)) { s += 5; hit = true; }
    const m = b.split(term).length - 1;
    if (m > 0) { s += Math.min(m, 6); hit = true; }
    if (hit && !intent) contentHits += 1;
  });
  // An entry must match at least one MEANINGFUL term. This stops every
  // page matching "how to ..." just because they all contain how-to text.
  const meaningful = terms.filter(x => !INTENT_WORDS.has(x));
  if (meaningful.length && contentHits === 0) return 0;
  // exact phrase in title is a strong signal
  if (q && t.includes(q.toLowerCase().trim())) s += 8;
  // how-to intent: boost how-to sections when the query asks how
  const wantsHow = /\b(how|set ?up|setup|create|install|configure|promote|generate|run|wire)\b/i.test(q || '');
  if (wantsHow && item.howto) s += 7;
  // section entries are more useful than page summaries when both match
  if (item.kind === 'section') s += 1;
  return s;
}

function initSearch() {
  const overlay = document.getElementById('searchOverlay');
  if (!overlay) return;
  const input = document.getElementById('searchInput');
  const results = document.getElementById('searchResults');
  let activeIdx = -1;
  let current = [];

  const open = () => {
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    input.value = '';
    render([]);
    setTimeout(() => input.focus(), 30);
    loadIndex();
  };
  const close = () => {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  };

  async function loadIndex() {
    await fetchIndex();
    if (input.value.trim()) run(input.value);
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  }
  function highlight(text, terms) {
    let out = escapeHtml(text);
    terms.forEach(t => {
      if (!t) return;
      const re = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig');
      out = out.replace(re, '<mark>$1</mark>');
    });
    return out;
  }



  function snippet(body, terms) {
    const lower = body.toLowerCase();
    let pos = -1;
    for (const term of terms) { const p = lower.indexOf(term); if (p >= 0) { pos = p; break; } }
    if (pos < 0) return body.slice(0, 160);
    const start = Math.max(0, pos - 60);
    return (start > 0 ? '…' : '') + body.slice(start, start + 200);
  }

  function run(q) {
    const terms = termsOf(q);
    if (!terms.length || !SEARCH_DATA) { render([]); return; }
    current = SEARCH_DATA
      .map(it => ({ it, sc: scoreEntry(it, terms, q) }))
      .filter(x => x.sc > 0)
      .sort((a, b) => b.sc - a.sc)
      .slice(0, 8)
      .map(x => x.it);
    activeIdx = current.length ? 0 : -1;
    render(current, terms);
  }

  function gotoAll() {
    const q = input.value.trim();
    if (!q) return;
    location.href = `${BASE}pages/search.html?q=${encodeURIComponent(q)}`;
  }

  function render(items, terms = []) {
    if (!input.value.trim()) {
      results.innerHTML = '<div class="search-empty">Type to search across every page - concepts, commands, and CLI.</div>';
      return;
    }
    if (!items.length) {
      results.innerHTML = `<div class="search-empty">No matches${SEARCH_DATA ? '' : ' - loading index…'}.</div>`;
      return;
    }
    const list = items.map((it, i) => {
      const href = `${BASE}${it.url}${it.anchor || ''}`;
      const crumb = it.kind === 'section'
        ? `${escapeHtml(it.page)} ›` : escapeHtml(it.page);
      const tag = it.howto ? '<span class="sr-howto">How-to</span>' : '';
      return `
      <a class="sr-item${i === activeIdx ? ' active' : ''}" href="${href}" data-i="${i}">
        <span class="sr-page">${crumb} ${tag}</span>
        <div class="sr-title">${highlight(it.title, terms)}</div>
        <div class="sr-snippet">${highlight(snippet(it.body, terms), terms)}</div>
      </a>`;
    }).join('');
    results.innerHTML = list +
      `<button class="sr-all" id="srAll">See all results for “${escapeHtml(input.value.trim())}” on one page →</button>`;
    const allBtn = document.getElementById('srAll');
    if (allBtn) allBtn.addEventListener('click', gotoAll);
  }

  input.addEventListener('input', () => run(input.value));
  input.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown') { e.preventDefault(); if (current.length) { activeIdx = (activeIdx + 1) % current.length; render(current, input.value.toLowerCase().split(/\s+/).filter(Boolean)); scrollActive(); } }
    else if (e.key === 'ArrowUp') { e.preventDefault(); if (current.length) { activeIdx = (activeIdx - 1 + current.length) % current.length; render(current, input.value.toLowerCase().split(/\s+/).filter(Boolean)); scrollActive(); } }
    else if (e.key === 'Enter') {
      // plain Enter -> consolidated results page; Enter on a highlighted
      // item with a modifier jumps straight to that section.
      if ((e.metaKey || e.ctrlKey) && activeIdx >= 0 && current[activeIdx]) {
        location.href = `${BASE}${current[activeIdx].url}${current[activeIdx].anchor || ''}`;
      } else {
        gotoAll();
      }
    }
    else if (e.key === 'Escape') { close(); }
  });
  function scrollActive() {
    const el = results.querySelector('.sr-item.active');
    if (el) el.scrollIntoView({ block: 'nearest' });
  }

  overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });

  // open triggers
  document.addEventListener('click', (e) => { if (e.target.closest('#searchTrigger')) open(); });
  document.addEventListener('keydown', (e) => {
    const typing = /^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName);
    if (e.key === '/' && !typing && !overlay.classList.contains('open')) { e.preventDefault(); open(); }
    if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) { e.preventDefault(); open(); }
    if (e.key === 'Escape' && overlay.classList.contains('open')) close();
  });
}


/* ============================================================
   Consolidated results page (pages/search.html)
   Reads ?q=, scores the index, groups hits by page, prioritizes
   how-to sections, deep-links into anchors, and builds a
   "related information" rail (sibling sections + cross-page
   topics + prev/next path) so the user never has to re-search.
   ============================================================ */
function escHtml(s) {
  return (s || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}
function hl(text, terms) {
  let out = escHtml(text);
  terms.forEach(t => {
    if (!t) return;
    const re = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig');
    out = out.replace(re, '<mark>$1</mark>');
  });
  return out;
}
function snip(body, terms, len) {
  len = len || 220;
  const lower = (body || '').toLowerCase();
  let pos = -1;
  for (const t of terms) { const p = lower.indexOf(t); if (p >= 0) { pos = p; break; } }
  if (pos < 0) return (body || '').slice(0, len);
  const start = Math.max(0, pos - 70);
  return (start > 0 ? '\u2026' : '') + body.slice(start, start + len) + (start + len < body.length ? '\u2026' : '');
}

async function initSearchPage() {
  const root = document.getElementById('searchPageResults');
  if (!root) return; // not the search page
  const form = document.getElementById('searchPageForm');
  const input = document.getElementById('searchPageInput');
  const meta = document.getElementById('searchPageMeta');
  const relatedEl = document.getElementById('searchPageRelated');

  const params = new URLSearchParams(location.search);
  const q0 = (params.get('q') || '').trim();
  input.value = q0;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const q = input.value.trim();
    const u = new URL(location.href);
    if (q) u.searchParams.set('q', q); else u.searchParams.delete('q');
    history.replaceState(null, '', u);
    runPage(q);
  });

  await fetchIndex();
  runPage(q0);
  if (!q0) setTimeout(() => input.focus(), 50);

  function runPage(q) {
    document.title = (q ? '\u201c' + q + '\u201d - Search' : 'Search') + ' - JFrog Learn';
    if (!q) {
      meta.textContent = 'Type a question above - for example, \u201chow to create a token\u201d.';
      root.innerHTML = '<div class="search-empty-lg">Search across every page. Results land here, grouped by topic, with deep links to the exact section.</div>';
      relatedEl.innerHTML = '';
      return;
    }
    const terms = termsOf(q);
    const scored = SEARCH_DATA
      .map(it => ({ it, sc: scoreEntry(it, terms, q) }))
      .filter(x => x.sc > 0)
      .sort((a, b) => b.sc - a.sc);

    if (!scored.length) {
      meta.textContent = 'No matches for \u201c' + q + '\u201d.';
      root.innerHTML = '<div class="search-empty-lg">Nothing matched <b>' + escHtml(q) + '</b>. Try fewer or simpler words, or browse the topics in the sidebar.</div>';
      relatedEl.innerHTML = '';
      return;
    }

    const groups = new Map();
    for (const { it, sc } of scored) {
      let g = groups.get(it.url);
      if (!g) {
        g = { url: it.url, page: it.page, group: it.group, pageTitle: it.pageTitle, best: 0, sections: [], pageEntry: null };
        groups.set(it.url, g);
      }
      g.best = Math.max(g.best, sc);
      if (it.kind === 'section') g.sections.push({ it, sc });
      else g.pageEntry = it;
    }
    const ordered = [...groups.values()].sort((a, b) => b.best - a.best);

    const hitCount = scored.filter(x => x.it.kind === 'section').length;
    meta.innerHTML = '<b>' + hitCount + '</b> matching section' + (hitCount === 1 ? '' : 's') +
      ' across <b>' + ordered.length + '</b> topic' + (ordered.length === 1 ? '' : 's') +
      ' for \u201c' + escHtml(q) + '\u201d.';

    root.innerHTML = ordered.map(g => {
      const secs = g.sections.sort((a, b) => (b.it.howto - a.it.howto) || (b.sc - a.sc)).slice(0, 6);
      const rows = secs.map(({ it }) => {
        const href = BASE + it.url + (it.anchor || '');
        const tag = it.howto ? '<span class="rg-howto">How-to</span>' : '';
        return '<a class="rg-sec" href="' + href + '">' +
          '<div class="rg-sec-head"><span class="rg-sec-title">' + hl(it.title, terms) + '</span>' + tag + '</div>' +
          '<p class="rg-sec-snip">' + hl(snip(it.body, terms), terms) + '</p></a>';
      }).join('');
      const pageHref = BASE + g.url;
      const fallback = '<a class="rg-sec" href="' + pageHref + '"><div class="rg-sec-head"><span class="rg-sec-title">' + escHtml(g.pageTitle) + '</span></div></a>';
      return '<section class="result-group">' +
        '<header class="rg-head"><div>' +
        '<span class="rg-group-label">' + escHtml(g.group || '') + '</span>' +
        '<h2 class="rg-title"><a href="' + pageHref + '">' + escHtml(g.pageTitle || g.page) + '</a></h2>' +
        '</div><a class="rg-open" href="' + pageHref + '">Open topic \u2192</a></header>' +
        '<div class="rg-secs">' + (rows || fallback) + '</div></section>';
    }).join('');

    buildRelated(ordered, terms);
  }

  function buildRelated(ordered, terms) {
    if (!ordered.length) { relatedEl.innerHTML = ''; return; }
    const top = ordered[0];
    const topFile = top.url.split('/').pop();
    const labels = SEARCH_META.labels || {};
    const related = (SEARCH_META.related || {})[topFile] || [];
    const chain = (SEARCH_META.chain || {})[topFile];

    let html = '<h2 class="related-h">Related information</h2>';

    const matchedAnchors = new Set(top.sections.map(s => s.it.anchor));
    const siblings = SEARCH_DATA.filter(e =>
      e.kind === 'section' && e.url === top.url && !matchedAnchors.has(e.anchor));
    if (siblings.length) {
      html += '<div class="related-block"><p class="related-cap">More in ' + escHtml(top.page) + '</p>';
      html += siblings.slice(0, 6).map(e =>
        '<a class="related-link" href="' + BASE + e.url + e.anchor + '">' +
        (e.howto ? '<span class="rl-dot rl-how"></span>' : '<span class="rl-dot"></span>') +
        escHtml(e.title) + '</a>').join('');
      html += '</div>';
    }

    if (related.length) {
      html += '<div class="related-block"><p class="related-cap">Related topics</p>';
      html += related.map(f =>
        '<a class="related-link related-topic" href="' + BASE + 'pages/' + f + '">' +
        '<span class="rl-arrow">\u2192</span>' + escHtml(labels[f] || f) + '</a>').join('');
      html += '</div>';
    }

    if (chain) {
      const linkFor = (arr) => {
        if (!arr) return '';
        const file = arr[0], dir = arr[1], title = arr[2];
        const href = file === '../index.html' ? (BASE + 'index.html') : (BASE + 'pages/' + file);
        return '<a class="related-link related-path" href="' + href + '"><span class="rl-dir">' + escHtml(dir) + '</span>' + escHtml(title) + '</a>';
      };
      html += '<div class="related-block"><p class="related-cap">Learning path</p>';
      html += linkFor(chain.prev) + linkFor(chain.next);
      html += '</div>';
    }

    relatedEl.innerHTML = html;
  }
}

/* ---- boot ---- */
document.addEventListener('DOMContentLoaded', () => {
  buildSidebar();
  initTheme();
  initMobileNav();
  initTabs();
  initScrollspy();
  initSearch();
  initSearchPage();
});
