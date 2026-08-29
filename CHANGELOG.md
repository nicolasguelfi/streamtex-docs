# Changelog — StreamTeX Documentation

All notable changes to the StreamTeX documentation will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Advanced manual — new chapter "Multilingual Documents"**
  (`bck_multilingual_documents.py`, atomic `bck_block_kwargs.py` +
  `bck_multilingual_pattern.py`, Section 3 "Navigation & Book"):
  - `st_book(block_args=, block_kwargs=)` documented for the first time
    outside the library CHANGELOG — forwarding contract, recommended
    `def build(lang: str = "en", **_)` signature, interaction with the
    pagination cache (kwargs fingerprint, `page_cache-<fp>.json`);
    reference example "a language passed to every `build()`"
    (streamtex #37).
  - The bilingual pattern with no i18n API: leaves `{"en": …, "fr": …}`
    in the block or in a shared lexicon, `T()` / `TF()` resolution with
    English fallback and bare-string `TypeError`, language in the address
    (`STX_LANG` > `?lang=` > default, `with_lang()` links), one static
    export per language, `BibConfig(locale=…)`, and the `check_i18n`
    quality gate (baseline/regress, inventory, parity, words, drift).
    Reference implementation: POSTAIR / AI Day 2026 (`sumvadis-streamtex`)
    (streamtex #41).
- **Deploy manual — `stx export html --lang` / `--suffix`** in the CLI
  commands section (streamtex #38).

### Removed

- **`references/` directory** — legacy artifact from before the
  `streamtex-claude` profile system. Contained only stale snapshots of
  `coding_standards.md` and `streamtex_cheatsheet_en.md` that drifted
  independently from the canonical source. No runtime consumer existed.
  The canonical references remain at `streamtex-claude/shared/references/`
  and the auto-installed mirror at `.claude/references/` (kept in sync
  by `stx claude update`).

## [0.7.7] — 2026-05-20 — Migration to streamtex-packs monorepo

### Changed

- **Pack naming convention** — packs now follow the convention
  `streamtex-pack-{name}`. The two packs consumed by streamtex-docs
  have been renamed accordingly:
  - `streamtex-design` → `streamtex-pack-design` (was a standalone
    GitHub repo; now lives in the `streamtex-packs` monorepo).
  - `streamtex-manuals` → `streamtex-pack-manuals` (was local-only;
    now versioned in the `streamtex-packs` monorepo).
- **Dependency declarations** in `pyproject.toml` updated to reference
  the monorepo via
  `git+https://github.com/nicolasguelfi/streamtex-packs.git@{prefixed-tag}#subdirectory={pack-name}`.
- **Python imports remain unchanged** — the Python module names
  `streamtex_design` and `streamtex_manuals` are preserved by design,
  so all block code continues to import them as before.
- `manuals/stx_manual_reuse/stx.toml` updated with new pack names + refs.
- `manuals/stx_manual_reuse/blocks/bck_reuse_layers.py`: cosmetic text
  string update to new pack names.
- streamtex dep bumped to `>=0.7.7,<0.8` (picks up the
  `scale_curves.toml` packaging fix shipped in 0.7.7).
- `.stx-version` bumped to `0.7.7`.

### Fixed

- The Hetzner/Coolify Docker build now succeeds — the broken dep
  `streamtex-manuals` (local-only, unresolvable via `--no-sources`)
  is replaced by a resolvable git URL pointing at the monorepo.

## [0.7.6] — 2026-05-20 — v2 relative scale documentation refresh

### Changed

- 5 documentation blocks updated to describe the relative architecture
  shipped in streamtex 0.7.6: `bck_font_sizes` (intro), `bck_indexed_font_scale`
  + `bck_font_scale_curves_demo` (advanced), `bck_font_scale_internals`
  (developer — major rewrite of TOML schema + add-a-curve walkthrough),
  `bck_pack_font_scale_integration` (reuse). All annotations now reflect
  the new Tailwind alias map (text_base = idx_7 = 18pt).
- `references/streamtex_cheatsheet_en.md`: "Indexed responsive font
  scale" section rewritten around the base + ratios model with the
  new ScaleConfig knob priority.
- streamtex dep bumped to >= 0.7.6 (relative scale architecture).
- streamtex-design dep transitively bumped to >= 0.2.3.

## [0.7.5] — 2026-05-20 — Indexed responsive font scale documentation

### Added

- New documentation block `bck_font_sizes` in `stx_manual_intro` —
  welcoming introduction to the 3 font-size systems available in
  streamtex, with a live 5-palier ladder and "which to use when"
  comparison table.
- New documentation block `bck_indexed_font_scale` in
  `stx_manual_advanced` — comprehensive deep-dive on the new scale:
  3 access modes, 4 named curves, full 29-palier visual reference,
  per-document configuration, out-of-range tolerance, identity table.
- New documentation block `bck_font_scale_curves_demo` in
  `stx_manual_advanced` — live head-to-head comparison of all four
  named curves (WORD_PROCESSOR / GEOMETRIC / BODY_CENTRIC / BELL) on
  identical content, with locally-scoped CSS variable overrides.
- New documentation block `bck_font_scale_internals` in
  `stx_manual_developer` — 3-layer architecture, TOML schema,
  "how to add a new curve" walkthrough, generator API, fallback
  chain, validation rules.
- New documentation block `bck_pack_font_scale_integration` in
  `stx_manual_reuse` — pack-author rule and before/after migration
  pattern showing how design-system bundles consume the indexed scale.

### Changed

- `references/streamtex_cheatsheet_en.md` — new "Indexed responsive
  font scale (recommended for new blocks)" section after the existing
  font-size reference, mirroring the streamtex-claude shared cheatsheet.
- streamtex dependency bumped to `>=0.7.5,<0.8` (was `>=0.7.3,<0.8`)
  to pick up `ScaleConfig` / `ScaleCurve` / `st_book(scale=…)` API and
  the `streamtex-design 0.2.2` migration of design-system bundles to
  `var(--stx-scale-K, …)`.

## [0.7.3] — 2026-05-19 (L5 callers migration — TOCConfig.numerate_titles removed upstream)

The library deprecated and now removed the `TOCConfig.numerate_titles`
field. Every doc/skill caller is migrated to
`numbering=NumberingMode.X`.

### Changed
- `cheatsheets/stx_cheatsheet_python.md` — full-featured book example
  and `TOCConfig` dataclass reference no longer mention
  `numerate_titles`; the field disappears from both places.
- `manuals/stx_manual_intro/blocks/bck_tags_enum.py` —
  `TOCConfig(numerate_titles=True, ...)` →
  `TOCConfig(numbering=NumberingMode.BOTH, ...)`.
- `manuals/stx_manual_intro/blocks/_atomic/bck_toc.py` — Field table
  row 1 retitled from `numerate_titles` (bool true/false) to
  `numbering` (NumberingMode value: BOTH / SIDEBAR_ONLY /
  MAIN_ONLY / NONE).
- `.claude/designer/skills/streamtex-quick-reference.md` will
  auto-refresh on the next `stx claude update` (the source file in
  `streamtex-claude/profiles/project/designer/skills/` is already
  updated).

## [0.7.2] — 2026-05-19 (Q10 follow-up + Q19 last bloc)

After the library cut deprecated AI-image functions in `streamtex
0.7.2`, every doc reference is rewritten on the modern API
(`st_image(prompt=..., editable=True, name=...)`). The last deferred
reuse-manual block (`bck_custom_import_mapping`) is now written —
the PLAN.md §18.9 + §19.2 (Q19/D19) provided the source spec that
was missing during Phase 2.

### Added (Q19 — last deferred bloc grounded on PLAN.md)
- `manuals/stx_manual_reuse/blocks/bck_custom_import_mapping.py` —
  documents the strict-separation doctrine (D19) between the
  pack-agnostic shared `/stx-import:*` commands and the user-prepared
  custom artefacts (`.claude/custom/skills/import-<pack>-mapping.md`
  + `.claude/custom/commands/refactor-<pack>/run.md`) that refactor
  imported code towards a pack's components. 5 sections:
  (1) why pack-agnostic in the shared profile, (2) custom skill
  template, (3) custom command template, (4) concrete example for
  `streamtex-design`, (5) storage and conservation strategies.
- Wired into `stx_manual_reuse/book.py`. The manual now ships all
  12 planned blocs (21 total).

### Changed
- `references/streamtex_cheatsheet_en.md` — AI Image Generation
  section: the `from streamtex import st_ai_image,
  st_ai_image_widget, generate_image` import + the two example
  blocks (declarative + widget) are replaced by `st_image(prompt=...,
  editable=True, name=...)` examples (same call covers both modes).
- `references/coding_standards.md` — sx-vs-st guidance: `st_ai_image,
  st_ai_image_widget, generate_image` → `st_image(prompt=...,
  editable=True), generate_image`.
- `manuals/stx_manual_ce/blocks/bck_ce_produce.py` +
  `bck_ce_faq.py` — `st_ai_image(prompt)` references refreshed
  to `st_image(prompt=..., editable=True, name=...)`.
- `manuals/stx_manual_ai/blocks/bck_ai_image_overview.py` — module
  docstring + `show_explanation` no longer mention the deprecated
  functions; the unified `st_image()` is presented as the single
  entry point.
- `manuals/stx_manual_ai/blocks/bck_ai_image_usage.py` — rewritten:
  the "Declarative Mode" section now teaches `st_image(prompt=...,
  editable=True, name=...)`; the "Interactive Widget" section is
  replaced by "Interactive editing — same call, editor panel"
  explaining that `editable=True` opens the Prompt / AI / Edit /
  History tabs on click; the Parameters Reference grid is rewritten
  to document `st_image()`'s AI params (left card) + common params
  (right card); the deprecation block becomes a "Upgrading from
  < 0.7" migration note explaining the removal.
- `manuals/stx_manual_ai/blocks/bck_profile_install.py` —
  AI-extras explanation references the unified API.

## [0.7.1] — 2026-05-19 (Autonomous doc legacy cleanup — Phases 1-5)

### Phase 1 — Foundation files (Claude instructions + cheatsheet)
- `streamtex-docs/CLAUDE.md` and `streamtex/CLAUDE.md`: the legacy
  `## StreamTeX Patterns` section (referencing the removed
  `streamtex-patterns` repo, `.claude/custom/streamtex-patterns/`
  folder, and `/stx-pattern:*` command family) is replaced by a
  modern `## Reuse architecture` section pointing to the
  `reuse-architecture` skill, `stx pack/component/ds/kit/validate`
  CLI, and the docstring-contract model.
- `references/streamtex_cheatsheet_en.md`: the `## Patterns` section
  (~17 obsolete `stx patterns *` commands and a docs/slides/core
  preset model) is replaced by a `## Reuse architecture` section
  documenting every active command (`stx pack {list,add,remove,
  info,new,set-primary,validate,sync}`, `stx component {list,show,
  find,validate,new,promote}`, `stx ds {list,show,switch,new,
  validate}`, `stx kit {list,show,install,new,validate}`,
  `stx validate [--strict]`) — each verified against the real CLI
  surface in `streamtex/cli/`.
- `manuals/stx_manual_reuse/blocks/bck_reuse_welcome.py`:
  vocabulary refresh — "Before patterns flow / After reuse
  architecture" before/after grid replaced by "Reusable artefacts /
  Distribution model" that documents the new state directly.

### Phase 2 — `stx_manual_reuse` — 11 new blocks (G9)
Each block grounded on a specific source file (cited in its module
docstring) to avoid drift. The 12th planned block,
`bck_custom_import_mapping`, is deferred — the concept is not yet
implemented in code (no source to ground from).
- `bck_pack_authoring` — pack scaffold, layout, manifest, entry-point.
- `bck_component_authoring` — scaffold, docstring contract, validate.
- `bck_kit_format` — kit TOML schema + required/optional fields + CLI.
- `bck_cli_template_format` — template directory layout + placeholders
  + kit wiring + authoring tips.
- `bck_pack_distribution` — three channels (local / git / pypi) with
  comparison table + release flows.
- `bck_ce_capture` — capture workflow (spot → scaffold → docstring →
  use → validate).
- `bck_ce_promote` — Q12 4-branch routing
  (primary_local / secondary_local_with_git / git_remote / pypi).
- `bck_validation` — code families (PR/PV/CV/DV/KV/BV), exit codes,
  severities, CI usage.
- `bck_troubleshooting` — recipe table for the most common error
  codes + a general debugging workflow.
- `bck_migration_from_patterns` — vocabulary mapping + CLI mapping +
  step-by-step migration recipe for 0.6.x projects.
- `bck_faq` — 10 recurring questions from the 0.7.x rollout.
- `book.py` reorganised into 8 logical parts.

### Phase 3 — Render purge (Q12 follow-up)
The CLI surface lost `stx deploy render` / `env-sync` in Q12.
Documentation now reflects that:
- `manuals/stx_manual_deploy/blocks/bck_render.py` deleted.
- `manuals/stx_manual_developer/blocks/_atomic/bck_render_deployment.py` deleted.
- `manuals/stx_manual_developer/blocks/bck_dev_ci_cd.py` and the
  deploy `book.py` updated to remove the Render entries.
- `bck_welcome.py` and `bck_level_badge.py` (deploy) cleaned of
  Render rows.
- `bck_cli_deploy_commands.py` — the `stx deploy render` section
  removed and `stx deploy status` updated.
- `bck_cli_architecture.py` (developer) — CLI tree replaces
  `render` with `hetzner`.
- `references/streamtex_cheatsheet_en.md` — Other-platforms section
  no longer lists `stx deploy render` / `env-sync`; `stx deploy status`
  no longer offers a `render` argument.
- Intro / advanced / collection-hub copy: `Render.com` mentions
  replaced by `Hetzner/Coolify`.

### Phase 4 — Vocabulary sweep (surgical, G10-G12)
Replaced unambiguous legacy strings; generic uses of "pattern"
(design pattern, atomic blocks pattern, testing patterns) kept in
place. Final state across `manuals/` + `references/`:
- `stx patterns <verb>` : 0 occurrences (was 17).
- `/stx-pattern:*` : 0 occurrences.
- `_pattern_library.md` : 0 occurrences.
- `block-blueprints.md` : 0 occurrences — every reference now points
  to `reuse-architecture.md` (7 places in `stx_manual_ai/`).
- `streamtex-patterns` repo/path : only legitimate mentions remain
  (`bck_pack_source_resolution`, `bck_migration_from_patterns`,
  `bck_faq` — all quoting the legacy term for context).

### Phase 5 — Housekeeping
- 5 orphan `*.bak` files removed (intro/advanced manuals).
- All 8 manuals (`intro/advanced/deploy/developer/ai/ce/reuse/
  collection`) compile and import all blocks: 178 blocks total.
- Repo-wide `ruff check .` passes.

### Volontairement hors scope (documenté pour la suite)
- Q10 — streamtex lib L1-L7 legacy API removal (code, not docs).
- F2 — ambiguous vocabulary judgment calls ("blueprint" case by
  case, generic "pattern" uses).
- `bck_custom_import_mapping` — concept not implemented in code yet.

## [0.7.0] — 2026-05-19 (Q13 — legacy purge)

### Changed (Q13a)
- `pyproject.toml` (root): `version = "0.7.0"` (was `0.6.0`,
  aligned with `.stx-version`); streamtex dependency bumped from
  `>=0.3.0` to `>=0.7.0`.
- `templates/template_project/pyproject.toml`,
  `templates/template_collection/pyproject.toml`,
  `templates/template_slides/pyproject.toml`: streamtex dependency
  bumped from `>=0.3.0` to `>=0.7.0`.
- `manuals/stx_manual_ai/blocks/bck_blueprints.py` renamed to
  `bck_block_templates.py` (title "Block Blueprints" → "Block
  composition templates"; legacy `block-blueprints.md` skill
  reference removed; block now points to the reuse-architecture
  skill + `stx component list`).

### Added (Q13b — equivalence ports before archive deletion)
- `manuals/stx_manual_reuse/blocks/bck_pack_source_resolution.py`
  — modern equivalent of the legacy `bck_scan_rule`: 3 pack
  locations / PEP 621 entry-point discovery / 5 lifecycle states
  with `PR0xx` codes / `_pack_manifest.toml` format / component
  granularity tags / `stx pack sync` + editable dev links.
- `manuals/stx_manual_reuse/blocks/bck_pack_consumption.py` —
  modern equivalent of the legacy `bck_install_flow`: end-to-end
  walkthrough from `stx project new` to capture + Q12 4-branch
  promote routing, with the 3-file persistence model.

### Removed (Q13a + Q13c)
- `manuals/_archive/stx_manual_patterns/.venv/` (Q13a — 555 MB
  build artifact, regeneratable).
- `manuals/_archive/stx_manual_patterns/` (Q13c) — full legacy
  manual; every block with no equivalent in `stx_manual_reuse`
  was ported in Q13b. Remaining archive blocks were either
  superseded by the live-rendered Wave 4 galleries or deferred to
  future authoring blocks per PLAN §19.2. Git history retains the
  archive.
- `manuals/_archive/` — empty parent directory removed.

## [Unreleased] — 2026-05-19 (Wave 3 Phase 6.4-6.5 + Phase 7)

### Removed
- `.claude/custom/streamtex-patterns/` — 14 files (12 patterns + index +
  manifest + .patterns-meta.json). The 4 docs-only patterns
  (`api_reference_card`, `composite_block`, `feature_walkthrough`,
  `manual_section`) were already migrated into the `streamtex-design`
  pack in Wave 1 Phase 2a; removing the local consumer copy completes
  Phase 7 / PLAN §23.5.

### Changed (Phase 6.4 — archive legacy manual)
- `manuals/stx_manual_patterns/` → `manuals/_archive/stx_manual_patterns/`
  (full move via `git mv`). The archived manual stays available in git
  history; PLAN §21.2 "archive out-of-scope" rule applies to it from
  now on.
- `run-manuals.sh` — renamed every `patterns` reference to `reuse`
  (variables `PATTERNS_PROJECT/PORT/LOG`, flags `--patterns/--no-patterns`,
  log file, banner labels). 31 references migrated.
- `.github/workflows/hetzner-deploy.yml` — service
  `streamtex-docs-patterns` (uuid `ag0u87txr5ygfr11pfqv0a1j`, host
  `docs-patterns.streamtex.org`) now serves `manuals/stx_manual_reuse`.
- `manuals/stx_manual_ce/blocks/bck_ce_prototype.py` and `bck_ce_faq.py`
  — vocabulary refresh: "captured patterns into
  `.claude/custom/streamtex-patterns/`" → "captured components into the
  project's primary local pack (`./mypack/components/`)"; promotion
  table updated to reflect `stx component promote --to=<pack>`.

### Phase 6.5 — Coolify deploy (PLAN v1.34 §19.6)
- Coolify env vars `FOLDER` (runtime + preview) for app
  `streamtex-docs-patterns` updated from `manuals/stx_manual_patterns`
  to `manuals/stx_manual_reuse` via `PATCH /api/v1/applications/<uuid>/envs`
  (uuids `v8oz1jp1bw8eb81y1efnibft` + `r13oubz7lxoc3iqsd8rz2cxu`).
- Auto-deploy on merge to `main` will redeploy `docs-patterns.streamtex.org`
  with the new `FOLDER` value; the existing Coolify slot is reused.

## [Unreleased prior] — 2026-05-19 (Wave 2 Phase 6.1-6.3 — partial stx_manual_reuse)

### Added
- **`manuals/stx_manual_reuse/`** — new manual for the streamtex 0.7.x
  reuse architecture (packs, components, design systems, kits). Skeleton
  fully wired (book.py, blocks/, custom/{styles,themes}.py, README.md,
  pyproject.toml with editable streamtex source). Five representative
  blocks ported per PLAN §19.2:
  1. `bck_reuse_welcome` — overview (source: `bck_intro.py`)
  2. `bck_reuse_vocabulary` — 9 glossary terms (ex nihilo from PLAN §2)
  3. `bck_reuse_layers` — 3-layer diagram (ex nihilo from PLAN §3)
  4. `bck_component_format` — Python component anatomy (source:
     `bck_format_spec.py` adapted)
  5. `bck_reference_card` — CLI cheatsheet (ex nihilo from PLAN §7)
- `manuals/stx_manuals_collection/collection.toml`: card `test-patterns`
  renamed to `test-reuse` (title + description updated). Port 8508
  unchanged — Wave 3 redeploys the Coolify slot to the new manual.

### Notes (Wave 3 follow-up)
- Remaining 16 blocks from PLAN §19.2 documented in the manual's
  README.md with source + porting action. They land in Wave 3 alongside
  Phase 6.4 (archive `stx_manual_patterns/`) and Phase 6.5 (update
  Coolify env `FOLDER=manuals/stx_manual_reuse`).
- `run-manuals.sh` and the Dockerfile still target `stx_manual_patterns`;
  flipped in Wave 3 with the deployment.
- `stx_manual_ce` / `stx_manual_intro` references refresh planned for
  Wave 3 Phase 5 alongside the CE sweep.

## [0.6.25] — 2026-05-12

### Added
- **New patterns manual** (`stx_manual_patterns`): documentation manual on the
  StreamTeX graphic-design patterns mechanism — `_pattern_library.md`,
  `_pattern_dictionary.md`, the `/stx-pattern:*` command family, and the
  `ptn_*` blueprints (`ptn_manual_section`, `ptn_api_reference_card`,
  `ptn_term_definition_list`, `ptn_narrative_transition`, etc.).
  Deployed at `https://docs-patterns.streamtex.org` once the Coolify
  service is registered.

### Changed
- **Chrome recommendation banner: off by default in `st_book`** (library
  0.6.25). The marker-runtime migration eliminated the Chrome-specific
  `:has()` cold-load freeze AND restored Firefox compatibility, so the
  banner no longer reflects reality. The `st_chrome_banner()` helper
  remains exported for users who want to opt back in explicitly.

## [0.6.24] — 2026-05-12

### Changed
- **Library upgrade**: bumped streamtex dependency from 0.6.10 to 0.6.24.
  The 0.6.21 → 0.6.24 patch chain delivers all the layout regression
  fixes required by Streamlit 1.56+:
  - 0.6.21 — Observer migrated from `streamlit.components.v1.html`
    (deprecated, removed after 2026-06-01) to
    `st.components.v2.component(isolate_styles=False)`. CSS adapted to
    Streamlit 1.56+ DOM structure (`stElementContainer`, `stLayoutWrapper`).
  - 0.6.22 — Layout-critical styles now written inline with `!important`
    by the observer JS, bypassing the CSS cascade.
  - 0.6.23 — Marker cell hidden inline (`display: none !important`); the
    one-shot `data-stx-processed` gate dropped so the observer can
    re-apply when Streamlit reconciles the parent.
  - 0.6.24 — Observer now watches `attribute` mutations in addition to
    `childList`; `applyMarker` is fully idempotent. Recovers from
    sidebar-slider reruns that previously wiped per-instance backgrounds
    and borders.
- **No content change** in any deployed manual — purely infrastructure.

### Added
- **Playwright e2e regression suite** (library): `tests/e2e/` with a
  direct attribute-strip recovery test that catches the kind of
  regression that motivated 0.6.21 → 0.6.24. Run with
  `uv run pytest -m e2e`.

## [0.6.16] — 2026-05-11

### Changed
- **Library upgrade**: marker-runtime architectural migration complete
  (library Phase 0 → 5, versions 0.6.11 → 0.6.16). Replaces the legacy
  CSS `:has()` selector pattern with a JavaScript MutationObserver that
  watches `<span class="stx-marker" data-stx-kind="…">` sentinels and
  applies layout classes on the parent `[data-testid="stVerticalBlock"]`.
  - Eliminates the 3–4 s Chrome cold-load freeze on long manuals
    (~1 054 `<style>` elements + ~958 `:has()` selectors → < 50
    elements + 0 `:has()` selectors).
  - Restores Firefox compatibility (`:has()` was unsupported in Firefox
    until v121, December 2023).
- **No user-facing API change** — every existing block module continues
  to work without modification.
- See the upstream streamtex CHANGELOG for per-version detail of the
  migration phases.

## [0.6.10] — 2026-04-15

### Changed
- **Library upgrade**: bumped streamtex dependency to 0.6.10 from PyPI.
- **Slide break enhancements**: new before/after spacing, MARKER_ONLY and HIDDEN modes now available in all manuals.

## [0.6.9] — 2026-04-08

### Changed
- **Library upgrade**: bumped streamtex dependency to 0.6.9 from PyPI.

## [0.6.8] — 2026-04-07

### Changed
- **Dockerfile**: added LaTeX system packages (`texlive-latex-base`, `texlive-fonts-recommended`, `dvisvgm`, `ghostscript`) for TikZ diagram rendering in deployed manuals.
- **Library upgrade**: bumped streamtex dependency to 0.6.8 from PyPI.

## [0.6.7] — 2026-04-05

### Added
- **`bck_ce_integrate` block** (CE manual): new documentation block for `/stx-ce:integrate` — routing table, workflow, frontmatter format.
- **CE cycle diagram updated**: 8 phases (was 7), INTEGRATE added after COMPOUND.

### Changed
- **`bck_ce_overview` block**: updated cycle list to 8 phases, updated iterative description.
- **CE manual `book.py`**: wired `bck_ce_integrate` after `bck_ce_compound`.
- **Library upgrade**: bumped streamtex dependency to 0.6.7 from PyPI.

## [0.6.6] — 2026-04-05

### Added
- **`bck_ce_pause` block** (CE manual): new documentation block for `/stx-ce:pause` session checkpoint — workflow diagram, checkpoint format, best practices.
- **CE cheatsheet updated**: 12 commands, 17 templates, pause/continue sections.

### Changed
- **`bck_ce_continue` block**: updated to document Step 0 checkpoint restoration and revised best practices (pause before leaving, continue when returning).
- **`bck_ce_commands_ref` block**: updated from 11 to 12 commands, added `/stx-ce:pause` entry.
- **`bck_ce_templates_ref` block**: updated from 16 to 17 templates, added `tpl_checkpoint` entry.
- **Library upgrade**: bumped streamtex dependency to 0.6.6 from PyPI.

## [0.6.2] — 2026-04-01

### Fixed
- **Dual-mode deployment**: added `cli` extra to dependencies (`streamtex[ai,cli,inspector,pdf]`) so `stx export html` works in Docker containers — `rich` and `jinja2` were missing.
- **Dockerfile**: added `uv pip install rich jinja2` as safety net for CLI dependencies.
- **nginx.conf**: added `autoindex on` fallback for static HTML directory listing.

### Changed
- **Templates**: all 3 project templates (project, slides, collection) now include `streamtex[cli]` in dependencies.

## [0.5.18] — 2026-03-30

### Changed
- **Library upgrade**: bumped streamtex dependency to 0.5.18 from PyPI
- **Deploy patterns**: included `.stx-version` in shared deploy patterns for correct version gating
- **Language consistency**: replaced French "la librairie" with English "the library" in CLAUDE.md

## [0.5.15] — 2026-03-29

### Added
- **`bck_dev_link`** block (developer manual): documents `stx dev register/link/unlink/status` workflow
- **`bck_text_wrapping`** block (intro manual): documents `Wrap.hyphens` and text wrapping modes
- **`bck_ai_image_editor`** block (AI manual): documents 4-tab image editor, Display tab, and `ModelCapabilities` system

## [0.5.14] — 2026-03-26

### Fixed
- **Version display**: bumped docs version from 0.5.10 to 0.5.14 — sidebar now shows correct "docs 0.5.14 · lib 0.5.14"

## [0.4.1] — 2026-03-20

### Changed
- **Deployment platform**: migrated from Render to Hetzner/Coolify with auto-deploy workflow
- **Coherence audit**: added release pipeline check (21 → 22 checks)

### Removed
- **Render deploy workflow**: replaced by Hetzner/Coolify pipeline

## [0.4.0] — 2026-03-20

### Added
- Version label in sidebar (docs version + library version) above Settings
- Changelog section as last block of every manual
- `CHANGELOG.md` for documentation version tracking

## [0.3.0] — 2026-03-01

### Added
- Initial 6 manuals: Introduction, Advanced, Deploy, Developer, AI, Collection hub
- Shared blocks infrastructure (`shared-blocks/`)
- CI with 5 structural checks (import, API compat, blocks, links, books)
- Hetzner/Coolify deployment with smart per-manual deploys
- Render deployment (6 services, shared Dockerfile)
