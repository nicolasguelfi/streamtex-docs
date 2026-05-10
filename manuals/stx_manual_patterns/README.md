# stx_manual_patterns

The **StreamTeX Patterns Manual** — documentation for the
`streamtex-patterns` catalog and its companion `stx patterns` CLI.

## What is this manual about?

This manual explains the **pattern mechanism** used across the StreamTeX
ecosystem to share reusable graphic-design recipes between projects:

- What a **pattern** is (Format A2 spec — frontmatter + structured
  markdown sections).
- How patterns are **discovered, installed, updated, and promoted**
  (presets, scopes, drift detection).
- The **extrapolation contract** (INVARIANTS / PARAMS / INTERDITS) that
  Claude Code follows when generating blocks from a pattern.
- The **`stx patterns` CLI** reference.
- How to **author a new pattern** end-to-end.
- The **frontier** between patterns (visual recipes) and blueprints
  (project skeletons).

## Audience

- StreamTeX users who want to **consume** patterns in their own
  projects.
- Pattern authors who want to **contribute** new patterns to the
  central `streamtex-patterns` repository.
- Tooling implementers building on top of the pattern catalog.

## Run

From this directory:

```bash
uv run streamlit run book.py
# or, with the stx CLI:
stx run
```

## Related repos

- `streamtex-patterns/` — the central catalog (single source of truth).
- `streamtex/` — the library implementing the `stx patterns` CLI.
- `streamtex-docs/manuals/stx_manual_intro/` — sister manual showing the
  patterns this one documents in **live action** (dogfooding).
