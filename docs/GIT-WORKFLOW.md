# Git and PR Workflow

**Owner directive:** 2026-10-20
**Status:** Active
**Scope:** every human or agent changing this repository.

## Non-negotiables

1. **Never work directly on `main`.** Start every task on a branch. Continuing
   an existing task on its branch is fine; starting unrelated work requires a
   new branch from current `main`.
2. **Pull before push.** `git fetch origin --prune` then
   `git pull --ff-only origin main` (or merge/rebase `origin/main` into the
   work branch) before every push.
3. **Pending PRs come first.** If open PRs exist, review and merge them before
   starting unrelated work. Fix their failing checks; do not bypass branch
   protection.
4. **Green gates only.** Required CI checks, local `verify_all.py`, and the
   relevant test suite must pass before a PR is mergeable.
5. **Clean up after merge.** Delete merged local/remote branches, prune stale
   tracking refs, and remove temporary worktrees.
6. **Log it.** Record merged PRs, branch cleanup, and pre-existing failures in
   the active session log and plan. Do not silently skip a red gate.

## Standard loop

```bash
git fetch origin --prune
git switch main
git pull --ff-only origin main
git switch -c feat/<short-slug>

# ... work, validate ...

git fetch origin --prune
git merge origin/main            # or rebase, if the branch is private
python3 scripts/verify_all.py
pytest -q

git push -u origin HEAD
gh pr create --fill
gh pr checks --watch
```

After merge:

```bash
git switch main
git pull --ff-only origin main
git branch -d <branch>
git push origin --delete <branch>   # if not auto-deleted
git fetch origin --prune
```

## Handling bot PRs

Dependabot PRs are normal PRs: update the branch if it is stale, wait for the
required checks, then merge with the repository's configured method. If a bot
PR fails because of a pre-existing issue, fix the issue on a separate branch
first (or in the bot branch if the fix is scoped), record it, and then merge.

## What not to do

- Do not force-push shared branches.
- Do not merge with red or missing required checks.
- Do not delete an unmerged branch without confirming its commits are preserved.
- Do not commit generated artifacts that the repository treats as derived unless
  the change is intentional and reproducible.
- Do not claim cleanup happened unless `git branch -vv`, `git ls-remote`, and
  `gh pr list` confirm it.
