"""Font sizes — three systems at a glance (semantic, absolute pt, indexed responsive).

A welcoming first-contact block for the intro manual. Introduces the three
ways to set font sizes in streamtex and recommends the indexed responsive
scale (added in 0.7.5) for any new block.
"""

from streamtex import *
import streamtex as stx
from streamtex.styles import Style
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem
from streamtex_design.components.comparison_table import comparison_table


DS = DesignSystem()


class BlockStyles:
    """Font-size intro block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    card = Style(
        "background: rgba(74, 144, 217, 0.06); "
        "border-left: 3px solid #4A90D9; "
        "padding: 14px 18px; border-radius: 0 6px 6px 0;",
        "font_sizes_card",
    )
    annotation = s.text_xs + s.project.colors.neutral_gray


bs = BlockStyles


def build():
    """Render the Font Sizes intro section."""
    st_space("v", 1)
    st_write(bs.heading, "Font sizes — three systems", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── Lead paragraph (uses indexed scale to dogfood) ────────────────
    st_write(
        s.text_lg + s.center_txt,
        "StreamTeX exposes ",
        (s.bold, "three"),
        " font-size systems. The newest one — ",
        (s.bold, "indexed responsive"),
        " — is the recommended default for any new block.",
    )
    st_space("v", 2)

    # ── Three-column overview ─────────────────────────────────────────
    st_write(bs.sub, "The three systems", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(
        cols="repeat(auto-fit, minmax(260px, 1fr))",
        grid_style=stx.StxStyles.container.grid.gap_24,
    ):
        with st_block(bs.card):
            st_write(s.text_xl + s.bold, "1. Semantic")
            st_space("v", 0.5)
            st_write(
                s.text_base,
                (s.bold, "s.medium "), "/ ",
                (s.bold, "s.large "), "/ ",
                (s.bold, "s.GIANT"),
            )
            st_space("v", 0.5)
            st_write(
                s.text_sm + s.project.colors.neutral_gray,
                "Named sizes from a fixed scale. Familiar but tied to "
                "absolute pt values and not responsive.",
            )

        with st_block(bs.card):
            st_write(s.text_xl + s.bold, "2. Absolute pt")
            st_space("v", 0.5)
            st_write(
                s.text_base,
                (s.bold, "s.text.sizes.pt4 "), "/ ",
                (s.bold, "pt16 "), "/ ",
                (s.bold, "pt196"),
            )
            st_space("v", 0.5)
            st_write(
                s.text_sm + s.project.colors.neutral_gray,
                "Exact point value, frozen forever. Use when a specific "
                "pt is part of the design contract.",
            )

        with st_block(bs.card):
            st_write(s.text_xl + s.project.colors.accent_teal + s.bold,
                     "3. Indexed (recommended)")
            st_space("v", 0.5)
            st_write(
                s.text_base,
                (s.bold, "s.text_xs "), "/ ",
                (s.bold, "s.text_base "), "/ ",
                (s.bold, "s.text_9xl"),
            )
            st_space("v", 0.5)
            st_write(
                s.text_sm + s.project.colors.neutral_gray,
                "29 paliers derived from a single base_pt_desktop + "
                "4 curve silhouettes. Responsive at 1024px and 480px.",
            )

    st_space("v", 2)

    # ── Live size demo ────────────────────────────────────────────────
    st_write(bs.sub, "Live demo — five paliers of the indexed scale",
             toc_lvl="+1")
    st_space("v", 1)

    st_write(
        s.text_base,
        "The same paragraph at five different paliers. Each line uses "
        "the indexed token directly — no manual pt value involved.",
    )
    st_space("v", 1)

    with st_block(s.project.containers.result_box):
        st_write(s.text_xs, "Sample paragraph (text_xs)")
        st_write(bs.annotation, "text_xs = palier 5 = 14pt desktop")
        st_space("v", 1)
        st_write(s.text_base, "Sample paragraph (text_base)")
        st_write(bs.annotation,
                 "text_base = palier 7 = 18pt desktop (= BASE)")
        st_space("v", 1)
        st_write(s.text_lg, "Sample paragraph (text_lg)")
        st_write(bs.annotation, "text_lg = palier 8 = 20pt desktop")
        st_space("v", 1)
        st_write(s.text_xl, "Sample paragraph (text_xl)")
        st_write(bs.annotation, "text_xl = palier 9 = 22pt desktop")
        st_space("v", 1)
        st_write(s.text_3xl, "Sample paragraph (text_3xl)")
        st_write(bs.annotation, "text_3xl = palier 11 = 28pt desktop")

    st_space("v", 2)

    # ── Which to use when ─────────────────────────────────────────────
    st_write(bs.sub, "Which system to use?", toc_lvl="+1")
    st_space("v", 1)

    comparison_table(
        design_system=DS,
        columns=["Situation", "Pick this", "Why"],
        rows=[
            ("Quick start / new block",
             "s.text_xs … s.text_9xl",
             "Responsive, future-proof. One knob — base_pt_desktop — "
             "rescales every palier on every breakpoint."),
            ("Exact pt forever",
             "s.text.sizes.pt16 / pt24 / pt48",
             "Pick when the design contract demands one frozen value."),
            ("Legacy code or muscle memory",
             "s.medium / s.large / s.GIANT",
             "Still supported — kept for blocks written before 0.7.5."),
        ],
    )
    st_space("v", 2)

    # ── Info callout — they are all responsive via CSS variables ─────
    with st_block(s.project.containers.tip_callout):
        st_write(s.text_lg + s.bold + s.project.colors.primary_blue,
                 "All three systems live behind CSS variables")
        st_space("v", 0.5)
        st_write(
            s.text_base,
            "Every token compiles to ",
            (s.bold, "var(--stx-scale-N, fallback)"),
            " under the hood. Resize the browser past 1024px or 480px to "
            "see the indexed paliers shrink automatically — the absolute "
            "pt and semantic sizes stay constant by design. Switching the "
            "base via ",
            (s.bold, "st_book(scale=ScaleConfig(base_pt_desktop=20))"),
            " rescales every palier proportionally on every breakpoint.",
        )

    st_space("v", 2)
    st_slide_break()
