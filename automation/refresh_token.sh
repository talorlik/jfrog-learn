#!/usr/bin/env bash
#
# refresh_token.sh - one-command Google Drive OAuth refresh for the NotebookLM
# sync. Mints a fresh refresh token (opens your browser once for consent - that
# step is unavoidable with OAuth user credentials), pushes the resulting JSON to
# the GitHub secret GOOGLE_OAUTH_CREDENTIALS, then re-runs the sync workflow.
#
# Prerequisites:
#   - automation/client_secret.json present (Desktop-app OAuth client from
#     Google Cloud Console -> APIs & Services -> Credentials). gitignored.
#   - gh CLI installed and authenticated (gh auth status).
#   - automation/requirements.txt installed (pip install -r requirements.txt).
#
# If you keep hitting expiry weekly, the root cause is usually the OAuth consent
# screen being in "Testing" status (7-day token lifetime). Publish the app to
# "In production" once - drive.file is non-sensitive, so no verification is
# required - and tokens stop expiring on a timer. See automation/SETUP.md.
set -euo pipefail

REPO="talorlik/jfrog-learn"
SECRET="GOOGLE_OAUTH_CREDENTIALS"
WORKFLOW="sync-to-drive.yml"

cd "$(dirname "$0")"

if [[ ! -f client_secret.json ]]; then
  echo "ERROR: client_secret.json not found in $(pwd)." >&2
  echo "Download the Desktop-app OAuth client JSON from Google Cloud Console" >&2
  echo "(APIs & Services -> Credentials) and save it here as client_secret.json." >&2
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: gh CLI not found. Install it and run 'gh auth login'." >&2
  exit 1
fi

# Resolve the Python interpreter. Prefer the local .venv so a system/Homebrew
# python3 (which won't have the OAuth deps) can never hijack the mint. A venv
# whose base interpreter was deleted by a Homebrew upgrade leaves a dangling
# symlink, so test that it actually runs, not just that the file exists.
if [[ -x .venv/bin/python3 ]] && .venv/bin/python3 -c '' 2>/dev/null; then
  PY=".venv/bin/python3"
else
  PY="python3"
  echo ">> No working .venv found; falling back to system python3 ($(command -v python3))." >&2
  echo "   If the next step fails on a missing dependency, create the venv:" >&2
  echo "     python3 -m venv .venv && .venv/bin/python3 -m pip install -r requirements.txt" >&2
fi

# Fail early with a clear message if the OAuth dependency is missing, rather
# than surfacing it from inside the helper after the browser tries to open.
if ! "$PY" -c 'import google_auth_oauthlib' 2>/dev/null; then
  echo "ERROR: google-auth-oauthlib is not installed for $PY." >&2
  echo "Install the pinned deps and re-run:" >&2
  echo "  $PY -m pip install -r requirements.txt" >&2
  exit 1
fi

# Mint the token. The helper opens a browser for consent and prints a single
# JSON line (client_id, client_secret, refresh_token) as its LAST stdout line.
echo ">> Minting a fresh refresh token (a browser window will open for consent)..."
tmp_json="$(mktemp)"
trap 'rm -f "$tmp_json"' EXIT

# Capture all output, then extract the single-line JSON the helper emits.
"$PY" get_oauth_token.py | tee /dev/tty | grep -E '^\{.*"refresh_token".*\}$' > "$tmp_json"

if [[ ! -s "$tmp_json" ]]; then
  echo "ERROR: no JSON credential line was produced. Did you approve the consent" >&2
  echo "screen? Re-run and click Allow. If it still fails, revoke prior access at" >&2
  echo "https://myaccount.google.com/permissions and try again." >&2
  exit 1
fi

echo ">> Updating GitHub secret $SECRET on $REPO..."
gh secret set "$SECRET" --repo "$REPO" < "$tmp_json"

echo ">> Triggering the sync workflow..."
gh workflow run "$WORKFLOW" --repo "$REPO"

echo ">> Done. Watch the run with:"
echo "     gh run watch --repo $REPO \$(gh run list --repo $REPO --workflow $WORKFLOW --limit 1 --json databaseId --jq '.[0].databaseId')"
echo ">> Reminder: delete client_secret.json if you do not want it lingering:"
echo "     rm $(pwd)/client_secret.json"
