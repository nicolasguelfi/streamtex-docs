"""What is a pattern? — introduction to the StreamTeX pattern catalog.

# @pattern: ptn_manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Intro page styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.center_txt
        + s.container.layouts.vertical_center_layout
    )


bs = BlockStyles


def build():
    """Introduce the concept of a 'pattern' and the catalog mechanism."""
    with st_block(s.center_txt):
        st_write(bs.heading, "What is a Pattern?", tag=t.div, toc_lvl="1")
        st_space("v", 2)

    # ---- Sub-topic A: definition ----
    st_write(bs.sub, "Definition", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A **pattern** is a markdown file describing a reusable visual
        primitive for StreamTeX projects: heading + frontmatter, structured
        sections (Visual / Structure / Code skeleton / Extrapolation
        rules / When to use), and a Python skeleton that an AI can
        adapt.

        Patterns are **read by Claude Code** at block-generation time,
        not imported as Python code. The catalog is a knowledge base,
        not a runtime dependency.
    """)
    st_space("v", 2)

    # ---- Sub-topic B: where they live ----
    st_write(bs.sub, "Where patterns live", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The single source of truth is the `streamtex-patterns` repo.
        Each consumer project pulls a **subset** (a preset) into its
        own `.claude/custom/streamtex-patterns/` folder via the
        `stx patterns` CLI.

        Patterns are organised by **scope**: `core/`, `slides/`,
        `docs/`, and per-project `projects/<name>/`.
    """)
    st_space("v", 1)

    show_code("""\
streamtex-patterns/
├── manifest.toml
├── _pattern_library.md      # global index
├── core/                    # universal atoms
│   ├── ptn_callout.md
│   ├── ptn_card_grid.md
│   └── ...
├── slides/                  # presentation-only
│   ├── ptn_stat_hero.md
│   └── ...
├── docs/                    # manual-only
│   ├── ptn_manual_section.md
│   ├── ptn_feature_walkthrough.md
│   └── ptn_api_reference_card.md
└── presets/
    ├── core.toml
    ├── slides.toml
    └── docs.toml""", language="text")
    st_space("v", 2)

    # ---- Sub-topic C: why patterns matter ----
    st_write(bs.sub, "Why a pattern catalog?", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Without a catalog, every project re-invents the same recipes
        (a ptn_callout, a stat hero, a manual section) — and they drift.

        A pattern catalog gives the ecosystem a **shared vocabulary**:
        when you say "use a `ptn_manual_section`", any contributor — human
        or AI — knows exactly what to produce.
    """)
    st_space("v", 1)

    with st_block(s.project.containers.tip_callout):
        st_write(s.project.titles.tip_label, "Key idea")
        st_space("v", 0.5)
        st_write(bs.body,
                 "Patterns are a **knowledge contract** between authors, "
                 "AI assistants, and consumer projects — not a runtime "
                 "library.")
    st_space("v", 2)

    # ---- Sub-topic D: how to read this manual ----
    st_write(bs.sub, "How to read this manual", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The next sections walk through the mechanism end-to-end:

        1. **Format spec (A2)** — what a pattern file looks like.
        2. **Discovery & install** — how `stx patterns` finds the
           catalog and copies patterns into a project.
        3. **Extrapolation contract** — the INVARIANTS / PARAMS /
           INTERDITS that Claude follows.
        4. **CLI reference** — `stx patterns install/update/promote`.
        5. **Authoring** — how to contribute a new pattern.
        6. **Patterns vs blueprints** — where the frontier sits.
    """)
    st_space("v", 1)

    show_details("""\
        This manual itself is a **dogfood test**: every block is
        annotated with the pattern it implements (`# @pattern: ...`).
        See the source to learn by example.
    """)
    st_space("v", 1)
