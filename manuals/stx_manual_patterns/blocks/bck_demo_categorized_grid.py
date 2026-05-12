"""Demo — ptn_categorized_grid template (named groups with tinted cells).

# @pattern: ptn_manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import (
    show_explanation, show_details, show_and_run,
)


class BlockStyles:
    """Demo styles for ptn_categorized_grid."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    body_c = s.large + s.center_txt
    keyword = s.bold + s.project.colors.primary_violet
    accent = s.bold + s.project.colors.accent_teal
    cat_label = (
        s.large + s.bold + s.project.colors.highlight_amber + s.center_txt
    )
    highlight = (
        s.large + s.bold + s.project.colors.highlight_amber + s.center_txt
    )
    cell_primary = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.center_txt
        + s.project.backgrounds.tip_bg
    )
    cell_accent = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.center_txt
        + s.project.backgrounds.interactive_result_bg
    )
    cell_active = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.center_txt
        + s.project.backgrounds.note_bg
    )


bs = BlockStyles


CATEGORIES = [
    ("Adaptations — Existing methods extended", "primary", [
        ("AgileGen", "Gherkin + memory pool"),
        ("Agentic DevOps", "Microsoft vision"),
    ]),
    ("AI-Native — Built for GenAI from scratch", "accent", [
        ("SE 3.0", "intent-centric"),
        ("V-Bounce", "V-model adapted"),
        ("Promptware", "SE for prompts"),
        ("MAISTRO", "7-phase agile"),
    ]),
    ("Process Plugins — Portable methodology", "active", [
        ("Compound Engineering -> GSE-One", ""),
    ]),
]


def build():
    """Dedicated demo for the ptn_categorized_grid slide template."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Demo — ptn_categorized_grid",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    # ---- What it is ----
    st_write(bs.sub, "What it is", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A vertical sequence of `ptn_card_grid` instances, each preceded
        by a **category header**, where each category uses a different
        cell tint (`primary` / `accent` / `active`). Used for
        taxonomies that have named groups: "Adaptations / AI-Native /
        Process Plugins", "NEW / ELEVATED / TRANSFORMED", etc.

        **When to use** — multi-tier taxonomies, decision spectrums,
        "old way / new way / our way" workshop content. **When NOT
        to use** — flat enumerations (use `ptn_card_grid`), comparison
        across attributes (use `ptn_comparison_table`).
    """)
    st_space("v", 2)

    # ---- Live render (code shown == code rendered) ----
    st_write(bs.sub, "Live render", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Three categories, each with its own tint. The eye identifies
        the grouping by color, never by header style alone.
    """)
    st_space("v", 1)

    def _demo():
        _tint_map = {
            "primary": bs.cell_primary,
            "accent": bs.cell_accent,
            "active": bs.cell_active,
        }
        for label, tint, items in CATEGORIES:
            st_write(bs.cat_label, label)
            st_space("v", 0.5)
            cell_style = _tint_map[tint]
            with st_grid(cols="repeat(auto-fit, minmax(220px, 1fr))",
                         gap="12px", cell_styles=cell_style) as g:
                for title, body in items:
                    with g.cell():
                        if body:
                            st_write(bs.body_c,
                                     (bs.keyword, title),
                                     (bs.body, f" — {body}"))
                        else:
                            st_write(bs.body_c,
                                     (bs.highlight, title))
            st_space("v", 1)

    show_and_run(_demo)
    st_space("v", 1)

    show_details("""\
        **INVARIANTS**: each category has its `cat_label` header; all
        cards within a single category share the same cell tint;
        different categories use different tints (that's how the eye
        identifies the grouping); responsive `auto-fit, minmax(220px,
        1fr)` is preserved from the underlying `ptn_card_grid`.
    """)
    st_space("v", 2)

    # ---- Sequence / timeline variant ----
    st_write(bs.sub, "Sequence / timeline variant", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        When the categories represent **temporal phases** (Day 1 /
        Day 2 / Day 3, Phase 1 / Phase 2, …) rather than qualitative
        groupings, the inner grid switches from `auto-fit` to a fixed
        column count (e.g. `1fr 1fr` for Morning / Afternoon) so the
        eye can align phases vertically. The "current" phase uses the
        `active` tint to indicate "you are here".
    """)
    st_space("v", 1)

    def _demo_timeline():
        timeline = [
            ("Day 1 — GenAI fundamentals", "primary",
             ("Vibecoding clinic", "GenAI basics workshop")),
            ("Day 2 — GenSEM methods", "active",
             ("GSE-One workshop", "Compound Engineering live")),
            ("Day 3 — Capstone", "accent",
             ("CalcApp project", "Wrap-up + Q&A")),
        ]
        _tint_map = {
            "primary": bs.cell_primary,
            "accent": bs.cell_accent,
            "active": bs.cell_active,
        }
        for label, tint, (am, pm) in timeline:
            st_write(bs.cat_label, label)
            st_space("v", 0.5)
            cell_style = _tint_map[tint]
            with st_grid(cols="1fr 1fr", gap="12px",
                         cell_styles=cell_style) as g:
                with g.cell():
                    st_write(bs.body_c, (bs.keyword, "Morning"),
                             (bs.body, f" — {am}"))
                with g.cell():
                    st_write(bs.body_c, (bs.keyword, "Afternoon"),
                             (bs.body, f" — {pm}"))
            st_space("v", 1)

    show_and_run(_demo_timeline)
    st_space("v", 1)

    show_details("""\
        **Difference with the default variant**: the inner grid is a
        fixed column count (here `"1fr 1fr"`), not `auto-fit`, because
        temporal alignment depends on a stable number of columns. The
        "current" phase is highlighted via the `active` tint. All
        other INVARIANTS still apply.
    """)
    st_space("v", 1)
