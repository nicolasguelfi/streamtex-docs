# Documentation legacy cleanup — autonomous run log

Started: 2026-05-19

## Design language (audit before run)

Canonical BlockStyles pattern (from `bck_reuse_welcome.py`, `bck_reuse_vocabulary.py`,
`bck_component_format.py`):

```python
class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub     = s.project.titles.section_subtitle   # violet/amber accent
    body    = s.large
    cell    = s.container.borders.solid_border + s.container.paddings.small_padding
    code    = s.container.paddings.small_padding + s.container.borders.solid_border
    section = s.bold + s.large                    # inner h3-like
```

Available palette (`custom/styles.py`):
- callouts: good/bad/tip/note/result_callout
- boxes: code_box, explanation_box, details_box
- labels: tip_label, warning_label, explanation_label, details_label
- cell: project.containers.cell

Naming: `bs.<role>` shortened alias, always.

## Phase log

### Phase 1 — Foundations (done, ruff + imports green)
- 1.1/1.2: `## StreamTeX Patterns` section in `streamtex-docs/CLAUDE.md`
  and `streamtex/CLAUDE.md` replaced by `## Reuse architecture`.
- 1.3: no CLAUDE.md in `streamtex-claude/` or `streamtex-design/`.
- 1.4: cheatsheet `## Patterns` section (17 obsolete commands)
  replaced by `## Reuse architecture` mapping every active CLI.
- 1.5: `bck_reuse_welcome.py` legacy refs (streamtex-patterns) refreshed.
- Pre-Phase 1: `bs.sub` in the 2 already-ported Q13b blocks aligned
  on `s.project.titles.section_subtitle` (canonical pattern).

### Phase 2 — Reuse manual (done, 11/12 new blocks)
- 11 blocks written, each grounded on cited source files in the
  module docstring. Wired into `book.py` (8 logical parts).
- Deferred: `bck_custom_import_mapping` — no source in code.

### Phase 3 — Render purge (done)
- Deleted: `bck_render.py` (deploy), `bck_render_deployment.py`
  (developer atomic).
- Fixed wirings: deploy `book.py`, developer `bck_dev_ci_cd.py`.
- Render mentions fixed in: cheatsheet, intro x2, advanced x2,
  collection.toml, deploy bck_welcome.py x2, deploy bck_level_badge.py,
  deploy bck_cli_deploy_commands.py, developer bck_cli_architecture.py,
  deploy book.py comment.
- Final scan: 0 legacy Render refs.

### Phase 4 — Surgical vocab sweep (done)
Final counts (legitimate quoted mentions excluded):
- `stx patterns <verb>`: 0
- `/stx-pattern:*`: 0
- `_pattern_library`: 0
- `block-blueprints.md`: 0 (7 fixes in stx_manual_ai)
- `ptn_*`: 10 — all false positives (real Python identifiers in
  `streamtex.bib` + Style instance names in cheatsheet examples).

### Phase 5 — Housekeeping (done)
- 5 `.bak` files deleted.
- 8 manuals compile + 178 blocks load.
- Repo-wide `ruff check` green.
- CHANGELOG entry consolidated (Q13 a/b/c merged into the
  Autonomous-cleanup entry).
