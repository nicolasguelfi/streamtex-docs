# StreamTeX Reuse Architecture Manual (`stx_manual_reuse`)

Reference manual for the StreamTeX reuse architecture: packs, components,
design systems, kits.

## Contents

- Concepts — welcome, vocabulary, layers, component anatomy, reference card
- Pack lifecycle — source resolution, consumption
- Authoring — packs, components, kits, CLI templates
- Distribution — channels (local / git / pypi)
- CE flows — capture, promote
- Pack Engineering — overview, bootstrap, refine
- Quality — validation, troubleshooting
- Self-demonstration — live galleries (components + design systems)
- Advanced — custom import mapping
- FAQ

## Running locally

```bash
cd manuals/stx_manual_reuse
uv sync
uv run streamlit run book.py
```
