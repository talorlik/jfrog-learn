# -*- coding: utf-8 -*-
"""Content bodies for each topic page. Imported by build_pages.py."""

# ---- prev/next chain (matches sidebar order) ----
NAV_ORDER = [
    ("fundamentals.html", "Fundamentals"),
    ("replication-federation.html", "Replication & Federation"),
    ("build-promotion.html", "Build promotion"),
    ("release-bundles.html", "Release Bundles & Distribution"),
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
# 1) REPLICATION & FEDERATION
# =====================================================================
_p = {
 "file": "replication-federation.html",
 "title": "Replication & Federation",
 "desc": "How JFrog keeps artifacts in sync across data centers and JPDs: push/pull replication versus federated repositories, and when to use each.",
 "badges": '<span class="lvl lvl-art">Artifactory</span><span class="lvl">Multi-site</span><span class="lvl">Deep-dive</span>',
 "h1": "Replication &amp; Federation",
 "lede": "Once you run JFrog in more than one location, you need copies of your artifacts to stay in sync. JFrog gives you two mechanisms — classic replication and federated repositories. They solve overlapping problems differently.",
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
    <p class="prose">A single Artifactory instance is one point in the world. The moment you have teams in London and Tokyo, a CI (Continuous Integration &mdash; the automated server that builds and tests your code) farm in another region, or a disaster-recovery site (a backup copy you can switch to if your main one fails), builds in one place need the same binaries that live in another. "Binaries" here just means the packaged outputs you store in Artifactory &mdash; Docker images, JAR files, npm packages, and so on. Pulling all of them across an ocean on every build is slow and fragile.</p>
    <div class="cards">
      <div class="card"><span class="card-num">01</span><h3>Latency</h3><p>Developers and CI resolve dependencies from a local copy instead of crossing continents on every download.</p></div>
      <div class="card"><span class="card-num">02</span><h3>Availability</h3><p>If one site or its network goes down, the others still have their own copy and keep building.</p></div>
      <div class="card"><span class="card-num">03</span><h3>Disaster recovery</h3><p>A synced standby instance lets you fail over with the artifacts already in place.</p></div>
    </div>
    <div class="callout callout-q">
      <p class="callout-title">First, one term you'll see everywhere: JPD</p>
      <p>A <b>JPD</b> stands for <b>JFrog Platform Deployment</b> &mdash; it's simply one complete, self-contained install of the JFrog Platform (Artifactory + Xray + the rest), running in one place. When this page says "site", "instance", or "deployment", it means one JPD. Syncing artifacts across sites means syncing them between JPDs.</p>
    </div>
    <p class="prose muted">JFrog offers two answers: <strong>replication</strong> (an older, one-directional copy job) and <strong>federation</strong> (newer, automatic, multi-directional mirroring). "One-directional" means data flows from a source to a target only; "multi-directional" means every copy can both send and receive. <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/repository-replication" target="_blank" rel="noopener">JFrog — Repository Replication</a>.</p>
  </section>

  <section id="replication" class="section">
    <span class="kicker kicker-art">Replication</span>
    <h2>Replication — copying repositories between instances</h2>
    <p class="prose"><strong>Replication</strong> synchronizes the contents of a repository on one Artifactory instance with a repository on another. It runs on a <em>schedule</em> &mdash; defined by a <b>cron</b> expression, which is just a compact string that says "run at these times" (for example, every hour) &mdash; or it can be triggered automatically as an <em>event</em> the moment something changes. It copies artifacts plus their <b>properties</b> (key/value tags attached to an artifact, like <code>stage=released</code>). Replication works on <span class="pill pill-local">local</span> and <span class="pill pill-remote">remote</span> repositories. <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/repository-replication" target="_blank" rel="noopener">Source</a>.</p>
    <div class="callout callout-q">
      <p class="callout-title">Key trait: it's one-directional</p>
      <p>A single replication has a clear source and target. Site A pushes to Site B, or Site B pulls from Site A — but one replication relationship only flows one way. To mirror both directions you configure two separate jobs.</p>
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
      <div class="flow-row flow-row-down"><span class="flow-down">— or, reversed initiator —</span></div>
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
    <h2>Federated repositories — automatic multi-directional mirroring</h2>
    <p class="prose">A <span class="pill pill-fed">Federated</span> repository behaves like a <span class="pill pill-local">local</span> repo, but it is bi-directionally mirrored across multiple <strong>members</strong> — up to 10 repositories living on different JFrog Platform Deployments (JPDs, defined above). "Bi-directional" means the sync flows both ways. Write to any member and the change <em>propagates</em> (spreads automatically) to all the others, <em>asynchronously</em> (in the background, so your write doesn't have to wait for every copy to finish). <a href="https://docs.jfrog.com/artifactory/docs/federated-repositories" target="_blank" rel="noopener">JFrog — Federated Repositories</a>.</p>
    <ul class="feature-list">
      <li><b>Bi-directional by design.</b> Every member is both source and target — no manual two-way setup. Deploy to London, it appears in Tokyo, and vice-versa.</li>
      <li><b>Async, queue-backed.</b> Changes are replicated through a persistent queue, so a temporary network blip doesn't lose data — it catches up when connectivity returns.</li>
      <li><b>Configuration is synced too.</b> Repository configuration (not just artifacts) is kept aligned across members.</li>
      <li><b>Up to 10 members.</b> A federation can span up to ten member repositories across JPDs.</li>
      <li><b>Enterprise tier.</b> Federated repositories require an Enterprise X (or higher) paid subscription — so you won't see them on the free tier.</li>
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
      <li><b>Add members.</b> In the Federated configuration, add member URLs for the other JPDs. For one JPD to trust another, they must first be linked — JFrog calls this the "circle of trust", set up through Mission Control (JFrog's tool for managing multiple deployments). Think of it as the two deployments exchanging IDs so they'll accept each other's data.</li>
      <li><b>Deploy anywhere.</b> Push an artifact to any member; verify it appears on the others within seconds.</li>
    </ol>
    <div class="callout callout-q">
      <p class="callout-title">Tip for your labs</p>
      <p><b>Prerequisite reminder:</b> on the free single-instance tier you can't truly demonstrate multi-JPD federation — you need at least two separate deployments. You <em>can</em> still create the repo types and read the configuration screens to understand the model. For a real two-site test, stand up two self-hosted instances ("self-hosted" means you run Artifactory yourself, e.g. in Docker, instead of using JFrog's cloud) — see the Docker lab on the <a href="fundamentals.html">Fundamentals</a> page.</p>
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
 "lede": "Promotion is how a binary graduates from dev to staging to release without ever being rebuilt — so what you tested is byte-for-byte what ships. It hinges on one idea: build-info that tracks artifacts by checksum, wherever they move.",
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
    <p class="prose"><strong>Build promotion changes a build's status to a more mature stage</strong> — for example <code>dev</code> → <code>staging</code> → <code>released</code> — and can optionally move or copy the build's artifacts (and their dependencies) into a target repository and set properties on them ("properties" are key/value tags like <code>stage=released</code>). The crucial part: <em>no rebuild happens</em>. The same binary that passed your tests is the one that advances. <a href="https://jfrog.com/help/r/how-does-build-promotion-work/artifactory-how-does-build-promotion-work" target="_blank" rel="noopener">JFrog — How build promotion works</a>.</p>
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
    <p class="prose">Promotion only works because Artifactory records <strong>build-info</strong> — a metadata record (a JSON document) capturing which artifacts a build produced, which dependencies it consumed, and the environment it ran in. Think of it as the build's birth certificate. Artifacts are tracked by their <strong>checksum</strong> — a short fingerprint computed from the file's exact bytes (using the SHA-1 and SHA-256 hashing algorithms); if even one byte changes, the checksum changes, so it uniquely identifies that exact file. Combined with the <code>build.name</code> and <code>build.number</code> properties, Artifactory always knows an artifact's identity no matter what repository it currently sits in. <a href="https://docs.jfrog.com/integrations/docs/manage-builds" target="_blank" rel="noopener">JFrog — Manage builds</a>, <a href="https://docs.jfrog.com/artifactory/docs/build-integration" target="_blank" rel="noopener">Build integration</a>.</p>
    <ul class="feature-list">
      <li><b>Location-agnostic.</b> Because identity is the checksum + build coordinates, moving an artifact between repos doesn't lose its lineage.</li>
      <li><b>Full traceability.</b> From a release artifact you can walk back to the exact build, its dependencies, and its source commit.</li>
      <li><b>Required first step.</b> Your CI must <em>publish</em> build-info before you can promote that build. The JFrog CLI (<code>jf</code>, JFrog's command-line tool) does this with <code>jf rt build-publish</code> &mdash; here <code>rt</code> means "Artifactory" (its internal name was "rt").</li>
    </ul>
  </section>

  <section id="copymove" class="section">
    <span class="kicker">Choice</span>
    <h2>Copy vs. move — and properties</h2>
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
    <p class="prose">The command is <code>jf rt build-promote</code> (alias <code>jf rt bpr</code> &mdash; an "alias" is just a shorter name for the same command). You name the build, its number, and the target repo, plus options for copy/move and the new status. <a href="https://jfrog.com/help/r/artifactory-rest-apis/build-promotion" target="_blank" rel="noopener">JFrog — Build promotion</a>.</p>
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
    <p class="prose">CI systems that don't use the CLI can call the promotion endpoint directly. <a href="https://jfrog.com/help/r/artifactory-rest-apis/build-promotion" target="_blank" rel="noopener">JFrog — Build Promotion REST API</a>.</p>
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
      <p>The power move: a <a href="fundamentals.html#policies">Policy + Watch</a> on <code>staging-local</code> blocks promotion to <code>release-local</code> if a High/Critical CVE with an available fix is present. (A <b>CVE</b> &mdash; Common Vulnerabilities and Exposures &mdash; is a publicly catalogued security flaw, each with an ID like <code>CVE-2021-44228</code>.) Promotion becomes your enforced quality gate, not a manual courtesy.</p>
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
 "lede": "A Release Bundle is a sealed, signed manifest of exactly which artifacts make up a release. JFrog Distribution then ships that bundle out to edge nodes and remote sites — so what arrives is provably identical to what you signed.",
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
    <p class="prose">Promotion moves binaries <em>inside</em> one platform. But shipping a release <em>out</em> — to a customer site, an edge location, or an <b>air-gapped network</b> (a network with no internet connection at all, for security) — raises new questions: which exact files belong to "v2.4.0"? Were any swapped in transit? Can the receiving side prove <b>provenance</b> (a verifiable record of where each file came from and that it wasn't altered)? A loose folder of artifacts answers none of these.</p>
    <p class="prose">A <strong>Release Bundle</strong> is the answer: an <em>immutable</em> (can never be changed after creation), <em>signed</em> specification of the precise set of artifacts that make up a release, with a checksum-verified <b>manifest</b> (the packing list &mdash; it names every file and its checksum fingerprint). <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/release-lifecycle-management" target="_blank" rel="noopener">JFrog — Release Lifecycle Management</a>.</p>
  </section>

  <section id="bundle" class="section">
    <span class="kicker kicker-x">Definition</span>
    <h2>What's inside a Release Bundle</h2>
    <ul class="feature-list">
      <li><b>A curated artifact set.</b> You select the artifacts that make up the release — by build, by file path, or by an <b>AQL</b> query (Artifactory Query Language, a JSON-based search language for finding artifacts by name, property, repo, etc.). The bundle records each one's checksum.</li>
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
      <figcaption>The bundle is created and sealed once, then distributed to one or many targets. Each target verifies signatures and checksums before exposing the artifacts. <a href="https://jfrog.com/help/r/jfrog-distribution-documentation/distributing-release-bundles" target="_blank" rel="noopener">JFrog — Distributing Release Bundles</a>.</figcaption>
    </figure>
  </section>

  <section id="distribution" class="section">
    <span class="kicker kicker-x">Distribution</span>
    <h2>Distribution &amp; edge nodes</h2>
    <p class="prose"><strong>JFrog Distribution</strong> is the service that takes a signed Release Bundle and delivers it to <strong>edge nodes</strong> — lightweight Artifactory instances positioned close to consumers (a factory floor, a CDN POP, an air-gapped enclave). Edge nodes are read-only consumption points: they receive distributed bundles but aren't general-purpose repositories. <a href="https://jfrog.com/help/r/jfrog-distribution-documentation/jfrog-distribution" target="_blank" rel="noopener">JFrog Distribution docs</a>.</p>
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
      <p>Consumers at the edge pull from a nearby node — fast and resilient — while you keep a single signed source of truth centrally. Air-gapped sites receive the bundle as a verifiable package rather than opening a live connection to your main platform.</p>
    </div>
  </section>

  <section id="cli" class="section">
    <span class="kicker kicker-lab">CLI</span>
    <h2>Create and distribute a bundle (CLI)</h2>
    <p class="prose">The JFrog CLI exposes release-bundle commands under <code>jf rbc</code> / <code>jf rbu</code> (create/update) and <code>jf rbd</code> (distribute) &mdash; these short names are just aliases for the longer commands below. The conceptual flow: <a href="https://jfrog.com/help/r/jfrog-cli/release-bundles" target="_blank" rel="noopener">JFrog CLI — Release Bundles</a>.</p>
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
    <p class="prose muted">The spec selects artifacts (by AQL/path); the signing key seals the manifest; the distribute step fans it out to matching edge sites. Exact subcommands vary by Release Lifecycle Management version — check the linked CLI reference for your platform.</p>
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
    <h2>Authentication — three ways in</h2>
    <div class="callout callout-q">
      <p class="callout-title">New to APIs? Start here</p>
      <p>An <b>API</b> (Application Programming Interface) is a way for programs to talk to Artifactory instead of a human clicking the web UI. <b>REST</b> is the most common style of web API: you send an <b>HTTP request</b> (the same protocol your browser uses) to a URL called an <b>endpoint</b>, using a <b>method</b> that states your intent &mdash; <code>GET</code> (read), <code>POST</code> (create), <code>PUT</code> (create/replace), <code>DELETE</code> (remove). Artifactory replies with <b>JSON</b> (a simple text format for structured data). That's the whole idea: a URL + a method + (sometimes) a JSON body.</p>
    </div>
    <p class="prose">Every Artifactory REST call needs to identify you (this is <b>authentication</b> &mdash; proving who you are). There are three accepted methods; pick access tokens for automation. <a href="https://jfrog.com/help/r/jfrog-platform-rest-apis/introduction-to-the-jfrog-platform-rest-apis" target="_blank" rel="noopener">JFrog — Intro to the REST APIs</a>.</p>
    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Method</th><th>How it's sent</th><th>Use when</th></tr></thead>
        <tbody>
          <tr><td><b>Access token</b> (recommended)</td><td><code>Authorization: Bearer &lt;token&gt;</code> &mdash; an HTTP header you attach to the request; "Bearer" just means "whoever carries this token is allowed in"</td><td>Any automation — scoped, revocable, no password exposure.</td></tr>
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
          <tr><td><code>/artifactory/api/system/ping</code></td><td>GET</td><td>Health check — returns <code>OK</code>.</td></tr>
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
    <p class="prose">If you've already configured a server with <code>jf c add</code> ("c" = config; this stores your server URL and token once), the CLI can call any Artifactory REST endpoint <em>using those stored credentials</em> — so you never type an auth header again. <a href="https://docs.jfrog.com/integrations/docs/use-api-endpoints-via-cli" target="_blank" rel="noopener">JFrog — Use API endpoints via CLI</a>.</p>
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
      <li><b>Use access tokens, never passwords</b> in automation — they're scoped and revocable.</li>
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
      <p>A <b>pull request (PR)</b> is how you propose changes on GitHub/GitLab &mdash; you push your branch and open a PR asking to merge it, so teammates (and bots) can review it before it lands. <b>"Shift-left"</b> means catching problems as early as possible in the development timeline (drawn left-to-right), because the earlier you catch a bug or vulnerability, the cheaper it is to fix.</p>
    </div>
    <p class="prose"><strong>Frogbot is a Git bot that scans your pull requests and repositories for security vulnerabilities using JFrog Xray</strong> (Xray is JFrog's security scanner). When a developer opens a PR, Frogbot scans it and posts the results as a comment (JFrog calls this a "decoration") directly on the PR — and if it finds no new issues, it says so. It works with GitHub, GitLab, Bitbucket, and Azure Repos. <a href="https://github.com/jfrog/frogbot" target="_blank" rel="noopener">jfrog/frogbot</a>.</p>
    <ul class="feature-list">
      <li><b>Only flags <em>new</em> issues.</b> A PR scan compares the project state before and after the change, so it reports only vulnerabilities the PR introduces — not pre-existing noise.</li>
      <li><b>Opens fix PRs.</b> When fixable issues are found and auto-fix is enabled, Frogbot opens a pull request that upgrades the vulnerable dependency to a fixed version.</li>
      <li><b>Requires Xray 3.29.0+.</b> Frogbot uses your JFrog platform's Xray to do the actual scanning. <a href="https://docs.jfrog.com/security/docs/how-to-commit-scan-and-pr-scan" target="_blank" rel="noopener">JFrog — Commit &amp; PR scan</a>.</li>
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
    <p class="prose muted">Source: <a href="https://docs.jfrog.com/security/docs/how-to-commit-scan-and-pr-scan" target="_blank" rel="noopener">JFrog — Scanning Commits and Pull Requests</a>.</p>
    <div class="callout callout-tip">
      <p class="callout-title">Required environment variables</p>
      <p>An "environment variable" is a named value the running job can read. Both modes need <code>JF_URL</code> (your platform URL, e.g. <code>https://my.jfrog.io</code>) and <code>JF_ACCESS_TOKEN</code> (a scoped access token &mdash; see the <a href="access-tokens.html">Access tokens</a> page), plus a Git token (<code>JF_GIT_TOKEN</code> / the CI's built-in token) so Frogbot has permission to comment and open PRs on your repo.</p>
    </div>
  </section>

  <section id="setup" class="section">
    <span class="kicker kicker-lab">How-to</span>
    <h2>Setting up Frogbot on GitHub Actions</h2>
    <ol class="steps">
      <li><b>Allow Frogbot to open PRs.</b> In GitHub → <em>Settings → Actions → General</em>, check <b>"Allow GitHub Actions to create and approve pull requests."</b></li>
      <li><b>(Recommended for OSS) Create a <code>frogbot</code> environment.</b> Settings → <em>Environments</em> → New environment named <code>frogbot</code>, and add reviewers. Those reviewers must approve before Frogbot scans a PR — a safety gate for public repos.</li>
      <li><b>Add the workflow file.</b> Drop a Frogbot workflow into <code>.github/workflows/</code> (template below), or use the JFrog GitHub App to have it opened for you automatically across selected repos.</li>
      <li><b>Add secrets/vars.</b> Provide <code>JF_URL</code> and <code>JF_ACCESS_TOKEN</code> as repository secrets. The built-in <code>GITHUB_TOKEN</code> covers Git operations.</li>
    </ol>
    <p class="prose muted">Sources: <a href="https://jfrog.com/help/r/jfrog-security-user-guide/shift-left-on-security/frogbot/installation/github-actions/installation" target="_blank" rel="noopener">JFrog — Frogbot GitHub Actions install</a>, <a href="https://docs.jfrog.com/integrations/docs/github-actions-frogbot-bulk-installation" target="_blank" rel="noopener">JFrog GitHub App bulk install</a>.</p>
  </section>

  <section id="yaml" class="section">
    <span class="kicker kicker-lab">YAML</span>
    <h2>The PR-scan workflow</h2>
    <p class="prose">A minimal GitHub Actions workflow that runs Frogbot on every pull request. A "workflow" is a YAML file in <code>.github/workflows/</code> that GitHub runs automatically when a trigger fires. <b>YAML</b> is an indentation-based config format &mdash; indentation (spaces, never tabs) defines the nesting. <a href="https://jfrog.com/help/r/jfrog-and-github-integration-guide/github-pr-scans-and-advanced-security" target="_blank" rel="noopener">JFrog — GitHub PR scans</a>.</p>
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
    <h2>IDE integration — catch it before the PR</h2>
    <p class="prose">Even earlier than the PR is the editor. JFrog ships plugins for <strong>VS Code, IntelliJ/JetBrains IDEs, Visual Studio, and Eclipse</strong> that scan your project's dependencies against Xray and surface vulnerabilities inline as you work. <a href="https://docs.jfrog.com/security/docs/ide-integrations" target="_blank" rel="noopener">JFrog — IDE integrations</a>.</p>
    <div class="cards cards-x">
      <div class="card"><h3>🧩 Inline findings</h3><p>Vulnerable dependencies are highlighted in your dependency files with severity and details, without leaving the editor.</p></div>
      <div class="card"><h3>🔗 Connect to your JPD</h3><p>Point the plugin at your JFrog platform URL + an access token; it uses your Xray for the database and policies.</p></div>
      <div class="card"><h3>⏪ Earliest feedback</h3><p>Fix issues before you even commit — the cheapest place to fix anything is in the editor.</p></div>
    </div>
    <div class="callout callout-tip">
      <p class="callout-title">The shift-left ladder</p>
      <p><b>IDE plugin</b> (as you type) → <b>Frogbot</b> (on the PR) → <b>Xray indexing + Watch</b> (in Artifactory) → <b>build-scan gate</b> (in CI). Each rung catches issues later and more expensively, so push detection as far left as you can.</p>
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
 "lede": "Pipelines is the platform's native CI/CD engine. You declare resources and steps in a YAML DSL stored in your Git repo, connect it through integrations, and Pipelines runs it on build nodes — with Artifactory and Xray built in.",
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
    <p class="prose"><strong>JFrog Pipelines is a CI/CD automation engine built into the JFrog Platform.</strong> You define pipelines in a <strong>YAML-based Pipelines DSL</strong> — a set of key-value files known as a <em>pipeline config</em> — and store them in a Git-compatible source repository (any repo on GitHub, GitLab, etc.). Pipelines syncs from that source, loads your DSL, and runs continuous integration and delivery on build nodes. <a href="https://jfrog.com/help/r/jfrog-pipelines-documentation/creating-pipelines" target="_blank" rel="noopener">JFrog — Creating Pipelines</a>.</p>
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
          <tr><td><b>Integration</b></td><td>A stored, secure connection to an external service — GitHub, Artifactory, Kubernetes, etc. You provide the URL endpoint and credentials once; Pipelines stores them centrally.</td></tr>
          <tr><td><b>Pipeline source</b></td><td>The Git repo (added via an integration) that holds your YAML DSL. Pipelines auto-syncs whenever you commit a change to the DSL.</td></tr>
          <tr><td><b>Resource</b></td><td>A source or destination of data used by the pipeline — e.g. a <code>GitRepo</code>, a <code>BuildInfo</code>, an image. Resources connect steps and can trigger them.</td></tr>
          <tr><td><b>Step</b></td><td>A unit of execution (e.g. a <code>Bash</code> step). Steps declare <code>inputResources</code> and <code>inputSteps</code> to express dependencies and ordering.</td></tr>
          <tr><td><b>Pipeline</b></td><td>The named collection of steps and resources that together form a workflow.</td></tr>
        </tbody>
      </table>
    </div>
    <p class="prose muted">Sources: <a href="https://jfrog.com/help/r/jfrog-pipelines-documentation/pipeline-example-hello-world" target="_blank" rel="noopener">JFrog — Pipeline Hello World</a>, <a href="https://jfrog.com/help/r/jfrog-pipelines-documentation/pipelines-step-by-step" target="_blank" rel="noopener">Pipelines step-by-step</a>.</p>
  </section>

  <section id="dsl" class="section">
    <span class="kicker kicker-lab">DSL</span>
    <h2>The YAML DSL: resources + steps</h2>
    <p class="prose">A pipeline config has two main sections. <strong>Resources</strong> declare the data sources/destinations; <strong>pipelines</strong> declare the steps that act on them. Steps wire together via <code>inputSteps</code> (run after) and <code>inputResources</code> (consume/produce). <a href="https://jfrog.com/help/r/jfrog-pipelines-documentation/pipeline-workflow-examples" target="_blank" rel="noopener">JFrog — Workflow examples</a>.</p>
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
      <li><b>Sign in</b> to the JFrog Platform with your Artifactory credentials. On JFrog Cloud, a default dynamic node pool is provisioned for you (a "node pool" is a group of build machines that scale up/down on demand), so you already have build nodes — nothing to install.</li>
      <li><b>Add a GitHub integration.</b> Administration → Pipelines → <b>Integrations</b> → add a GitHub integration with a personal access token (a GitHub token that grants API access) that has the <code>repo</code> + <code>admin</code> <b>scopes</b> (a "scope" is a permission the token is allowed to use).</li>
      <li><b>Add a pipeline source.</b> Point Pipelines at the repo (and branch) holding your YAML DSL, connected through that integration. Pipelines syncs and processes the DSL.</li>
      <li><b>Commit DSL changes.</b> Every commit to the YAML re-syncs the source and reloads the pipeline.</li>
      <li><b>Run it.</b> Trigger manually or via a <code>GitRepo</code> resource that fires steps when the repo changes.</li>
    </ol>
    <p class="prose muted">Source: <a href="https://jfrog.com/help/r/jfrog-pipelines-documentation/pipeline-example-hello-world" target="_blank" rel="noopener">JFrog — Pipeline Example: Hello World</a>.</p>
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
      <figcaption>The official Hello World demonstrates a GitHub integration, a pipeline source, a <code>GitRepo</code> trigger, and <code>inputResources</code>/<code>inputSteps</code> dependencies. Fork the JFrog example repo, update the path values, commit, and watch it run. <a href="https://jfrog.com/help/r/jfrog-pipelines-documentation/pipeline-example-hello-world" target="_blank" rel="noopener">JFrog — Hello World</a>.</figcaption>
    </figure>
    <div class="callout callout-tip">
      <p class="callout-title">Where Artifactory &amp; Xray plug in</p>
      <p>Add a <code>BuildInfo</code> resource to publish build-info to Artifactory, then a promotion step (see <a href="build-promotion.html">Build promotion</a>) gated by an Xray scan. That turns a plain CI pipeline into a secured, traceable delivery pipeline — the whole point of doing CI <em>inside</em> JFrog.</p>
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
 "lede": "Authentication answers \u201cwho are you?\u201d; authorization answers \u201cwhat may you touch?\u201d JFrog uses access tokens for the first and a Users \u2192 Groups \u2192 Permission Targets hierarchy for the second. Get this model right and everything else \u2014 the REST API, Frogbot, CI \u2014 falls into place.",
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
    <h2>Access tokens \u2014 the modern way to authenticate</h2>
    <div class="callout callout-q">
      <p class="callout-title">Authentication vs. authorization</p>
      <p>Two words that sound alike but mean different things. <b>Authentication</b> = proving <em>who you are</em> (done with an access token). <b>Authorization</b> = deciding <em>what you're allowed to do</em> (done with the permissions model later on this page). A token gets you in the door; permissions decide which rooms you can enter.</p>
    </div>
    <p class="prose">An <strong>access token</strong> is a signed credential that identifies you (or a service) to the JFrog Platform. Unlike a password, a token is <em>scoped</em> (it can be limited to specific resources \u2014 "scope" = the set of things it's allowed to touch), <em>revocable</em> (you can kill it without changing your password), and <em>expirable</em> (it can auto-die after a set time). That makes tokens the right choice for CI jobs, the REST API, Frogbot, and IDE plugins. <a href="https://jfrog.com/help/r/jfrog-platform-administration-documentation/access-tokens" target="_blank" rel="noopener">JFrog \u2014 Access Tokens</a>.</p>
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
          <tr><td><b>Admin</b></td><td>Full administrative access to the platform.</td><td>Platform bootstrap/IaC only \u2014 guard it carefully.</td></tr>
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
    <h2>Creating an access token \u2014 three ways</h2>
    <h3 class="subhead">1. From the UI</h3>
    <ol class="steps">
      <li><b>Open token management.</b> Administration \u2192 User Management \u2192 <b>Access Tokens</b> \u2192 <b>Generate Token</b>.</li>
      <li><b>Choose the scope.</b> Pick the user/identity, set an expiry, and (optionally) restrict the scope.</li>
      <li><b>Copy it once.</b> The token value is shown a single time \u2014 store it in a secret manager immediately.</li>
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
    <p class="prose muted">Sources: <a href="https://jfrog.com/help/r/jfrog-platform-administration-documentation/access-tokens" target="_blank" rel="noopener">JFrog \u2014 Access Tokens</a>, <a href="https://jfrog.com/help/r/jfrog-cli/access-tokens" target="_blank" rel="noopener">JFrog CLI \u2014 Access Tokens</a>.</p>
  </section>

  <section id="model" class="section">
    <span class="kicker kicker-art">Model</span>
    <h2>The authorization model: Users \u2192 Groups \u2192 Permission Targets</h2>
    <p class="prose">JFrog never grants permissions to a user directly on a repo. Instead, permissions flow through a three-layer hierarchy. Understanding it is the key to keeping access manageable as your platform grows. <a href="https://jfrog.com/help/r/jfrog-platform-administration-documentation/permissions" target="_blank" rel="noopener">JFrog \u2014 Permissions</a>.</p>
    <figure class="flow" aria-label="Permission hierarchy">
      <div class="flow-row">
        <div class="flow-step flow-art"><span class="flow-step-n">1</span><b>Users</b><small>people &amp; service identities</small></div>
        <span class="flow-conn">\u2192 belong to \u2192</span>
        <div class="flow-step flow-art"><span class="flow-step-n">2</span><b>Groups</b><small>roles, e.g. ci-bots, devs</small></div>
        <span class="flow-conn">\u2192 assigned in \u2192</span>
        <div class="flow-step flow-xray"><span class="flow-step-n">3</span><b>Permission targets</b><small>access to repos/builds</small></div>
      </div>
      <figcaption>Assign users to <b>groups</b> (by role), then grant <b>groups</b> access in <b>permission targets</b>. New hires just join a group and inherit the right access \u2014 no per-user wiring. <a href="https://jfrog.com/help/r/jfrog-platform-administration-documentation/permissions" target="_blank" rel="noopener">JFrog \u2014 Permissions</a>.</figcaption>
    </figure>
  </section>

  <section id="targets" class="section">
    <span class="kicker kicker-x">Authorization</span>
    <h2>Permission targets \u2014 fine-grained access</h2>
    <p class="prose">A <strong>permission target</strong> binds a set of resources (repositories, builds, or release bundles) to the actions a user/group may perform on them. Actions include <strong>read, write/deploy, delete, manage, annotate</strong> (set properties), and <strong>cache</strong> management. You can target specific repos or use wildcards.</p>
    <div class="table-wrap">
      <table class="datatable">
        <thead><tr><th>Element</th><th>Meaning</th></tr></thead>
        <tbody>
          <tr><td><b>Resource scope</b></td><td>Which repos/builds/release-bundles this target covers.</td></tr>
          <tr><td><code>ANY</code></td><td>Wildcard \u2014 every repository.</td></tr>
          <tr><td><code>ANY LOCAL</code></td><td>Every <span class="pill pill-local">local</span> repository.</td></tr>
          <tr><td><code>ANY REMOTE</code></td><td>Every <span class="pill pill-remote">remote</span> repository.</td></tr>
          <tr><td><b>Actions</b></td><td>read / deploy(write) / delete / manage / annotate / cache, granted per user or group.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="callout callout-q">
      <p class="callout-title">Read vs. deploy vs. manage</p>
      <p><b>Read</b> = pull/resolve artifacts. <b>Deploy</b> = push new artifacts. <b>Delete</b> = remove them. <b>Manage</b> = edit the permission target itself (grant access to others) \u2014 the most powerful, hand it out sparingly.</p>
    </div>
    <p class="prose muted">Sources: <a href="https://jfrog.com/help/r/self-managed-pro-pro-x-start-guide/set-up-users-groups-and-permissions" target="_blank" rel="noopener">JFrog \u2014 Set up users, groups &amp; permissions</a>, <a href="https://jfrog.com/help/r/jfrog-platform-administration-documentation/permissions" target="_blank" rel="noopener">JFrog \u2014 Permissions</a>.</p>
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
    <h2>Two distinct goals \u2014 don't conflate them</h2>
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
    <p class="prose">JFrog publishes official Helm charts. You add the chart repo, prepare a couple of secrets (master + join keys), then install into a namespace. <a href="https://jfrog.com/help/r/jfrog-installation-setup-documentation/install-artifactory-on-kubernetes-using-helm" target="_blank" rel="noopener">JFrog \u2014 Install Artifactory on Kubernetes</a>.</p>
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
    <p class="prose muted"><code>upgrade --install</code> is <b>idempotent</b> \u2014 running it once or many times reaches the same result: it installs the first time and upgrades thereafter. ("Idempotent" is a key GitOps property: re-running a command is always safe.) For production, supply a <code>values.yaml</code> file (external database, ingress, persistent volumes) instead of bare <code>--set</code> flags.</p>
  </section>

  <section id="keys" class="section">
    <span class="kicker">Prereq</span>
    <h2>Master &amp; join keys \u2014 generate them first</h2>
    <p class="prose">The JFrog Platform is made of several small services ("microservices") that must trust each other. They authenticate with a shared <strong>join key</strong>, and Artifactory encrypts its stored config with a <strong>master key</strong>. You generate both as random hexadecimal strings and pass them to the chart \u2014 ideally as Kubernetes secrets rather than inline on the command line, so they don't leak into your shell history.</p>
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
    <p class="prose">Artifactory can host Helm charts in a <span class="pill pill-local">local</span> repo, proxy public charts via a <span class="pill pill-remote">remote</span> repo, and aggregate both behind a <span class="pill pill-virtual">virtual</span> repo. You then point the Helm client at the virtual repo's API URL. <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/helm-chart-repositories" target="_blank" rel="noopener">JFrog \u2014 Helm Chart Repositories</a>.</p>
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
      <figcaption>Clients only ever talk to the <b>virtual</b> repo; Artifactory resolves from local-first then remote. <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/helm-chart-repositories" target="_blank" rel="noopener">JFrog \u2014 Helm Chart Repositories</a>.</figcaption>
    </figure>
  </section>

  <section id="oci" class="section">
    <span class="kicker kicker-lab">Modern</span>
    <h2>OCI: push &amp; pull charts as OCI artifacts</h2>
    <p class="prose">Modern Helm (v3.8+) treats charts as <strong>OCI artifacts</strong>. <b>OCI</b> (Open Container Initiative) is the open standard that defines how container images are packaged and stored in registries \u2014 so "chart as an OCI artifact" means your chart is stored using the exact same mechanism as a Docker image, in the same kind of registry. Artifactory supports this directly, so you can push and pull charts to an OCI-enabled repository. <a href="https://jfrog.com/help/r/jfrog-artifactory-documentation/helm-oci-repositories" target="_blank" rel="noopener">JFrog \u2014 Helm OCI Repositories</a>.</p>
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
