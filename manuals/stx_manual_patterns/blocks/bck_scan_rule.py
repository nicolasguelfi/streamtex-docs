"""Scan & discovery rules — how patterns are found, presets, drift detection.

# @pattern: manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Scan rule page styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.container.layouts.vertical_center_layout
    )
    cell_head = s.bold + s.project.colors.accent_teal


bs = BlockStyles


def build():
    """Explain how patterns are discovered, scoped, and tracked."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Discovery, Scopes & Drift",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    # ---- Source resolution ----
    st_write(bs.sub, "How `stx patterns` finds the catalog",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The CLI resolves the pattern source through a TOML config
        cascade — **no environment variable**, by design. State stays
        in files so a project's pattern setup is portable.

        The resolution order:

        1. `--source <path>` (CLI flag, override)
        2. `[patterns].source` in `<project>/stx.toml` or `pyproject.toml`
        3. `[patterns].source` in `<workspace>/stx.toml`
        4. Auto-discover: `<workspace>/streamtex-patterns/`
        5. Otherwise: error with the list of paths tried.
    """)
    st_space("v", 1)

    show_code("""\
# streamtex-dev/stx.toml  (workspace level)
[patterns]
source = "./streamtex-patterns"
default_preset = "slides"

# projects/ai4se6d/stx.toml  (project level — overrides workspace)
[patterns]
source = "../../streamtex-patterns"
preset = "ai4se6d"
""", language="toml")
    st_space("v", 2)

    # ---- Scopes ----
    st_write(bs.sub, "Scopes", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A pattern's **scope** is the top-level directory under
        `streamtex-patterns/`. It encodes where the pattern is
        appropriate to use.
    """)
    st_space("v", 1)

    with st_grid(cols="1fr 3fr", gap="8px") as g:
        with g.cell(bs.cell):
            st_write(bs.body, (s.bold + s.project.colors.accent_teal, "core/"))
        with g.cell(bs.cell):
            st_write(bs.body, "Universal atoms (callout, card_grid, "
                              "comparison_table, takeaways) — safe in any project.")
        with g.cell(bs.cell):
            st_write(bs.body, (s.bold + s.project.colors.accent_teal, "slides/"))
        with g.cell(bs.cell):
            st_write(bs.body, "Visually dramatic templates (stat_hero, "
                              "evidence_insight) — use only in presentations.")
        with g.cell(bs.cell):
            st_write(bs.body, (s.bold + s.project.colors.accent_teal, "docs/"))
        with g.cell(bs.cell):
            st_write(bs.body, "Code+demo recipes (manual_section, "
                              "feature_walkthrough, api_reference_card) — "
                              "use only in manuals.")
        with g.cell(bs.cell):
            st_write(bs.body, (s.bold + s.project.colors.accent_teal, "projects/<X>/"))
        with g.cell(bs.cell):
            st_write(bs.body, "Ultra-specific to one project — never "
                              "promoted to core.")
    st_space("v", 2)

    # ---- Presets ----
    st_write(bs.sub, "Presets — named install recipes", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A preset is a `presets/<name>.toml` file listing the patterns
        to install together. Presets can extend each other, so
        `slides` and `docs` both build on top of `core`.
    """)
    st_space("v", 1)

    show_code("""\
# presets/docs.toml
[preset]
name = "docs"
description = "StreamTeX-docs-style manuals (extends core)"

[patterns]
include = [
  "docs/manual_section.md",
  "docs/feature_walkthrough.md",
  "docs/api_reference_card.md",
  "docs/composite_block.md",
]
exclude = []

[depends_on]
extends = "core"
""", language="toml")
    st_space("v", 2)

    # ---- Drift detection ----
    st_write(bs.sub, "Drift detection on update", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Every install records a SHA per pattern in
        `<project>/.claude/custom/streamtex-patterns/.patterns-meta.json`.

        On `stx patterns update`, the CLI compares **local SHA** with
        **source SHA** to decide what to do without losing local edits.
    """)
    st_space("v", 1)

    show_code("""\
# .patterns-meta.json (excerpt)
{
  "patterns": {
    "callout": {
      "source": "core/callout.md",
      "sha": "ab12cd34...",
      "installed_at": "2026-05-10T08:42:11Z"
    },
    "manual_section": {
      "source": "docs/manual_section.md",
      "sha": "ef56gh78...",
      "installed_at": "2026-05-10T08:42:11Z"
    }
  }
}""", language="json")
    st_space("v", 1)

    with st_grid(cols="1fr 1fr 2fr", gap="8px") as g:
        with g.cell(bs.cell):
            st_write(bs.body, (s.bold, "Local"))
        with g.cell(bs.cell):
            st_write(bs.body, (s.bold, "Source"))
        with g.cell(bs.cell):
            st_write(bs.body, (s.bold, "Action"))
        with g.cell(bs.cell):
            st_write(bs.body, "unchanged")
        with g.cell(bs.cell):
            st_write(bs.body, "unchanged")
        with g.cell(bs.cell):
            st_write(bs.body, "skip")
        with g.cell(bs.cell):
            st_write(bs.body, "unchanged")
        with g.cell(bs.cell):
            st_write(bs.body, "changed")
        with g.cell(bs.cell):
            st_write(bs.body, "update silently")
        with g.cell(bs.cell):
            st_write(bs.body, "changed")
        with g.cell(bs.cell):
            st_write(bs.body, "unchanged")
        with g.cell(bs.cell):
            st_write(bs.body, "skip + info (local edit preserved)")
        with g.cell(bs.cell):
            st_write(bs.body, "changed")
        with g.cell(bs.cell):
            st_write(bs.body, "changed")
        with g.cell(bs.cell):
            st_write(bs.body, "refuse + suggest "
                              "`diff` / `promote` / `--force`")
    st_space("v", 2)

    # ---- copy vs symlink ----
    st_write(bs.sub, "Modes — copy vs symlink", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        - **`copy`** (default) — robust, portable, snapshot in git;
          chosen by consumer projects.
        - **`symlink`** — pattern author iterating on the catalog;
          edits become live in any project linked to the source.
    """)
    st_space("v", 1)

    show_code("""\
# Pattern authors only — live edits across projects
stx patterns install --preset slides --mode symlink
""", language="bash")
    st_space("v", 1)

    show_details("""\
        Symlink mode is **opt-in** because it bypasses drift detection
        — the project tracks the upstream `HEAD` directly.
    """)
    st_space("v", 1)
