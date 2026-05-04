---
name: github-issue-to-md
description: >-
  Fetches GitHub issues for the current repository using the GitHub CLI (gh),
  resolves the repo from git remote origin, and renders full issue content as
  Markdown for analysis or handoff. Use when the user asks to extract, pull, or
  display issues via gh, export an issue to Markdown, or summarize a GitHub
  issue from the linked remote. Triggers: gh issue, issue to markdown,
  提取 issue, GitHub issue 导出.
disable-model-invocation: true
---

# GitHub issue → Markdown (gh)

## Preconditions

- `gh` is installed and authenticated: `gh auth status` must succeed.
- Run shell commands from the **repository root** (directory containing `.git`).
- `git remote get-url origin` should point at GitHub (`github.com` or `GH_HOST` enterprise). `gh` uses this remote when `--repo` is omitted.

## Workflow (agent)

1. **Confirm context**: `cd` to the workspace root that owns the issue (same repo as the linked GitHub project).
2. **Optional sanity check**: `git remote get-url origin` — note `owner/repo` if you need `--repo owner/repo` explicitly.
3. **Fetch issue data** (replace `N` with the issue number):
   ```bash
   gh issue view N --json title,body,state,author,labels,number,url,createdAt,updatedAt,comments
   ```
4. **Parse JSON** and present to the user using the **Markdown template** below (fill every applicable field; if `comments` is empty, state that explicitly).

## Listing issues (optional)

```bash
gh issue list --state open --limit 50 --json number,title,state,labels,url
```

Useful when the user does not know the issue number.

## Markdown output template

Render the issue for the user in this structure (adapt headings if the repo uses another language; keep field names clear):

```markdown
## Issue #<number>: <title>

| Field | Value |
|------|--------|
| **State** | <OPEN|CLOSED> |
| **URL** | <url> |
| **Author** | <author.login> (<author.name if present>) |
| **Created** | <createdAt> |
| **Updated** | <updatedAt> |
| **Labels** | <comma-separated label names, or "None"> |

### Body

<body markdown pasted verbatim>

### Comments

For each comment: **author**, **timestamp** (if available), then body verbatim. If there are no comments: *No comments.*

---
*Source: fetched with `gh issue view <N> --json ...` from repo linked by `origin`.*
```

## Error handling

- If `gh issue view` fails: suggest `gh auth login`, verify issue number exists, or pass `--repo owner/repo` explicitly.
- Private repos require `gh` credentials with access.

## Scope notes

- This skill is **read-only** for issues (no edits, no closing).
- Parser behavior of the project is unchanged; this only **surfaces** issue text for AI or human follow-up.
