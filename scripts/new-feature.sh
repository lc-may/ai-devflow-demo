#!/usr/bin/env bash
# Creates a new branch from up-to-date local main, or switches to it if it already exists locally.
set -euo pipefail

usage() {
  echo "Usage: $0 <branch-suffix|full-branch-name>" >&2
  echo "  Examples:" >&2
  echo "    $0 uart-parser       -> creates feature/uart-parser from updated main, or checks it out if it exists" >&2
  echo "    $0 hotfix/critical   -> same for hotfix/critical" >&2
  exit 1
}

if [[ $# -lt 1 ]]; then
  usage
fi

raw="$1"
if [[ "$raw" == */* ]]; then
  branch="$raw"
else
  branch="feature/${raw}"
fi

git rev-parse --git-dir >/dev/null 2>&1 || {
  echo "Error: not a git repository." >&2
  exit 1
}

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Error: working tree has uncommitted changes. Commit or stash them before switching branches." >&2
  exit 1
fi

if git show-ref --verify --quiet "refs/heads/${branch}"; then
  echo "Branch already exists locally: ${branch}"
  git checkout "${branch}"
else
  echo "Fetching origin..."
  git fetch origin

  echo "Updating main..."
  git checkout main
  git pull origin main

  echo "Creating branch: ${branch}"
  git checkout -b "${branch}"
fi

echo "Done. Current branch: $(git branch --show-current)"
