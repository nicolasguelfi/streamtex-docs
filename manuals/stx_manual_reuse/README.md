# StreamTeX Reuse Architecture Manual (`stx_manual_reuse`)

The reference manual for the `streamtex 0.7.x` reuse architecture:
packs, components, design systems, kits. Replaces the legacy
`stx_manual_patterns` (archived in Wave 3).

## Status

**Wave 2 (partial)** — 5 representative blocks ported:

1. `bck_reuse_welcome` — overview (Why this architecture)
2. `bck_reuse_vocabulary` — the 9 glossary terms
3. `bck_reuse_layers` — 3-layer diagram (lib / packs / consumer projects)
4. `bck_component_format` — anatomy of a Python component
5. `bck_reference_card` — CLI cheatsheet for `stx pack` / `component` /
   `ds` / `kit` / `validate`

**Wave 3 (planned)** — 16 remaining blocks per PLAN §19.2 mapping table:

| # | Block | Source | Action |
|---|---|---|---|
| 5 | `bck_component_authoring` | `bck_authoring.py` | Adapt walkthrough A2 → Python (`stx component new`, validation) |
| 6 | `bck_design_system_format` | `bck_styles_consolidated.py` | Refactor: demo → anatomy via the `default` DS |
| 7 | `bck_kit_format` | — | Write ex nihilo from PLAN §4.5 |
| 8 | `bck_cli_template_format` | — | Write from PLAN §4.3 |
| 9 | `bck_pack_authoring` | `bck_install_flow.py` | Adapt install flow → pack scaffolding (§24.1) |
| 10 | `bck_pack_distribution` | — | Write from PLAN §6 |
| 11 | `bck_pack_consumption` | `bck_cli_overview.py` | Refactor: `stx patterns` → `stx pack/component/ds/kit/validate` |
| 12 | `bck_ce_capture` | — | Write from PLAN §8.1 |
| 13 | `bck_ce_promote` | — | Write from PLAN §8.3 |
| 14 | `bck_validation` | `bck_scan_rule.py` | Adapt scan rule → `validate_*` API |
| 15 | `bck_gallery_components` | Fusion of `bck_gallery_*` + `bck_demo_*` (11 files) | Reconnect to `streamtex_design.components` |
| 16 | `bck_gallery_design_systems` | — | Write from PLAN §9.4 + Phase 2 DSs |
| 17 | `bck_troubleshooting` | — | Write from PLAN §12 |
| 18 | `bck_migration_from_patterns` | `bck_blueprints_vs_patterns.py` + `bck_extrapolation.py` | Refactor: blueprints vs patterns → unified components (granularity tag) |
| 19 | `bck_custom_import_mapping` | — | Write from PLAN §18.9 / D19 (Q19) |
| 20 | `bck_faq` | — | Write ex nihilo |

## Deployment (Wave 3)

The existing Coolify service `streamtex-docs-patterns` (uuid
`ag0u87txr5ygfr11pfqv0a1j`, host `docs-patterns.streamtex.org`) will be
re-pointed to this manual by updating its `FOLDER` env var to
`manuals/stx_manual_reuse` then triggering a restart (PLAN v1.34 §19.6).

## Running locally

```bash
cd manuals/stx_manual_reuse
uv sync
uv run streamlit run book.py
```
