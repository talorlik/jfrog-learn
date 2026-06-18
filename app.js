// Theme toggle
(function () {
  const t = document.querySelector('[data-theme-toggle]'), r = document.documentElement;
  let d = matchMedia('(prefers-color-scheme:dark)').matches ? 'dark' : 'light';
  r.setAttribute('data-theme', d);
  const render = () => {
    t.setAttribute('aria-label', 'Switch to ' + (d === 'dark' ? 'light' : 'dark') + ' mode');
    t.innerHTML = d === 'dark'
      ? '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
      : '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  };
  render();
  t.addEventListener('click', () => { d = d === 'dark' ? 'light' : 'dark'; r.setAttribute('data-theme', d); render(); });
})();

// Mobile sidebar
(function () {
  const sb = document.getElementById('sidebar'), btn = document.getElementById('menuBtn'), scrim = document.getElementById('scrim');
  const close = () => { sb.classList.remove('open'); scrim.classList.remove('show'); };
  btn.addEventListener('click', () => { sb.classList.toggle('open'); scrim.classList.toggle('show'); });
  scrim.addEventListener('click', close);
  sb.querySelectorAll('.nav-link').forEach(l => l.addEventListener('click', () => { if (innerWidth <= 980) close(); }));
})();

// Tabs
(function () {
  const tabs = document.querySelectorAll('.tab'), panels = document.querySelectorAll('.tab-panel');
  tabs.forEach(tab => tab.addEventListener('click', () => {
    const id = tab.dataset.tab;
    tabs.forEach(t => { t.classList.toggle('active', t === tab); t.setAttribute('aria-selected', t === tab); });
    panels.forEach(p => p.classList.toggle('active', p.dataset.panel === id));
  }));
})();

// Scrollspy
(function () {
  const links = [...document.querySelectorAll('.nav-link')];
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
})();
