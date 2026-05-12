# Changelog — StreamTeX Documentation

All notable changes to the StreamTeX documentation will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
