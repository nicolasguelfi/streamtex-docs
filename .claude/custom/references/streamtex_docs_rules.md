# streamtex-docs — Repo-Specific Rules

These rules apply ONLY to the `streamtex-docs` repository (the official documentation project).
They complement the standard documentation profile rules in CLAUDE.md.

## Library Protection (MANDATORY)
**NEVER** automatically modify the `streamtex` library code (the `streamtex` package/repo) without explicit user approval.
Any change that could affect functional or non-functional properties (performance, caching, state management, API behavior) of the library MUST be:
1. **Investigated and explained** to the user first
2. **Explicitly approved** by the user before any modification
3. **Applied only in the `streamtex` repo**, never patched from `streamtex-docs`

This applies even for seemingly small fixes. The library is a shared dependency — unintended side effects can propagate to all users.

## Change Propagation (MANDATORY)
When a change is made to the **streamtex library** or to **shared configuration** (e.g. `.streamlit/config.toml`, templates, CLI generators), you MUST verify and propagate the change to **all impacted components**:
1. **All manuals** — `manuals/stx_manual_*/` (config, blocks referencing the changed feature)
2. **Templates** — `templates/template_project/`, `templates/template_collection/` (so new projects inherit the change)
3. **CLI generators** — `streamtex/cli/project_cmd.py` and related (so `stx project new` produces up-to-date projects)
4. **User-facing documentation** — manual blocks that describe the changed feature or configuration
5. **Coding standards & cheatsheet** — `.claude/references/` if the change affects coding conventions

Always ask yourself: *"Who else uses this? Where else is this referenced?"* before considering a change complete.

## Release Workflow (PyPI)
1. Bump version in `pyproject.toml` + `streamtex/__init__.py` (in the `streamtex` repo)
2. `uv run pytest tests/ -v && uv run ruff check streamtex/`
3. `uv lock && git add pyproject.toml streamtex/__init__.py uv.lock && git commit && git push`
4. `gh release create vX.Y.Z -R nicolasguelfi/streamtex` → triggers publish.yml → PyPI

## Render Deploy — Manual Mode Active
The `push` trigger is **disabled** in `.github/workflows/render-deploy.yml` (free tier limits).
- Deploys are done **only** via: `gh workflow run render-deploy.yml -R nicolasguelfi/streamtex-docs`
- **After a series of important manual commits**, suggest the user trigger a manual deploy
- To re-enable auto-deploy when docs are stable: uncomment the `push` lines in the workflow

## Staging Workflow
Staging (`https://docs-staging.streamtex.org`) runs on Hetzner/Coolify with `Dockerfile.staging`.
It installs the streamtex lib from a **git branch** at container startup (not from PyPI).

### Commands (`deploy-staging.sh`)
```bash
./deploy-staging.sh --lib-branch fix/foo                    # lib branch only
./deploy-staging.sh --lib-branch fix/foo --docs-branch fix/bar  # both branches
./deploy-staging.sh --status                                # show session + staleness
./deploy-staging.sh --cleanup                               # reset to main/main
./deploy-staging.sh --conclude                              # merge branches → main
```

### Rules (MANDATORY)
- **NEVER push staging infra changes to `streamtex-docs/main`** — triggers prod redeploy of all services
- For `Dockerfile.staging`, `staging-banner.sh`, `deploy-staging.sh` changes: create a branch, use `--docs-branch`
- The staging banner shows lib branch, commit, version, docs branch, commit, and deploy time
- After validation: merge branches → main (use `--conclude` or manual merge + cleanup)

### Technical constraints
- Container uses `/app/.venv/bin/` binaries directly (not `uv run`) to avoid lockfile re-sync
- `uv pip install --no-cache` to avoid stale git refs
- Docs git info passed as Coolify env vars (`.git/` excluded from Docker image by `.dockerignore`)
