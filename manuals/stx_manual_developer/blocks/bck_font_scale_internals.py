"""Indexed font scale — internals for library contributors.

Covers the 3-layer architecture (TOML data, default.css variables, Python
tokens), the generator API (compute_scale, emit_scale_css), the fallback
chain, validation rules, and a step-by-step "add a new curve" recipe.
"""

from streamtex import *
import streamtex as stx
from streamtex.enums import Tags as t, ListTypes as lt
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation
from streamtex_design.design_systems.default import DesignSystem
from streamtex_design.components.callout import callout


DS = DesignSystem()


class BlockStyles:
    """Font scale internals block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    layer_card = Style(
        "background: rgba(0, 188, 212, 0.06); "
        "border-left: 3px solid #00BCD4; "
        "padding: 16px 18px; border-radius: 0 6px 6px 0; height: 100%;",
        "fs_layer_card",
    )
    layer_label = Style(
        "color: #00BCD4; font-weight: bold; "
        "text-transform: uppercase; letter-spacing: 1.5px;",
        "fs_layer_label",
    ) + s.text_sm


bs = BlockStyles


def build():
    """Render the indexed font scale internals deep dive."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Indexed font scale — internals",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # ── 1. Three-layer architecture ───────────────────────────────
        st_write(bs.sub, "Three-layer architecture", toc_lvl="+1")
        st_space("v", 1)

        st_write(
            s.text_base,
            "The indexed scale flows from a single source of truth "
            "(scale_curves.toml) through CSS custom properties to the "
            "Python tokens consumers use. Each layer has one responsibility.",
        )
        st_space("v", 1)

        with st_grid(
            cols="repeat(auto-fit, minmax(260px, 1fr))",
            grid_style=stx.StxStyles.container.grid.gap_24,
        ):
            with st_block(bs.layer_card):
                st_write(bs.layer_label, "Layer 1 — Data")
                st_space("v", 0.5)
                st_write(s.text_lg + s.bold, "Python generator")
                st_space("v", 0.5)
                st_write(
                    s.text_base,
                    "streamtex/styles/scale.py loads scale_curves.toml at "
                    "import time, validates it, and exposes ScaleCurve, "
                    "ScaleConfig, compute_scale(), and emit_scale_css().",
                )

            with st_block(bs.layer_card):
                st_write(bs.layer_label, "Layer 2 — Transport")
                st_space("v", 0.5)
                st_write(s.text_lg + s.bold, "CSS custom properties")
                st_space("v", 0.5)
                st_write(
                    s.text_base,
                    "emit_static_css() output ships inside default.css as "
                    "29 :root --stx-scale-N variables, plus two media-query "
                    "overrides for tablet (≤1024px) and mobile (≤480px).",
                )

            with st_block(bs.layer_card):
                st_write(bs.layer_label, "Layer 3 — API")
                st_space("v", 0.5)
                st_write(s.text_lg + s.bold, "Python tokens")
                st_space("v", 0.5)
                st_write(
                    s.text_base,
                    "Text.sizes.idx_0…idx_28 wrap each variable in a Style "
                    "with a fallback pt value. StxStyles re-exposes them as "
                    "s.scale[N] subscript and s.text_xs…text_9xl aliases.",
                )
        st_space("v", 2)

        # ── 2. scale_curves.toml content ──────────────────────────────
        st_write(bs.sub, "The data file — scale_curves.toml", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            One TOML section per named curve. Each provides exactly 29 ints
            per breakpoint (desktop / tablet / mobile). Editing the TOML and
            regenerating default.css is enough to ship new values — no
            Python code changes required.
        """)
        st_space("v", 1)

        show_code("""\
# streamtex/styles/scale_curves.toml (truncated)

[metadata]
schema_version = "0.1"
default_curve = "word_processor"

[word_processor]
description = "Classical word-processor scale (Word/Docs lineage)."
desktop = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 28, 32, 36, 40,
           48, 60, 72, 96, 128, 156, 168, 180, 188, 192, 194, 195, 196, 200]
tablet  = [7, 8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 30, 36,
           42, 50, 60, 78, 100, 120, 130, 140, 145, 148, 150, 152, 154, 156]
mobile  = [6, 7, 7, 8, 9, 10, 11, 13, 14, 16, 18, 20, 22, 26, 30,
           36, 42, 50, 64, 84, 100, 108, 116, 120, 124, 126, 128, 130, 132]

# 3 more curves follow: [geometric], [body_centric], [bell]
""", language="toml")
        st_space("v", 2)

        # ── 3. How to add a new curve ─────────────────────────────────
        st_write(bs.sub, "How to add a new curve", toc_lvl="+1")
        st_space("v", 1)

        with st_list(list_type=lt.ordered, li_style=s.text_base) as l:
            with l.item():
                st_write(
                    s.text_base,
                    (s.bold, "Edit the TOML. "),
                    "Add a new [my_curve] section to "
                    "streamtex/styles/scale_curves.toml with three "
                    "29-element lists (desktop, tablet, mobile).",
                )
            with l.item():
                st_write(
                    s.text_base,
                    (s.bold, "Add the enum entry. "),
                    "Append MY_CURVE = \"my_curve\" to the ScaleCurve "
                    "Enum in streamtex/styles/scale.py — the string "
                    "value must match the TOML section name.",
                )
            with l.item():
                st_write(
                    s.text_base,
                    (s.bold, "Validate. "),
                    "Run uv run python -m streamtex.styles.scale — the "
                    "module's __main__ guard prints the generated CSS "
                    "block. If validation fails, you get a ValueError "
                    "pointing at the offending values.",
                )
            with l.item():
                st_write(
                    s.text_base,
                    (s.bold, "Regenerate default.css. "),
                    "Pipe emit_static_css() output into the BEGIN/END "
                    "markers in streamtex/static/default.css. The default "
                    "curve is metadata.default_curve in the TOML — change "
                    "that string to switch the library-wide default.",
                )
        st_space("v", 2)

        # ── 4. The generator API ──────────────────────────────────────
        st_write(bs.sub, "Generator API", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            ``compute_scale(config)`` resolves a ScaleConfig into three lists
            (desktop, tablet, mobile). ``emit_scale_css(config)`` wraps the
            result in :root + media-query CSS ready for injection.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex.styles.scale import (
    ScaleConfig, ScaleCurve, compute_scale, emit_scale_css,
)

cfg = ScaleConfig(curve=ScaleCurve.GEOMETRIC, count=20)

desktop, tablet, mobile = compute_scale(cfg)
# → [10, 11, 13, 15, 17, 20, 23, 26, 30, 35,
#    40, 46, 53, 61, 70, 81, 93, 107, 123, 142]

css_block = emit_scale_css(cfg)
# → ":root {\\n    --stx-scale-0: 10pt;\\n    ...\\n} ..."
""")
        st_space("v", 2)

        # ── 5. Fallback chain ─────────────────────────────────────────
        st_write(bs.sub, "Resolution order — fallback chain", toc_lvl="+1")
        st_space("v", 1)

        callout(
            design_system=DS,
            variant="info",
            title="var(--stx-scale-N, fallback_pt)",
            body=(
                "At render time each indexed token resolves in this order: "
                "(1) :root override emitted by st_book(scale=...), if any. "
                "(2) Static :root block in default.css (default curve, "
                "count=29). (3) The Style's hardcoded fallback pt — the "
                "constant after the comma in var(...). This last layer "
                "guarantees that the token always produces a visible size "
                "even if the stylesheet fails to load."
            ),
        )
        st_space("v", 2)

        # ── 6. Validation rules ───────────────────────────────────────
        st_write(bs.sub, "Validation rules", toc_lvl="+1")
        st_space("v", 1)

        callout(
            design_system=DS,
            variant="warn",
            title="_load_curves() at import time",
            body=(
                "Every curve must declare exactly 29 ints per breakpoint "
                "(desktop, tablet, mobile) — otherwise ValueError. All "
                "values must be positive integers — otherwise ValueError. "
                "Monotonic non-decreasing values emit a warning (not an "
                "error): the library still loads but logs a "
                "'visual inconsistency risk' message to streamtex.styles."
            ),
        )

        st_space("v", 2)
        st_slide_break()
