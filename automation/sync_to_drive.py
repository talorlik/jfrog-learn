#!/usr/bin/env python3
"""
sync_to_drive.py — Convert every JFrog Learn content page to Markdown and mirror
it into Google Drive as native Google Docs (one Doc per page) inside a
'jfrog-learning' folder, plus an auto-rebuilt index Doc. Designed to run in CI on
every push to main, then have NotebookLM use the Docs as sources.

Auth (two modes; OAuth is preferred for personal @gmail.com accounts):

  1. OAuth user credentials (recommended) — the script acts as YOU, so created
     Docs count against your own 15 GB Drive quota. Provide a single env var
     GOOGLE_OAUTH_CREDENTIALS containing JSON with:
         {"client_id": "...", "client_secret": "...", "refresh_token": "..."}
     In CI, store that JSON as the GitHub secret GOOGLE_OAUTH_CREDENTIALS.

  2. Service account (only works for Google Workspace / Shared Drives) — provide
     the key JSON via GOOGLE_SERVICE_ACCOUNT_JSON, or a key file path via
     GOOGLE_APPLICATION_CREDENTIALS. NOTE: a service account has its own
     zero-quota Drive, so CREATING files in a personal My Drive folder fails with
     'storageQuotaExceeded'. Use OAuth instead on personal accounts.

Scope: the OAuth path requests the NON-SENSITIVE 'drive.file' scope, which lets
the app see/manage only files IT creates. This avoids Google's verification +
logo + authorized-domain requirements, so the OAuth app can be published to
production (refresh tokens never expire) with no review.

Folder: because of drive.file, the app manages its OWN 'jfrog-learning' folder.
DRIVE_FOLDER_ID is optional and normally unset; if set to a folder the app can't
access (e.g. one created by another tool), the script detects that and falls back
to creating/reusing its own folder by name (DRIVE_FOLDER_NAME, default
'jfrog-learning').

Idempotency: the folder is the source of truth. Each run looks up Docs by exact
name; if found it UPDATES the existing Doc's content (same file id, so NotebookLM
source links stay valid); if not found it CREATES a new Doc.

Diagrams: handled upstream in html_to_markdown.py (CSS/HTML diagrams -> Mermaid
fenced code blocks; text fallback otherwise). No image rendering needed today.
"""
from __future__ import annotations

import io
import json
import os
import sys
import time
from pathlib import Path

from google.oauth2 import service_account
from google.oauth2.credentials import Credentials as UserCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

import html_to_markdown as H

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = REPO_ROOT / "pages"
FOLDER_NAME = os.environ.get("DRIVE_FOLDER_NAME", "jfrog-learning")
EXPLICIT_FOLDER_ID = os.environ.get("DRIVE_FOLDER_ID", "").strip()

# Pages to exclude from the sync (search functionality, etc.)
EXCLUDE = {"search"}

GOOGLE_DOC_MIME = "application/vnd.google-apps.document"
FOLDER_MIME = "application/vnd.google-apps.folder"
SITE_BASE_URL = os.environ.get("SITE_BASE_URL", "https://talorlik.github.io/jfrog-learn")

# Non-sensitive scope: the app can only see/manage files IT creates. This avoids
# Google's verification + logo + authorized-domain requirements, so the OAuth app
# can be published to 'In production' (refresh tokens then never expire) with no
# review. Consequence: the app manages its OWN 'jfrog-learning' folder and Docs;
# it cannot touch files created outside the app (e.g. a manually uploaded Doc).
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# Order pages match the site's learning path / sidebar
PAGE_ORDER = [
    "fundamentals",
    "replication-federation",
    "build-promotion",
    "release-bundles",
    "rest-api",
    "frogbot",
    "pipelines",
    "access-tokens",
    "kubernetes-helm",
]

DOC_NAME_PREFIX = "JFrog Learn — "
INDEX_DOC_NAME = "JFrog Learn — Index"


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

TOKEN_URI = "https://oauth2.googleapis.com/token"


def _oauth_creds_from_json(raw: str):
    info = json.loads(raw)
    missing = [k for k in ("client_id", "client_secret", "refresh_token") if not info.get(k)]
    if missing:
        sys.exit(
            "ERROR: GOOGLE_OAUTH_CREDENTIALS is missing required field(s): "
            + ", ".join(missing)
            + ". It must be JSON with client_id, client_secret, refresh_token."
        )
    return UserCredentials(
        token=None,
        refresh_token=info["refresh_token"],
        client_id=info["client_id"],
        client_secret=info["client_secret"],
        token_uri=info.get("token_uri", TOKEN_URI),
        scopes=SCOPES,
    )


def get_drive():
    """Build a Drive client. Prefer OAuth user creds (works on personal Gmail);
    fall back to a service account (Workspace / Shared Drives only)."""
    oauth = os.environ.get("GOOGLE_OAUTH_CREDENTIALS", "").strip()
    sa_raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    keyfile = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "").strip()

    if oauth:
        creds = _oauth_creds_from_json(oauth)
        print("auth: OAuth user credentials")
    elif sa_raw:
        creds = service_account.Credentials.from_service_account_info(
            json.loads(sa_raw), scopes=SCOPES
        )
        print("auth: service account (JSON)")
    elif keyfile and Path(keyfile).exists():
        creds = service_account.Credentials.from_service_account_file(keyfile, scopes=SCOPES)
        print("auth: service account (key file)")
    else:
        sys.exit(
            "ERROR: no credentials. Set GOOGLE_OAUTH_CREDENTIALS (recommended; JSON "
            "with client_id, client_secret, refresh_token), or a service account via "
            "GOOGLE_SERVICE_ACCOUNT_JSON / GOOGLE_APPLICATION_CREDENTIALS."
        )
    # cache_discovery=False avoids a noisy warning in CI
    return build("drive", "v3", credentials=creds, cache_discovery=False)


# ---------------------------------------------------------------------------
# Drive helpers
# ---------------------------------------------------------------------------

def _q_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'")


def find_or_create_folder(drive, name: str) -> str:
    # If a folder id is pinned, use it ONLY if this app can actually access it.
    # Under the drive.file scope the app can't see files it didn't create, so a
    # folder made elsewhere (e.g. via another tool) will 404/403 here — in that
    # case we fall through and manage our own folder instead.
    if EXPLICIT_FOLDER_ID:
        try:
            drive.files().get(
                fileId=EXPLICIT_FOLDER_ID, fields="id", supportsAllDrives=True
            ).execute()
            return EXPLICIT_FOLDER_ID
        except HttpError as e:
            status = getattr(getattr(e, "resp", None), "status", None)
            if status in (403, 404):
                print(
                    f"NOTE: DRIVE_FOLDER_ID={EXPLICIT_FOLDER_ID} is not accessible to "
                    f"this app (scope is drive.file, which only sees app-created "
                    f"files). Falling back to an app-owned '{name}' folder."
                )
            else:
                raise
    # Find an app-created folder by name (drive.file only returns app-created ones).
    q = (
        f"name = '{_q_escape(name)}' and mimeType = '{FOLDER_MIME}' "
        f"and trashed = false"
    )
    res = drive.files().list(
        q=q, fields="files(id,name)", spaces="drive",
        supportsAllDrives=True, includeItemsFromAllDrives=True,
    ).execute()
    files = res.get("files", [])
    if files:
        return files[0]["id"]
    meta = {"name": name, "mimeType": FOLDER_MIME}
    folder = drive.files().create(body=meta, fields="id", supportsAllDrives=True).execute()
    print(f"created folder '{name}' -> {folder['id']}")
    return folder["id"]


def find_doc(drive, folder_id: str, name: str):
    q = (
        f"name = '{_q_escape(name)}' and mimeType = '{GOOGLE_DOC_MIME}' "
        f"and '{folder_id}' in parents and trashed = false"
    )
    res = drive.files().list(
        q=q, fields="files(id,name,modifiedTime)", spaces="drive",
        supportsAllDrives=True, includeItemsFromAllDrives=True,
    ).execute()
    files = res.get("files", [])
    return files[0] if files else None


def _media_from_markdown(md_text: str) -> MediaIoBaseUpload:
    data = md_text.encode("utf-8")
    return MediaIoBaseUpload(
        io.BytesIO(data), mimetype="text/markdown", resumable=False
    )


def upsert_doc(drive, folder_id: str, name: str, md_text: str) -> tuple[str, str]:
    """Create or update a Google Doc from Markdown. Returns (file_id, action)."""
    media = _media_from_markdown(md_text)
    existing = find_doc(drive, folder_id, name)
    for attempt in range(3):
        try:
            if existing:
                fid = existing["id"]
                # Update content in place: upload new markdown media; Drive
                # re-converts it into the Google Doc, keeping the same file id.
                drive.files().update(
                    fileId=fid, media_body=media, supportsAllDrives=True,
                    body={"name": name},
                ).execute()
                return fid, "updated"
            else:
                meta = {
                    "name": name,
                    "mimeType": GOOGLE_DOC_MIME,
                    "parents": [folder_id],
                }
                created = drive.files().create(
                    body=meta, media_body=media, fields="id",
                    supportsAllDrives=True,
                ).execute()
                return created["id"], "created"
        except HttpError as e:
            status = getattr(e, "status_code", None) or getattr(e.resp, "status", None)
            if status in (429, 500, 502, 503) and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise
    raise RuntimeError(f"failed to upsert '{name}'")


# ---------------------------------------------------------------------------
# Build markdown for each page
# ---------------------------------------------------------------------------

def doc_name_for(slug: str, title: str) -> str:
    return f"{DOC_NAME_PREFIX}{title}"


def list_pages() -> list[str]:
    slugs = []
    for p in sorted(PAGES_DIR.glob("*.html")):
        slug = p.stem
        if slug in EXCLUDE:
            continue
        slugs.append(slug)
    # order known pages first, then any extras alphabetically
    ordered = [s for s in PAGE_ORDER if s in slugs]
    extras = [s for s in slugs if s not in PAGE_ORDER]
    return ordered + extras


def build_markdown(slug: str) -> tuple[str, str]:
    html = (PAGES_DIR / f"{slug}.html").read_text(encoding="utf-8")
    title, body = H.convert_page(html)
    src_url = f"{SITE_BASE_URL}/pages/{slug}.html"
    header = f"# {title}\n\n*Source: [{title}]({src_url})*\n\n"
    return title, header + body + "\n"


def build_index_markdown(entries: list[dict]) -> str:
    lines = [
        "# JFrog Learn — Index",
        "",
        "*Auto-generated index of all JFrog Learn pages, kept in sync with the "
        f"[website]({SITE_BASE_URL}/) on every push.*",
        "",
        "Each entry links to its Google Doc (use these as NotebookLM sources) and "
        "to the live page.",
        "",
        "## Pages",
        "",
    ]
    for i, e in enumerate(entries, 1):
        doc_link = f"https://docs.google.com/document/d/{e['file_id']}/edit"
        lines.append(
            f"{i}. **[{e['title']}]({doc_link})** — "
            f"[live page]({e['site_url']})"
        )
    lines += [
        "",
        "---",
        "",
        f"Total pages: {len(entries)}. Folder: '{FOLDER_NAME}'.",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    dry = "--dry-run" in sys.argv
    out_dir = REPO_ROOT / "automation" / "_md_preview"
    if dry:
        out_dir.mkdir(parents=True, exist_ok=True)

    slugs = list_pages()
    print(f"pages to sync ({len(slugs)}): {', '.join(slugs)}")

    if dry:
        entries = []
        for slug in slugs:
            title, md = build_markdown(slug)
            (out_dir / f"{slug}.md").write_text(md, encoding="utf-8")
            entries.append({
                "title": title,
                "file_id": f"DRYRUN_{slug}",
                "site_url": f"{SITE_BASE_URL}/pages/{slug}.html",
            })
            print(f"  [dry] {slug}: {len(md)} chars -> {out_dir / (slug + '.md')}")
        idx = build_index_markdown(entries)
        (out_dir / "_index.md").write_text(idx, encoding="utf-8")
        print(f"  [dry] index -> {out_dir / '_index.md'}")
        print("dry run complete; no Drive writes performed.")
        return

    drive = get_drive()
    folder_id = find_or_create_folder(drive, FOLDER_NAME)
    print(f"folder '{FOLDER_NAME}' -> {folder_id}")

    entries = []
    for slug in slugs:
        title, md = build_markdown(slug)
        name = doc_name_for(slug, title)
        fid, action = upsert_doc(drive, folder_id, name, md)
        print(f"  {action}: {name} -> {fid}")
        entries.append({
            "title": title,
            "file_id": fid,
            "site_url": f"{SITE_BASE_URL}/pages/{slug}.html",
        })

    # Always rebuild the index doc last (so it has all fresh file ids)
    idx_md = build_index_markdown(entries)
    idx_id, idx_action = upsert_doc(drive, folder_id, INDEX_DOC_NAME, idx_md)
    print(f"  {idx_action}: {INDEX_DOC_NAME} -> {idx_id}")

    print(f"\nDone. {len(entries)} page Docs + 1 index in folder '{FOLDER_NAME}'.")
    print(f"Folder: https://drive.google.com/drive/folders/{folder_id}")


if __name__ == "__main__":
    main()
