# JFrog Learn Design System

Design reference for the JFrog Learn static site. All tokens and components
live in `assets/style.css`. This document mirrors that structure: shared
values in `:root`, then explicit **dark** and **light** theme palettes.

Implementation uses `data-theme="dark"` | `data-theme="light"` on
`<html>` (not `.dark` / `.light` classes). Dark is the default when no
attribute is set (`:root` and `[data-theme="dark"]` share the same tokens).

---

## Design principles

- **Bottom-up learning UX** - scannable hierarchy, diagrams, callouts, and
  labs on long-form topic pages.
- **Product semantics** - green for Artifactory, violet for Xray, amber for
  hands-on labs.
- **Readable prose** - muted body copy, strong headings, mono for labels and
  metadata.
- **Subtle depth** - panel surfaces, soft borders, light grid on the page
  background, hover lift on cards.
- **Theme-aware UI** - semantic CSS variables swap per theme; fenced code
  blocks stay dark in both themes for terminal-like readability.

---

## Theme mechanism

| Concern | Detail |
| ------- | ------ |
| Attribute | `document.documentElement.setAttribute('data-theme', 'dark' \| 'light')` |
| Persistence | `localStorage` key `jf-theme` |
| Fallback | `prefers-color-scheme: dark` when no saved preference |
| Toggle | Fixed `.theme-toggle` button (sun/moon icon) |
| Source | `assets/app.js` - `initTheme()` |

---

## `:root` (shared tokens)

These custom properties are theme-independent. Components should prefer
these over hard-coded values.

### Typography families

| Token | Stack | Role |
| ----- | ----- | ---- |
| `--font-display` | Space Grotesk, system-ui, sans-serif | Headings, titles, tags, pills |
| `--font-body` | Inter, system-ui, sans-serif | Body copy, UI labels |
| `--font-mono` | JetBrains Mono, ui-monospace, monospace | Eyebrows, kickers, code, metadata |

Google Fonts load (weights): Space Grotesk 400-700, Inter 400-600, JetBrains
Mono 400-600.

### Type scale (fluid clamp)

| Token | Range |
| ----- | ----- |
| `--text-xs` | 0.75rem - 0.85rem |
| `--text-sm` | 0.875rem - 0.95rem |
| `--text-base` | 1rem - 1.075rem |
| `--text-lg` | 1.15rem - 1.4rem |
| `--text-xl` | 1.5rem - 2.3rem |
| `--text-2xl` | 2.1rem - 3.6rem |

### Spacing

| Token | Value |
| ----- | ----- |
| `--space-1` | 0.25rem |
| `--space-2` | 0.5rem |
| `--space-3` | 0.75rem |
| `--space-4` | 1rem |
| `--space-5` | 1.25rem |
| `--space-6` | 1.5rem |
| `--space-8` | 2rem |
| `--space-10` | 2.5rem |
| `--space-12` | 3rem |
| `--space-16` | 4rem |
| `--space-20` | 5rem |
| `--space-24` | 6rem |

### Radius

| Token | Value |
| ----- | ----- |
| `--radius-sm` | 0.4rem |
| `--radius-md` | 0.6rem |
| `--radius-lg` | 0.9rem |
| `--radius-xl` | 1.3rem |
| `--radius-full` | 9999px |

### Layout and motion

| Token | Value | Use |
| ----- | ----- | --- |
| `--sidebar-w` | 268px | Fixed left navigation width |
| `--maxw` | 920px | Main content column max width |
| `--transition` | 200ms cubic-bezier(0.16, 1, 0.3, 1) | Hovers, borders, theme-adjacent UI |

### Base document styles (both themes)

- `line-height`: 1.65 on `body`
- Headings: `line-height` 1.12, `letter-spacing` -0.02em, `text-wrap: balance`
- Body background: `var(--bg)` plus 46px grid using `var(--grid-line)`
- Links default: `color: var(--primary)`; in-body links use underline with
  `color-mix` under primary
- Inline `code`: `var(--font-mono)`, `var(--panel-2)` background,
  `var(--border-soft)` border
- Focus: 2px `var(--primary)` outline, 3px offset
- `em` in prose: not italic - `color: var(--primary)`, `font-weight: 500`
- Reduced motion: animations and transitions collapse to near-zero

---

## Dark theme

Selector: `:root`, `[data-theme="dark"]`

Default for all pages (`<html data-theme="dark">` in templates).

### Surfaces and text

| Token | Hex | Role |
| ----- | --- | ---- |
| `--bg` | `#0d100e` | Page background |
| `--surface` | `#14181500` | Legacy/transparent surface |
| `--surface-1` | `#16191600` | Legacy/transparent surface |
| `--panel` | `#171c18` | Cards, sidebar, modals |
| `--panel-2` | `#1d231e` | Nested panels, table headers, hover rows |
| `--border` | `#2a3129` | Primary borders |
| `--border-soft` | `#222823` | Dividers, subtle borders |
| `--text` | `#dfe6df` | Primary text |
| `--text-muted` | `#93a094` | Body prose, secondary UI |
| `--text-faint` | `#5f6b60` | Labels, captions, placeholders |

### Brand accents

| Token | Hex | Product meaning |
| ----- | --- | --------------- |
| `--primary` | `#43c75a` | Artifactory / JFrog green |
| `--primary-soft` | `#1e2d20` | Green tinted backgrounds |
| `--primary-dim` | `#2c8c3c` | Muted green (reserved) |
| `--xray` | `#b66bff` | Xray violet |
| `--xray-soft` | `#2a1d3b` | Violet tinted backgrounds |
| `--lab` | `#ffb24d` | Hands-on labs amber |
| `--lab-soft` | `#33260f` | Amber tinted backgrounds |

### Severity (Xray)

| Token | Hex |
| ----- | --- |
| `--crit` | `#ff5a6e` |
| `--high` | `#ff8a3d` |
| `--med` | `#ffc24d` |
| `--low` | `#5fb0ff` |
| `--unk` | `#8b96a0` |

### Elevation and grid

| Token | Value |
| ----- | ----- |
| `--shadow` | `0 18px 48px rgba(0, 0, 0, 0.45)` |
| `--shadow-sm` | `0 4px 14px rgba(0, 0, 0, 0.3)` |
| `--grid-line` | `rgba(255, 255, 255, 0.03)` |

---

## Light theme

Selector: `[data-theme="light"]`

Overrides only the semantic color tokens below; all `:root` layout, type,
and radius tokens stay the same.

### Surfaces and text

| Token | Hex | Role |
| ----- | --- | ---- |
| `--bg` | `#f4f6f3` | Page background |
| `--panel` | `#ffffff` | Cards, sidebar, modals |
| `--panel-2` | `#eef2ee` | Nested panels, table headers |
| `--border` | `#dbe2db` | Primary borders |
| `--border-soft` | `#e6ebe6` | Dividers |
| `--text` | `#16201a` | Primary text |
| `--text-muted` | `#566057` | Body prose |
| `--text-faint` | `#9aa49b` | Labels, captions |

Note: light theme does not redefine `--surface` or `--surface-1`.

### Brand accents

| Token | Hex |
| ----- | --- |
| `--primary` | `#1f9d3a` |
| `--primary-soft` | `#dcf3e1` |
| `--primary-dim` | `#178a31` |
| `--xray` | `#8b3bd6` |
| `--xray-soft` | `#f0e4fb` |
| `--lab` | `#cc7a12` |
| `--lab-soft` | `#fbeed6` |

### Severity

| Token | Hex |
| ----- | --- |
| `--crit` | `#d62a45` |
| `--high` | `#c9591a` |
| `--med` | `#a87900` |
| `--low` | `#1f6fc9` |
| `--unk` | `#6a7480` |

### Elevation and grid

| Token | Value |
| ----- | ----- |
| `--shadow` | `0 18px 44px rgba(20, 40, 25, 0.1)` |
| `--shadow-sm` | `0 4px 14px rgba(20, 40, 25, 0.07)` |
| `--grid-line` | `rgba(0, 0, 0, 0.025)` |

---

## Theme-invariant colors

These literals do not change with light/dark UI theme.

### On-primary text

Dark green text on bright green buttons and badges:

| Literal | Use |
| ------- | --- |
| `#08120a` | `.btn-primary`, `.skip-link`, `.flow-step-n`, `.ask-docs:hover` |
| `#0d100e` | `.sev` labels, `.search-page-go` |

### Fenced code blocks (`.code`, `.codeblock`)

Terminal-style in **both** themes:

| Element | Dark theme | Light theme |
| ------- | ---------- | ----------- |
| Block background | `#0a0d0b` | `#10231a` |
| Code text | `#9fe6ad` | `#9fe6ad` |
| Comment (`.cm`) | `#6b8f73` | `#6b8f73` |
| Border | `var(--border)` | `var(--border)` |

### Overlays and scrims

| Element | Value |
| ------- | ----- |
| Mobile scrim (`.scrim`) | `rgba(0, 0, 0, 0.5)` |
| Search overlay | `rgba(0, 0, 0, 0.55)` + `backdrop-filter: blur(3px)` |

### Other fixed accents

| Literal | Use |
| ------- | --- |
| `#231600` | Active lab tab text (`.tab.active`) |
| `#fff` | Xray flow step number text |
| `rgba(67, 199, 90, 0.25)` | Brand mark drop shadow |
| `rgba(67, 199, 90, 0.32)` | Primary button hover glow |

### Brand mark (SVG)

| Part | Color |
| ---- | ----- |
| Rounded rect | `#43c75a` |
| Inner bars | `#0d100e` (opacity 1, 0.65, 0.35) |

---

## Semantic accent mapping

Use product-colored modifiers consistently across components.

| Modifier | CSS hook | Accent token |
| -------- | -------- | ------------ |
| Artifactory | `.kicker-art`, `.tag-art`, `.lvl-art`, `.hl`, `[data-accent="art"]` | `--primary` |
| Xray | `.kicker-x`, `.tag-xray`, `.lvl-xray`, `.hl-x`, `[data-accent="xray"]` | `--xray` |
| Labs | `.kicker-lab`, `.lvl-lab`, `[data-accent="lab"]` | `--lab` |
| API / info | `[data-accent="api"]` | `--low` |

Topic cards set `--accent` via `data-accent` and use `color-mix(in oklab, ...)`
for borders and icon backgrounds.

---

## Layout architecture

```
+-- sidebar (fixed, 268px) --+-- main (#main, margin-left: sidebar-w) --+
|  brand                      |  theme-toggle (fixed top-right)          |
|  search-trigger             |  page content (max-width: 920px)         |
|  ask-docs                   |  sections / diagrams / footer            |
|  nav groups + links         |                                          |
+-----------------------------+------------------------------------------+
```

| Region | Key classes | Notes |
| ------ | ----------- | ----- |
| Skip link | `.skip-link` | Visible on focus only |
| Sidebar | `.sidebar` | Frosted `color-mix` panel, blur 12px |
| Main | `#main` | Horizontal padding `clamp(1.2rem, 4vw, 4rem)` |
| Mobile | `.menu-btn`, `.scrim` | Sidebar slides in below 980px |

### Responsive breakpoints

| Max width | Behavior |
| --------- | -------- |
| 980px | Sidebar off-canvas; hamburger menu; reduced theme toggle size |
| 860px | Search results page: single column |
| 760px | Diagrams/flows stack vertically; split grids become 1 column |
| 640px | Page prev/next nav stacks |
| 560px | KV lists stack; search form tightens |

---

## Component catalog

All components consume theme tokens unless listed in
[Theme-invariant colors](#theme-invariant-colors).

### Navigation

| Class | Description |
| ----- | ----------- |
| `.nav-link` | Muted default; hover `panel-2`; active/current uses `primary-soft` + left border |
| `.nav-group` | Uppercase mono label, `text-faint` |
| `.search-trigger` | Sidebar search opener with `/` kbd hint |
| `.ask-docs` | NotebookLM CTA; hover flips to solid `primary` |

### Hero and page chrome

| Class | Description |
| ----- | ----------- |
| `.home-hero`, `.hero` | Large display heading, eyebrow, lede, CTAs |
| `.eyebrow` | Mono uppercase, `primary` |
| `.page-head` | Breadcrumb, title, badges, lede |
| `.breadcrumb` | Muted trail with `primary` hover |
| `.lvl` | Topic level pill (`lvl-art`, `lvl-xray`, `lvl-lab`) |

### Actions

| Class | Description |
| ----- | ----------- |
| `.btn-primary` | Filled `primary`, dark text `#08120a`, hover lift + green glow |
| `.btn-ghost` | Border `border`; hover `primary` border and text |

### Content blocks

| Class | Description |
| ----- | ----------- |
| `.section` | Top border `border-soft`, vertical rhythm |
| `.kicker` | Pill section label; product variants tint border/text |
| `.prose` | Muted long copy; `strong` uses `--text` |
| `.callout` | Panel + border; `.callout-tip` (green), `.callout-q` (blue/low) |
| `.analogy` | Gradient panel; `.analogy-x` uses xray soft gradient |
| `.muted` | Small faint helper text |

### Cards and grids

| Class | Description |
| ----- | ----------- |
| `.topic-card` | Home grid card with left accent bar on hover |
| `.card`, `.next-card` | Numbered/feature cards; hover lift |
| `.split-item` | Two-column compare panels |
| `.gloss` | Glossary `dt`/`dd` tiles |
| `.recap` | Gradient summary box (`primary-soft` + `xray-soft`) |

### Data display

| Class | Description |
| ----- | ----------- |
| `.datatable` | Full-width table in `.table-wrap` |
| `.pill-*` | Repo type badges (local, remote, virtual, fed) |
| `.sev-*` | Severity chips on dark text `#0d100e` |
| `.chip` | Filter/tag chips |
| `.kv-list` | Key/value permission rows |

### Diagrams (CSS-only, no image assets)

| Class | Description |
| ----- | ----------- |
| `.diagram`, `.flow`, `.bigmodel` | Bordered panel containers |
| `.diag-node`, `.bm-box` | Node boxes with semantic border colors |
| `.onion` | Nested Xray layer diagram |
| `.flow-step` | Numbered pipeline steps |
| `.pw-grid` | Policy vs watch side-by-side |

Diagram node semantics: `.node-local` (primary), `.node-remote` (med),
`.node-virtual` (low), `.node-dev` (xray), `.node-ext` (unk).

### Labs and tabs

| Class | Description |
| ----- | ----------- |
| `.tab` / `.tab.active` | Lab track switcher; active = solid `lab` |
| `.panel-intro` | Amber left-border intro |
| `.lab-steps` | Numbered steps with `.ls-n` badges |

### Search

| Class | Description |
| ----- | ----------- |
| `.search-overlay` | Command-palette modal |
| `.search-box` | Rounded panel with results list |
| `.sr-item` | Result row; `mark` highlight uses primary mix |
| `.search-page-form` | Full-page search with focus ring `primary-soft` |
| `.result-group` | Grouped results on `pages/search.html` |

### Footer and page nav

| Class | Description |
| ----- | ----------- |
| `.footer` | Faint small print |
| `.page-nav` | Prev/next cards at bottom of topic pages |

---

## Accessibility

- Skip link to `#main`
- `aria-label` on theme toggle, menu, search triggers
- `aria-current="page"` on active nav link
- `:focus-visible` ring on interactive elements
- `prefers-reduced-motion: reduce` disables animations
- Search modal keyboard navigation (implemented in `app.js`)

---

## Related artifacts

| Artifact | Scope |
| -------- | ----- |
| `assets/style.css` | Source of truth for all site styling |
| `assets/app.js` | Theme toggle, sidebar, search behavior |
| `automation/build_docx.py` | Google Docs mirror uses separate inline-code and callout colors (see `AGENTS.md` section 6) |

When changing the public design, update `assets/style.css` first, then keep
this document in sync.
