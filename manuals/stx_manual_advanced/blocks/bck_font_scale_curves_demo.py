"""Font scale curves — live side-by-side comparison of the 4 named curves.

Renders the same headline + body + caption block four times, each scoped
to a per-block style attribute that overrides ``--stx-scale-*`` for that
container only. Values come from ``compute_scale(ScaleConfig(curve=...))``
at build time.
"""

from streamtex import *
from streamtex.enums import Tags as t
from streamtex.styles import Style
from streamtex.styles.scale import ScaleConfig, ScaleCurve, compute_scale
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem
from streamtex_design.components.callout import callout


DS = DesignSystem()


class BlockStyles:
    """Curve demo block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    section = Style(
        "padding: 18px 20px; "
        "border: 1px solid rgba(74, 144, 217, 0.18); "
        "border-radius: 8px; margin-bottom: 12px;",
        "curve_section",
    )


bs = BlockStyles


# Curves displayed side-by-side, in this order.
_CURVES = [
    (ScaleCurve.WORD_PROCESSOR,
     "WORD_PROCESSOR — the default, balanced for general documents."),
    (ScaleCurve.GEOMETRIC,
     "GEOMETRIC — uniform ~1.15 ratio, predictable for design systems."),
    (ScaleCurve.BODY_CENTRIC,
     "BODY_CENTRIC — dense in 14-32pt, prose-friendly."),
    (ScaleCurve.BELL,
     "BELL — sparse extremes + one giant hero, best for slides."),
]


def _scope_style(curve: ScaleCurve) -> Style:
    """Build an inline Style that overrides --stx-scale-* for one curve.

    The CSS variables are emitted on the block itself; they cascade to all
    descendants, so every s.scale[N] / s.text_* token nested inside picks
    up the new values without further wiring.
    """
    desktop, _, _ = compute_scale(ScaleConfig(curve=curve, count=29))
    css_vars = " ".join(f"--stx-scale-{i}: {v}pt;"
                        for i, v in enumerate(desktop))
    return bs.section + Style(css_vars, f"scope_{curve.value}")


def build():
    """Render the same content under each of the 4 named curves."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Curves head-to-head — same content, four scales",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        st_write(
            s.text_base + s.center_txt,
            "The same headline + body + caption rendered four times. Each "
            "section overrides ",
            (s.bold, "--stx-scale-*"),
            " on its own container, so paliers visibly differ across "
            "curves while every other style stays identical.",
        )
        st_space("v", 2)

    # Render one section per curve
    for curve, description in _CURVES:
        desktop, _, _ = compute_scale(ScaleConfig(curve=curve, count=29))
        with st_block(_scope_style(curve)):
            st_write(s.text_sm + s.project.colors.neutral_gray, description)
            st_space("v", 0.5)
            # Headline — palier 16 (text_7xl)
            st_write(s.text_7xl + s.bold,
                     f"Headline ({curve.value})")
            st_space("v", 0.5)
            # Body — palier 5 (text_lg)
            st_write(
                s.text_lg,
                "Body paragraph at palier 5. Notice how the gap between "
                "this body text and the headline above changes from curve "
                "to curve — the headline palier moves while the body palier "
                "stays at the same index.",
            )
            st_space("v", 0.5)
            # Caption — palier 2 (text_xs)
            st_write(
                s.text_xs + s.project.colors.neutral_gray,
                f"Caption at palier 2 — desktop pt = {desktop[2]} "
                f"(palier 5 body = {desktop[5]}pt, palier 16 headline = "
                f"{desktop[16]}pt).",
            )

    st_space("v", 2)

    with st_block(s.center_txt):
        # ── Conclusion — when to pick which curve ─────────────────────
        callout(
            design_system=DS,
            variant="info",
            title="Picking a curve",
            body=(
                "WORD_PROCESSOR is safe for any mixed document. GEOMETRIC "
                "is the right pick when designers will hand-tune palette and "
                "want predictable ratios. BODY_CENTRIC suits dense prose "
                "(manuals, reports). BELL is for slide decks with one hero "
                "title and tight body — extremes collapse to a single sky-high "
                "palier so the entire deck reads at one giant size."
            ),
        )

        st_space("v", 2)
        st_slide_break()
