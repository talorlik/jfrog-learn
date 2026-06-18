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
2. An **OAuth consent screen** (External, with you as a test user).
3. An **OAuth client** of type **Desktop app** (download `client_secret.json`).
4. Run a helper script once to **mint a refresh token**.
5. Add that token JSON as the GitHub **secret** `GOOGLE_OAUTH_CREDENTIALS`.
6. Set the GitHub **variable** `DRIVE_FOLDER_ID`.

Total time: ~10 minutes.

---

## Step 1 — Create a Google Cloud project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Top project dropdown → **New Project**. Name it e.g. `jfrog-learn-sync` →
   **Create**. Make sure it's selected in the top bar.

## Step 2 — Enable the Google Drive API

1. **APIs & Services → Library**
   ([link](https://console.cloud.google.com/apis/library)).
2. Search **Google Drive API**, open it, click **Enable**.

## Step 3 — Configure the OAuth consent screen

1. **APIs & Services → OAuth consent screen**
   ([link](https://console.cloud.google.com/apis/credentials/consent)).
2. User type: **External** → **Create**.
3. Fill the required fields: **App name** (e.g. `jfrog-learn-sync`), **User
   support email** (your email), **Developer contact email** (your email).
   Leave the rest blank → **Save and Continue**.
4. **Scopes** page → just **Save and Continue** (the script requests the Drive
   scope at run time; you don't need to add it here).
5. **Test users** page → **Add Users** → enter **your own Gmail address** →
   **Save and Continue**.

   > Keeping the app in "Testing" mode is fine. The only caveat: refresh tokens
   > for apps in Testing can expire after 7 days. To make the token permanent,
   > after finishing setup come back here and click **Publish app** (you can
   > ignore Google's verification prompt — it's not required for your own Drive
   > with a Testing/Published personal app). See "Keeping the token alive" below.

## Step 4 — Create an OAuth client (Desktop app)

1. **APIs & Services → Credentials**
   ([link](https://console.cloud.google.com/apis/credentials)).
2. **Create Credentials → OAuth client ID**.
3. **Application type: Desktop app**. Name it e.g. `jfrog-learn-cli` → **Create**.
4. In the dialog, click **Download JSON**. Save it as **`client_secret.json`**
   inside the `automation/` folder of your local clone of this repo.

## Step 5 — Mint a refresh token (run once, locally)

On your own computer (it needs a browser):

```bash
cd automation
pip install -r requirements.txt google-auth-oauthlib
python get_oauth_token.py            # uses ./client_secret.json
```

1. A browser opens. **Sign in with the same Gmail account** you added as a test
   user, and **approve** Drive access. (You may see an "unverified app" warning
   because it's your own test app — click **Advanced → Go to … (unsafe)** to
   continue; it's your own app accessing your own Drive.)
2. The script prints a **single line of JSON** containing `client_id`,
   `client_secret`, and `refresh_token`. **Copy that entire line.**

> Keep `client_secret.json` and the printed token private. The repo's
> `.gitignore` already excludes them so they won't be committed.

## Step 6 — Add the token as a GitHub secret

1. GitHub repo → **Settings → Secrets and variables → Actions**
   ([link](https://github.com/talorlik/jfrog-learn/settings/secrets/actions)).
2. **Secrets** tab → **New repository secret**.
3. **Name:** `GOOGLE_OAUTH_CREDENTIALS`
4. **Value:** paste the single JSON line from Step 5 → **Add secret**.

## Step 7 — Point CI at the existing folder

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

## Step 8 — Run it

The workflow runs automatically on any push to `main` that changes `pages/**`.
To run it immediately:

1. GitHub repo → **Actions** tab → **Sync to Google Drive** → **Run workflow**.

   [Open the workflow](https://github.com/talorlik/jfrog-learn/actions/workflows/sync-to-drive.yml)

When it finishes, open the `jfrog-learning` folder in Drive — one Google Doc per
page plus **JFrog Learn — Index**.

## Step 9 — Add the Docs to NotebookLM

1. Open [NotebookLM](https://notebooklm.google.com/) → **New notebook**.
2. **Add source → Google Drive**, then select the JFrog Learn Docs.
3. Since the sync updates Docs **in place** (same file ID), re-syncing just needs
   a **refresh** in NotebookLM, not re-adding.

---

## Keeping the token alive

If your OAuth app stays in **Testing** mode, Google may expire the refresh token
after ~7 days, and the workflow will start failing with an auth error. To make it
permanent, go back to the **OAuth consent screen** and click **Publish app**.
Publishing a personal app for your own Drive does **not** require Google's
verification review. After publishing, the refresh token from Step 5 keeps
working indefinitely. (If a token ever does expire, just re-run Step 5 and update
the secret.)

## Running locally (optional)

```bash
cd automation
pip install -r requirements.txt

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
  7-day window lapsed. **Publish** the OAuth app (see above), or re-run Step 5 and
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
