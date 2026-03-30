# Changelog — StreamTeX Documentation

All notable changes to the StreamTeX documentation will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
