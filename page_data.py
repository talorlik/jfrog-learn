# -*- coding: utf-8 -*-
"""Content bodies for each topic page. Imported by build_pages.py."""

# ---- prev/next chain (matches sidebar order) ----
NAV_ORDER = [
    ("fundamentals.html", "Fundamentals"),
    ("replication-federation.html", "Replication & Federation"),
    ("build-promotion.html", "Build promotion"),
    ("release-bundles.html", "Release Bundles & Distribution"),
    ("xray-policies-watches.html", "Xray Policies & Watches"),
    ("rest-api.html", "Artifactory REST API"),
    ("frogbot.html", "Frogbot & IDE"),
    ("pipelines.html", "JFrog Pipelines"),
    ("access-tokens.html", "Access tokens & permissions"),
    ("kubernetes-helm.html", "Kubernetes / Helm setup"),
]

def chain(file):
    idx = [i for i, (f, _) in enumerate(NAV_ORDER) if f == file][0]
    if idx == 0:
        prev = ("../index.html", "Back to", "Home")
    else:
        pf, pt = NAV_ORDER[idx - 1]
        prev = (pf, "Previous", pt)
    if idx == len(NAV_ORDER) - 1:
        nxt = ("../index.html", "Back to", "Home")
    else:
        nf, nt = NAV_ORDER[idx + 1]
        nxt = (nf, "Next", nt)
    return prev, nxt


PAGE_LIST = []

# =====================================================================
# 1) FUNDAMENTALS (migrated from the former static page)
# =====================================================================
_p = {
 "file": "fundamentals.html",
 "title": 'Fundamentals',
 "desc": 'JFrog Artifactory & Xray from first principles: the problem they solve, core vocabulary, the 4 repository types, deep recursive scanning, policies & watches, and three hands-on lab tracks.',
 "badges": '<span class="lvl lvl-art">Artifactory</span><span class="lvl lvl-xray">Xray</span><span class="lvl">Beginner → core</span>',
 "h1": 'Artifactory &amp; Xray from first principles',
 "lede": "Two products, one job: control every <em>binary</em> your software is built from, and prove it's safe. This page builds the whole picture from the bottom up - plain-language concepts, diagrams, comparison tables, then real hands-on labs.",
 "sections": [
    {"id": "problem", "label": "The problem it solves"},
    {"id": "glossary", "label": "Vocabulary first"},
    {"id": "artifactory", "label": "What Artifactory is"},
    {"id": "repos", "label": "The 4 repository types"},
    {"id": "architecture", "label": "How it fits together"},
    {"id": "packages", "label": "Package types"},
    {"id": "xray", "label": "What Xray is"},
    {"id": "xray-how", "label": "How scanning works"},
    {"id": "policies", "label": "Policies & Watches"},
    {"id": "labs", "label": "Choose your track"},
    {"id": "cli", "label": "CLI cheat sheet"},
    {"id": "mental-model", "label": "Full mental model"},
],
 "body": """

  <!-- THE PROBLEM -->
  <section id="problem" class="section">
    <span class="kicker">Foundations</span>
    <h2>The problem these tools solve</h2>
    <p class="prose">Before any product names, understand the pain. When you build software, your code is only a small part of what actually ships. The rest is <strong>binaries</strong> - compiled libraries, container images, packages - that you either build yourself or download from the internet.</p>

    <div class="callout callout-q">
      <p class="callout-title">What is a "binary" / "artifact"?</p>
      <p>Anything your build produces or consumes that isn't source code: a <code>.jar</code>, an <code>npm</code> package, a Docker image, a Python wheel, a Helm chart, a compiled <code>.exe</code>. The generic industry word is <strong>artifact</strong>. JFrog calls itself an "artifact repository manager" - a place to store and serve these.</p>
    </div>

    <p class="prose">Without a central system, teams hit four recurring problems:</p>
    <div class="cards">
      <div class="card"><span class="card-num">01</span><h3>Where do builds get dependencies?</h3><p>Everyone pulls directly from the public internet (npm registry, Docker Hub, Maven Central). It's slow, breaks when those sites are down, and you have no control over what enters your builds.</p></div>
      <div class="card"><span class="card-num">02</span><h3>Where do <em>our</em> builds go?</h3><p>You compile something internally. Where does it live so other teams and your CI/CD can reliably grab the exact version? Email and shared drives don't scale.</p></div>
      <div class="card"><span class="card-num">03</span><h3>Is any of it dangerous?</h3><p>A public package might carry a known vulnerability (a <strong>CVE</strong>) or a banned open-source license. You need to know <em>before</em> it reaches production - not after a breach.</p></div>
      <div class="card"><span class="card-num">04</span><h3>Can we prove what's inside?</h3><p>Auditors and customers increasingly ask: "List every component in this release." That list is called an <strong>SBOM</strong>. Producing it by hand is impossible.</p></div>
    </div>

    <div class="split">
      <div class="split-item"><span class="tag tag-art">Artifactory</span><p>solves problems <b>1, 2 &amp; 4</b> - it's the single, trusted home for all binaries flowing in and out.</p></div>
      <div class="split-item"><span class="tag tag-xray">Xray</span><p>solves problem <b>3</b> (and helps with 4) - it continuously scans everything Artifactory stores for vulnerabilities and license risks.</p></div>
    </div>
    <p class="prose muted">They are designed to work together: Artifactory is the warehouse, Xray is the security inspector standing inside it. <a href="https://jfrog.com/blog/what-is-artifactory-jfrog/" target="_blank" rel="noopener">JFrog - What is Artifactory</a>.</p>
  </section>

  <!-- GLOSSARY -->
  <section id="glossary" class="section">
    <span class="kicker">Foundations</span>
    <h2>Vocabulary you'll see everywhere</h2>
    <p class="prose">JFrog docs assume you know these. Skim now, refer back later.</p>
    <div class="glossary">
      <div class="gloss"><dt>Artifact / Binary</dt><dd>Any built/downloaded file: a package, image, library. The thing being stored.</dd></div>
      <div class="gloss"><dt>Repository</dt><dd>A named container inside Artifactory that holds artifacts of one package type (e.g. a Docker repo, an npm repo).</dd></div>
      <div class="gloss"><dt>Package type</dt><dd>The ecosystem format - Docker, Maven, npm, PyPI, Helm, etc. Artifactory "speaks" each one natively.</dd></div>
      <div class="gloss"><dt>Registry</dt><dd>The package-ecosystem word for a repository (e.g. "Docker registry"). Same idea.</dd></div>
      <div class="gloss"><dt>Dependency</dt><dd>A third-party artifact your code needs to build or run.</dd></div>
      <div class="gloss"><dt>CVE</dt><dd>Common Vulnerabilities &amp; Exposures - a globally unique ID for a known security flaw, e.g. <code>CVE-2021-44228</code> (Log4Shell).</dd></div>
      <div class="gloss"><dt>SCA</dt><dd>Software Composition Analysis - scanning the open-source pieces of your software for risk. This is Xray's core job.</dd></div>
      <div class="gloss"><dt>SBOM</dt><dd>Software Bill of Materials - a complete, machine-readable inventory of every component in a release (formats: SPDX, CycloneDX).</dd></div>
      <div class="gloss"><dt>JPD</dt><dd>JFrog Platform Deployment - one running instance of the JFrog platform (your server / cloud tenant).</dd></div>
      <div class="gloss"><dt>build-info</dt><dd>Metadata Artifactory records about a build: which artifacts, which dependencies, which environment. Enables traceability.</dd></div>
      <div class="gloss"><dt>Promotion</dt><dd>Moving an artifact from one repo to the next as it passes quality gates (dev → staging → release).</dd></div>
      <div class="gloss"><dt>Watch + Policy</dt><dd>Xray's enforcement pair: a Policy defines the rules, a Watch says where to apply them. (Detailed later.)</dd></div>
    </div>
  </section>

  <!-- ARTIFACTORY -->
  <section id="artifactory" class="section">
    <span class="kicker kicker-art">Artifactory</span>
    <h2>What Artifactory actually is</h2>
    <p class="prose"><strong>JFrog Artifactory is a universal binary repository manager</strong> - one central place to store, version, secure and serve every artifact your organization produces or depends on. "Universal" means it natively supports 40+ package formats (Docker, Maven, npm, PyPI, Helm, NuGet, Go, Terraform, even ML models) at the same time. <a href="https://jfrog.com/artifactory/" target="_blank" rel="noopener">JFrog Artifactory</a>.</p>

    <div class="analogy">
      <span class="analogy-icon" aria-hidden="true">📦</span>
      <div>
        <p class="analogy-title">One-sentence analogy</p>
        <p>Artifactory is a <strong>smart warehouse for software parts</strong>. Parts arrive from outside suppliers (the public internet), parts are manufactured in-house (your builds), and everything is catalogued, version-stamped, access-controlled, and handed out through a single front desk.</p>
      </div>
    </div>

    <p class="prose">Three things make it more than a file server:</p>
    <ul class="feature-list">
      <li><b>It speaks every package language.</b> Your <code>npm install</code>, <code>docker pull</code>, or <code>mvn build</code> point at Artifactory and it behaves exactly like the native registry would.</li>
      <li><b>It proxies and caches the internet.</b> Public dependencies pass <em>through</em> Artifactory once, get cached, and stay available even if the upstream source goes down. <a href="https://stackoverflow.com/questions/54112370/what-is-the-difference-between-local-repository-remote-respository-and-virtual" target="_blank" rel="noopener">Stack Overflow explanation</a>.</li>
      <li><b>It's a control point.</b> Because everything flows through it, you can apply access control, scanning (Xray), and policies in one place. <a href="https://www.youtube.com/watch?v=1RwtO42In94" target="_blank" rel="noopener">JFrog overview</a>.</li>
    </ul>
  </section>

  <!-- REPOSITORY TYPES -->
  <section id="repos" class="section">
    <span class="kicker kicker-art">Artifactory</span>
    <h2>The 4 repository types (the core concept)</h2>
    <p class="prose">If you learn only one thing about Artifactory, learn this. Every repository is one of four types. They combine into a clean pattern that every JFrog setup follows.</p>

    <figure class="diagram" aria-label="Diagram of how the four repository types relate">
      <div class="diag-grid">
        <div class="diag-col">
          <p class="diag-label">Outside world</p>
          <div class="diag-node node-ext">Public registries<small>Docker Hub · npm · Maven Central · PyPI</small></div>
        </div>
        <div class="diag-arrow">proxy &amp; cache →</div>
        <div class="diag-col">
          <p class="diag-label">Inside Artifactory</p>
          <div class="diag-node node-remote">REMOTE repo<small>caches external artifacts</small></div>
          <div class="diag-node node-local">LOCAL repo<small>stores your own builds</small></div>
          <div class="diag-bracket">▸ both wrapped by ▸</div>
          <div class="diag-node node-virtual">VIRTUAL repo<small>one URL = local + remote combined</small></div>
        </div>
        <div class="diag-arrow">single URL →</div>
        <div class="diag-col">
          <p class="diag-label">Developer / CI</p>
          <div class="diag-node node-dev">your build tool<small>npm · docker · mvn · pip</small></div>
        </div>
      </div>
      <figcaption>The standard pattern: developers and CI talk to <b>one virtual repo URL</b>; Artifactory routes deploys to the local repo and resolves dependencies from local first, then the remote cache, then the internet. Federated repos (4th type) sit alongside for multi-site sync. <a href="https://docs.jfrog.com/artifactory/docs/repository-management" target="_blank" rel="noopener">JFrog Repository Management</a>.</figcaption>
    </figure>

    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Type</th><th>What it does</th><th>Can you upload to it?</th><th>Real-world use</th></tr></thead>
        <tbody>
          <tr><td><span class="pill pill-local">Local</span></td><td>Physically stores artifacts <em>your</em> org creates internally.</td><td><b class="yes">Yes</b> - this is your deploy target.</td><td>Your CI pushes built Docker images, release JARs, internal libraries here.</td></tr>
          <tr><td><span class="pill pill-remote">Remote</span></td><td>A caching <em>proxy</em> for an external registry. Fetches on demand, caches locally.</td><td><b class="no">No</b> - artifacts arrive by proxying.</td><td>A proxy of Docker Hub or npm registry so builds are fast and survive outages.</td></tr>
          <tr><td><span class="pill pill-virtual">Virtual</span></td><td>Aggregates many local + remote repos under <em>one URL</em>. Resolves in priority order.</td><td><b class="partial">Via default deploy target</b> (points to a local).</td><td>The single endpoint your developers configure. Hides internal/external complexity.</td></tr>
          <tr><td><span class="pill pill-fed">Federated</span></td><td>A local repo auto-mirrored bi-directionally across multiple sites (JPDs).</td><td><b class="yes">Yes</b> - like a local, but synced.</td><td>Global teams (London ↔ Tokyo) sharing one source of truth. Enterprise tier.</td></tr>
        </tbody>
      </table>
    </div>
    <p class="prose muted">Sources: <a href="https://docs.jfrog.com/artifactory/docs/managing-configuration-entities" target="_blank" rel="noopener">JFrog config entities</a>, <a href="https://jfrog.com/help/r/jfrog-federated-repositories/jfrog-federated-repositories" target="_blank" rel="noopener">JFrog Federated Repositories</a>. Local/remote/virtual need a Pro subscription; federated needs Enterprise X+.</p>

    <div class="callout callout-tip">
      <p class="callout-title">The "aha" moment</p>
      <p>A <strong>virtual</strong> repo is the magic layer. Your <code>npm</code> client points at one URL. Behind it, Artifactory checks your <em>local</em> repo first (internal packages), then the <em>remote</em> cache (previously downloaded public packages), and only then reaches out to the public internet. The developer never has to know or care where a package lives. <a href="https://www.youtube.com/watch?v=bKp1Vif9oO4" target="_blank" rel="noopener">JFrog artifact management demo</a>.</p>
    </div>
    <p class="prose muted" style="margin-top:var(--space-6)">Want to go deeper on keeping repos in sync across sites? See <a href="replication-federation.html">Replication &amp; Federation</a>.</p>
  </section>

  <!-- ARCHITECTURE -->
  <section id="architecture" class="section">
    <span class="kicker kicker-art">Artifactory</span>
    <h2>How it fits in your pipeline</h2>
    <p class="prose">Zoom out. Here's where Artifactory sits in a normal CI/CD flow, and where Xray plugs in. This is the picture to hold in your head.</p>

    <figure class="flow" aria-label="End-to-end pipeline diagram showing Artifactory and Xray">
      <div class="flow-row">
        <div class="flow-step"><span class="flow-step-n">1</span><b>Developer</b><small>writes code, runs build locally</small></div>
        <span class="flow-conn">→</span>
        <div class="flow-step"><span class="flow-step-n">2</span><b>CI/CD</b><small>GitHub Actions builds artifact</small></div>
        <span class="flow-conn">→</span>
        <div class="flow-step flow-art"><span class="flow-step-n">3</span><b>Artifactory</b><small>stores artifact + records build-info</small></div>
      </div>
      <div class="flow-row flow-row-down"><span class="flow-down">↓ every artifact is indexed &amp; scanned</span></div>
      <div class="flow-row">
        <div class="flow-step flow-xray"><span class="flow-step-n">4</span><b>Xray</b><small>scans for CVEs &amp; license risk</small></div>
        <span class="flow-conn">→</span>
        <div class="flow-step"><span class="flow-step-n">5</span><b>Policy gate</b><small>pass → promote · fail → block/alert</small></div>
        <span class="flow-conn">→</span>
        <div class="flow-step"><span class="flow-step-n">6</span><b>Production</b><small>only approved artifacts ship</small></div>
      </div>
      <figcaption>Artifacts get <em>promoted</em> through repositories as they pass each gate. Xray watches the whole warehouse continuously, so a CVE disclosed tomorrow still flags an artifact you stored last month. <a href="https://jfrog.com/whitepaper/best-practices-for-introducing-jfrog-xray-into-your-devsecops-process/" target="_blank" rel="noopener">JFrog DevSecOps best practices</a>.</figcaption>
    </figure>

    <div class="callout callout-q">
      <p class="callout-title">What's "promotion"?</p>
      <p>You typically have separate repos per maturity stage: <code>dev-local</code> → <code>staging-local</code> → <code>release-local</code>. Promotion = moving (or copying) an artifact up a stage once it passes tests and scans. Same binary, no rebuild - so what you tested is exactly what ships. Full walkthrough on the <a href="build-promotion.html">Build promotion</a> page.</p>
    </div>
  </section>

  <!-- PACKAGE TYPES -->
  <section id="packages" class="section">
    <span class="kicker kicker-art">Artifactory</span>
    <h2>Package types it supports</h2>
    <p class="prose">"Universal" is the selling point: 40+ ecosystems, one platform. You don't need them all - pick the ones your stack uses. Here are the common ones a DevOps team touches. <a href="https://docs.jfrog.com/artifactory/docs/supported-package-types" target="_blank" rel="noopener">Full list</a>.</p>
    <div class="chips">
      <span class="chip">Docker / OCI</span><span class="chip">Helm</span><span class="chip">Maven</span><span class="chip">Gradle</span><span class="chip">npm</span><span class="chip">PyPI</span><span class="chip">Go</span><span class="chip">NuGet</span><span class="chip">Cargo (Rust)</span><span class="chip">Conan (C++)</span><span class="chip">Debian</span><span class="chip">RPM / YUM</span><span class="chip">Terraform</span><span class="chip">Conda</span><span class="chip">Hugging Face (ML)</span><span class="chip">RubyGems</span><span class="chip">Generic (anything)</span>
    </div>
    <div class="callout callout-tip">
      <p class="callout-title">DevOps reality check</p>
      <p>For a typical cloud-native team, you'll create repos for: <b>Docker</b> (your images), <b>Helm</b> (your charts), and a remote proxy of <b>Docker Hub</b>. Add <b>npm</b>/<b>PyPI</b>/<b>Go</b> remotes per language. The <b>Generic</b> type stores literally anything (tarballs, configs, ML weights) when no native type fits.</p>
    </div>
  </section>

  <!-- XRAY -->
  <section id="xray" class="section">
    <span class="kicker kicker-x">Xray</span>
    <h2>What Xray actually is</h2>
    <p class="prose"><strong>JFrog Xray is a Software Composition Analysis (SCA) tool.</strong> It scans everything Artifactory stores - packages, container images, builds - to detect security vulnerabilities, malicious packages, license risks, and operational issues. It's natively integrated with Artifactory, so binary scanning turns on with a single checkbox. <a href="https://docs.jfrog.com/security/docs/xray" target="_blank" rel="noopener">JFrog Xray docs</a>.</p>

    <div class="analogy analogy-x">
      <span class="analogy-icon" aria-hidden="true">🔍</span>
      <div>
        <p class="analogy-title">One-sentence analogy</p>
        <p>If Artifactory is the warehouse, Xray is the <strong>security inspector living inside it</strong> - X-raying every box that arrives, cross-checking it against a global database of known threats, and raising an alarm (or locking the door) when something dangerous is found.</p>
      </div>
    </div>

    <div class="cards cards-x">
      <div class="card"><h3>🛡️ Vulnerabilities</h3><p>Matches components against CVE databases (NVD, GitHub, vendor feeds + JFrog's own security research) to find known flaws.</p></div>
      <div class="card"><h3>⚖️ License compliance</h3><p>Flags open-source licenses your org bans or must track (e.g. GPL in a proprietary product).</p></div>
      <div class="card"><h3>🐛 Malicious packages</h3><p>Detects deliberately poisoned packages - including malicious ML models on Hugging Face.</p></div>
      <div class="card"><h3>📋 SBOM &amp; impact</h3><p>Generates a full Software Bill of Materials and shows the impact graph of any flaw across your components.</p></div>
    </div>
    <p class="prose muted">Sources: <a href="https://cloudsecurity.org/tool/jfrog-xray" target="_blank" rel="noopener">Xray architecture overview</a>, <a href="https://jfrog.com/help/r/jfrog-security-user-guide/products/xray/features-and-capabilities/sca/sbom" target="_blank" rel="noopener">JFrog SBOM</a>.</p>
  </section>

  <!-- XRAY HOW -->
  <section id="xray-how" class="section">
    <span class="kicker kicker-x">Xray</span>
    <h2>How scanning actually works</h2>
    <p class="prose">Xray's superpower is <strong>deep recursive scanning</strong>. It doesn't just look at your top-level package - it peels open every layer: dependencies, dependencies-of-dependencies, files inside Docker layers, archives inside archives. <a href="https://jfrog.com/article/impact-analysis/" target="_blank" rel="noopener">JFrog Impact Analysis</a>.</p>

    <figure class="diagram diagram-x" aria-label="Deep recursive scanning diagram">
      <p class="diag-label center">Deep recursive scan - peeling the onion</p>
      <div class="onion">
        <div class="onion-layer l1"><span>Your Docker image</span>
          <div class="onion-layer l2"><span>Base OS layer</span>
            <div class="onion-layer l3"><span>App package (npm/jar)</span>
              <div class="onion-layer l4"><span>Direct dependency</span>
                <div class="onion-layer l5"><span class="cve-found">↳ vulnerable lib · CVE-2021-44228</span></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <figcaption>Xray finds the vulnerable component buried 5 levels deep, then uses <b>impact analysis</b> to show every artifact, build, and image affected by it. <a href="https://dev.to/jfrog/easy-automatic-vulnerability-detection-in-the-jfrog-platform-5928" target="_blank" rel="noopener">JFrog vulnerability detection</a>.</figcaption>
    </figure>

    <h3 class="subhead">The scanning lifecycle</h3>
    <ol class="steps">
      <li><b>Index.</b> When a repo is marked for Xray, every artifact is broken into its component graph and indexed.</li>
      <li><b>Scan.</b> Each component is matched against the vulnerability + license databases.</li>
      <li><b>Continuous re-check.</b> When a <em>new</em> CVE is published, Xray re-evaluates already-stored artifacts - no rescan needed. This is why it catches yesterday's "safe" image today.</li>
      <li><b>Report &amp; enforce.</b> Findings appear as <em>violations</em> (when they break a policy) with severity, affected components, and remediation (which version fixes it). <a href="https://docs.jfrog.com/security/docs/understanding-and-analyzing-xray-scan-results-p" target="_blank" rel="noopener">Understanding scan results</a>.</li>
    </ol>

    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Where you can trigger a scan</th><th>How</th><th>Best for</th></tr></thead>
        <tbody>
          <tr><td>Inside Artifactory (automatic)</td><td>Enable Xray indexing on a repo - scans on upload</td><td>Continuous coverage of everything stored</td></tr>
          <tr><td>CI/CD pipeline</td><td><code>jf build-scan</code> / <code>jf scan</code></td><td>Failing a build before bad code ships</td></tr>
          <tr><td>Local machine (shift-left)</td><td><code>jf scan</code> on source, <code>jf docker scan</code> on an image</td><td>Catching issues before you even commit</td></tr>
          <tr><td>IDE / Pull request</td><td>JFrog IDE plugins &amp; Frogbot</td><td>Instant developer feedback + autofix PRs</td></tr>
        </tbody>
      </table>
    </div>
    <p class="prose muted">Source: <a href="https://docs.jfrog.com/integrations/docs/cli-command-summaries" target="_blank" rel="noopener">JFrog CLI command summaries</a>. For PR scanning and IDE setup, see <a href="frogbot.html">Frogbot &amp; IDE integration</a>.</p>
  </section>

  <!-- POLICIES -->
  <section id="policies" class="section">
    <span class="kicker kicker-x">Xray</span>
    <h2>Policies &amp; Watches (how enforcement works)</h2>
    <p class="prose">Finding problems is useless unless you act on them. Xray's enforcement runs on two linked objects. This trips up newcomers, so here's the clean split:</p>

    <div class="pw-grid">
      <div class="pw-card pw-policy">
        <span class="pw-badge">Defines the RULES</span>
        <h3>Policy</h3>
        <p>A set of rules describing what counts as a problem and what to do about it.</p>
        <ul>
          <li><b>Type:</b> Security · License · Operational risk</li>
          <li><b>Rule:</b> e.g. "severity ≥ High" or "license = GPL"</li>
          <li><b>Action:</b> notify · fail build · block download · create ticket</li>
        </ul>
      </div>
      <div class="pw-link" aria-hidden="true">
        <span>applied via</span>
        <svg width="40" height="24" viewBox="0 0 40 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12h32M28 6l8 6-8 6"/></svg>
      </div>
      <div class="pw-card pw-watch">
        <span class="pw-badge">Defines the SCOPE</span>
        <h3>Watch</h3>
        <p>A binding that says <em>where</em> a policy applies and turns it on.</p>
        <ul>
          <li><b>Targets:</b> specific repos, builds, or projects</li>
          <li><b>Attaches:</b> one or more policies</li>
          <li><b>Result:</b> matches → <em>violations</em> get generated</li>
        </ul>
      </div>
    </div>

    <div class="callout callout-tip">
      <p class="callout-title">Remember it this way</p>
      <p><b>Policy = the law</b> (what's illegal + the punishment). <b>Watch = the jurisdiction + the police</b> (where the law applies and who enforces it). A finding only becomes a <em>violation</em> when a Watch points a Policy at the repo where it lives. <a href="https://docs.jfrog.com/security/docs/policies-in-jfrog-xray" target="_blank" rel="noopener">JFrog Policy &amp; Governance</a>.</p>
    </div>

    <h3 class="subhead">Severity levels you'll triage</h3>
    <div class="sev-row">
      <span class="sev sev-crit">Critical</span>
      <span class="sev sev-high">High</span>
      <span class="sev sev-med">Medium</span>
      <span class="sev sev-low">Low</span>
      <span class="sev sev-unknown">Unknown</span>
    </div>
    <p class="prose muted">A common starter policy: "generate violations for <b>High + Critical</b> security issues, but only when a fixed version is available" - so you're not alerted on problems you can't yet fix. <a href="https://stackoverflow.com/questions/75474890/jfrog-xray-violations-should-not-occure-for-libraries-where-there-is-no-fix-vers" target="_blank" rel="noopener">Stack Overflow on fix-version rule</a>.</p>
  </section>

  <!-- LABS -->
  <section id="labs" class="section">
    <span class="kicker kicker-lab">Hands-on</span>
    <h2>Choose your hands-on track</h2>
    <p class="prose">Reading gets you understanding; doing gets you skill. Pick a track based on how deep you want to go. All three reach the same goal: <b>store an artifact, then scan it with Xray.</b></p>

    <div class="tabs" id="labTabs">
      <div class="tab-bar" role="tablist" aria-label="Lab tracks">
        <button class="tab active" role="tab" aria-selected="true" data-tab="cloud">☁️ JFrog Cloud (free tier)</button>
        <button class="tab" role="tab" aria-selected="false" data-tab="docker">🐳 Local Docker (self-hosted)</button>
        <button class="tab" role="tab" aria-selected="false" data-tab="concepts">⌨️ Concepts + CLI</button>
      </div>

      <div class="tab-panel active" role="tabpanel" data-panel="cloud">
        <p class="panel-intro"><b>Fastest path to a working platform.</b> JFrog runs a free cloud tier (AWS/Azure/GCP) - no install, ready in minutes. Best first stop. <a href="https://jfrog.com/start-free/" target="_blank" rel="noopener">Start free</a>.</p>
        <ol class="lab-steps">
          <li><span class="ls-n">1</span><div><b>Sign up for the free cloud subscription.</b> Go to <a href="https://jfrog.com/start-free/" target="_blank" rel="noopener">jfrog.com/start-free</a> → choose Cloud (free). You get a tenant like <code>yourname.jfrog.io</code> with Artifactory + Xray. Free tier: ~2&nbsp;GB storage, 10&nbsp;GB transfer. <a href="https://devops.com/jfrog-adds-free-devops-tier-in-the-cloud/" target="_blank" rel="noopener">Free tier announcement</a>.</div></li>
          <li><span class="ls-n">2</span><div><b>Log in to the web UI.</b> Explore the two main tabs: <em>Application</em> (browse repos/artifacts) and <em>Administration</em> (create repos, configure Xray).</div></li>
          <li><span class="ls-n">3</span><div><b>Create your first repositories.</b> Administration → Repositories → <b>+ Add Repository</b>. Make a <span class="pill pill-local">Local</span> Docker repo (<code>docker-local</code>), a <span class="pill pill-remote">Remote</span> proxy of Docker Hub (<code>docker-remote</code>), and a <span class="pill pill-virtual">Virtual</span> repo combining both (<code>docker</code>). <a href="https://medium.com/@vniranjan251203/jfrog-artifactory-and-maven-package-type-2fe0af1765b0" target="_blank" rel="noopener">Repo creation walkthrough</a>.</div></li>
          <li><span class="ls-n">4</span><div><b>Connect the CLI.</b> Install JFrog CLI (see the CLI tab) then run <code>jf c add</code> and paste your <code>*.jfrog.io</code> URL + a token. Verify with <code>jf rt ping</code>.</div></li>
          <li><span class="ls-n">5</span><div><b>Push an image.</b> <code>jf docker push yourname.jfrog.io/docker-local/demo:1.0</code> - then find it in the UI under your local repo.</div></li>
          <li><span class="ls-n">6</span><div><b>Turn on Xray.</b> Administration → Xray → <b>Indexed Resources</b> → add <code>docker-local</code>. The image scans automatically.</div></li>
          <li><span class="ls-n">7</span><div><b>Create a Policy + Watch.</b> Administration → Xray → <b>Watches &amp; Policies</b>. Make a Security policy (rule: severity ≥ High, action: notify) and a Watch targeting <code>docker-local</code>. <a href="https://www.youtube.com/watch?v=ztcDI47FnmA" target="_blank" rel="noopener">Policies/watches video</a>.</div></li>
          <li><span class="ls-n">8</span><div><b>Read the results.</b> Open the artifact → <em>Xray</em> tab. Review vulnerabilities by severity, affected components, and fix versions. You've completed the loop. 🎉</div></li>
        </ol>
        <div class="callout callout-tip"><p class="callout-title">Why start here</p><p>Zero infrastructure to maintain, real cloud UI, and everything in this guide works out of the box. Graduate to local Docker once you want to understand the moving parts.</p></div>
      </div>

      <div class="tab-panel" role="tabpanel" data-panel="docker">
        <p class="panel-intro"><b>Run the whole platform on your Mac (OrbStack/Docker).</b> You'll see exactly what services make up Artifactory + Xray. Requires Docker Engine 25+ &amp; Docker Compose v2; ARM64 (Apple Silicon) is supported via Docker. <a href="https://jfrog.com/start-free/install/" target="_blank" rel="noopener">Install guide</a>.</p>
        <div class="callout callout-q"><p class="callout-title">Heads up on resources</p><p>The full platform (Artifactory + Xray + PostgreSQL + RabbitMQ) wants ~4 CPU / 8&nbsp;GB RAM. Your 8&nbsp;GB Mac setup is the realistic minimum - close other heavy apps.</p></div>
        <ol class="lab-steps">
          <li><span class="ls-n">1</span><div><b>Download the trial Docker-Compose bundle.</b><pre class="code"><code>curl -L "https://releases.jfrog.io/artifactory/jfrog-prox/org/artifactory/pro/docker/jfrog-platform-trial-prox/[RELEASE]/jfrog-platform-trial-prox-[RELEASE]-compose.tar.gz" -o jfrog-compose.tar.gz</code></pre><a href="https://jfrog.com/start-free/install/" target="_blank" rel="noopener">Source</a></div></li>
          <li><span class="ls-n">2</span><div><b>Extract &amp; enter the directory.</b><pre class="code"><code>tar -xvf jfrog-compose.tar.gz
cd jfrog-platform-trial-prox-*</code></pre></div></li>
          <li><span class="ls-n">3</span><div><b>Run the config script</b> (sets up folder structure + the <code>.env</code> file Compose uses). Follow its prompts.</div></li>
          <li><span class="ls-n">4</span><div><b>Start everything.</b><pre class="code"><code>docker compose -p trial-pro up -d</code></pre>Give it a few minutes - Xray boots after Artifactory and PostgreSQL are healthy. <a href="https://docs.jfrog.com/installation/docs/installing-xray" target="_blank" rel="noopener">Xray install steps</a>.</div></li>
          <li><span class="ls-n">5</span><div><b>Open the UI.</b> Browse to <code>http://localhost:8082</code>. Default login <code>admin</code> / <code>password</code> - change it immediately.</div></li>
          <li><span class="ls-n">6</span><div><b>Apply your free license.</b> Paste the license key from your JFrog account to unlock Xray.</div></li>
          <li><span class="ls-n">7</span><div><b>From here, follow Cloud steps 3-8</b> - create local/remote/virtual repos, push an image, enable Xray indexing, set a policy + watch, read results. The UI is identical.</div></li>
          <li><span class="ls-n">8</span><div><b>Tear down cleanly.</b><pre class="code"><code>docker compose -p trial-pro down</code></pre>Add <code>-v</code> only if you want to wipe the data volumes too.</div></li>
        </ol>
        <p class="prose muted">Prefer Kubernetes? See <a href="kubernetes-helm.html">Kubernetes / Helm setup</a> for installing Artifactory on a cluster with the JFrog Helm charts.</p>
      </div>

      <div class="tab-panel" role="tabpanel" data-panel="concepts">
        <p class="panel-intro"><b>For when you don't want to run a server - just learn the commands &amp; integration patterns.</b> The JFrog CLI binary is <code>jf</code>. One tool drives Artifactory and Xray. <a href="https://docs.jfrog.com/integrations/docs/cli-command-summaries" target="_blank" rel="noopener">CLI summaries</a>.</p>
        <ol class="lab-steps">
          <li><span class="ls-n">1</span><div><b>Install the CLI</b> (macOS, Homebrew):<pre class="code"><code>brew install jfrog-cli</code></pre>Or one-liner: <code>curl -fL https://install-cli.jfrog.io | sh</code>. Verify: <code>jf --version</code>.</div></li>
          <li><span class="ls-n">2</span><div><b>Configure a server connection.</b><pre class="code"><code>jf c add my-jpd --url=https://yourname.jfrog.io --interactive</code></pre>Use an access token, not a password. Test: <code>jf rt ping</code>.</div></li>
          <li><span class="ls-n">3</span><div><b>Scan your source code (shift-left)</b> - no upload needed:<pre class="code"><code>jf scan .</code></pre>Scans the dependencies in the current project against Xray. <a href="https://github.com/jfrog/documentation/blob/main/jfrog-applications/jfrog-applications/jfrog-cli/cli-for-jfrog-security/how-tos/scan-your-source-code.md" target="_blank" rel="noopener">Source-scan docs</a>.</div></li>
          <li><span class="ls-n">4</span><div><b>Scan a local Docker image:</b><pre class="code"><code>jf docker scan my-app:1.0.0</code></pre>First run downloads ~100&nbsp;MB of Xray scanner binaries. <a href="https://docs.jfrog.com/artifactory/docs/jf-docker" target="_blank" rel="noopener">jf docker docs</a>.</div></li>
          <li><span class="ls-n">5</span><div><b>Scan an artifact already in Artifactory, against a watch:</b><pre class="code"><code>jf xr scan --target "docker-local/demo:1.0" --watches "my-watch"</code></pre><a href="https://deepwiki.com/jfrog/jfrog-cli/3.2-xray-commands" target="_blank" rel="noopener">Xray CLI commands</a>.</div></li>
          <li><span class="ls-n">6</span><div><b>Wire it into GitHub Actions</b> (fail the build on Critical issues):<pre class="code"><code>- name: Security Scan
  run: jf build-scan ${{ github.repository }} ${{ github.run_number }} --fail=true --vuln=Critical</code></pre><a href="https://docs.jfrog.com/integrations/docs/cli-command-summaries" target="_blank" rel="noopener">CI integration</a>. Note: the build must be added under <em>Administration → Xray → Indexed Resources</em> first.</div></li>
        </ol>
        <div class="callout callout-tip"><p class="callout-title">Mental model for the CLI</p><p><code>jf rt …</code> = Artifactory (uploads, downloads, repos). <code>jf xr …</code> = Xray (scans). <code>jf scan</code> / <code>jf docker scan</code> / <code>jf build-scan</code> = convenient shortcuts that combine both.</p></div>
      </div>
    </div>
  </section>

  <!-- CLI CHEAT SHEET -->
  <section id="cli" class="section">
    <span class="kicker kicker-lab">Hands-on</span>
    <h2>CLI cheat sheet</h2>
    <p class="prose">The commands you'll reach for most. <code>jf</code> is the binary; older docs use <code>jfrog</code>. <a href="https://deepwiki.com/jfrog/jfrog-cli/3.2-xray-commands" target="_blank" rel="noopener">Reference</a>.</p>
    <div class="table-wrap">
      <table class="datatable mono-table">
        <thead><tr><th>Command</th><th>What it does</th></tr></thead>
        <tbody>
          <tr><td><code>jf c add</code></td><td>Add a JFrog server connection</td></tr>
          <tr><td><code>jf rt ping</code></td><td>Test the Artifactory connection</td></tr>
          <tr><td><code>jf rt u &lt;file&gt; &lt;repo&gt;</code></td><td>Upload (deploy) an artifact</td></tr>
          <tr><td><code>jf rt dl &lt;repo/path&gt;</code></td><td>Download an artifact</td></tr>
          <tr><td><code>jf docker push &lt;image&gt;</code></td><td>Push a Docker image (auto-login + build-info)</td></tr>
          <tr><td><code>jf scan .</code></td><td>Scan local source dependencies with Xray</td></tr>
          <tr><td><code>jf docker scan &lt;image&gt;</code></td><td>Scan a local Docker image</td></tr>
          <tr><td><code>jf xr scan --target … --watches …</code></td><td>Scan an artifact in Artifactory against a watch</td></tr>
          <tr><td><code>jf build-scan &lt;name&gt; &lt;num&gt; --fail=true</code></td><td>Scan a build in CI; fail on violations</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <!-- MENTAL MODEL -->
  <section id="mental-model" class="section">
    <span class="kicker">Synthesis</span>
    <h2>The full mental model on one screen</h2>
    <p class="prose">Everything above, compressed. If you can re-draw this from memory, you understand the platform.</p>
    <figure class="bigmodel" aria-label="Complete mental model diagram">
      <div class="bm-band bm-in">
        <span class="bm-tag">IN</span>
        <div class="bm-box">Public registries<small>Docker Hub, npm, PyPI…</small></div>
        <span class="bm-op">+</span>
        <div class="bm-box">Your CI builds<small>images, jars, charts</small></div>
      </div>
      <div class="bm-arrow">↓ everything flows through ↓</div>
      <div class="bm-band bm-core">
        <div class="bm-core-inner">
          <span class="bm-title bm-title-art">ARTIFACTORY · the warehouse</span>
          <div class="bm-repos">
            <span class="pill pill-remote">Remote (cache)</span>
            <span class="pill pill-local">Local (your builds)</span>
            <span class="pill pill-virtual">Virtual (one URL)</span>
            <span class="pill pill-fed">Federated (multi-site)</span>
          </div>
          <div class="bm-xray">
            <span class="bm-title bm-title-x">XRAY · the inspector</span>
            <span class="bm-xray-line">deep recursive scan → CVEs · licenses · SBOM → Policy + Watch → violation</span>
          </div>
        </div>
      </div>
      <div class="bm-arrow">↓ only what passes the gate ↓</div>
      <div class="bm-band bm-out">
        <span class="bm-tag">OUT</span>
        <div class="bm-box">Developers &amp; CI<small>resolve via one virtual URL</small></div>
        <span class="bm-op">→</span>
        <div class="bm-box">Production<small>approved artifacts only</small></div>
      </div>
    </figure>
    <div class="recap">
      <p class="recap-title">If you remember 4 things:</p>
      <ol>
        <li><b>Artifactory = the single warehouse</b> for every binary, in and out.</li>
        <li><b>4 repo types</b>: Local (yours), Remote (cached internet), Virtual (one URL over both), Federated (multi-site).</li>
        <li><b>Xray = the inspector</b> doing deep recursive scans for CVEs &amp; license risk, continuously.</li>
        <li><b>Policy (the rule) + Watch (the scope)</b> = how findings turn into enforced violations.</li>
      </ol>
    </div>
  </section>

  """,
}
_p["prev"], _p["next"] = chain(_p["file"])
PAGE_LIST.append(_p)


# =====================================================================
# 2) REPLICATION & FEDERATION
# =====================================================================
_p = {
 "file": "replication-federation.html",
 "title": "Replication & Federation",
 "desc": "How JFrog keeps artifacts in sync across data centers and JPDs: push/pull replication versus federated repositories, and when to use each.",
 "badges": '<span class="lvl lvl-art">Artifactory</span><span class="lvl">Multi-site</span><span class="lvl">Deep-dive</span>',
 "h1": "Replication &amp; Federation",
 "lede": "Once you run JFrog in more than one location, you need copies of your artifacts to stay in sync. JFrog gives you two mechanisms - classic replication and federated repositories. They solve overlapping problems differently.",
 "sections": [
   {"id": "why", "label": "Why sync at all"},
   {"id": "replication", "label": "Replication"},
   {"id": "modes", "label": "Push vs. pull"},
   {"id": "federation", "label": "Federated repositories"},
   {"id": "compare", "label": "Which to choose"},
   {"id": "howto", "label": "How to set it up"},
 ],
 "body": """
  <section id="why" class="section">
    <span class="kicker kicker-art">Concept</span>
    <h2>Why sync artifacts across sites at all?</h2>
    <p class="prose">A single Artifactory instance is one point in the world. The moment you have teams in London and Tokyo, a CI (Continuous Integration - the automated server that builds and tests your code) farm in another region, or a disaster-recovery site (a backup copy you can switch to if your main one fails), builds in one place need the same binaries that live in another. "Binaries" here just means the packaged outputs you store in Artifactory - Docker images, JAR files, npm packages, and so on. Pulling all of them across an ocean on every build is slow and fragile.</p>
    <div class="cards">
      <div class="card"><span class="card-num">01</span><h3>Latency</h3><p>Developers and CI resolve dependencies from a local copy instead of crossing continents on every download.</p></div>
      <div class="card"><span class="card-num">02</span><h3>Availability</h3><p>If one site or its network goes down, the others still have their own copy and keep building.</p></div>
      <div class="card"><span class="card-num">03</span><h3>Disaster recovery</h3><p>A synced standby instance lets you fail over with the artifacts already in place.</p></div>
    </div>
    <div class="callout callout-q">
      <p class="callout-title">First, one term you'll see everywhere: JPD</p>
      <p>A <b>JPD</b> stands for <b>JFrog Platform Deployment</b> - it's simply one complete, self-contained install of the JFrog Platform (Artifactory + Xray + the rest), running in one place. When this page says "site", "instance", or "deployment", it means one JPD. Syncing artifacts across sites means syncing them between JPDs.</p>
    </div>
    <p class="prose muted">JFrog offers two answers: <strong>replication</strong> (an older, one-directional copy job) and <strong>federation</strong> (newer, automatic, multi-directional mirroring). "One-directional" means data flows from a source to a target only; "multi-directional" means every copy can both send and receive. <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/repository-replication" target="_blank" rel="noopener">JFrog - Repository Replication</a>.</p>
  </section>

  <section id="replication" class="section">
    <span class="kicker kicker-art">Replication</span>
    <h2>Replication - copying repositories between instances</h2>
    <p class="prose"><strong>Replication</strong> synchronizes the contents of a repository on one Artifactory instance with a repository on another. It runs on a <em>schedule</em> - defined by a <b>cron</b> expression, which is just a compact string that says "run at these times" (for example, every hour) - or it can be triggered automatically as an <em>event</em> the moment something changes. It copies artifacts plus their <b>properties</b> (key/value tags attached to an artifact, like <code>stage=released</code>). Replication works on <span class="pill pill-local">local</span> and <span class="pill pill-remote">remote</span> repositories. <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/repository-replication" target="_blank" rel="noopener">Source</a>.</p>
    <div class="callout callout-q">
      <p class="callout-title">Key trait: it's one-directional</p>
      <p>A single replication has a clear source and target. Site A pushes to Site B, or Site B pulls from Site A - but one replication relationship only flows one way. To mirror both directions you configure two separate jobs.</p>
    </div>
  </section>

  <section id="modes" class="section">
    <span class="kicker kicker-art">Replication</span>
    <h2>Push vs. pull replication</h2>
    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Mode</th><th>Who initiates</th><th>How it works</th><th>Typical use</th></tr></thead>
        <tbody>
          <tr><td><b>Push</b></td><td>The <em>source</em> instance</td><td>The source repo pushes new/changed artifacts out to a target repo on a remote instance.</td><td>A central build site fanning releases out to regional mirrors.</td></tr>
          <tr><td><b>Pull</b></td><td>The <em>target</em> instance</td><td>A <span class="pill pill-remote">remote</span> repo's "replication" pulls content from its upstream Artifactory on a schedule.</td><td>An edge/DR site keeping itself current from a master.</td></tr>
        </tbody>
      </table>
    </div>
    <figure class="flow" aria-label="Push vs pull replication">
      <div class="flow-row">
        <div class="flow-step flow-art"><span class="flow-step-n">A</span><b>Source JPD</b><small>has the artifacts</small></div>
        <span class="flow-conn">→ push →</span>
        <div class="flow-step"><span class="flow-step-n">B</span><b>Target JPD</b><small>receives a copy</small></div>
      </div>
      <div class="flow-row flow-row-down"><span class="flow-down">- or, reversed initiator -</span></div>
      <div class="flow-row">
        <div class="flow-step"><span class="flow-step-n">A</span><b>Source JPD</b><small>has the artifacts</small></div>
        <span class="flow-conn">← pull ←</span>
        <div class="flow-step flow-art"><span class="flow-step-n">B</span><b>Target JPD</b><small>fetches the copy</small></div>
      </div>
      <figcaption>Push and pull move data the same direction (A → B); they differ only in <em>which side starts the transfer</em>. Push is good when the source can reach the target; pull is good when only the target can reach out (for example, a firewalled edge site that is allowed to make outbound connections but not receive inbound ones). <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/repository-replication" target="_blank" rel="noopener">JFrog Replication</a>.</figcaption>
    </figure>
  </section>

  <section id="federation" class="section">
    <span class="kicker kicker-x">Federation</span>
    <h2>Federated repositories - automatic multi-directional mirroring</h2>
    <p class="prose">A <span class="pill pill-fed">Federated</span> repository behaves like a <span class="pill pill-local">local</span> repo, but it is bi-directionally mirrored across multiple <strong>members</strong> - up to 10 repositories living on different JFrog Platform Deployments (JPDs, defined above). "Bi-directional" means the sync flows both ways. Write to any member and the change <em>propagates</em> (spreads automatically) to all the others, <em>asynchronously</em> (in the background, so your write doesn't have to wait for every copy to finish). <a href="https://docs.jfrog.com/artifactory/docs/federated-repositories" target="_blank" rel="noopener">JFrog - Federated Repositories</a>.</p>
    <ul class="feature-list">
      <li><b>Bi-directional by design.</b> Every member is both source and target - no manual two-way setup. Deploy to London, it appears in Tokyo, and vice-versa.</li>
      <li><b>Async, queue-backed.</b> Changes are replicated through a persistent queue, so a temporary network blip doesn't lose data - it catches up when connectivity returns.</li>
      <li><b>Configuration is synced too.</b> Repository configuration (not just artifacts) is kept aligned across members.</li>
      <li><b>Up to 10 members.</b> A federation can span up to ten member repositories across JPDs.</li>
      <li><b>Enterprise tier.</b> Federated repositories require an Enterprise X (or higher) paid subscription - so you won't see them on the free tier.</li>
    </ul>
    <div class="callout callout-tip">
      <p class="callout-title">The mental shortcut</p>
      <p><b>Replication = a copy job you schedule, one direction at a time.</b> <b>Federation = a self-healing cluster of mirror repos that stay in sync automatically, both ways.</b> Federation is the modern default for "active-active" multi-site (every site is live and writable at once); replication still fits one-way disaster-recovery (DR) standbys and edge-cache patterns.</p>
    </div>
  </section>

  <section id="compare" class="section">
    <span class="kicker">Decision</span>
    <h2>Which one should you use?</h2>
    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Dimension</th><th>Replication</th><th>Federated repos</th></tr></thead>
        <tbody>
          <tr><td>Direction</td><td>One-way per job</td><td>Multi-directional (all members)</td></tr>
          <tr><td>Trigger</td><td>Scheduled / event</td><td>Automatic on every write</td></tr>
          <tr><td>Members</td><td>Two endpoints per job</td><td>Up to 10 across JPDs</td></tr>
          <tr><td>Config sync</td><td><b class="no">No</b> (artifacts &amp; properties)</td><td><b class="yes">Yes</b> (config too)</td></tr>
          <tr><td>Resilience</td><td>Re-runs on schedule</td><td>Persistent queue, self-healing</td></tr>
          <tr><td>License</td><td>Pro / Enterprise</td><td>Enterprise X+</td></tr>
          <tr><td>Best for</td><td>DR standby, edge caches, one-way distribution</td><td>Active-active global teams, single source of truth</td></tr>
        </tbody>
      </table>
    </div>
    <p class="prose muted">Sources: <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/repository-replication" target="_blank" rel="noopener">JFrog Replication</a>, <a href="https://docs.jfrog.com/artifactory/docs/federated-repositories" target="_blank" rel="noopener">JFrog Federated Repositories</a>.</p>
  </section>

  <section id="howto" class="section">
    <span class="kicker kicker-lab">How-to</span>
    <h2>Setting each one up</h2>
    <h3 class="subhead">Configure replication (UI)</h3>
    <ol class="steps">
      <li><b>Open the repo.</b> Administration → Repositories → select a local or remote repo → <b>Replications</b> tab.</li>
      <li><b>Add a replication.</b> Provide the target instance URL, the target repository key, and credentials (use an access token).</li>
      <li><b>Pick a schedule.</b> Set a cron expression (e.g. every hour) and choose whether to enable event-based replication for near-real-time push.</li>
      <li><b>Save &amp; test.</b> Run it once manually and confirm artifacts land in the target.</li>
    </ol>
    <h3 class="subhead">Create a federated repository (UI)</h3>
    <ol class="steps">
      <li><b>Add repository → Federated.</b> Choose the package type, then create the repo on your first JPD.</li>
      <li><b>Add members.</b> In the Federated configuration, add member URLs for the other JPDs. For one JPD to trust another, they must first be linked - JFrog calls this the "circle of trust", set up through Mission Control (JFrog's tool for managing multiple deployments). Think of it as the two deployments exchanging IDs so they'll accept each other's data.</li>
      <li><b>Deploy anywhere.</b> Push an artifact to any member; verify it appears on the others within seconds.</li>
    </ol>
    <div class="callout callout-q">
      <p class="callout-title">Tip for your labs</p>
      <p><b>Prerequisite reminder:</b> on the free single-instance tier you can't truly demonstrate multi-JPD federation - you need at least two separate deployments. You <em>can</em> still create the repo types and read the configuration screens to understand the model. For a real two-site test, stand up two self-hosted instances ("self-hosted" means you run Artifactory yourself, e.g. in Docker, instead of using JFrog's cloud) - see the Docker lab on the <a href="fundamentals.html">Fundamentals</a> page.</p>
    </div>
  </section>
""",
}
_p["prev"], _p["next"] = chain(_p["file"])
PAGE_LIST.append(_p)


# =====================================================================
# 2) BUILD PROMOTION
# =====================================================================
_p = {
 "file": "build-promotion.html",
 "title": "Build promotion",
 "desc": "Move a build through dev to staging to release without rebuilding. build-info, status changes, copy vs move, and the CLI and REST commands that do it.",
 "badges": '<span class="lvl lvl-art">Artifactory</span><span class="lvl">Lifecycle</span><span class="lvl lvl-lab">CLI + REST</span>',
 "h1": "Build promotion in practice",
 "lede": "Promotion is how a binary graduates from dev to staging to release without ever being rebuilt - so what you tested is byte-for-byte what ships. It hinges on one idea: build-info that tracks artifacts by checksum, wherever they move.",
 "sections": [
   {"id": "what", "label": "What promotion is"},
   {"id": "buildinfo", "label": "build-info & identity"},
   {"id": "copymove", "label": "Copy vs. move"},
   {"id": "cli", "label": "Promote via CLI"},
   {"id": "rest", "label": "Promote via REST"},
   {"id": "pattern", "label": "Repo layout pattern"},
 ],
 "body": """
  <section id="what" class="section">
    <span class="kicker kicker-art">Concept</span>
    <h2>What build promotion actually is</h2>
    <p class="prose">First, two words you'll see a lot. A <b>build</b> is one run of your CI/CD pipeline that produces artifacts ("CI/CD" = Continuous Integration / Continuous Delivery, the automated build-test-ship flow). A <b>stage</b> is a maturity level a build has reached, such as dev, staging, or released.</p>
    <p class="prose"><strong>Build promotion changes a build's status to a more mature stage</strong> - for example <code>dev</code> → <code>staging</code> → <code>released</code> - and can optionally move or copy the build's artifacts (and their dependencies) into a target repository and set properties on them ("properties" are key/value tags like <code>stage=released</code>). The crucial part: <em>no rebuild happens</em>. The same binary that passed your tests is the one that advances. <a href="https://jfrog.com/help/r/how-does-build-promotion-work/artifactory-how-does-build-promotion-work" target="_blank" rel="noopener">JFrog - How build promotion works</a>.</p>
    <div class="analogy">
      <span class="analogy-icon" aria-hidden="true">🎟️</span>
      <div>
        <p class="analogy-title">One-sentence analogy</p>
        <p>Promotion is a <strong>stamp on a passport</strong>, not a new passport. The traveller (your binary) is unchanged; it just earns a visa for the next country (stage). Because it's the same passport, you have proof the thing entering production is exactly the thing you vetted.</p>
      </div>
    </div>
  </section>

  <section id="buildinfo" class="section">
    <span class="kicker kicker-art">Foundation</span>
    <h2>build-info and artifact identity</h2>
    <p class="prose">Promotion only works because Artifactory records <strong>build-info</strong> - a metadata record (a JSON document) capturing which artifacts a build produced, which dependencies it consumed, and the environment it ran in. Think of it as the build's birth certificate. Artifacts are tracked by their <strong>checksum</strong> - a short fingerprint computed from the file's exact bytes (using the SHA-1 and SHA-256 hashing algorithms); if even one byte changes, the checksum changes, so it uniquely identifies that exact file. Combined with the <code>build.name</code> and <code>build.number</code> properties, Artifactory always knows an artifact's identity no matter what repository it currently sits in. <a href="https://docs.jfrog.com/integrations/docs/manage-builds" target="_blank" rel="noopener">JFrog - Manage builds</a>, <a href="https://docs.jfrog.com/artifactory/docs/build-integration" target="_blank" rel="noopener">Build integration</a>.</p>
    <ul class="feature-list">
      <li><b>Location-agnostic.</b> Because identity is the checksum + build coordinates, moving an artifact between repos doesn't lose its lineage.</li>
      <li><b>Full traceability.</b> From a release artifact you can walk back to the exact build, its dependencies, and its source commit.</li>
      <li><b>Required first step.</b> Your CI must <em>publish</em> build-info before you can promote that build. The JFrog CLI (<code>jf</code>, JFrog's command-line tool) does this with <code>jf rt build-publish</code> - here <code>rt</code> means "Artifactory" (its internal name was "rt").</li>
    </ul>
  </section>

  <section id="copymove" class="section">
    <span class="kicker">Choice</span>
    <h2>Copy vs. move - and properties</h2>
    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Option</th><th>Effect</th><th>When to use</th></tr></thead>
        <tbody>
          <tr><td><code>--copy=true</code></td><td>Duplicates artifacts into the target repo; originals stay in the source.</td><td>You want the artifact in both the staging and release repos (common).</td></tr>
          <tr><td><code>--copy=false</code> (move)</td><td>Relocates artifacts to the target; removes them from the source.</td><td>Strict single-home layouts where each stage owns its artifacts exclusively.</td></tr>
          <tr><td>Set properties</td><td>Stamps key/value properties on promoted artifacts (e.g. <code>stage=released</code>).</td><td>Driving downstream queries, watches, or cleanup policies.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="callout callout-tip">
      <p class="callout-title">Default to copy</p>
      <p>Copying keeps a clear audit trail at each stage and avoids surprises if a later gate fails. Use move only when you deliberately want a single physical home per maturity level.</p>
    </div>
  </section>

  <section id="cli" class="section">
    <span class="kicker kicker-lab">CLI</span>
    <h2>Promote a build with the JFrog CLI</h2>
    <p class="prose">The command is <code>jf rt build-promote</code> (alias <code>jf rt bpr</code> - an "alias" is just a shorter name for the same command). You name the build, its number, and the target repo, plus options for copy/move and the new status. <a href="https://jfrog.com/help/r/artifactory-rest-apis/build-promotion" target="_blank" rel="noopener">JFrog - Build promotion</a>.</p>
    <p class="code-label">Promote build "TestBuild" #49 to a release repo</p>
    <div class="codeblock"><code><span class="cm"># --status: new maturity label  | --copy=true: keep originals (false=move)</span>
<span class="cm"># --source-repo: where artifacts live now  | final args: build name, number, target repo</span>
jf rt build-promote \\
  --status=Released \\
  --copy=true \\
  --source-repo=staging-local \\
  TestBuild 49 release-local</code></div>
    <p class="prose muted">This copies build <code>TestBuild/49</code>'s artifacts from <code>staging-local</code> into <code>release-local</code> and marks the build status <code>Released</code>. Drop <code>--copy=true</code> (or set it false) to move instead.</p>
    <div class="callout callout-q">
      <p class="callout-title">Prerequisite</p>
      <p>The build must already be published to Artifactory: <code>jf rt build-publish TestBuild 49</code> after collecting build-info during your CI run. Only then is there a build to promote.</p>
    </div>
  </section>

  <section id="rest" class="section">
    <span class="kicker kicker-lab">REST</span>
    <h2>Promote a build via the REST API</h2>
    <p class="prose">CI systems that don't use the CLI can call the promotion endpoint directly. <a href="https://jfrog.com/help/r/artifactory-rest-apis/build-promotion" target="_blank" rel="noopener">JFrog - Build Promotion REST API</a>.</p>
    <p class="code-label">POST to the build-promote endpoint</p>
    <div class="codeblock"><code>POST /artifactory/api/build/promote/TestBuild/49
Authorization: Bearer &lt;access-token&gt;
Content-Type: application/json

{
  "status": "Released",
  "sourceRepo": "staging-local",
  "targetRepo": "release-local",
  "copy": true,
  "properties": { "stage": ["released"] }
}</code></div>
    <p class="prose muted">The path carries the build name and number; the JSON body carries everything else. See the <a href="rest-api.html">Artifactory REST API</a> page for auth details and the <code>jf api</code> shortcut.</p>
  </section>

  <section id="pattern" class="section">
    <span class="kicker">Pattern</span>
    <h2>The repository layout promotion assumes</h2>
    <figure class="flow" aria-label="Promotion across maturity repos">
      <div class="flow-row">
        <div class="flow-step flow-art"><span class="flow-step-n">1</span><b>dev-local</b><small>CI publishes here</small></div>
        <span class="flow-conn">→ promote →</span>
        <div class="flow-step flow-art"><span class="flow-step-n">2</span><b>staging-local</b><small>passes tests + Xray</small></div>
        <span class="flow-conn">→ promote →</span>
        <div class="flow-step flow-art"><span class="flow-step-n">3</span><b>release-local</b><small>production-approved</small></div>
      </div>
      <figcaption>Each arrow is a <code>build-promote</code> that advances status and (optionally) copies the same binary forward. An Xray <b>Watch</b> on each repo can gate the move. <a href="https://jfrog.com/help/r/get-started-with-the-jfrog-platform/onboarding-best-practices-jfrog-artifactory" target="_blank" rel="noopener">JFrog onboarding best practices</a>.</figcaption>
    </figure>
    <div class="callout callout-tip">
      <p class="callout-title">Tie it back to Xray</p>
      <p>The power move: a <a href="xray-policies-watches.html">Policy + Watch</a> on <code>staging-local</code> blocks promotion to <code>release-local</code> if a High/Critical CVE with an available fix is present. (A <b>CVE</b> - Common Vulnerabilities and Exposures - is a publicly catalogued security flaw, each with an ID like <code>CVE-2021-44228</code>.) Promotion becomes your enforced quality gate, not a manual courtesy. To write that rule and wire the Watch, see <a href="xray-policies-watches.html">Xray Policies &amp; Watches</a>.</p>
    </div>
  </section>
""",
}
_p["prev"], _p["next"] = chain(_p["file"])
PAGE_LIST.append(_p)


# =====================================================================
# 3) RELEASE BUNDLES & DISTRIBUTION
# =====================================================================
_p = {
 "file": "release-bundles.html",
 "title": "Release Bundles & Distribution",
 "desc": "Immutable, signed collections of artifacts and how JFrog Distribution ships them to edge nodes and air-gapped sites with verifiable provenance.",
 "badges": '<span class="lvl lvl-art">Artifactory</span><span class="lvl lvl-xray">Supply chain</span><span class="lvl">Deep-dive</span>',
 "h1": "Release Bundles &amp; Distribution",
 "lede": "A Release Bundle is a sealed, signed manifest of exactly which artifacts make up a release. JFrog Distribution then ships that bundle out to edge nodes and remote sites - so what arrives is provably identical to what you signed.",
 "sections": [
   {"id": "problem", "label": "The problem"},
   {"id": "bundle", "label": "What a Release Bundle is"},
   {"id": "lifecycle", "label": "Bundle lifecycle"},
   {"id": "distribution", "label": "Distribution & edge nodes"},
   {"id": "cli", "label": "Create & distribute (CLI)"},
   {"id": "vs", "label": "Bundle vs. promotion"},
 ],
 "body": """
  <section id="problem" class="section">
    <span class="kicker kicker-art">Concept</span>
    <h2>The problem Release Bundles solve</h2>
    <p class="prose">Promotion moves binaries <em>inside</em> one platform. But shipping a release <em>out</em> - to a customer site, an edge location, or an <b>air-gapped network</b> (a network with no internet connection at all, for security) - raises new questions: which exact files belong to "v2.4.0"? Were any swapped in transit? Can the receiving side prove <b>provenance</b> (a verifiable record of where each file came from and that it wasn't altered)? A loose folder of artifacts answers none of these.</p>
    <p class="prose">A <strong>Release Bundle</strong> is the answer: an <em>immutable</em> (can never be changed after creation), <em>signed</em> specification of the precise set of artifacts that make up a release, with a checksum-verified <b>manifest</b> (the packing list - it names every file and its checksum fingerprint). <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/release-lifecycle-management" target="_blank" rel="noopener">JFrog - Release Lifecycle Management</a>.</p>
  </section>

  <section id="bundle" class="section">
    <span class="kicker kicker-x">Definition</span>
    <h2>What's inside a Release Bundle</h2>
    <ul class="feature-list">
      <li><b>A curated artifact set.</b> You select the artifacts that make up the release - by build, by file path, or by an <b>AQL</b> query (Artifactory Query Language, a JSON-based search language for finding artifacts by name, property, repo, etc.). The bundle records each one's checksum.</li>
      <li><b>Immutability.</b> Once created, the bundle's contents can't change. A new release means a new bundle version.</li>
      <li><b>Cryptographic signing.</b> The bundle manifest is signed with a <b>GPG key</b> (GPG = GNU Privacy Guard, a standard tool for cryptographic signatures). The signer holds a private key; recipients hold the matching public key and use it to confirm the bundle came from you and wasn't tampered with.</li>
      <li><b>Provenance metadata.</b> The bundle carries the source build-info and (optionally) Xray security-scan results, giving the receiver evidence of exactly what was built and what was vetted.</li>
    </ul>
    <div class="analogy analogy-x">
      <span class="analogy-icon" aria-hidden="true">📜</span>
      <div>
        <p class="analogy-title">One-sentence analogy</p>
        <p>A Release Bundle is a <strong>tamper-evident shipping manifest with a wax seal</strong>. It lists every item in the crate, and the seal proves nobody opened it between the warehouse and the customer's loading dock.</p>
      </div>
    </div>
  </section>

  <section id="lifecycle" class="section">
    <span class="kicker">Flow</span>
    <h2>The bundle lifecycle</h2>
    <figure class="flow" aria-label="Release bundle lifecycle">
      <div class="flow-row">
        <div class="flow-step flow-art"><span class="flow-step-n">1</span><b>Create</b><small>select artifacts → sign</small></div>
        <span class="flow-conn">→</span>
        <div class="flow-step flow-art"><span class="flow-step-n">2</span><b>Sign</b><small>GPG-signed manifest</small></div>
        <span class="flow-conn">→</span>
        <div class="flow-step flow-xray"><span class="flow-step-n">3</span><b>Distribute</b><small>push to edge nodes</small></div>
        <span class="flow-conn">→</span>
        <div class="flow-step"><span class="flow-step-n">4</span><b>Verify &amp; consume</b><small>checksum-checked on arrival</small></div>
      </div>
      <figcaption>The bundle is created and sealed once, then distributed to one or many targets. Each target verifies signatures and checksums before exposing the artifacts. <a href="https://jfrog.com/help/r/jfrog-distribution-documentation/distributing-release-bundles" target="_blank" rel="noopener">JFrog - Distributing Release Bundles</a>.</figcaption>
    </figure>
  </section>

  <section id="distribution" class="section">
    <span class="kicker kicker-x">Distribution</span>
    <h2>Distribution &amp; edge nodes</h2>
    <p class="prose"><strong>JFrog Distribution</strong> is the service that takes a signed Release Bundle and delivers it to <strong>edge nodes</strong> - lightweight Artifactory instances positioned close to consumers (a factory floor, a CDN POP, an air-gapped enclave). Edge nodes are read-only consumption points: they receive distributed bundles but aren't general-purpose repositories. <a href="https://jfrog.com/help/r/jfrog-distribution-documentation/jfrog-distribution" target="_blank" rel="noopener">JFrog Distribution docs</a>.</p>
    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Component</th><th>Role</th></tr></thead>
        <tbody>
          <tr><td><b>Distribution service</b></td><td>Orchestrates creating, signing, and shipping bundles to targets.</td></tr>
          <tr><td><b>Edge node</b></td><td>A consumption-only Artifactory at the destination that hosts distributed bundles.</td></tr>
          <tr><td><b>Distribution target</b></td><td>The rule selecting which edge node(s) a given bundle goes to.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="callout callout-tip">
      <p class="callout-title">Why edge nodes matter</p>
      <p>Consumers at the edge pull from a nearby node - fast and resilient - while you keep a single signed source of truth centrally. Air-gapped sites receive the bundle as a verifiable package rather than opening a live connection to your main platform.</p>
    </div>
  </section>

  <section id="cli" class="section">
    <span class="kicker kicker-lab">CLI</span>
    <h2>Create and distribute a bundle (CLI)</h2>
    <p class="prose">The JFrog CLI exposes release-bundle commands under <code>jf rbc</code> / <code>jf rbu</code> (create/update) and <code>jf rbd</code> (distribute) - these short names are just aliases for the longer commands below. The conceptual flow: <a href="https://jfrog.com/help/r/jfrog-cli/release-bundles" target="_blank" rel="noopener">JFrog CLI - Release Bundles</a>.</p>
    <p class="code-label">Create a signed bundle from a spec, then distribute</p>
    <div class="codeblock"><code><span class="cm"># 1. Create release bundle "my-app" v2.4.0 from a spec file.</span>
<span class="cm">#    --spec: JSON listing which artifacts to include (by path/AQL)</span>
<span class="cm">#    --signing-key: the GPG key that signs (seals) the manifest</span>
jf release-bundle-create my-app 2.4.0 \\
  --spec=release-spec.json \\
  --signing-key=my-gpg-key

<span class="cm"># 2. Distribute it to every edge node matching the pattern (* is a wildcard)</span>
jf release-bundle-distribute my-app 2.4.0 \\
  --site="edge-eu-*"</code></div>
    <p class="prose muted">The spec selects artifacts (by AQL/path); the signing key seals the manifest; the distribute step fans it out to matching edge sites. Exact subcommands vary by Release Lifecycle Management version - check the linked CLI reference for your platform.</p>
  </section>

  <section id="vs" class="section">
    <span class="kicker">Compare</span>
    <h2>Release Bundle vs. build promotion</h2>
    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Aspect</th><th>Build promotion</th><th>Release Bundle + Distribution</th></tr></thead>
        <tbody>
          <tr><td>Scope</td><td>Within one platform</td><td>Across platforms / out to edges</td></tr>
          <tr><td>Mutability</td><td>Status changes over time</td><td>Immutable once signed</td></tr>
          <tr><td>Integrity proof</td><td>Checksum tracking</td><td>GPG-signed manifest</td></tr>
          <tr><td>Primary goal</td><td>Advance maturity stage</td><td>Ship a sealed release safely</td></tr>
          <tr><td>Air-gap friendly</td><td><b class="no">No</b></td><td><b class="yes">Yes</b></td></tr>
        </tbody>
      </table>
    </div>
    <p class="prose muted">They compose: promote a build to <code>release-local</code> with an Xray gate (see <a href="build-promotion.html">Build promotion</a>), then bundle and distribute that vetted set to the edge.</p>
  </section>
""",
}
_p["prev"], _p["next"] = chain(_p["file"])
PAGE_LIST.append(_p)


# =====================================================================
# 4) ARTIFACTORY REST API
# =====================================================================
_p = {
 "file": "rest-api.html",
 "title": "Artifactory REST API",
 "desc": "Authentication, the most useful Artifactory REST endpoints, and how to drive them from curl and the JFrog CLI to automate repos, users, and more.",
 "badges": '<span class="lvl lvl-art">Artifactory</span><span class="lvl" style="color:var(--low);border-color:color-mix(in oklab,var(--low) 40%,var(--border))">Integration</span><span class="lvl lvl-lab">Reference</span>',
 "h1": "The Artifactory REST API",
 "lede": "Everything you can click in the UI, you can automate over HTTP. This page covers how to authenticate, the endpoints you'll actually use, and how to call them from curl and the JFrog CLI's built-in API shortcut.",
 "sections": [
   {"id": "auth", "label": "Authentication"},
   {"id": "endpoints", "label": "Key endpoints"},
   {"id": "curl", "label": "Calling with curl"},
   {"id": "jfapi", "label": "The jf api shortcut"},
   {"id": "create", "label": "Create a repo via API"},
   {"id": "best", "label": "Best practices"},
 ],
 "body": """
  <section id="auth" class="section">
    <span class="kicker">Foundation</span>
    <h2>Authentication - three ways in</h2>
    <div class="callout callout-q">
      <p class="callout-title">New to APIs? Start here</p>
      <p>An <b>API</b> (Application Programming Interface) is a way for programs to talk to Artifactory instead of a human clicking the web UI. <b>REST</b> is the most common style of web API: you send an <b>HTTP request</b> (the same protocol your browser uses) to a URL called an <b>endpoint</b>, using a <b>method</b> that states your intent - <code>GET</code> (read), <code>POST</code> (create), <code>PUT</code> (create/replace), <code>DELETE</code> (remove). Artifactory replies with <b>JSON</b> (a simple text format for structured data). That's the whole idea: a URL + a method + (sometimes) a JSON body.</p>
    </div>
    <p class="prose">Every Artifactory REST call needs to identify you (this is <b>authentication</b> - proving who you are). There are three accepted methods; pick access tokens for automation. <a href="https://jfrog.com/help/r/jfrog-platform-rest-apis/introduction-to-the-jfrog-platform-rest-apis" target="_blank" rel="noopener">JFrog - Intro to the REST APIs</a>.</p>
    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Method</th><th>How it's sent</th><th>Use when</th></tr></thead>
        <tbody>
          <tr><td><b>Access token</b> (recommended)</td><td><code>Authorization: Bearer &lt;token&gt;</code> - an HTTP header you attach to the request; "Bearer" just means "whoever carries this token is allowed in"</td><td>Any automation - scoped, revocable, no password exposure.</td></tr>
          <tr><td>Basic auth</td><td><code>-u user:password</code></td><td>Quick local tests only; avoid in scripts.</td></tr>
          <tr><td>API key</td><td><code>X-JFrog-Art-Api: &lt;key&gt;</code></td><td>Legacy integrations (being phased out in favor of tokens).</td></tr>
        </tbody>
      </table>
    </div>
    <p class="prose muted">See the <a href="access-tokens.html">Access tokens &amp; permissions</a> page for how to mint and scope a token.</p>
  </section>

  <section id="endpoints" class="section">
    <span class="kicker kicker-lab">Reference</span>
    <h2>The endpoints you'll actually use</h2>
    <div class="table-wrap">
      <table class="datatable mono-table">
        <thead><tr><th>Endpoint</th><th>Method</th><th>Does</th></tr></thead>
        <tbody>
          <tr><td><code>/artifactory/api/system/ping</code></td><td>GET</td><td>Health check - returns <code>OK</code>.</td></tr>
          <tr><td><code>/artifactory/api/repositories</code></td><td>GET</td><td>List all repositories.</td></tr>
          <tr><td><code>/artifactory/api/repositories/&lt;key&gt;</code></td><td>PUT</td><td>Create/configure a repository.</td></tr>
          <tr><td><code>/artifactory/api/repositories/&lt;key&gt;</code></td><td>GET</td><td>Read one repo's config.</td></tr>
          <tr><td><code>/artifactory/api/storage/&lt;repo&gt;/&lt;path&gt;</code></td><td>GET</td><td>File/folder info &amp; metadata.</td></tr>
          <tr><td><code>/artifactory/api/build/promote/&lt;name&gt;/&lt;num&gt;</code></td><td>POST</td><td>Promote a build (see Build promotion).</td></tr>
          <tr><td><code>/access/api/v1/users/&lt;username&gt;</code></td><td>GET/PUT</td><td>Manage a user.</td></tr>
          <tr><td><code>/access/api/v1/groups/&lt;group&gt;</code></td><td>GET/PUT</td><td>Manage a group.</td></tr>
          <tr><td><code>/access/api/v1/tokens</code></td><td>POST</td><td>Create an access token.</td></tr>
        </tbody>
      </table>
    </div>
    <p class="prose muted">Note the two base paths: <code>/artifactory/api/...</code> for repository/storage operations, and <code>/access/api/...</code> for identity (users, groups, tokens). Sources: <a href="https://jfrog.com/help/r/jfrog-platform-rest-apis/introduction-to-the-jfrog-platform-rest-apis" target="_blank" rel="noopener">JFrog REST APIs</a>, <a href="https://www.devopsschool.com/blog/artifactory-artifactory-7-x-rest-api-quickstart/" target="_blank" rel="noopener">REST quickstart</a>.</p>
  </section>

  <section id="curl" class="section">
    <span class="kicker kicker-lab">How-to</span>
    <h2>Calling the API with curl</h2>
    <p class="prose"><code>curl</code> is a built-in command-line tool for making HTTP requests. <code>-H</code> attaches a header; <code>$JF_TOKEN</code> reads your token from an environment variable so it never appears in the command itself.</p>
    <p class="code-label">Health check</p>
    <div class="codeblock"><code><span class="cm"># -H attaches the auth header; the URL is the endpoint we call</span>
curl -H "Authorization: Bearer $JF_TOKEN" \\
  https://yourname.jfrog.io/artifactory/api/system/ping
<span class="cm"># → the server replies: OK</span></code></div>
    <p class="code-label">List every repository as JSON</p>
    <div class="codeblock"><code><span class="cm"># jq (a JSON tool) pretty-prints the reply</span>
curl -H "Authorization: Bearer $JF_TOKEN" \\
  https://yourname.jfrog.io/artifactory/api/repositories | jq .</code></div>
    <div class="callout callout-tip">
      <p class="callout-title">Put the token in an env var</p>
      <p>Never paste tokens inline in shared scripts. Export <code>JF_TOKEN</code> once (ideally from a secret manager) and reference it. Rotate it on a schedule.</p>
    </div>
  </section>

  <section id="jfapi" class="section">
    <span class="kicker kicker-lab">Shortcut</span>
    <h2>The <code>jf api</code> shortcut</h2>
    <p class="prose">If you've already configured a server with <code>jf c add</code> ("c" = config; this stores your server URL and token once), the CLI can call any Artifactory REST endpoint <em>using those stored credentials</em> - so you never type an auth header again. <a href="https://docs.jfrog.com/integrations/docs/use-api-endpoints-via-cli" target="_blank" rel="noopener">JFrog - Use API endpoints via CLI</a>.</p>
    <p class="code-label">Same "list repositories" call, authenticated automatically</p>
    <div class="codeblock"><code>jf rt curl -XGET /api/repositories
<span class="cm"># or the generic platform call:</span>
jf api /artifactory/api/repositories</code></div>
    <p class="prose muted">This is the fastest way to script against Artifactory during your labs: configure once, then drive any endpoint without juggling tokens in every command.</p>
  </section>

  <section id="create" class="section">
    <span class="kicker kicker-lab">Worked example</span>
    <h2>Create a local Docker repo via the API</h2>
    <p class="code-label">PUT a repository configuration</p>
    <div class="codeblock"><code><span class="cm"># -XPUT = PUT method (create/replace). The URL ends in the new repo's key (name).</span>
<span class="cm"># -d sends the JSON body below. rclass = repo class (local/remote/virtual).</span>
curl -XPUT -H "Authorization: Bearer $JF_TOKEN" \\
  -H "Content-Type: application/json" \\
  https://yourname.jfrog.io/artifactory/api/repositories/docker-local \\
  -d '{
    "rclass": "local",
    "packageType": "docker"
  }'</code></div>
    <p class="prose muted">Swap <code>"rclass": "remote"</code> plus a <code>"url"</code> field for a proxy repo, or <code>"virtual"</code> with a <code>"repositories"</code> list to aggregate several repos behind one. This is exactly what the UI's "Add Repository" form does under the hood. (If "local / remote / virtual" is new, see the <a href="fundamentals.html">Fundamentals</a> page.)</p>
  </section>

  <section id="best" class="section">
    <span class="kicker">Guidance</span>
    <h2>Best practices</h2>
    <ul class="feature-list">
      <li><b>Use access tokens, never passwords</b> in automation - they're scoped and revocable.</li>
      <li><b>Prefer <code>jf api</code> / <code>jf rt curl</code></b> in CLI contexts so credentials stay in CLI config, not your shell history.</li>
      <li><b>Check <code>/system/ping</code> first</b> in scripts to fail fast on connectivity/auth problems.</li>
      <li><b>Treat config-as-code.</b> Keep repo-creation JSON in version control so your platform is reproducible.</li>
      <li><b>Rotate tokens</b> and scope them to the minimum permission target needed (see <a href="access-tokens.html">Access tokens</a>).</li>
    </ul>
  </section>
""",
}
_p["prev"], _p["next"] = chain(_p["file"])
PAGE_LIST.append(_p)


# =====================================================================
# 5) FROGBOT & IDE INTEGRATION
# =====================================================================
_p = {
 "file": "frogbot.html",
 "title": "Frogbot & IDE",
 "desc": "Frogbot is a Git bot that scans pull requests with JFrog Xray and opens fix PRs automatically. Plus IDE plugins that flag vulnerabilities as you code.",
 "badges": '<span class="lvl lvl-xray">Xray</span><span class="lvl">Shift-left</span><span class="lvl lvl-lab">How-to</span>',
 "h1": "Frogbot &amp; IDE integration",
 "lede": "Shift security as far left as it goes: Frogbot scans every pull request with Xray and can open fix PRs on its own, while the JFrog IDE plugins flag vulnerable dependencies while you're still typing.",
 "sections": [
   {"id": "what", "label": "What Frogbot is"},
   {"id": "modes", "label": "PR scan vs. repo scan"},
   {"id": "setup", "label": "Setup on GitHub Actions"},
   {"id": "yaml", "label": "The workflow YAML"},
   {"id": "ide", "label": "IDE integration"},
 ],
 "body": """
  <section id="what" class="section">
    <span class="kicker kicker-x">Concept</span>
    <h2>What Frogbot is</h2>
    <div class="callout callout-q">
      <p class="callout-title">Two terms first: PR and "shift-left"</p>
      <p>A <b>pull request (PR)</b> is how you propose changes on GitHub/GitLab - you push your branch and open a PR asking to merge it, so teammates (and bots) can review it before it lands. <b>"Shift-left"</b> means catching problems as early as possible in the development timeline (drawn left-to-right), because the earlier you catch a bug or vulnerability, the cheaper it is to fix.</p>
    </div>
    <p class="prose"><strong>Frogbot is a Git bot that scans your pull requests and repositories for security vulnerabilities using JFrog Xray</strong> (Xray is JFrog's security scanner). When a developer opens a PR, Frogbot scans it and posts the results as a comment (JFrog calls this a "decoration") directly on the PR - and if it finds no new issues, it says so. It works with GitHub, GitLab, Bitbucket, and Azure Repos. <a href="https://github.com/jfrog/frogbot" target="_blank" rel="noopener">jfrog/frogbot</a>.</p>
    <ul class="feature-list">
      <li><b>Only flags <em>new</em> issues.</b> A PR scan compares the project state before and after the change, so it reports only vulnerabilities the PR introduces - not pre-existing noise.</li>
      <li><b>Opens fix PRs.</b> When fixable issues are found and auto-fix is enabled, Frogbot opens a pull request that upgrades the vulnerable dependency to a fixed version.</li>
      <li><b>Requires Xray 3.29.0+.</b> Frogbot uses your JFrog platform's Xray to do the actual scanning. <a href="https://docs.jfrog.com/security/docs/how-to-commit-scan-and-pr-scan" target="_blank" rel="noopener">JFrog - Commit &amp; PR scan</a>.</li>
    </ul>
  </section>

  <section id="modes" class="section">
    <span class="kicker">Two modes</span>
    <h2>Pull-request scan vs. repository scan</h2>
    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Mode</th><th>Command</th><th>What it does</th></tr></thead>
        <tbody>
          <tr><td><b>Pull Request</b></td><td><code>frogbot scan-pull-request</code></td><td>Scans a PR by diffing before/after the change. Only <em>new</em> issues are reported, as PR comments.</td></tr>
          <tr><td><b>Repository (commit) scan</b></td><td><code>frogbot scan-repository</code></td><td>Scans the latest commit of a branch for all existing vulnerabilities. With auto-fix on, opens fix PRs for upgradable dependencies.</td></tr>
        </tbody>
      </table>
    </div>
    <p class="prose muted">Source: <a href="https://docs.jfrog.com/security/docs/how-to-commit-scan-and-pr-scan" target="_blank" rel="noopener">JFrog - Scanning Commits and Pull Requests</a>.</p>
    <div class="callout callout-tip">
      <p class="callout-title">Required environment variables</p>
      <p>An "environment variable" is a named value the running job can read. Both modes need <code>JF_URL</code> (your platform URL, e.g. <code>https://my.jfrog.io</code>) and <code>JF_ACCESS_TOKEN</code> (a scoped access token - see the <a href="access-tokens.html">Access tokens</a> page), plus a Git token (<code>JF_GIT_TOKEN</code> / the CI's built-in token) so Frogbot has permission to comment and open PRs on your repo.</p>
    </div>
  </section>

  <section id="setup" class="section">
    <span class="kicker kicker-lab">How-to</span>
    <h2>Setting up Frogbot on GitHub Actions</h2>
    <ol class="steps">
      <li><b>Allow Frogbot to open PRs.</b> In GitHub → <em>Settings → Actions → General</em>, check <b>"Allow GitHub Actions to create and approve pull requests."</b></li>
      <li><b>(Recommended for OSS) Create a <code>frogbot</code> environment.</b> Settings → <em>Environments</em> → New environment named <code>frogbot</code>, and add reviewers. Those reviewers must approve before Frogbot scans a PR - a safety gate for public repos.</li>
      <li><b>Add the workflow file.</b> Drop a Frogbot workflow into <code>.github/workflows/</code> (template below), or use the JFrog GitHub App to have it opened for you automatically across selected repos.</li>
      <li><b>Add secrets/vars.</b> Provide <code>JF_URL</code> and <code>JF_ACCESS_TOKEN</code> as repository secrets. The built-in <code>GITHUB_TOKEN</code> covers Git operations.</li>
    </ol>
    <p class="prose muted">Sources: <a href="https://jfrog.com/help/r/jfrog-security-user-guide/shift-left-on-security/frogbot/installation/github-actions/installation" target="_blank" rel="noopener">JFrog - Frogbot GitHub Actions install</a>, <a href="https://docs.jfrog.com/integrations/docs/github-actions-frogbot-bulk-installation" target="_blank" rel="noopener">JFrog GitHub App bulk install</a>.</p>
  </section>

  <section id="yaml" class="section">
    <span class="kicker kicker-lab">YAML</span>
    <h2>The PR-scan workflow</h2>
    <p class="prose">A minimal GitHub Actions workflow that runs Frogbot on every pull request. A "workflow" is a YAML file in <code>.github/workflows/</code> that GitHub runs automatically when a trigger fires. <b>YAML</b> is an indentation-based config format - indentation (spaces, never tabs) defines the nesting. <a href="https://jfrog.com/help/r/jfrog-and-github-integration-guide/github-pr-scans-and-advanced-security" target="_blank" rel="noopener">JFrog - GitHub PR scans</a>.</p>
    <div class="codeblock"><code>name: "Frogbot Scan Pull Request"   <span class="cm"># label shown in the Actions tab</span>
on:                                  <span class="cm"># what triggers this workflow</span>
  pull_request_target:               <span class="cm"># run when a PR is opened/updated</span>
    types: [ opened, synchronize ]   <span class="cm"># "synchronize" = new commits pushed to the PR</span>

permissions:                         <span class="cm"># what the job is allowed to do</span>
  pull-requests: write               <span class="cm"># needed to post the scan comment</span>
  contents: read                     <span class="cm"># read the repo files to scan them</span>
  id-token: write

jobs:
  scan-pull-request:
    runs-on: ubuntu-latest           <span class="cm"># the VM type GitHub runs the job on</span>
    <span class="cm"># PR must be approved by a "frogbot" environment reviewer before scanning</span>
    environment: frogbot
    steps:
      - uses: jfrog/frogbot@v2       <span class="cm"># the official Frogbot action, version 2</span>
        env:                         <span class="cm"># env vars passed to Frogbot</span>
          JF_URL: ${{ vars.JF_URL }}                    <span class="cm"># vars.* = a repo variable (not secret)</span>
          JF_ACCESS_TOKEN: ${{ secrets.JF_ACCESS_TOKEN }} <span class="cm"># secrets.* = an encrypted repo secret</span>
          JF_GIT_TOKEN: ${{ secrets.GITHUB_TOKEN }}      <span class="cm"># auto-provided by GitHub Actions</span></code></div>
    <p class="prose muted">For the repository (auto-fix) mode, use a separate workflow triggered on push to your default branch (or on a schedule) that runs Frogbot in <code>scan-repository</code> mode. <a href="https://jfrog.com/help/r/jfrog-and-github-integration-guide/configure-frogbot-in-github-actions" target="_blank" rel="noopener">Configure Frogbot in GitHub Actions</a>.</p>
  </section>

  <section id="ide" class="section">
    <span class="kicker kicker-x">Shift-left</span>
    <h2>IDE integration - catch it before the PR</h2>
    <p class="prose">Even earlier than the PR is the editor. JFrog ships plugins for <strong>VS Code, IntelliJ/JetBrains IDEs, Visual Studio, and Eclipse</strong> that scan your project's dependencies against Xray and surface vulnerabilities inline as you work. <a href="https://docs.jfrog.com/security/docs/ide-integrations" target="_blank" rel="noopener">JFrog - IDE integrations</a>.</p>
    <div class="cards cards-x">
      <div class="card"><h3>🧩 Inline findings</h3><p>Vulnerable dependencies are highlighted in your dependency files with severity and details, without leaving the editor.</p></div>
      <div class="card"><h3>🔗 Connect to your JPD</h3><p>Point the plugin at your JFrog platform URL + an access token; it uses your Xray for the database and policies.</p></div>
      <div class="card"><h3>⏪ Earliest feedback</h3><p>Fix issues before you even commit - the cheapest place to fix anything is in the editor.</p></div>
    </div>
    <div class="callout callout-tip">
      <p class="callout-title">The shift-left ladder</p>
      <p><b>IDE plugin</b> (as you type) → <b>Frogbot</b> (on the PR) → <b>Xray indexing + <a href="xray-policies-watches.html">Watch</a></b> (in Artifactory) → <b>build-scan gate</b> (in CI). Each rung catches issues later and more expensively, so push detection as far left as you can. The Watch and the policies behind every rung are covered in <a href="xray-policies-watches.html">Xray Policies &amp; Watches</a>.</p>
    </div>
  </section>
""",
}
_p["prev"], _p["next"] = chain(_p["file"])
PAGE_LIST.append(_p)


# =====================================================================
# 6) JFROG PIPELINES
# =====================================================================
_p = {
 "file": "pipelines.html",
 "title": "JFrog Pipelines",
 "desc": "JFrog's YAML-based CI/CD engine: integrations, resources, steps, and pipeline sources. Build a working pipeline from a Hello World example up.",
 "badges": '<span class="lvl lvl-lab">CI/CD</span><span class="lvl lvl-art">Platform</span><span class="lvl">How-to</span>',
 "h1": "JFrog Pipelines",
 "lede": "Pipelines is the platform's native CI/CD engine. You declare resources and steps in a YAML DSL stored in your Git repo, connect it through integrations, and Pipelines runs it on build nodes - with Artifactory and Xray built in.",
 "sections": [
   {"id": "what", "label": "What Pipelines is"},
   {"id": "concepts", "label": "Core building blocks"},
   {"id": "dsl", "label": "The YAML DSL"},
   {"id": "steps", "label": "First pipeline (steps)"},
   {"id": "example", "label": "Hello World example"},
 ],
 "body": """
  <section id="what" class="section">
    <span class="kicker kicker-lab">Concept</span>
    <h2>What JFrog Pipelines is</h2>
    <div class="callout callout-q">
      <p class="callout-title">Plain-English glossary for this page</p>
      <p><b>CI/CD</b> = Continuous Integration / Continuous Delivery: automating the build &rarr; test &rarr; ship cycle. <b>DSL</b> = Domain-Specific Language: a small, purpose-built language (here, written in YAML) for describing pipelines. <b>Build node</b> = a machine (or container) that actually runs your pipeline steps. <b>YAML</b> = an indentation-based text config format.</p>
    </div>
    <p class="prose"><strong>JFrog Pipelines is a CI/CD automation engine built into the JFrog Platform.</strong> You define pipelines in a <strong>YAML-based Pipelines DSL</strong> - a set of key-value files known as a <em>pipeline config</em> - and store them in a Git-compatible source repository (any repo on GitHub, GitLab, etc.). Pipelines syncs from that source, loads your DSL, and runs continuous integration and delivery on build nodes. <a href="https://jfrog.com/help/r/jfrog-pipelines-documentation/creating-pipelines" target="_blank" rel="noopener">JFrog - Creating Pipelines</a>.</p>
    <div class="callout callout-q">
      <p class="callout-title">How is this different from GitHub Actions?</p>
      <p>Both run YAML-defined CI/CD. Pipelines' edge is native integration with Artifactory (build-info, promotion) and Xray (scanning gates) plus centrally-managed, secure integrations and reusable resources. If you already live in the JFrog platform, Pipelines keeps everything in one place. You can also combine it with Jenkins, GitHub Actions, or Azure DevOps.</p>
    </div>
  </section>

  <section id="concepts" class="section">
    <span class="kicker">Building blocks</span>
    <h2>The core building blocks</h2>
    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Concept</th><th>What it is</th></tr></thead>
        <tbody>
          <tr><td><b>Integration</b></td><td>A stored, secure connection to an external service - GitHub, Artifactory, Kubernetes, etc. You provide the URL endpoint and credentials once; Pipelines stores them centrally.</td></tr>
          <tr><td><b>Pipeline source</b></td><td>The Git repo (added via an integration) that holds your YAML DSL. Pipelines auto-syncs whenever you commit a change to the DSL.</td></tr>
          <tr><td><b>Resource</b></td><td>A source or destination of data used by the pipeline - e.g. a <code>GitRepo</code>, a <code>BuildInfo</code>, an image. Resources connect steps and can trigger them.</td></tr>
          <tr><td><b>Step</b></td><td>A unit of execution (e.g. a <code>Bash</code> step). Steps declare <code>inputResources</code> and <code>inputSteps</code> to express dependencies and ordering.</td></tr>
          <tr><td><b>Pipeline</b></td><td>The named collection of steps and resources that together form a workflow.</td></tr>
        </tbody>
      </table>
    </div>
    <p class="prose muted">Sources: <a href="https://jfrog.com/help/r/jfrog-pipelines-documentation/pipeline-example-hello-world" target="_blank" rel="noopener">JFrog - Pipeline Hello World</a>, <a href="https://jfrog.com/help/r/jfrog-pipelines-documentation/pipelines-step-by-step" target="_blank" rel="noopener">Pipelines step-by-step</a>.</p>
  </section>

  <section id="dsl" class="section">
    <span class="kicker kicker-lab">DSL</span>
    <h2>The YAML DSL: resources + steps</h2>
    <p class="prose">A pipeline config has two main sections. <strong>Resources</strong> declare the data sources/destinations; <strong>pipelines</strong> declare the steps that act on them. Steps wire together via <code>inputSteps</code> (run after) and <code>inputResources</code> (consume/produce). <a href="https://jfrog.com/help/r/jfrog-pipelines-documentation/pipeline-workflow-examples" target="_blank" rel="noopener">JFrog - Workflow examples</a>.</p>
    <p class="code-label">A step that runs after another step succeeds</p>
    <div class="codeblock"><code>pipelines:
  - name: demo_pipeline
    steps:
      - name: build_step
        type: Bash
        configuration:
          inputResources:
            - name: my_git_repo      <span class="cm"># a GitRepo resource</span>
        execution:
          onExecute:
            - echo "building…"

      - name: publish_step
        type: Bash
        configuration:
          inputSteps:
            - name: build_step       <span class="cm"># runs only after build_step</span>
        execution:
          onExecute:
            - echo "publishing build-info to Artifactory"</code></div>
  </section>

  <section id="steps" class="section">
    <span class="kicker kicker-lab">How-to</span>
    <h2>Standing up your first pipeline</h2>
    <ol class="steps">
      <li><b>Sign in</b> to the JFrog Platform with your Artifactory credentials. On JFrog Cloud, a default dynamic node pool is provisioned for you (a "node pool" is a group of build machines that scale up/down on demand), so you already have build nodes - nothing to install.</li>
      <li><b>Add a GitHub integration.</b> Administration → Pipelines → <b>Integrations</b> → add a GitHub integration with a personal access token (a GitHub token that grants API access) that has the <code>repo</code> + <code>admin</code> <b>scopes</b> (a "scope" is a permission the token is allowed to use).</li>
      <li><b>Add a pipeline source.</b> Point Pipelines at the repo (and branch) holding your YAML DSL, connected through that integration. Pipelines syncs and processes the DSL.</li>
      <li><b>Commit DSL changes.</b> Every commit to the YAML re-syncs the source and reloads the pipeline.</li>
      <li><b>Run it.</b> Trigger manually or via a <code>GitRepo</code> resource that fires steps when the repo changes.</li>
    </ol>
    <p class="prose muted">Source: <a href="https://jfrog.com/help/r/jfrog-pipelines-documentation/pipeline-example-hello-world" target="_blank" rel="noopener">JFrog - Pipeline Example: Hello World</a>.</p>
  </section>

  <section id="example" class="section">
    <span class="kicker">Worked example</span>
    <h2>The "Hello World" example, end to end</h2>
    <figure class="flow" aria-label="Hello World pipeline flow">
      <div class="flow-row">
        <div class="flow-step"><span class="flow-step-n">1</span><b>Fork example repo</b><small>jfrog-pipelines-simple-example</small></div>
        <span class="flow-conn">→</span>
        <div class="flow-step flow-art"><span class="flow-step-n">2</span><b>Add GitHub integration</b><small>token w/ repo+admin scope</small></div>
        <span class="flow-conn">→</span>
        <div class="flow-step flow-art"><span class="flow-step-n">3</span><b>Add pipeline source</b><small>points at the YAML</small></div>
        <span class="flow-conn">→</span>
        <div class="flow-step"><span class="flow-step-n">4</span><b>Sync &amp; run</b><small>GitRepo trigger fires steps</small></div>
      </div>
      <figcaption>The official Hello World demonstrates a GitHub integration, a pipeline source, a <code>GitRepo</code> trigger, and <code>inputResources</code>/<code>inputSteps</code> dependencies. Fork the JFrog example repo, update the path values, commit, and watch it run. <a href="https://jfrog.com/help/r/jfrog-pipelines-documentation/pipeline-example-hello-world" target="_blank" rel="noopener">JFrog - Hello World</a>.</figcaption>
    </figure>
    <div class="callout callout-tip">
      <p class="callout-title">Where Artifactory &amp; Xray plug in</p>
      <p>Add a <code>BuildInfo</code> resource to publish build-info to Artifactory, then a promotion step (see <a href="build-promotion.html">Build promotion</a>) gated by an Xray scan. That turns a plain CI pipeline into a secured, traceable delivery pipeline - the whole point of doing CI <em>inside</em> JFrog.</p>
    </div>
  </section>
""",
}
_p["prev"], _p["next"] = chain(_p["file"])
PAGE_LIST.append(_p)


# =====================================================================
# 7) ACCESS TOKENS & PERMISSIONS
# =====================================================================
_p = {
 "file": "access-tokens.html",
 "title": "Access tokens & permissions",
 "desc": "How JFrog identity works: access tokens (scoped, revocable), users, groups, and permission targets that grant fine-grained access to repos, builds, and release bundles.",
 "badges": '<span class="lvl lvl-art">Platform</span><span class="lvl lvl-xray">Security</span><span class="lvl lvl-lab">How-to</span>',
 "h1": "Access tokens &amp; permissions",
 "lede": "Authentication answers \u201cwho are you?\u201d; authorization answers \u201cwhat may you touch?\u201d JFrog uses access tokens for the first and a Users \u2192 Groups \u2192 Permission Targets hierarchy for the second. Get this model right and everything else - the REST API, Frogbot, CI - falls into place.",
 "sections": [
   {"id": "tokens", "label": "Access tokens"},
   {"id": "types", "label": "Token scopes"},
   {"id": "create", "label": "Creating a token"},
   {"id": "model", "label": "Users, groups, targets"},
   {"id": "targets", "label": "Permission targets"},
   {"id": "howto", "label": "Set up permissions"},
 ],
 "body": """
  <section id="tokens" class="section">
    <span class="kicker kicker-art">Concept</span>
    <h2>Access tokens - the modern way to authenticate</h2>
    <div class="callout callout-q">
      <p class="callout-title">Authentication vs. authorization</p>
      <p>Two words that sound alike but mean different things. <b>Authentication</b> = proving <em>who you are</em> (done with an access token). <b>Authorization</b> = deciding <em>what you're allowed to do</em> (done with the permissions model later on this page). A token gets you in the door; permissions decide which rooms you can enter.</p>
    </div>
    <p class="prose">An <strong>access token</strong> is a signed credential that identifies you (or a service) to the JFrog Platform. Unlike a password, a token is <em>scoped</em> (it can be limited to specific resources - "scope" = the set of things it's allowed to touch), <em>revocable</em> (you can kill it without changing your password), and <em>expirable</em> (it can auto-die after a set time). That makes tokens the right choice for CI jobs, the REST API, Frogbot, and IDE plugins. <a href="https://jfrog.com/help/r/jfrog-platform-administration-documentation/access-tokens" target="_blank" rel="noopener">JFrog - Access Tokens</a>.</p>
    <ul class="feature-list">
      <li><b>No password exposure.</b> A leaked token can be revoked in isolation; your account password is never embedded in scripts.</li>
      <li><b>Scoped to least privilege.</b> Grant a token only the access a given job actually needs.</li>
      <li><b>Sent as a Bearer header.</b> Every authenticated REST call uses <code>Authorization: Bearer &lt;token&gt;</code> (see the <a href="rest-api.html">REST API</a> page).</li>
    </ul>
  </section>

  <section id="types" class="section">
    <span class="kicker">Scopes</span>
    <h2>Token scopes: user, admin, and custom</h2>
    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Scope</th><th>What it grants</th><th>Use for</th></tr></thead>
        <tbody>
          <tr><td><b>User</b></td><td>The same permissions the named user already has (inherits their group memberships and permission targets).</td><td>A token that acts \u201cas me\u201d for everyday automation.</td></tr>
          <tr><td><b>Admin</b></td><td>Full administrative access to the platform.</td><td>Platform bootstrap/IaC only - guard it carefully.</td></tr>
          <tr><td><b>Custom / scoped</b></td><td>Exactly the resource scopes you specify (e.g. read on one repo).</td><td>Least-privilege service tokens for a single job.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="callout callout-tip">
      <p class="callout-title">Default to least privilege</p>
      <p><b>"Least privilege"</b> means giving each token only the access it truly needs and nothing more. Reach for a <b>custom-scoped</b> token tied to a service identity before an admin token. If a custom token leaks, the "blast radius" (how much damage an attacker could do) is one repo, not your whole platform.</p>
    </div>
  </section>

  <section id="create" class="section">
    <span class="kicker kicker-lab">How-to</span>
    <h2>Creating an access token - three ways</h2>
    <h3 class="subhead">1. From the UI</h3>
    <ol class="steps">
      <li><b>Open token management.</b> Administration \u2192 User Management \u2192 <b>Access Tokens</b> \u2192 <b>Generate Token</b>.</li>
      <li><b>Choose the scope.</b> Pick the user/identity, set an expiry, and (optionally) restrict the scope.</li>
      <li><b>Copy it once.</b> The token value is shown a single time - store it in a secret manager immediately.</li>
    </ol>
    <h3 class="subhead">2. With the JFrog CLI</h3>
    <p class="code-label">Create a token (alias <code>jf atc</code>)</p>
    <div class="codeblock"><code>jf access-token-create --expiry=3600   <span class="cm"># expiry is in seconds: 3600 = 1 hour</span>
<span class="cm"># scope it to a specific user, or add --groups / --scope</span>
jf atc --groups=ci-bots --expiry=86400 <span class="cm"># atc = alias; 86400s = 24 hours; token inherits the ci-bots group's access</span></code></div>
    <h3 class="subhead">3. Over the REST API</h3>
    <p class="code-label">POST to the tokens endpoint</p>
    <div class="codeblock"><code><span class="cm"># POST = create. Minting a token needs an admin token in the header.</span>
<span class="cm"># subject: who the token represents | scope: which permissions it gets | expires_in: seconds</span>
curl -XPOST -H "Authorization: Bearer $ADMIN_TOKEN" \\
  -H "Content-Type: application/json" \\
  https://yourname.jfrog.io/access/api/v1/tokens \\
  -d '{
    "subject": "ci-bot",
    "scope": "applied-permissions/groups:ci-bots",
    "expires_in": 86400
  }'</code></div>
    <p class="prose muted">Sources: <a href="https://jfrog.com/help/r/jfrog-platform-administration-documentation/access-tokens" target="_blank" rel="noopener">JFrog - Access Tokens</a>, <a href="https://jfrog.com/help/r/jfrog-cli/access-tokens" target="_blank" rel="noopener">JFrog CLI - Access Tokens</a>.</p>
  </section>

  <section id="model" class="section">
    <span class="kicker kicker-art">Model</span>
    <h2>The authorization model: Users \u2192 Groups \u2192 Permission Targets</h2>
    <p class="prose">JFrog never grants permissions to a user directly on a repo. Instead, permissions flow through a three-layer hierarchy. Understanding it is the key to keeping access manageable as your platform grows. <a href="https://jfrog.com/help/r/jfrog-platform-administration-documentation/permissions" target="_blank" rel="noopener">JFrog - Permissions</a>.</p>
    <figure class="flow" aria-label="Permission hierarchy">
      <div class="flow-row">
        <div class="flow-step flow-art"><span class="flow-step-n">1</span><b>Users</b><small>people &amp; service identities</small></div>
        <span class="flow-conn">\u2192 belong to \u2192</span>
        <div class="flow-step flow-art"><span class="flow-step-n">2</span><b>Groups</b><small>roles, e.g. ci-bots, devs</small></div>
        <span class="flow-conn">\u2192 assigned in \u2192</span>
        <div class="flow-step flow-xray"><span class="flow-step-n">3</span><b>Permission targets</b><small>access to repos/builds</small></div>
      </div>
      <figcaption>Assign users to <b>groups</b> (by role), then grant <b>groups</b> access in <b>permission targets</b>. New hires just join a group and inherit the right access - no per-user wiring. <a href="https://jfrog.com/help/r/jfrog-platform-administration-documentation/permissions" target="_blank" rel="noopener">JFrog - Permissions</a>.</figcaption>
    </figure>
  </section>

  <section id="targets" class="section">
    <span class="kicker kicker-x">Authorization</span>
    <h2>Permission targets - fine-grained access</h2>
    <p class="prose">A <strong>permission target</strong> binds a set of resources (repositories, builds, or release bundles) to the actions a user/group may perform on them. Actions include <strong>read, write/deploy, delete, manage, annotate</strong> (set properties), and <strong>cache</strong> management. You can target specific repos or use wildcards.</p>
    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Element</th><th>Meaning</th></tr></thead>
        <tbody>
          <tr><td><b>Resource scope</b></td><td>Which repos/builds/release-bundles this target covers.</td></tr>
          <tr><td><code>ANY</code></td><td>Wildcard - every repository.</td></tr>
          <tr><td><code>ANY LOCAL</code></td><td>Every <span class="pill pill-local">local</span> repository.</td></tr>
          <tr><td><code>ANY REMOTE</code></td><td>Every <span class="pill pill-remote">remote</span> repository.</td></tr>
          <tr><td><b>Actions</b></td><td>read / deploy(write) / delete / manage / annotate / cache, granted per user or group.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="callout callout-q">
      <p class="callout-title">Read vs. deploy vs. manage</p>
      <p><b>Read</b> = pull/resolve artifacts. <b>Deploy</b> = push new artifacts. <b>Delete</b> = remove them. <b>Manage</b> = edit the permission target itself (grant access to others) - the most powerful, hand it out sparingly.</p>
    </div>
    <p class="prose muted">Sources: <a href="https://jfrog.com/help/r/self-managed-pro-pro-x-start-guide/set-up-users-groups-and-permissions" target="_blank" rel="noopener">JFrog - Set up users, groups &amp; permissions</a>, <a href="https://jfrog.com/help/r/jfrog-platform-administration-documentation/permissions" target="_blank" rel="noopener">JFrog - Permissions</a>.</p>
  </section>

  <section id="howto" class="section">
    <span class="kicker kicker-lab">How-to</span>
    <h2>Wiring up a least-privilege setup</h2>
    <ol class="steps">
      <li><b>Create role groups.</b> Administration \u2192 User Management \u2192 Groups \u2192 add e.g. <code>developers</code>, <code>ci-bots</code>, <code>release-managers</code>.</li>
      <li><b>Add users to groups.</b> Put each person/service identity in the group(s) matching their role.</li>
      <li><b>Create permission targets.</b> Administration \u2192 User Management \u2192 Permissions \u2192 add a target; pick the repos (or <code>ANY LOCAL</code>) and grant each group only the actions it needs.</li>
      <li><b>Mint scoped tokens.</b> For automation, create custom-scoped tokens bound to the <code>ci-bots</code> group rather than handing out personal tokens.</li>
      <li><b>Review &amp; rotate.</b> Periodically audit targets, expire stale tokens, and confirm no group has more than it needs.</li>
    </ol>
    <div class="callout callout-tip">
      <p class="callout-title">Tie it together</p>
      <p>This model powers everything else on this site: the token you mint here is the <code>Bearer</code> in the <a href="rest-api.html">REST API</a> page, the <code>JF_ACCESS_TOKEN</code> for <a href="frogbot.html">Frogbot</a>, and the credential a <a href="pipelines.html">Pipelines</a> integration stores.</p>
    </div>
  </section>
""",
}
_p["prev"], _p["next"] = chain(_p["file"])
PAGE_LIST.append(_p)


# =====================================================================
# 8) KUBERNETES / HELM SETUP
# =====================================================================
_p = {
 "file": "kubernetes-helm.html",
 "title": "Kubernetes / Helm setup",
 "desc": "Two angles on JFrog + Kubernetes: install Artifactory on a cluster with the official Helm charts, and use Artifactory as a Helm/OCI chart registry.",
 "badges": '<span class="lvl lvl-art">Artifactory</span><span class="lvl lvl-lab">Kubernetes</span><span class="lvl">How-to</span>',
 "h1": "Kubernetes &amp; Helm setup",
 "lede": "There are two distinct things people mean by \u201cJFrog and Kubernetes.\u201d One: run Artifactory itself on a cluster using the official Helm charts. Two: use Artifactory as the Helm/OCI registry your charts live in. This page covers both, in order.",
 "sections": [
   {"id": "two", "label": "Two distinct goals"},
   {"id": "install", "label": "Install Artifactory on K8s"},
   {"id": "keys", "label": "Master & join keys"},
   {"id": "registry", "label": "Artifactory as Helm registry"},
   {"id": "oci", "label": "OCI push & pull"},
 ],
 "body": """
  <section id="two" class="section">
    <span class="kicker kicker-art">Orientation</span>
    <h2>Two distinct goals - don't conflate them</h2>
    <div class="cards">
      <div class="card"><span class="card-num">A</span><h3>Run Artifactory <em>on</em> K8s</h3><p>Deploy the JFrog Platform itself into a Kubernetes cluster using the official Helm charts. This is an infrastructure/install task.</p></div>
      <div class="card"><span class="card-num">B</span><h3>Use Artifactory <em>as</em> a Helm registry</h3><p>Store and serve your own Helm charts (classic or OCI) from an Artifactory repository. This is a day-to-day usage task.</p></div>
    </div>
    <div class="callout callout-q">
      <p class="callout-title">Quick glossary before we start</p>
      <p><b>Kubernetes (K8s)</b> = a system that runs and manages containers across a cluster of machines. <b>Helm</b> = the "package manager" for Kubernetes; it installs apps from <b>charts</b> (a chart is a bundle of templated Kubernetes config). <b>Namespace</b> = a labelled partition inside a cluster that keeps one app's resources separate from another's. <b>Secret</b> = a Kubernetes object for storing sensitive values (keys, passwords) more safely than plain text.</p>
    </div>
    <p class="prose muted">Both rely on Helm, which is why they get confused. Sources: <a href="https://jfrog.com/help/r/jfrog-installation-setup-documentation/install-artifactory-on-kubernetes-using-helm" target="_blank" rel="noopener">Install Artifactory on Kubernetes</a>, <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/helm-chart-repositories" target="_blank" rel="noopener">Helm Chart Repositories</a>.</p>
  </section>

  <section id="install" class="section">
    <span class="kicker kicker-lab">Goal A</span>
    <h2>Installing Artifactory on Kubernetes with Helm</h2>
    <p class="prose">JFrog publishes official Helm charts. You add the chart repo, prepare a couple of secrets (master + join keys), then install into a namespace. <a href="https://jfrog.com/help/r/jfrog-installation-setup-documentation/install-artifactory-on-kubernetes-using-helm" target="_blank" rel="noopener">JFrog - Install Artifactory on Kubernetes</a>.</p>
    <p class="code-label">1) Add the JFrog Helm chart repository</p>
    <div class="codeblock"><code>helm repo add jfrog https://charts.jfrog.io   <span class="cm"># register JFrog's chart repo under the name "jfrog"</span>
helm repo update                              <span class="cm"># refresh the local list of available charts</span></code></div>
    <p class="code-label">2) Install Artifactory into its own namespace</p>
    <div class="codeblock"><code><span class="cm"># upgrade --install: install (or upgrade) a release named "artifactory"</span>
<span class="cm"># --set passes the master/join keys; --create-namespace makes the namespace if missing</span>
<span class="cm"># last arg jfrog/artifactory = which chart to install (repo/chart)</span>
helm upgrade --install artifactory \\
  --set artifactory.masterKey=${MASTER_KEY} \\
  --set artifactory.joinKey=${JOIN_KEY} \\
  --namespace artifactory --create-namespace \\
  jfrog/artifactory</code></div>
    <p class="prose muted"><code>upgrade --install</code> is <b>idempotent</b> - running it once or many times reaches the same result: it installs the first time and upgrades thereafter. ("Idempotent" is a key GitOps property: re-running a command is always safe.) For production, supply a <code>values.yaml</code> file (external database, ingress, persistent volumes) instead of bare <code>--set</code> flags.</p>
  </section>

  <section id="keys" class="section">
    <span class="kicker">Prereq</span>
    <h2>Master &amp; join keys - generate them first</h2>
    <p class="prose">The JFrog Platform is made of several small services ("microservices") that must trust each other. They authenticate with a shared <strong>join key</strong>, and Artifactory encrypts its stored config with a <strong>master key</strong>. You generate both as random hexadecimal strings and pass them to the chart - ideally as Kubernetes secrets rather than inline on the command line, so they don't leak into your shell history.</p>
    <p class="code-label">Generate 32-byte hex keys</p>
    <div class="codeblock"><code><span class="cm"># openssl makes 32 random bytes as hex; export saves each to an env var</span>
export MASTER_KEY=$(openssl rand -hex 32)
export JOIN_KEY=$(openssl rand -hex 32)

<span class="cm"># better: store them as Kubernetes secrets (kubectl = the K8s command-line tool)</span>
<span class="cm"># instead of putting them inline with --set. -n = in the artifactory namespace.</span>
kubectl create namespace artifactory
kubectl create secret generic my-masterkey \\
  --from-literal=master-key=${MASTER_KEY} -n artifactory
kubectl create secret generic my-joinkey \\
  --from-literal=join-key=${JOIN_KEY} -n artifactory</code></div>
    <div class="callout callout-q">
      <p class="callout-title">Why these matter</p>
      <p>Lose the <b>master key</b> and you can't decrypt your stored configuration; mismatch the <b>join key</b> across nodes and the microservices won't trust each other. Generate once, store securely, reuse on upgrades.</p>
    </div>
  </section>

  <section id="registry" class="section">
    <span class="kicker kicker-lab">Goal B</span>
    <h2>Using Artifactory as a Helm chart registry</h2>
    <p class="prose">Artifactory can host Helm charts in a <span class="pill pill-local">local</span> repo, proxy public charts via a <span class="pill pill-remote">remote</span> repo, and aggregate both behind a <span class="pill pill-virtual">virtual</span> repo. You then point the Helm client at the virtual repo's API URL. <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/helm-chart-repositories" target="_blank" rel="noopener">JFrog - Helm Chart Repositories</a>.</p>
    <p class="code-label">Add your Artifactory Helm repo to the Helm client</p>
    <div class="codeblock"><code>helm repo add my-charts \\
  https://yourname.jfrog.io/artifactory/api/helm/helm-virtual \\
  --username &lt;user&gt; --password &lt;token&gt;
helm repo update</code></div>
    <figure class="flow" aria-label="Helm repository types in Artifactory">
      <div class="flow-row">
        <div class="flow-step flow-art"><span class="flow-step-n">L</span><b>helm-local</b><small>your charts</small></div>
        <span class="flow-conn">+</span>
        <div class="flow-step"><span class="flow-step-n">R</span><b>helm-remote</b><small>proxies public charts</small></div>
        <span class="flow-conn">\u2192 both behind \u2192</span>
        <div class="flow-step flow-art"><span class="flow-step-n">V</span><b>helm-virtual</b><small>single URL clients use</small></div>
      </div>
      <figcaption>Clients only ever talk to the <b>virtual</b> repo; Artifactory resolves from local-first then remote. <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/helm-chart-repositories" target="_blank" rel="noopener">JFrog - Helm Chart Repositories</a>.</figcaption>
    </figure>
  </section>

  <section id="oci" class="section">
    <span class="kicker kicker-lab">Modern</span>
    <h2>OCI: push &amp; pull charts as OCI artifacts</h2>
    <p class="prose">Modern Helm (v3.8+) treats charts as <strong>OCI artifacts</strong>. <b>OCI</b> (Open Container Initiative) is the open standard that defines how container images are packaged and stored in registries - so "chart as an OCI artifact" means your chart is stored using the exact same mechanism as a Docker image, in the same kind of registry. Artifactory supports this directly, so you can push and pull charts to an OCI-enabled repository. <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/helm-oci-repositories" target="_blank" rel="noopener">JFrog - Helm OCI Repositories</a>.</p>
    <p class="code-label">Package, push, and pull a chart over OCI</p>
    <div class="codeblock"><code><span class="cm"># package your chart folder into a versioned .tgz archive</span>
helm package ./my-chart            <span class="cm"># \u2192 produces my-chart-1.0.0.tgz</span>

<span class="cm"># push it to an OCI repo in Artifactory (oci:// tells Helm to use the OCI protocol)</span>
helm push my-chart-1.0.0.tgz \\
  oci://yourname.jfrog.io/helm-oci-local

<span class="cm"># pull it back, or install it directly from the OCI repo</span>
<span class="cm"># (my-release = a name you pick for this deployment)</span>
helm pull oci://yourname.jfrog.io/helm-oci-local/my-chart --version 1.0.0
helm install my-release \\
  oci://yourname.jfrog.io/helm-oci-local/my-chart --version 1.0.0</code></div>
    <div class="callout callout-tip">
      <p class="callout-title">Authenticate first</p>
      <p>Run <code>helm registry login yourname.jfrog.io -u &lt;user&gt; -p &lt;token&gt;</code> before pushing over OCI. The token is one you mint on the <a href="access-tokens.html">Access tokens</a> page, scoped to deploy on the chart repo.</p>
    </div>
    <p class="prose muted">Sources: <a href="https://jfrog.com/help/r/jfrog-installation-setup-documentation/install-artifactory-on-kubernetes-using-helm" target="_blank" rel="noopener">Install on K8s</a>, <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/helm-chart-repositories" target="_blank" rel="noopener">Helm Chart Repositories</a>, <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/helm-oci-repositories" target="_blank" rel="noopener">Helm OCI Repositories</a>.</p>
  </section>
""",
}
_p["prev"], _p["next"] = chain(_p["file"])
PAGE_LIST.append(_p)


# =====================================================================
# 10) XRAY SECURITY: POLICIES & WATCHES (deep treatment)
# =====================================================================
_p = {
 "file": "xray-policies-watches.html",
 "title": "Xray Policies & Watches",
 "desc": "Write Xray security, license, and operational-risk rules; pick enforcement actions with grace periods; create a watch and attach the policy. The hands-on layer above the Fundamentals overview.",
 "badges": '<span class="lvl lvl-xray">Xray</span><span class="lvl">Security</span><span class="lvl lvl-lab">Hands-on</span>',
 "h1": "Xray Policies &amp; Watches",
 "lede": "Finding a vulnerability is only half the job - the other half is acting on it automatically. This page is the hands-on layer: how to write the rules inside a Policy, choose what happens when a rule is broken, then create a Watch and point it at your repositories. If the words Policy and Watch are new, read the short Policies &amp; Watches primer on Fundamentals first; here we go deeper and actually build them.",
 "sections": [
   {"id": "recap", "label": "30-second recap"},
   {"id": "model", "label": "The enforcement model"},
   {"id": "types", "label": "The 3 policy types"},
   {"id": "security-rules", "label": "Writing security rules"},
   {"id": "license-rules", "label": "Writing license rules"},
   {"id": "oprisk-rules", "label": "Operational-risk rules"},
   {"id": "actions", "label": "Enforcement actions"},
   {"id": "watches", "label": "Watches: the scope"},
   {"id": "lab-policy", "label": "Lab A: build a policy"},
   {"id": "lab-watch", "label": "Lab B: build a watch"},
   {"id": "connect", "label": "How this connects"},
   {"id": "recap-box", "label": "Recap"},
   {"id": "sources", "label": "Sources"},
 ],
 "body": """
  <section id="recap" class="section">
    <span class="kicker kicker-x">Recap</span>
    <h2>30-second recap (the two objects)</h2>
    <p class="prose">Xray's enforcement rests on two linked objects. The <a href="fundamentals.html#policies">Fundamentals page</a> explains the concept in full; here is the one-line version so this page stands on its own. A <strong>Policy</strong> is the <em>law</em>: a set of rules that say what counts as a problem and what to do about it. A <strong>Watch</strong> is the <em>jurisdiction and the police</em>: it says <em>where</em> the law applies and switches enforcement on. A finding only becomes a <strong>violation</strong> when a Watch points a Policy at the place the finding lives. <a href="https://jfrog.com/help/r/jfrog-security-documentation/creating-xray-policies-and-rules" target="_blank" rel="noopener">JFrog - Policy and Governance</a>.</p>
    <div class="callout callout-q">
      <p class="callout-title">One term before we start: violation</p>
      <p>A <b>violation</b> is the record Xray creates when an artifact actually breaks a rule that a Watch has switched on. No Watch, no violation - even if the vulnerability is real and indexed. That is the single most common point of confusion, so keep it in mind as you read.</p>
    </div>
  </section>

  <section id="model" class="section">
    <span class="kicker kicker-x">Mental model</span>
    <h2>The enforcement model, end to end</h2>
    <p class="prose">Every piece below has exactly one job. Read the chain left to right: Xray indexes an artifact, a Watch decides it is in scope, the Watch's Policy checks its rules, and if a rule's conditions are met a violation is created and its actions fire.</p>
    <figure class="flow" aria-label="Xray enforcement pipeline from indexed artifact to action">
      <div class="flow-row">
        <div class="flow-step flow-x"><span class="flow-step-n">1</span><b>Indexed artifact</b><small>component graph, scanned</small></div>
        <span class="flow-conn">&rarr;</span>
        <div class="flow-step flow-x"><span class="flow-step-n">2</span><b>Watch</b><small>is it in scope?</small></div>
        <span class="flow-conn">&rarr;</span>
        <div class="flow-step flow-x"><span class="flow-step-n">3</span><b>Policy + rules</b><small>conditions met?</small></div>
      </div>
      <div class="flow-row flow-row-down"><span class="flow-down">if a rule matches</span></div>
      <div class="flow-row">
        <div class="flow-step"><span class="flow-step-n">4</span><b>Violation</b><small>the record</small></div>
        <span class="flow-conn">&rarr;</span>
        <div class="flow-step flow-lab"><span class="flow-step-n">5</span><b>Actions</b><small>notify / fail / block</small></div>
      </div>
      <figcaption>The Policy holds the rules; the Watch supplies the scope. You build them in either order, but nothing is enforced until a Watch ties a Policy to a resource. <a href="https://docs.jfrog.com/security/docs/watches-in-jfrog-xray" target="_blank" rel="noopener">JFrog - Watches in Xray</a>.</figcaption>
    </figure>
  </section>

  <section id="types" class="section">
    <span class="kicker kicker-x">Policy types</span>
    <h2>The three policy types</h2>
    <p class="prose">When you create a Policy you pick exactly one type. The type decides which rule conditions you can configure. You cannot mix a license rule into a security policy - you would create one policy of each type and attach both to the same Watch.</p>
    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Type</th><th>What it catches</th><th>Typical rule</th></tr></thead>
        <tbody>
          <tr><td><b>Security</b></td><td>Known vulnerabilities (CVEs) and malicious packages in your components.</td><td>Block anything with a High or Critical CVE that has a fix available.</td></tr>
          <tr><td><b>License Compliance</b></td><td>Open-source licenses your organization bans or must track.</td><td>Fail the build if a component uses GPL-3.0.</td></tr>
          <tr><td><b>Operational Risk</b></td><td>Components that are outdated, deprecated, end-of-life, or poorly maintained.</td><td>Alert if a dependency has not been updated in 12+ months.</td></tr>
        </tbody>
      </table>
    </div>
    <p class="prose muted">Source: <a href="https://docs.jfrog.com/security/docs/create-policies" target="_blank" rel="noopener">JFrog - Create Policies</a>.</p>
  </section>

  <section id="security-rules" class="section">
    <span class="kicker kicker-x">Writing rules</span>
    <h2>Writing a security rule</h2>
    <p class="prose">A <strong>rule</strong> is a condition plus the actions to take when it matches. A security policy gives you two ways to define the condition - by how severe the vulnerability is, or by its exact CVSS score. <b>CVSS</b> (Common Vulnerability Scoring System) is the industry-standard 0-10 number that rates how dangerous a flaw is; higher is worse.</p>
    <div class="split">
      <div class="split-item" data-accent="xray">
        <h3 class="subhead">By minimal severity</h3>
        <p>Pick the lowest severity that should trip the rule. Everything at that level or higher matches.</p>
        <p class="sev-row">
          <span class="sev sev-crit">Critical</span>
          <span class="sev sev-high">High</span>
          <span class="sev sev-med">Medium</span>
          <span class="sev sev-low">Low</span>
          <span class="sev sev-unknown">All</span>
        </p>
        <p class="muted">Example: minimal severity = High catches both High and Critical, ignores Medium and below.</p>
      </div>
      <div class="split-item" data-accent="xray">
        <h3 class="subhead">By CVSS range</h3>
        <p>Set a numeric band, for example CVSS 7.0 to 10.0, when you want finer control than the named buckets give you.</p>
        <p class="muted">Useful when your org's risk threshold sits between two severity labels.</p>
      </div>
    </div>
    <p class="prose">Two extra conditions sharpen a security rule so you alert on what is actually actionable:</p>
    <ul class="feature-list">
      <li><b>Fix version available.</b> Only flag vulnerabilities that have a released fix, so developers always have somewhere to go. This dramatically cuts noise.</li>
      <li><b>Malicious package.</b> Trip on packages JFrog's security research has flagged as deliberately malicious (for example, typosquats), regardless of CVSS.</li>
    </ul>
    <div class="callout callout-tip">
      <p class="callout-title">A good first security rule</p>
      <p>Minimal severity = <b>High</b>, with <b>fix version available</b> turned on, action = <b>create a violation</b> plus <b>notify</b>. It is loud enough to matter, quiet enough to act on, and blocks nothing until you trust it. Tighten to <b>block download</b> later.</p>
    </div>
    <p class="prose muted">Source: <a href="https://docs.jfrog.com/security/docs/create-policies" target="_blank" rel="noopener">JFrog - Create Policies (Security Policy Rules)</a>.</p>
  </section>

  <section id="license-rules" class="section">
    <span class="kicker kicker-x">Writing rules</span>
    <h2>Writing a license rule</h2>
    <p class="prose">A license policy enforces which open-source licenses are allowed in your software. You define the condition as one of two lists.</p>
    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Approach</th><th>How it works</th><th>When to use it</th></tr></thead>
        <tbody>
          <tr><td><b>Banned licenses</b></td><td>List the licenses you forbid (e.g. GPL-3.0, AGPL-3.0). A component carrying any of them trips the rule.</td><td>You only need to block a handful of known-problematic licenses.</td></tr>
          <tr><td><b>Allowed licenses</b></td><td>List the only licenses you permit (e.g. MIT, Apache-2.0, BSD-3-Clause). Anything outside the list trips the rule.</td><td>Strict shops that want an explicit allow-list - safer by default.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="callout callout-q">
      <p class="callout-title">Why a single component can carry several licenses</p>
      <p>Open-source packages are sometimes dual-licensed or bundle code under more than one license. Xray evaluates every license it detects on a component, so a rule can trip on one license even when others are fine. Build your list with that in mind.</p>
    </div>
    <p class="prose muted">Source: <a href="https://jfrog.com/help/r/jfrog-security-documentation/creating-xray-policies-and-rules" target="_blank" rel="noopener">JFrog - Policy and Governance (license rules)</a>.</p>
  </section>

  <section id="oprisk-rules" class="section">
    <span class="kicker kicker-x">Writing rules</span>
    <h2>Operational-risk rules</h2>
    <p class="prose">Operational risk is about <em>maintainability</em>, not security - components that are stale or abandoned are a liability even when no CVE exists yet. JFrog's documented examples make the intent concrete:</p>
    <ul class="feature-list">
      <li><b>Staleness.</b> Alert developers if a dependency has not been updated in 12+ months.</li>
      <li><b>End-of-life.</b> Fail builds if a package is flagged as end-of-life.</li>
      <li><b>Deprecation.</b> Block downloads of deprecated components.</li>
    </ul>
    <p class="prose muted">Source: <a href="https://docs.jfrog.com/security/docs/create-policies" target="_blank" rel="noopener">JFrog - Create Policies (Operational Risk Rule)</a>.</p>
  </section>

  <section id="actions" class="section">
    <span class="kicker kicker-x">Enforcement</span>
    <h2>What a rule can do: enforcement actions</h2>
    <p class="prose">Each rule, when matched, always records a <strong>violation</strong>. On top of that you choose any number of automatic actions. They fall into two families: <em>notify</em> (tell someone) and <em>block</em> (stop the artifact from moving).</p>
    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Action</th><th>Family</th><th>Effect</th></tr></thead>
        <tbody>
          <tr><td>Generate a violation</td><td>Always on</td><td>The record that something broke a rule. Everything else is optional on top.</td></tr>
          <tr><td>Notify watch recipients / developer / email list</td><td>Notify</td><td>Email the watch owner, the resource's developer, or a configured address list.</td></tr>
          <tr><td>Trigger a webhook</td><td>Notify</td><td>Call an external endpoint (Slack, a pipeline, your own service) when the rule is violated.</td></tr>
          <tr><td>Create a Jira ticket</td><td>Notify</td><td>Open a tracking ticket automatically for each violation.</td></tr>
          <tr><td>Fail builds</td><td>Block</td><td>Make a CI build fail when the rule is violated. Supports a grace period.</td></tr>
          <tr><td>Block downloads</td><td>Block</td><td>Stop the artifact from being downloaded from Artifactory. Supports a grace period.</td></tr>
          <tr><td>Block Release Bundle promotion / distribution</td><td>Block</td><td>Stop a Release Bundle from being promoted or distributed in the release lifecycle. Supports a grace period.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="callout callout-tip">
      <p class="callout-title">Grace periods: how to roll out blocking without an outage</p>
      <p>The three blocking actions let you set a <b>grace period</b> - a window where the violation is recorded and teams are warned, but the block does not yet bite. This is the safe way to introduce enforcement: start in notify-only, switch on blocking with a grace period, then let the grace period expire once teams have caught up. <a href="https://docs.jfrog.com/security/docs/create-policies" target="_blank" rel="noopener">JFrog - Create Policies (enforcement actions)</a>.</p>
    </div>
  </section>

  <section id="watches" class="section">
    <span class="kicker kicker-x">Scope</span>
    <h2>Watches: choosing the scope</h2>
    <p class="prose">A Watch answers one question: <em>which resources do these policies apply to?</em> When you add resources to a Watch you choose from four kinds of target. A Watch must have at least one policy attached, or it enforces nothing.</p>
    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Resource</th><th>What it scopes</th><th>Example</th></tr></thead>
        <tbody>
          <tr><td><b>Repositories</b></td><td>Everything stored in one or more repos.</td><td>Watch <code>docker-prod-local</code> for Critical CVEs.</td></tr>
          <tr><td><b>Builds</b></td><td>The artifacts and dependencies captured in named builds.</td><td>Watch the <code>payments-api</code> build to gate CI.</td></tr>
          <tr><td><b>Release Bundles</b></td><td>The signed, immutable bundles you promote and distribute.</td><td>Block distribution of a bundle with a vulnerable base layer.</td></tr>
          <tr><td><b>Projects</b></td><td>All resources grouped under a JFrog Project.</td><td>Apply one compliance baseline across a whole team's project.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="callout callout-tip">
      <p class="callout-title">Best practice: one Watch per environment</p>
      <p>JFrog recommends separate Watches for different environments - a permissive, notify-only Watch on dev repos and a strict, blocking Watch on production repos - so the same finding is handled appropriately for where it lives. <a href="https://docs.jfrog.com/security/docs/create-watches" target="_blank" rel="noopener">JFrog - Create Watches (best practices)</a>.</p>
    </div>
  </section>

  <section id="lab-policy" class="section">
    <span class="kicker kicker-lab">Lab A</span>
    <h2>Lab A: create a security policy</h2>
    <div class="panel-intro">
      <p>Goal: a policy that records and notifies on High/Critical vulnerabilities that have a fix, blocking nothing yet. This is the exact click-path from the JFrog docs.</p>
    </div>
    <ol class="lab-steps">
      <li><span class="ls-n">1</span><div><b>Open Watches &amp; Policies.</b> In the JFrog Platform, go to <b>Xray &rarr; Watches &amp; Policies</b>.</div></li>
      <li><span class="ls-n">2</span><div><b>New Policy.</b> Click <b>New Policy</b> and enter a name, for example <code>prod-security-baseline</code>. Add a short description of its purpose.</div></li>
      <li><span class="ls-n">3</span><div><b>Pick the type.</b> Choose <b>Security Policy</b>.</div></li>
      <li><span class="ls-n">4</span><div><b>Add a rule.</b> Click <b>Add Rule</b>. Set the rule category to <b>By Minimal Severity = High</b>, and enable <b>Fix version available</b> so you only flag actionable findings.</div></li>
      <li><span class="ls-n">5</span><div><b>Set actions.</b> Leave the default violation on, and add <b>Notify the watch recipient</b>. Do not enable blocking yet - you will tighten later.</div></li>
      <li><span class="ls-n">6</span><div><b>Save.</b> Save the policy. It now exists but enforces nothing until a Watch uses it - that is Lab B.</div></li>
    </ol>
    <p class="prose muted">Source: <a href="https://docs.jfrog.com/security/docs/create-policies" target="_blank" rel="noopener">JFrog - Create Policies</a>.</p>
  </section>

  <section id="lab-watch" class="section">
    <span class="kicker kicker-lab">Lab B</span>
    <h2>Lab B: create a watch and attach the policy</h2>
    <div class="panel-intro">
      <p>Goal: point the policy from Lab A at a real repository so findings start becoming violations.</p>
    </div>
    <ol class="lab-steps">
      <li><span class="ls-n">1</span><div><b>New Watch.</b> Still under <b>Xray &rarr; Watches &amp; Policies</b>, click <b>New Watch</b> and give it a unique name, for example <code>prod-repos-watch</code>.</div></li>
      <li><span class="ls-n">2</span><div><b>Add resources.</b> Click <b>Add Resources</b> and select what to monitor - a <b>Repository</b> (e.g. your production Docker repo), a <b>Build</b>, a <b>Release Bundle</b>, or a <b>Project</b>. Click <b>Apply</b>.</div></li>
      <li><span class="ls-n">3</span><div><b>Attach the policy.</b> Link the <code>prod-security-baseline</code> policy from Lab A. A Watch can carry several policies - add a license policy here too if you have one.</div></li>
      <li><span class="ls-n">4</span><div><b>Save &amp; apply.</b> Save the Watch. Xray evaluates the in-scope resources against the attached policies and starts generating violations on matches.</div></li>
      <li><span class="ls-n">5</span><div><b>Verify.</b> Open the Watch and review its violations. Seeing the High/Critical findings you expected confirms the policy and scope line up.</div></li>
    </ol>
    <div class="callout callout-q">
      <p class="callout-title">Reminder you will thank yourself for</p>
      <p>If you created the policy but see no violations, check that a Watch actually attaches it to the right resource. A policy with no Watch is inert by design.</p>
    </div>
    <p class="prose muted">Source: <a href="https://docs.jfrog.com/security/docs/create-watches" target="_blank" rel="noopener">JFrog - Create Watches</a>.</p>
  </section>

  <section id="connect" class="section">
    <span class="kicker kicker-x">Connections</span>
    <h2>How this connects to the rest of the platform</h2>
    <p class="prose">Policies and Watches are the engine; other pages show where that engine plugs in across the software lifecycle:</p>
    <ul class="feature-list">
      <li><b>Shift left.</b> The same policies drive earlier feedback - in the IDE and on pull requests - covered on <a href="frogbot.html">Frogbot &amp; IDE</a>.</li>
      <li><b>Promotion gates.</b> A Watch on a staging repo can block promotion to release when a High/Critical CVE is present - see the worked example on <a href="build-promotion.html#pattern">Build promotion</a>.</li>
      <li><b>The basics.</b> If indexing, scanning, or the Policy-vs-Watch split still feel fuzzy, the <a href="fundamentals.html#xray">Fundamentals</a> page covers them from zero.</li>
    </ul>
  </section>

  <section id="recap-box" class="section">
    <div class="recap">
      <h2>Recap</h2>
      <ul>
        <li><b>Policy = rules, Watch = scope.</b> Nothing is enforced until a Watch attaches a Policy to a resource; the result of a match is a <b>violation</b>.</li>
        <li><b>Three policy types.</b> Security (CVEs, malicious), License (banned or allowed lists), Operational risk (stale, EOL, deprecated). One type per policy; attach several policies to one Watch.</li>
        <li><b>Sharpen security rules</b> with minimal severity or a CVSS range, plus <b>fix-available</b> to cut noise.</li>
        <li><b>Actions</b> are notify (email, webhook, Jira) or block (fail build, block download, block bundle promotion). Blocking actions support a <b>grace period</b> for safe rollout.</li>
        <li><b>Watches</b> target repositories, builds, release bundles, or projects. Use one Watch per environment.</li>
      </ul>
    </div>
  </section>

  <section id="sources" class="section">
    <span class="kicker">Sources &amp; further reading</span>
    <h2>Sources / further reading</h2>
    <ul class="feature-list">
      <li><a href="https://docs.jfrog.com/security/docs/create-policies" target="_blank" rel="noopener">JFrog Docs - Create Policies</a> (policy types, rule conditions, enforcement actions, grace periods).</li>
      <li><a href="https://docs.jfrog.com/security/docs/create-watches" target="_blank" rel="noopener">JFrog Docs - Create Watches</a> (resources, attaching policies, best practices).</li>
      <li><a href="https://docs.jfrog.com/security/docs/watches-in-jfrog-xray" target="_blank" rel="noopener">JFrog Docs - Watches in JFrog Xray</a> (what a Watch is and what it targets).</li>
      <li><a href="https://jfrog.com/help/r/jfrog-security-documentation/creating-xray-policies-and-rules" target="_blank" rel="noopener">JFrog Help - Policy and Governance</a> (policies across the SDLC, best practices).</li>
    </ul>
  </section>
""",
}
_p["prev"], _p["next"] = chain(_p["file"])
PAGE_LIST.append(_p)


# =====================================================================
# SEARCH METADATA (consumed by build_search_index.py + search.html)
# =====================================================================

# Sidebar group each page belongs to (mirrors NAV in assets/app.js).
GROUPS = {
    "index.html": "Overview",
    "fundamentals.html": "Core concepts",
    "replication-federation.html": "Core concepts",
    "build-promotion.html": "Core concepts",
    "release-bundles.html": "Distribution",
    "xray-policies-watches.html": "Automation & security",
    "rest-api.html": "Automation & security",
    "frogbot.html": "Automation & security",
    "pipelines.html": "Automation & security",
    "access-tokens.html": "Automation & security",
    "kubernetes-helm.html": "Platform ops",
}

# Fundamentals is now generated from PAGE_LIST like every other page; its
# section anchors live in that page dict. (Previously declared here as a
# special-case when fundamentals was a hand-authored static page.)

# Curated cross-page "related topics" so a result set links the user to
# connected material without re-searching. file -> list of related files.
RELATED = {
    "fundamentals.html": [
        "access-tokens.html", "rest-api.html", "kubernetes-helm.html", "build-promotion.html",
    ],
    "replication-federation.html": [
        "fundamentals.html", "release-bundles.html", "kubernetes-helm.html",
    ],
    "build-promotion.html": [
        "release-bundles.html", "xray-policies-watches.html", "rest-api.html", "fundamentals.html",
    ],
    "release-bundles.html": [
        "build-promotion.html", "replication-federation.html", "rest-api.html",
    ],
    "xray-policies-watches.html": [
        "frogbot.html", "build-promotion.html", "fundamentals.html", "pipelines.html",
    ],
    "rest-api.html": [
        "access-tokens.html", "build-promotion.html", "frogbot.html", "pipelines.html",
    ],
    "frogbot.html": [
        "xray-policies-watches.html", "rest-api.html", "access-tokens.html", "fundamentals.html",
    ],
    "pipelines.html": [
        "build-promotion.html", "rest-api.html", "frogbot.html", "access-tokens.html",
    ],
    "access-tokens.html": [
        "rest-api.html", "frogbot.html", "kubernetes-helm.html", "pipelines.html",
    ],
    "kubernetes-helm.html": [
        "access-tokens.html", "fundamentals.html", "replication-federation.html", "rest-api.html",
    ],
}
