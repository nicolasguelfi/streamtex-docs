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


# Palier → pt fallback table — desktop values for WORD_PROCESSOR with
# base_pt_desktop = 18 (palier 7 anchor). All paliers above/below derive
# from the curve's adimensional ratios: desktop[i] = round(18 * ratios[i]).
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
            title="A single base value drives every palier",
            body=(
                "The indexed scale is RELATIVE: a single base_pt_desktop "
                "(default 18pt at palier 7) is multiplied by 29 adimensional "
                "ratios to produce every desktop palier. Tablet and mobile "
                "columns are then derived uniformly via tablet_scale (0.85) "
                "and mobile_scale (0.70). Changing the base re-scales "
                "everything proportionally — no per-palier hand-tuning "
                "needed. Curves differ only in their ratio silhouette; they "
                "all anchor at palier 7 = base_pt_desktop."
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
                    "st_write(s.text_xs,   'Caption')    # idx_5 = 14pt\n"
                    "st_write(s.text_base, 'Body')       # idx_7 = 18pt (BASE)\n"
                    "st_write(s.text_3xl,  'Heading')    # idx_11 = 28pt\n"
                    "st_write(s.text_7xl,  'Hero title') # idx_16 = 60pt",
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
                    "    # 12=32pt, 10=24pt, 8=20pt, 6=16pt\n"
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
                    "st_write(Text.sizes.idx_7, 'BASE = 18pt')\n"
                    "st_write(s.text.sizes.idx_12, 'Display = 32pt')",
                )
        st_space("v", 2)

        # ── 3. Four named curves ──────────────────────────────────────
        st_write(bs.sub, "The four named curves", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Each curve is a 29-value **ratio profile** shipped in
            ``streamtex/styles/scale_curves.toml``. All four curves share
            the SAME base — they differ only in their silhouette
            (the relative ratios between paliers). Anchor: ``ratios[7] = 1.0``
            so palier 7 always equals ``base_pt_desktop`` (default 18pt).
            Pick one per document via ``st_book(scale=ScaleConfig(curve=...))``.
        """)
        st_space("v", 1)

        comparison_table(
            design_system=DS,
            columns=["Curve", "Intended use",
                     "Ratios at key paliers (5 / 7 / 8 / 12 / 16)"],
            rows=[
                ("WORD_PROCESSOR (default)",
                 "General documents — Word/Docs lineage. "
                 "Fine at small sizes, coarser in display range.",
                 "0.78 / 1.00 / 1.11 / 1.78 / 3.33"),
                ("GEOMETRIC",
                 "Uniform visual ratio (~1.125) between paliers. "
                 "Predictable for design systems.",
                 "0.79 / 1.00 / 1.13 / 1.80 / 2.88"),
                ("BODY_CENTRIC",
                 "Dense in the body range (14-32pt). "
                 "Best for prose-heavy manuals.",
                 "0.89 / 1.00 / 1.11 / 1.56 / 3.11"),
                ("BELL",
                 "Sparse at extremes, dense in the middle. "
                 "One giant hero + small captions for slides.",
                 "0.33 / 1.00 / 1.33 / 1.78 / 10.89"),
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
                if i == 7:
                    st_write(
                        bs.palier_label,
                        f"idx_{i} = {_PALIER_PT[i]}pt  "
                        "← BASE = base_pt_desktop = 18pt by default",
                    )
                else:
                    st_write(
                        bs.palier_label,
                        f"idx_{i} = {_PALIER_PT[i]}pt",
                    )
    st_space("v", 2)

    with st_block(s.center_txt):
        # ── 5. Per-document config ────────────────────────────────────
        st_write(bs.sub, "Per-document configuration", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Pass a ``ScaleConfig`` to ``st_book(scale=...)`` to override
            any of the four knobs that drive the scale. The change is
            scoped to that book's HTML output. All four fields are
            optional — unset fields fall back to the TOML defaults
            (base_pt_desktop=18, base_idx=7, tablet_scale=0.85,
            mobile_scale=0.70, curve=WORD_PROCESSOR).
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import st_book, ScaleConfig, ScaleCurve

# 1) Bigger desktop type — every palier follows on every breakpoint.
#    Use when the project ships at a larger reading size (e.g. projection,
#    accessibility-first sites).
st_book([blocks...], scale=ScaleConfig(base_pt_desktop=24))

# 2) Shift the anchor — palier other than 7 maps to base_pt_desktop.
#    Use when the project's natural body text is at a different index
#    than the default (rare; advanced).
st_book([blocks...], scale=ScaleConfig(base_idx=8))

# 3) Custom breakpoint shrink — tighter or looser tablet/mobile.
#    Defaults: tablet_scale=0.85, mobile_scale=0.70.
st_book([blocks...], scale=ScaleConfig(
    tablet_scale=0.9,    # tablet keeps 90% of desktop (less shrink)
    mobile_scale=0.65,   # mobile drops to 65% (more shrink)
))

# 4) Different silhouette — same base, different ratio profile.
st_book([blocks...], scale=ScaleConfig(curve=ScaleCurve.GEOMETRIC))

# Combine any subset of knobs.
st_book([blocks...], scale=ScaleConfig(
    curve=ScaleCurve.GEOMETRIC,
    base_pt_desktop=24,
    tablet_scale=0.9,
    mobile_scale=0.65,
))""")
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
                "Desktop ≥ 1024px uses base_pt_desktop × ratios. "
                "Tablet 480-1024px applies tablet_scale (default 0.85) "
                "uniformly to every desktop palier. Mobile < 480px applies "
                "mobile_scale (default 0.70). Resize this window past 1024 "
                "and 480 to see every palier above shrink in lockstep."
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
                     "pt (desktop @ base=18)"],
            rows=[
                ("s.text_xs",   "s.scale[5]",  "s.text.sizes.idx_5",  "14pt"),
                ("s.text_sm",   "s.scale[6]",  "s.text.sizes.idx_6",  "16pt"),
                ("s.text_base", "s.scale[7]",  "s.text.sizes.idx_7",  "18pt (BASE)"),
                ("s.text_lg",   "s.scale[8]",  "s.text.sizes.idx_8",  "20pt"),
                ("s.text_xl",   "s.scale[9]",  "s.text.sizes.idx_9",  "22pt"),
                ("s.text_2xl",  "s.scale[10]", "s.text.sizes.idx_10", "24pt"),
                ("s.text_3xl",  "s.scale[11]", "s.text.sizes.idx_11", "28pt"),
                ("s.text_4xl",  "s.scale[12]", "s.text.sizes.idx_12", "32pt"),
                ("s.text_5xl",  "s.scale[13]", "s.text.sizes.idx_13", "36pt"),
                ("s.text_6xl",  "s.scale[15]", "s.text.sizes.idx_15", "48pt"),
                ("s.text_7xl",  "s.scale[16]", "s.text.sizes.idx_16", "60pt"),
                ("s.text_8xl",  "s.scale[17]", "s.text.sizes.idx_17", "72pt"),
                ("s.text_9xl",  "s.scale[19]", "s.text.sizes.idx_19", "128pt"),
            ],
        )

        st_space("v", 2)
        st_slide_break()
