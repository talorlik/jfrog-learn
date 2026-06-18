# Setup: JFrog Learn → Google Drive sync

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

You only do the steps below **once**. After that it is fully automated.

---

## What you'll set up

1. A Google Cloud **project** with the **Drive API** enabled.
2. A **service account** + a **JSON key**.
3. **Share** the `jfrog-learning` Drive folder with the service account.
4. Add the JSON key as a GitHub **secret** (`GOOGLE_SERVICE_ACCOUNT_JSON`).
5. (Optional) Add the folder ID as a GitHub **variable** (`DRIVE_FOLDER_ID`).

Total time: ~10 minutes.

---

## Step 1 — Create a Google Cloud project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. In the top project dropdown, click **New Project**.
3. Name it e.g. `jfrog-learn-sync` and click **Create**.
4. Make sure the new project is selected (top bar) before continuing.

## Step 2 — Enable the Google Drive API

1. Go to **APIs & Services → Library**
   ([direct link](https://console.cloud.google.com/apis/library)).
2. Search for **Google Drive API**, open it, and click **Enable**.

> You do **not** need to enable the Docs API — the sync uploads Markdown and lets
> Drive convert it to a Google Doc, which is higher fidelity.

## Step 3 — Create a service account

1. Go to **APIs & Services → Credentials**
   ([direct link](https://console.cloud.google.com/apis/credentials)).
2. Click **Create Credentials → Service account**.
3. Give it a name, e.g. `drive-sync`. Click **Create and Continue**.
4. You can **skip** the optional "grant access" and "grant users" steps —
   click **Done**.
5. You'll now see the service account listed. **Copy its email address** — it
   looks like:

   ```
   drive-sync@jfrog-learn-sync.iam.gserviceaccount.com
   ```

   You'll need it in Step 5.

## Step 4 — Create a JSON key

1. Click the service account you just created to open it.
2. Go to the **Keys** tab → **Add Key → Create new key**.
3. Choose **JSON** and click **Create**. A `.json` file downloads to your
   computer. **Keep this file private — it grants access to the account.**

## Step 5 — Share the Drive folder with the service account

A service account has its **own** empty Drive, so it can't see your folder until
you share it. This is the key step that lets CI write into *your* folder.

1. In [Google Drive](https://drive.google.com/), open (or create) the folder
   named **`jfrog-learning`**.
   - A folder already exists for this project:
     **[jfrog-learning](https://drive.google.com/drive/folders/1zk92hPtiIWvFULqCaBlDhj9IgblbIsJg)**
     (ID `1zk92hPtiIWvFULqCaBlDhj9IgblbIsJg`).
2. Right-click the folder → **Share**.
3. Paste the service account **email** from Step 3.
4. Set its role to **Editor**, uncheck "Notify people", and click **Share**.

> Docs created here are owned by the service account but live inside your folder,
> so you see and use them normally. Sharing as Editor lets CI both create and
> update them.

## Step 6 — Add the JSON key as a GitHub secret

1. In GitHub, open the repo → **Settings → Secrets and variables → Actions**.
2. On the **Secrets** tab, click **New repository secret**.
3. **Name:** `GOOGLE_SERVICE_ACCOUNT_JSON`
4. **Value:** open the JSON key file from Step 4 in a text editor, copy its
   **entire contents**, and paste them in. Click **Add secret**.

   [Open repo secrets settings](https://github.com/talorlik/jfrog-learn/settings/secrets/actions)

## Step 7 — (Optional but recommended) Pin the folder ID

So CI writes to the exact existing folder instead of searching by name:

1. Same page → **Variables** tab → **New repository variable**.
2. **Name:** `DRIVE_FOLDER_ID`
3. **Value:** `1zk92hPtiIWvFULqCaBlDhj9IgblbIsJg`
4. Click **Add variable**.

   [Open repo variables settings](https://github.com/talorlik/jfrog-learn/settings/variables/actions)

> Without this, the workflow finds a folder named `jfrog-learning` that the
> service account can see (the one you shared in Step 5).

---

## Step 8 — Run it

The workflow (`.github/workflows/sync-to-drive.yml`) runs automatically on any
push to `main` that changes `pages/**`. To run it immediately:

1. GitHub repo → **Actions** tab → **Sync to Google Drive** workflow.
2. Click **Run workflow → Run workflow** (uses `workflow_dispatch`).

   [Open the workflow](https://github.com/talorlik/jfrog-learn/actions/workflows/sync-to-drive.yml)

When it finishes, open the `jfrog-learning` folder in Drive — you'll see one
Google Doc per page plus **JFrog Learn — Index**.

## Step 9 — Add the Docs to NotebookLM

1. Open [NotebookLM](https://notebooklm.google.com/) → **New notebook**.
2. **Add source → Google Drive**, then select the JFrog Learn Docs (or the whole
   folder's Docs). NotebookLM then gives you native chat over the content.

> NotebookLM has no public "add source" API, so this one step is manual. Because
> the sync updates Docs **in place** (same file ID), re-syncing your existing
> NotebookLM sources just needs a **refresh** in NotebookLM, not re-adding.

---

## Running locally (optional)

```bash
cd automation
pip install -r requirements.txt

# Dry run — writes Markdown previews to automation/_md_preview/, no Drive writes:
python sync_to_drive.py --dry-run

# Real run against Drive (point at your downloaded key file):
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
export DRIVE_FOLDER_ID=1zk92hPtiIWvFULqCaBlDhj9IgblbIsJg
python sync_to_drive.py
```

## Troubleshooting

- **`no service account credentials`** — the `GOOGLE_SERVICE_ACCOUNT_JSON` secret
  is missing or empty. Re-check Step 6.
- **`File not found` / folder created in the wrong place** — the folder wasn't
  shared with the service account (Step 5), or `DRIVE_FOLDER_ID` points at a
  folder the service account can't access. If `DRIVE_FOLDER_ID` is unset and the
  account can't see your folder, it will create its **own** `jfrog-learning`
  folder (inside its own Drive, which you can't see). Always do Step 5, and
  prefer Step 7.
- **`403 insufficientPermissions`** — the folder was shared as Viewer, not
  Editor. Re-share as **Editor**.
- **A Doc looks wrong** — open it; if structure is off, it's a converter issue in
  `automation/html_to_markdown.py`. Run `python sync_to_drive.py --dry-run` and
  inspect the Markdown in `automation/_md_preview/`.

## Files

- `automation/html_to_markdown.py` — HTML → Markdown converter (headings, lists,
  tables, code, callouts, glossaries, diagrams → Mermaid).
- `automation/sync_to_drive.py` — converts every page and upserts Google Docs in
  the Drive folder; rebuilds the index Doc.
- `automation/requirements.txt` — Python dependencies.
- `.github/workflows/sync-to-drive.yml` — runs the sync on push to `main`.
