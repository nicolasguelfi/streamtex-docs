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
from streamtex_design.components.comparison_table import comparison_table


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
            "(scale_curves.toml — one base_pt_desktop + 29 adimensional "
            "ratios per curve) through CSS custom properties to the Python "
            "tokens consumers use. Each layer has one responsibility.",
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
                    "streamtex/styles/scale.py loads ratios + base from "
                    "scale_curves.toml at import time, then derives "
                    "desktop = base × ratios (and tablet/mobile via uniform "
                    "scale factors). Exposes ScaleCurve, ScaleConfig, "
                    "compute_scale(), and emit_scale_css().",
                )

            with st_block(bs.layer_card):
                st_write(bs.layer_label, "Layer 2 — Transport")
                st_space("v", 0.5)
                st_write(s.text_lg + s.bold, "CSS custom properties")
                st_space("v", 0.5)
                st_write(
                    s.text_base,
                    "emit_static_css() output ships inside default.css as "
                    "87 var(--stx-scale-N) declarations across 3 "
                    "breakpoints — 29 :root values for desktop, plus two "
                    "media-query overrides for tablet (≤1024px) and "
                    "mobile (≤480px).",
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
                    "s.scale[N] subscript and s.text_xs…text_9xl Tailwind "
                    "aliases (text_base = idx_7 = BASE).",
                )
        st_space("v", 2)

        # ── 2. scale_curves.toml content ──────────────────────────────
        st_write(bs.sub, "The data file — scale_curves.toml", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Schema v0.2: one TOML section per named curve, each providing
            29 adimensional ratios. [metadata] declares the single base
            value (base_pt_desktop), the anchor index (base_idx, where
            ratios[base_idx] must equal 1.0), the tablet/mobile uniform
            scale factors, and the default curve. desktop[i] is computed at
            import time as round(base_pt_desktop * ratios[i]). Editing the
            TOML and regenerating default.css is enough to ship new values
            — no Python code changes required.
        """)
        st_space("v", 1)

        show_code("""\
# streamtex/styles/scale_curves.toml (truncated)

[metadata]
schema_version = "0.2"
base_pt_desktop = 18      # palier-7 desktop pt (the only absolute value)
base_idx = 7              # ratios[base_idx] MUST equal 1.0
tablet_scale = 0.85       # tablet[i] = round(desktop[i] * 0.85)
mobile_scale = 0.70       # mobile[i] = round(desktop[i] * 0.70)
default_curve = "word_processor"

[word_processor]
description = "Classical word-processor scale (Word/Docs lineage)."
ratios = [
    0.44, 0.50, 0.56, 0.61, 0.67, 0.78, 0.89, 1.00, 1.11, 1.22,
    1.33, 1.56, 1.78, 2.00, 2.22, 2.67, 3.33, 4.00, 5.33, 7.11,
    8.67, 9.33, 10.00, 10.44, 10.67, 10.78, 10.83, 10.89, 11.11,
]

# 3 more curves follow: [geometric], [body_centric], [bell]
# Each has its own [name].ratios = [29 floats] with ratios[7] = 1.0
""", language="toml")
        st_space("v", 2)

        # ── 3. How to add a new curve ─────────────────────────────────
        st_write(bs.sub, "How to add a new curve", toc_lvl="+1")
        st_space("v", 1)

        with st_list(list_type=lt.ordered, li_style=s.text_base) as l:
            with l.item():
                st_write(
                    s.text_base,
                    (s.bold, "Edit scale_curves.toml. "),
                    "Add a new [my_new_curve] section with a single key, "
                    "ratios = [29 floats]. CRITICAL: ratios[base_idx] = 1.0 "
                    "(default base_idx=7) — this is the anchor that ties "
                    "your curve to base_pt_desktop.",
                )
            with l.item():
                st_write(
                    s.text_base,
                    (s.bold, "Add the enum entry. "),
                    "Append MY_NEW_CURVE = \"my_new_curve\" to the "
                    "ScaleCurve Enum in streamtex/styles/scale.py — the "
                    "string value must match the TOML section name.",
                )
            with l.item():
                st_write(
                    s.text_base,
                    (s.bold, "Verify. "),
                    "Run uv run python -m streamtex.styles.scale — the "
                    "module's __main__ guard prints the generated CSS "
                    "block. If validation fails (e.g. ratios[7] ≠ 1.0), "
                    "you get a ValueError pointing at the offending value.",
                )
            with l.item():
                st_write(
                    s.text_base,
                    (s.bold, "Add a test. "),
                    "test_scale.py::TestComputeScale::test_all_named_"
                    "curves_valid is already parametrized over every "
                    "ScaleCurve member — adding the enum entry is enough "
                    "for the test to pick up the new curve automatically.",
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

# Override the base — every palier follows proportionally.
cfg = ScaleConfig(curve=ScaleCurve.GEOMETRIC, base_pt_desktop=24)

desktop, tablet, mobile = compute_scale(cfg)
# desktop[7] = base_pt_desktop = 24 (anchor)
# tablet[i]  = round(desktop[i] * tablet_scale)   # 0.85 default
# mobile[i]  = round(desktop[i] * mobile_scale)   # 0.70 default

css_block = emit_scale_css(cfg)
# → ":root {\\n    --stx-scale-0: ...pt;\\n    ...\\n} ..."
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
                "Every curve must declare exactly 29 ratios — otherwise "
                "ValueError. ratios[base_idx] MUST equal 1.0; otherwise "
                "the curve is rejected at import time. All ratios must be "
                "positive floats — otherwise ValueError. Monotonic "
                "non-decreasing ratios emit a warning (not an error): the "
                "library still loads but logs a 'visual inconsistency "
                "risk' message to streamtex.styles."
            ),
        )
        st_space("v", 2)

        # ── 7. Changing the base ──────────────────────────────────────
        st_write(bs.sub, "Changing the base", toc_lvl="+1")
        st_space("v", 1)

        st_write(
            s.text_base,
            "For an individual document, ",
            (s.bold, "st_book(scale=ScaleConfig(base_pt_desktop=X))"),
            " is the simplest knob to rescale every palier on every "
            "breakpoint without touching the curve or the ratios.",
        )
        st_space("v", 1)

        comparison_table(
            design_system=DS,
            columns=["base_pt_desktop", "Use case",
                     "Palier 7 desktop (BASE)"],
            rows=[
                ("16",
                 "Dense documents — manuals, reports, multi-column prose.",
                 "16pt"),
                ("18 (default)",
                 "General reading — articles, blog posts, mixed media.",
                 "18pt"),
                ("24",
                 "Presentation projection or accessibility-first sites.",
                 "24pt"),
            ],
        )

        st_space("v", 2)
        st_slide_break()
