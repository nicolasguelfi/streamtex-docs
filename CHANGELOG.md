# Changelog — StreamTeX Documentation

All notable changes to the StreamTeX documentation will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
