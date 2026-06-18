/* ============================================================
   JFrog Learn — shared app script (multi-page)
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
let SEARCH_DATA = null;
let searchLoading = false;

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
    if (SEARCH_DATA || searchLoading) return;
    searchLoading = true;
    try {
      const res = await fetch(`${BASE}search-index.json`);
      SEARCH_DATA = await res.json();
    } catch (e) {
      SEARCH_DATA = [];
    }
    searchLoading = false;
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

  function score(item, terms) {
    let s = 0;
    const t = item._title, h = item._headings, b = item._body;
    terms.forEach(term => {
      if (t.includes(term)) s += 10;
      if (h.includes(term)) s += 5;
      const m = b.split(term).length - 1;
      s += Math.min(m, 6);
    });
    return s;
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
    const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length || !SEARCH_DATA) { render([]); return; }
    current = SEARCH_DATA
      .map(it => ({ it, sc: score(it, terms) }))
      .filter(x => x.sc > 0)
      .sort((a, b) => b.sc - a.sc)
      .slice(0, 12)
      .map(x => x.it);
    activeIdx = current.length ? 0 : -1;
    render(current, terms);
  }

  function render(items, terms = []) {
    if (!input.value.trim()) {
      results.innerHTML = '<div class="search-empty">Type to search across every page — concepts, commands, and CLI.</div>';
      return;
    }
    if (!items.length) {
      results.innerHTML = `<div class="search-empty">No matches${SEARCH_DATA ? '' : ' — loading index…'}.</div>`;
      return;
    }
    results.innerHTML = items.map((it, i) => `
      <a class="sr-item${i === activeIdx ? ' active' : ''}" href="${BASE}${it.url}" data-i="${i}">
        <span class="sr-page">${escapeHtml(it.page)}</span>
        <div class="sr-title">${highlight(it.title, terms)}</div>
        <div class="sr-snippet">${highlight(snippet(it.body, terms), terms)}</div>
      </a>`).join('');
  }

  input.addEventListener('input', () => run(input.value));
  input.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown') { e.preventDefault(); if (current.length) { activeIdx = (activeIdx + 1) % current.length; render(current, input.value.toLowerCase().split(/\s+/).filter(Boolean)); scrollActive(); } }
    else if (e.key === 'ArrowUp') { e.preventDefault(); if (current.length) { activeIdx = (activeIdx - 1 + current.length) % current.length; render(current, input.value.toLowerCase().split(/\s+/).filter(Boolean)); scrollActive(); } }
    else if (e.key === 'Enter') { if (activeIdx >= 0 && current[activeIdx]) location.href = `${BASE}${current[activeIdx].url}`; }
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

/* ---- boot ---- */
document.addEventListener('DOMContentLoaded', () => {
  buildSidebar();
  initTheme();
  initMobileNav();
  initTabs();
  initScrollspy();
  initSearch();
});
