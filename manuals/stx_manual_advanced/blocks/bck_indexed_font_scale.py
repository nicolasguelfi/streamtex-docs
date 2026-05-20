"""Indexed responsive font scale — the deep dive (0.7.5+).

Covers the three access modes, the four named curves, the 29-palier visual
reference, per-document configuration, out-of-range clamping behaviour, and
the identity table between Tailwind alias, subscript, and direct attribute.
"""

from streamtex import *
import streamtex as stx
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation
from streamtex_design.design_systems.default import DesignSystem
from streamtex_design.components.callout import callout
from streamtex_design.components.comparison_table import comparison_table


DS = DesignSystem()


class BlockStyles:
    """Indexed font scale block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    palier_cell = Style(
        "border: 1px solid rgba(74, 144, 217, 0.25); "
        "padding: 8px 6px; border-radius: 4px; text-align: center;",
        "palier_cell",
    )
    palier_label = s.text_xs + s.project.colors.neutral_gray
    mode_card = Style(
        "background: rgba(74, 144, 217, 0.06); "
        "border-left: 3px solid #4A90D9; "
        "padding: 16px 18px; border-radius: 0 6px 6px 0; height: 100%;",
        "mode_card",
    )


bs = BlockStyles


# Palier → pt fallback table (matches text.py WORD_PROCESSOR desktop values)
_PALIER_PT = [
    8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 28, 32, 36, 40,
    48, 60, 72, 96, 128, 156, 168, 180, 188, 192, 194, 195, 196, 200,
]


def build():
    """Render the comprehensive indexed font scale deep dive."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Indexed responsive font scale",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # ── 1. Motivation ─────────────────────────────────────────────
        callout(
            design_system=DS,
            variant="info",
            title="Why an indexed scale?",
            body=(
                "Pre-0.7.5, font sizes were either fixed pt values (s.pt16) "
                "or named buckets (s.medium, s.large). Both froze the layout "
                "at desktop size. The indexed scale adds a 29-palier "
                "responsive ladder — each token resolves to a CSS variable "
                "that shrinks automatically at 1024px and 480px breakpoints."
            ),
        )
        st_space("v", 2)

        # ── 2. Three access modes ─────────────────────────────────────
        st_write(bs.sub, "Three access modes — same value", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(
            cols="repeat(auto-fit, minmax(280px, 1fr))",
            grid_style=stx.StxStyles.container.grid.gap_24,
        ):
            with st_block(bs.mode_card):
                st_write(s.text_xl + s.bold, "Tailwind alias")
                st_space("v", 0.5)
                st_write(
                    s.text_base,
                    "The most readable mode — 13 stable names mapped to "
                    "specific paliers. Names never change even when the "
                    "underlying curve does.",
                )
                st_space("v", 0.5)
                show_code(
                    "st_write(s.text_xs,   'Caption')\n"
                    "st_write(s.text_base, 'Body')\n"
                    "st_write(s.text_3xl,  'Heading')\n"
                    "st_write(s.text_7xl,  'Hero title')",
                )

            with st_block(bs.mode_card):
                st_write(s.text_xl + s.bold, "Subscript")
                st_space("v", 0.5)
                st_write(
                    s.text_base,
                    "Dynamic indexing — pick the palier at runtime, "
                    "ideal for loops over heading levels.",
                )
                st_space("v", 0.5)
                show_code(
                    "for level in range(4):\n"
                    "    idx = 12 - level * 2\n"
                    "    st_write(s.scale[idx],\n"
                    "             f'H{level+1} heading')",
                )

            with st_block(bs.mode_card):
                st_write(s.text_xl + s.bold, "Direct attribute")
                st_space("v", 0.5)
                st_write(
                    s.text_base,
                    "Autocomplete-friendly named attribute on Text.sizes "
                    "— useful when an editor's static analyser is the "
                    "primary reader.",
                )
                st_space("v", 0.5)
                show_code(
                    "from streamtex.styles import Text\n"
                    "\n"
                    "st_write(Text.sizes.idx_6, 'Palier 6')\n"
                    "st_write(s.text.sizes.idx_12, 'Heading')",
                )
        st_space("v", 2)

        # ── 3. Four named curves ──────────────────────────────────────
        st_write(bs.sub, "The four named curves", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Each curve is a complete 29-value mapping shipped in
            ``streamtex/styles/scale_curves.toml``. Pick one per document
            via ``st_book(scale=ScaleConfig(curve=...))``.
        """)
        st_space("v", 1)

        comparison_table(
            design_system=DS,
            columns=["Curve", "Intended use", "Key paliers"],
            rows=[
                ("WORD_PROCESSOR (default)",
                 "General documents — Word/Docs lineage. "
                 "Fine at small sizes, coarser in display range.",
                 "8 / 12 / 16 / 24 / 48 / 96 / 196"),
                ("GEOMETRIC",
                 "Uniform visual ratio (~1.15) between paliers. "
                 "Predictable for design systems.",
                 "10 / 17 / 30 / 53 / 93 / 163 / 497"),
                ("BODY_CENTRIC",
                 "Dense in the body range (14-32pt). "
                 "Best for prose-heavy manuals.",
                 "8 / 16 / 20 / 28 / 56 / 128 / 196"),
                ("BELL",
                 "Sparse at extremes, dense in the middle. "
                 "One giant hero + small captions for slides.",
                 "6 / 18 / 24 / 32 / 64 / 196 / 196"),
            ],
        )
        st_space("v", 2)

        # ── 4. Live 29-palier visual reference ────────────────────────
        st_write(bs.sub, "29-palier visual reference (live)", toc_lvl="+1")
        st_space("v", 1)

        st_write(
            s.text_base,
            "Every palier rendered with its actual token. Resize the "
            "browser past 1024px or 480px to see the values shrink.",
        )
        st_space("v", 1)

    # The grid renders best edge-to-edge — open a separate block
    with st_grid(cols=4, cell_styles=bs.palier_cell) as g:
        for i in range(29):
            with g.cell():
                st_write(s.scale[i], "Aa")
                st_write(bs.palier_label, f"idx_{i} = {_PALIER_PT[i]}pt")
    st_space("v", 2)

    with st_block(s.center_txt):
        # ── 5. Per-document config ────────────────────────────────────
        st_write(bs.sub, "Per-document configuration", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Pass a ``ScaleConfig`` to ``st_book(scale=...)`` to override
            the curve and palier count for one document — the change is
            scoped to that book's HTML output.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import st_book, ScaleConfig, ScaleCurve

st_book(
    [blocks...],
    scale=ScaleConfig(
        curve=ScaleCurve.GEOMETRIC,   # WORD_PROCESSOR | GEOMETRIC | BODY_CENTRIC | BELL
        count=20,                      # 1..29 paliers exposed
    ),
)""")
        st_space("v", 2)

        # ── 6. Out-of-range tolerance ─────────────────────────────────
        st_write(bs.sub, "Out-of-range tolerance", toc_lvl="+1")
        st_space("v", 1)

        callout(
            design_system=DS,
            variant="info",
            title="Subscript clamps silently",
            body=(
                "s.scale[-5] returns s.scale[0]. s.scale[100] returns "
                "s.scale[28]. The library debug-logs the clamp but never "
                "raises — your block keeps rendering even when an index "
                "drifts out of range."
            ),
        )
        st_space("v", 1)

        with st_block(s.project.containers.result_box):
            st_write(s.text_base + s.bold, "Live clamp demo")
            st_space("v", 0.5)
            st_write(s.scale[-5], "s.scale[-5]  → clamped to s.scale[0]")
            st_write(s.scale[100], "s.scale[100] → clamped to s.scale[28]")
        st_space("v", 2)

        # ── 7. Responsive demo invitation ─────────────────────────────
        st_write(bs.sub, "Responsive — resize the browser", toc_lvl="+1")
        st_space("v", 1)

        callout(
            design_system=DS,
            variant="info",
            title="Three breakpoints out of the box",
            body=(
                "Desktop ≥ 1024px uses the curve's desktop column. "
                "Tablet 480-1024px swaps to ~75% of desktop. "
                "Mobile < 480px swaps to ~60%. Resize this window past "
                "1024 and 480 to see every palier above shrink in lockstep."
            ),
        )
        st_space("v", 2)

        # ── 8. Identity table ─────────────────────────────────────────
        st_write(bs.sub, "Identity table — three names, one palier",
                 toc_lvl="+1")
        st_space("v", 1)

        comparison_table(
            design_system=DS,
            columns=["Tailwind alias", "Subscript", "Direct attribute",
                     "pt (desktop)"],
            rows=[
                ("s.text_xs",   "s.scale[2]",  "s.text.sizes.idx_2",  "10pt"),
                ("s.text_sm",   "s.scale[3]",  "s.text.sizes.idx_3",  "11pt"),
                ("s.text_base", "s.scale[4]",  "s.text.sizes.idx_4",  "12pt"),
                ("s.text_lg",   "s.scale[5]",  "s.text.sizes.idx_5",  "14pt"),
                ("s.text_xl",   "s.scale[6]",  "s.text.sizes.idx_6",  "16pt"),
                ("s.text_2xl",  "s.scale[7]",  "s.text.sizes.idx_7",  "18pt"),
                ("s.text_3xl",  "s.scale[9]",  "s.text.sizes.idx_9",  "22pt"),
                ("s.text_4xl",  "s.scale[10]", "s.text.sizes.idx_10", "24pt"),
                ("s.text_5xl",  "s.scale[12]", "s.text.sizes.idx_12", "32pt"),
                ("s.text_6xl",  "s.scale[15]", "s.text.sizes.idx_15", "48pt"),
                ("s.text_7xl",  "s.scale[16]", "s.text.sizes.idx_16", "60pt"),
                ("s.text_8xl",  "s.scale[17]", "s.text.sizes.idx_17", "72pt"),
                ("s.text_9xl",  "s.scale[19]", "s.text.sizes.idx_19", "128pt"),
            ],
        )

        st_space("v", 2)
        st_slide_break()
