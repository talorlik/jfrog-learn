#!/usr/bin/env python3
"""
get_oauth_token.py — one-time helper to mint an OAuth refresh token so the sync
can act as YOU (your personal Google account), avoiding the service-account
zero-quota problem.

Run this ONCE on your own computer. It opens a browser, you log in and approve
Drive access, and it prints a JSON blob. Paste that JSON into the GitHub secret
GOOGLE_OAUTH_CREDENTIALS. You never need to run this again unless the token is
revoked.

Prerequisites:
    pip install google-auth-oauthlib
    A Desktop-app OAuth client downloaded as client_secret.json (see SETUP.md).

Usage:
    python get_oauth_token.py                 # looks for ./client_secret.json
    python get_oauth_token.py /path/to/client_secret.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    sys.exit(
        "Missing dependency. Run:  pip install google-auth-oauthlib\n"
        "Then re-run this script."
    )

# Must match sync_to_drive.py. drive.file is non-sensitive (no verification),
# so the app can be published to production and tokens won't expire after 7 days.
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def main():
    client_secret = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("client_secret.json")
    if not client_secret.exists():
        sys.exit(
            f"Cannot find {client_secret}. Download your OAuth *Desktop app* client\n"
            "from Google Cloud Console (APIs & Services -> Credentials) and save it\n"
            "as client_secret.json next to this script (or pass its path)."
        )

    flow = InstalledAppFlow.from_client_secrets_file(str(client_secret), SCOPES)
    # Opens a local browser; falls back to console if no browser is available.
    try:
        creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")
    except Exception:
        creds = flow.run_console()

    if not creds.refresh_token:
        sys.exit(
            "No refresh_token was returned. Re-run and make sure to APPROVE the "
            "consent screen (use a fresh consent: revoke prior access if needed)."
        )

    out = {
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "refresh_token": creds.refresh_token,
    }
    blob = json.dumps(out)

    print("\n" + "=" * 70)
    print("SUCCESS. Copy the single line below and paste it into the GitHub secret")
    print("named  GOOGLE_OAUTH_CREDENTIALS  (Settings -> Secrets and variables ->")
    print("Actions -> New repository secret):")
    print("=" * 70 + "\n")
    print(blob)
    print("\n" + "=" * 70)
    print("Keep this private. It grants Drive access to your account.")
    print("=" * 70)


if __name__ == "__main__":
    main()
