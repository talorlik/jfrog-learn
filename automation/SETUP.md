# Setup: JFrog Learn → Google Drive sync (OAuth)

This automation converts every JFrog Learn content page (HTML) into a native
**Google Doc** — preserving headings, lists, tables, code blocks, and diagrams
(as Mermaid) — and mirrors them into a Google Drive folder named
**`jfrog-learning`**. It runs automatically on every push to `main`, so the Docs
stay in sync with the site. You then add those Docs as **NotebookLM** sources to
get native chat over the content.

- **One Doc per page** + an auto-rebuilt **index Doc** that links to every page.
- **Idempotent:** each run updates the existing Doc in place (same file ID), so
  NotebookLM source links keep working. New pages create new Docs automatically.
- **Diagrams:** the site's CSS/HTML diagrams are converted to Mermaid fenced
  blocks inside the Docs.

## Why OAuth (and not a service account)

A Google **service account** has its own Drive with **zero storage quota**, so
when it tries to *create* a file in a personal (`@gmail.com`) Drive folder it
fails with `storageQuotaExceeded`. The fix that works on a free personal account
is **OAuth**: the sync authenticates **as you**, so created Docs count against
your own 15 GB. You approve access once and store a refresh token as a GitHub
secret — no passwords, no billing, revocable any time.

You only do the steps below **once**. After that it is fully automated.

---

## What you'll set up

1. A Google Cloud **project** with the **Drive API** enabled.
2. The **Google Auth Platform** configured (consent screen) with you as a test
   user, then an **OAuth client** of type **Desktop app**. In the current console
   these are one connected flow — the consent config is a prerequisite wizard you
   run once, then you create the client and download `client_secret.json`.
3. A helper script run once (in a project-local `venv`) to **mint a refresh
   token**.
4. That token JSON added as the GitHub **secret** `GOOGLE_OAUTH_CREDENTIALS`.
5. The GitHub **variable** `DRIVE_FOLDER_ID` set.

Total time: ~10 minutes.

> Note on the UI: Google renamed this area to the **Google Auth Platform**. The
> old "OAuth consent screen" page is now the **Branding** + **Audience** sections,
> and "Credentials → OAuth client IDs" is now the **Clients** section. The steps
> below use the current names.

---

## Step 1 — Create a Google Cloud project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Top project dropdown → **New Project**. Name it e.g. `jfrog-learn-sync` →
   **Create**. Make sure it's selected in the top bar.

## Step 2 — Enable the Google Drive API

1. **APIs & Services → Library**
   ([link](https://console.cloud.google.com/apis/library)).
2. Search **Google Drive API**, open it, click **Enable**.

## Step 3 — Configure the Google Auth Platform and create the OAuth client

In the current console these are one connected flow: the consent screen is a
one-time **Get started** wizard, and only after it's configured can you create a
client. Everything below lives under **Menu → Google Auth Platform**
([link](https://console.cloud.google.com/auth/overview)).

**3a. Configure the consent screen (one-time wizard).** Open **Google Auth
Platform → Branding**. If you see *"Google Auth Platform not configured yet"*,
click **Get started**, then:

1. **App Information** — enter an **App name** (e.g. `jfrog-learn-sync`) and pick
   your email as **User support email** → **Next**.
2. **Audience** — select **External** → **Next**.
3. **Contact Information** — enter your email → **Next**.
4. **Finish** — tick **I agree to the Google API Services: User Data Policy** →
   **Continue** → **Create**.

> You don't configure scopes here — the script requests the Drive scope at run
> time. (Scopes live under **Data access** if you ever need them.)

**3b. Add yourself as a test user.** Go to **Google Auth Platform → Audience**.
Under **Test users**, click **Add users**, enter **your own Gmail address**, and
click **Save**.

> Keeping the app in **Testing** is fine. Caveat: refresh tokens for Testing
> apps can expire after ~7 days. To make the token permanent, on the **Audience**
> page click **Publish app** (you can ignore Google's verification prompt — it's
> not required for your own personal-Drive app). See "Keeping the token alive".

**3c. Create the OAuth client (Desktop app).** Go to **Google Auth Platform →
Clients** → **Create client**
([link](https://console.cloud.google.com/auth/clients)):

1. **Application type: Desktop app** (NOT "Web application" — Desktop app needs
   no redirect URIs and works with the local helper script).
2. **Name** it e.g. `jfrog-learn-cli` → **Create**.
3. In the confirmation dialog click **Download JSON** (or later, the download
   icon next to the client in the Clients list). Save it as
   **`client_secret.json`** inside the `automation/` folder of your local clone.

## Step 4 — Mint a refresh token (run once, locally)

On your own computer (it needs a browser). Use a **project-local virtual
environment** so dependencies stay inside the repo and don't touch your system
Python:

```bash
cd automation

# Create and activate a venv inside the project (one time):
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# Install deps into the venv:
pip install -r requirements.txt google-auth-oauthlib

# Run the helper (uses ./client_secret.json):
python get_oauth_token.py
```

1. A browser opens. **Sign in with the same Gmail account** you added as a test
   user, and **approve** Drive access. (You may see an "unverified app" warning
   because it's your own test app — click **Advanced → Go to … (unsafe)** to
   continue; it's your own app accessing your own Drive.)
2. The script prints a **single line of JSON** containing `client_id`,
   `client_secret`, and `refresh_token`. **Copy that entire line.**

> The `.venv/` folder is git-ignored, so it won't be committed. When you're done
> you can run `deactivate`. CI does **not** use this venv — GitHub Actions
> installs `requirements.txt` fresh on its runner.
>
> Keep `client_secret.json` and the printed token private. The repo's
> `.gitignore` already excludes them so they won't be committed.

## Step 5 — Add the token as a GitHub secret

1. GitHub repo → **Settings → Secrets and variables → Actions**
   ([link](https://github.com/talorlik/jfrog-learn/settings/secrets/actions)).
2. **Secrets** tab → **New repository secret**.
3. **Name:** `GOOGLE_OAUTH_CREDENTIALS`
4. **Value:** paste the single JSON line from Step 4 → **Add secret**.

## Step 6 — Point CI at the existing folder

1. Same page → **Variables** tab → **New repository variable**
   ([link](https://github.com/talorlik/jfrog-learn/settings/variables/actions)).
2. **Name:** `DRIVE_FOLDER_ID`
3. **Value:** `1zk92hPtiIWvFULqCaBlDhj9IgblbIsJg`
   (the existing
   [jfrog-learning folder](https://drive.google.com/drive/folders/1zk92hPtiIWvFULqCaBlDhj9IgblbIsJg))
   → **Add variable**.

> Because the sync now runs **as you**, it can already see and write this folder
> in your own Drive — no folder sharing needed.

---

## Step 7 — Run it

The workflow runs automatically on any push to `main` that changes `pages/**`.
To run it immediately:

1. GitHub repo → **Actions** tab → **Sync to Google Drive** → **Run workflow**.

   [Open the workflow](https://github.com/talorlik/jfrog-learn/actions/workflows/sync-to-drive.yml)

When it finishes, open the `jfrog-learning` folder in Drive — one Google Doc per
page plus **JFrog Learn — Index**.

## Step 8 — Add the Docs to NotebookLM

1. Open [NotebookLM](https://notebooklm.google.com/) → **New notebook**.
2. **Add source → Google Drive**, then select the JFrog Learn Docs.
3. Since the sync updates Docs **in place** (same file ID), re-syncing just needs
   a **refresh** in NotebookLM, not re-adding.

---

## Keeping the token alive

If your OAuth app stays in **Testing** mode, Google may expire the refresh token
after ~7 days, and the workflow will start failing with an auth error. To make it
permanent, go to **Google Auth Platform → Audience** and click **Publish app**.
Publishing a personal app for your own Drive does **not** require Google's
verification review. After publishing, the refresh token from Step 4 keeps
working indefinitely. (If a token ever does expire, just re-run Step 4 and update
the secret.)

## Running locally (optional)

```bash
cd automation
source .venv/bin/activate          # the venv created in Step 4

# Dry run — writes Markdown previews to automation/_md_preview/, no Drive writes:
python sync_to_drive.py --dry-run

# Real run against Drive, as you (paste your token JSON into the env var):
export GOOGLE_OAUTH_CREDENTIALS='{"client_id":"...","client_secret":"...","refresh_token":"..."}'
export DRIVE_FOLDER_ID=1zk92hPtiIWvFULqCaBlDhj9IgblbIsJg
python sync_to_drive.py
```

## Troubleshooting

- **`no credentials` / `GOOGLE_OAUTH_CREDENTIALS is missing required field(s)`** —
  the secret is empty or malformed. It must be the exact single JSON line printed
  by `get_oauth_token.py` (with `client_id`, `client_secret`, `refresh_token`).
- **`invalid_grant` / token expired** — your app is in Testing mode and the
  7-day window lapsed. **Publish** the OAuth app (see above), or re-run Step 4 and
  update the secret.
- **`storageQuotaExceeded`** — this should no longer happen with OAuth. If you
  see it, the workflow is still using the old service-account secret; make sure
  `GOOGLE_OAUTH_CREDENTIALS` is set (it takes priority) and remove the old
  `GOOGLE_SERVICE_ACCOUNT_JSON` secret if present.
- **No `refresh_token` returned by the helper** — re-run it; if Google skips the
  consent screen (because you already approved), first revoke access at
  [myaccount.google.com/permissions](https://myaccount.google.com/permissions)
  then run it again so it issues a fresh refresh token.

## Files

- `automation/html_to_markdown.py` — HTML → Markdown converter.
- `automation/sync_to_drive.py` — converts pages and upserts Google Docs;
  rebuilds the index Doc. Prefers OAuth; falls back to a service account.
- `automation/get_oauth_token.py` — one-time helper to mint the OAuth refresh
  token.
- `automation/requirements.txt` — Python dependencies for the sync (CI). The
  token helper additionally needs `google-auth-oauthlib` (installed locally only).
- `.github/workflows/sync-to-drive.yml` — runs the sync on push to `main`.
