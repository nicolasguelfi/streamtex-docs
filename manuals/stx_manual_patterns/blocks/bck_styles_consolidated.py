"""Showcase — Consolidated style bundles from streamtex-patterns/styles/.

Renders every bundle defined in
`streamtex-patterns/styles/styles_consolidated.py` so a designer can
visually pick the right variant for a new block.

# @pattern: ptn_manual_section
"""

import importlib.util
from pathlib import Path

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_explanation, show_details


# ----------------------------------------------------------------------------
# Load streamtex-patterns/styles/styles_consolidated.py as `sc`
# ----------------------------------------------------------------------------

_THIS = Path(__file__).resolve()
_CONSOLIDATED = (
    _THIS.parents[4] / "streamtex-patterns" / "styles" / "styles_consolidated.py"
)

sc = None
_import_error = ""
try:
    _spec = importlib.util.spec_from_file_location("sc_module", _CONSOLIDATED)
    sc = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(sc)
except Exception as e:
    _import_error = f"{type(e).__name__}: {e}"


# ----------------------------------------------------------------------------
# Local frame styles (for the showcase chrome, NOT the showcased bundles)
# ----------------------------------------------------------------------------


class BlockStyles:
    """Frame styles for the showcase grid itself."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    body_c = s.large + s.center_txt

    # Per-variant block styles (2 cols × 3 rows)
    row_label_style = (
        s.large
        + s.bold
        + s.project.colors.primary_violet
        + s.center_txt
    )
    name_style = s.large + s.bold + s.text.fonts.font_monospace
    expr_style = (
        s.medium
        + s.text.fonts.font_monospace
        + s.project.colors.neutral_gray
    )

    # Cell style applied uniformly to all 6 cells of a variant block.
    # `word-break: break-word` + `overflow-wrap: anywhere` are MANDATORY
    # here: long monospace identifiers like `st_grid(cols, gap,
    # cell_styles)` rendered at Large size do NOT wrap by default and
    # bleed across cell boundaries (visual bug fixed).
    variant_cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.container.layouts.vertical_center_layout
        + Style(
            "word-break: break-word; overflow-wrap: anywhere;",
            "showcase_wrap_break",
        )
    )
    sample_box = (
        s.container.paddings.small_padding
        + Style(
            "border: 1px dashed rgba(167, 139, 250, 0.3); "
            "border-radius: 6px;",
            "showcase_sample_box",
        )
    )


bs = BlockStyles

# Per-variant 2-column grid: fixed-width label column + flexible value column.
# Wide value column ensures long monospace strings have room before wrapping.
_VARIANT_COLS = "200px 1fr"
_GAP = "0px"


# ----------------------------------------------------------------------------
# Helper: render one variant as a 2-col × 3-row block
# ----------------------------------------------------------------------------


def _showcase(items):
    """Render each variant as a self-contained `2 cols × 3 rows` block.

    Layout per variant:
        ┌──────────────┬──────────────────────────────────────┐
        │ Name         │ <canonical attribute path>           │
        ├──────────────┼──────────────────────────────────────┤
        │ Composition  │ <formula>                            │
        ├──────────────┼──────────────────────────────────────┤
        │ Live render  │ <style applied to sample content>    │
        └──────────────┴──────────────────────────────────────┘

    Variants are separated by `st_space("v", 1.5)` for visual rhythm.
    """
    for name, expr, render_fn in items:
        with st_grid(cols=_VARIANT_COLS, gap=_GAP,
                     cell_styles=bs.variant_cell) as g:
            # Row 1: Name
            with g.cell():
                st_write(bs.row_label_style, "Name", tag=t.div)
            with g.cell():
                st_write(bs.name_style, name, tag=t.div)
            # Row 2: Composition
            with g.cell():
                st_write(bs.row_label_style, "Composition", tag=t.div)
            with g.cell():
                st_write(bs.expr_style, expr, tag=t.div)
            # Row 3: Live render
            with g.cell():
                st_write(bs.row_label_style, "Live render", tag=t.div)
            with g.cell():
                render_fn()
        st_space("v", 1.5)


# ============================================================================
# build()
# ============================================================================


def build():
    """Showcase every bundle exposed by styles_consolidated.py."""
    with st_block(s.center_txt):
        st_write(bs.heading,
                 "Consolidated styles — bundle showcase",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    if sc is None:
        st_write(s.large + s.project.colors.warning_red,
                 "⚠️ Could not load styles_consolidated.py")
        st_write(bs.expr_style, _import_error)
        st_write(s.large,
                 "Expected at: " + str(_CONSOLIDATED))
        return

    show_explanation("""\
        Every bundle exposed by
        `streamtex-patterns/styles/styles_consolidated.py` is rendered
        below as a 3-column showcase: **name** (the canonical attribute
        path), **composition** (how the style is built), and **live
        render** (the style applied to representative content).

        Use this page as a visual catalog when choosing which bundle to
        wire into your project's `custom/styles.py` or when authoring a
        new pattern.
    """)
    st_space("v", 2)

    # ── 1. Colors ────────────────────────────────────────────────────────
    _section_header(
        "1. Colors — semantic palette",
        "Six core slots cover every callout / emphasis variant; three "
        "named hues (violet, teal, amber) are kept as explicit aliases "
        "for projects whose visual language references the hue rather "
        "than its semantic role.",
    )

    def _swatch(color_style):
        st_write(s.large + color_style, "Sample text — Hello", tag=t.div)

    _showcase([
        ("Colors.primary",   "color: #7AB8F5",
         lambda: _swatch(sc.Colors.primary)),
        ("Colors.accent",    "color: #2EC4B6",
         lambda: _swatch(sc.Colors.accent)),
        ("Colors.highlight", "color: #F39C12",
         lambda: _swatch(sc.Colors.highlight)),
        ("Colors.success",   "color: #27AE60",
         lambda: _swatch(sc.Colors.success)),
        ("Colors.critical",  "color: #E74C3C",
         lambda: _swatch(sc.Colors.critical)),
        ("Colors.muted",     "color: #95A5A6",
         lambda: _swatch(sc.Colors.muted)),
        ("Colors.violet",    "color: #a78bfa",
         lambda: _swatch(sc.Colors.violet)),
        ("Colors.teal",      "color: #2EC4B6",
         lambda: _swatch(sc.Colors.teal)),
        ("Colors.amber",     "color: #F39C12",
         lambda: _swatch(sc.Colors.amber)),
    ])
    st_space("v", 3)

    # ── 2. Backgrounds ───────────────────────────────────────────────────
    _section_header(
        "2. Backgrounds — translucent tints",
        "Background overlays aligned with the Colors palette. Used as "
        "the bg layer of callouts, cell tints, info / tip boxes.",
    )

    def _bg_swatch(bg_style):
        with st_block(bg_style + bs.sample_box):
            st_write(s.large + s.center_txt, "sample background")

    _showcase([
        ("Backgrounds.info_bg",     "rgba(122, 184, 245, 0.12)",
         lambda: _bg_swatch(sc.Backgrounds.info_bg)),
        ("Backgrounds.warning_bg",  "rgba(243, 156,  18, 0.12)",
         lambda: _bg_swatch(sc.Backgrounds.warning_bg)),
        ("Backgrounds.critical_bg", "rgba(231,  76,  60, 0.15)",
         lambda: _bg_swatch(sc.Backgrounds.critical_bg)),
        ("Backgrounds.success_bg",  "rgba( 39, 174,  96, 0.15)",
         lambda: _bg_swatch(sc.Backgrounds.success_bg)),
        ("Backgrounds.accent_bg",   "rgba( 46, 196, 182, 0.12)",
         lambda: _bg_swatch(sc.Backgrounds.accent_bg)),
        ("Backgrounds.muted_bg",    "rgba(149, 165, 166, 0.08)",
         lambda: _bg_swatch(sc.Backgrounds.muted_bg)),
    ])
    st_space("v", 3)

    # ── 3. Titles ────────────────────────────────────────────────────────
    _section_header(
        "3. Titles — projection-safe hierarchy",
        "Sizes tuned for live projection at 10–20 m. Each variant is a "
        "Style.create(color + bold + size) composition.",
    )

    _showcase([
        ("Titles.slide_title",   "primary + bold + Huge",
         lambda: st_write(sc.Titles.slide_title,   "Slide Title", tag=t.div)),
        ("Titles.section_title", "accent + bold + huge",
         lambda: st_write(sc.Titles.section_title, "Section Title", tag=t.div)),
        ("Titles.page_title",    "primary + bold + LARGE",
         lambda: st_write(sc.Titles.page_title,    "Page Title", tag=t.div)),
        ("Titles.subtitle",      "highlight + bold + Large",
         lambda: st_write(sc.Titles.subtitle,      "Subtitle", tag=t.div)),
        ("Titles.body",          "Large (no color, no weight)",
         lambda: st_write(sc.Titles.body,          "Body paragraph text",
                          tag=t.div)),
        ("Titles.caption",       "muted + large",
         lambda: st_write(sc.Titles.caption,       "Caption / source note",
                          tag=t.div)),
    ])
    st_space("v", 3)

    # ── 4. Headings ──────────────────────────────────────────────────────
    _section_header(
        "4. Headings — centered title aliases",
        "Replaces the 480 ad-hoc occurrences of `heading = X + "
        "center_txt` with explicit names per hierarchy level "
        "(resolves the polysemous `heading` anti-pattern).",
    )

    _showcase([
        ("Headings.slide_heading",     "Titles.slide_title + center",
         lambda: st_write(sc.Headings.slide_heading,
                          "Slide heading", tag=t.div)),
        ("Headings.section_heading",   "Titles.section_title + center",
         lambda: st_write(sc.Headings.section_heading,
                          "Section heading", tag=t.div)),
        ("Headings.page_heading",      "Titles.page_title + center",
         lambda: st_write(sc.Headings.page_heading,
                          "Page heading", tag=t.div)),
        ("Headings.subtitle_centered", "Titles.subtitle + center",
         lambda: st_write(sc.Headings.subtitle_centered,
                          "Subtitle centered", tag=t.div)),
    ])
    st_space("v", 3)

    # ── 5. Keywords ──────────────────────────────────────────────────────
    _section_header(
        "5. Keywords — inline bold-coloured emphasis",
        "Use inside tuples of `st_write`, e.g. "
        "`st_write(body, (Keywords.warn, \"19% slower\"), ...)`. "
        "The semantic role is encoded by the color name.",
    )

    def _kw_demo(kw_style, term):
        st_write(s.large,
                 "Predicted ",
                 (kw_style, term),
                 ", measured otherwise.")

    _showcase([
        ("Keywords.primary",   "bold + Colors.primary",
         lambda: _kw_demo(sc.Keywords.primary,   "24% faster")),
        ("Keywords.accent",    "bold + Colors.accent",
         lambda: _kw_demo(sc.Keywords.accent,    "Cursor IDE")),
        ("Keywords.highlight", "bold + Colors.highlight",
         lambda: _kw_demo(sc.Keywords.highlight, "AI productivity paradox")),
        ("Keywords.warn",      "bold + Colors.highlight (alias)",
         lambda: _kw_demo(sc.Keywords.warn,      "still believed")),
        ("Keywords.success",   "bold + Colors.success",
         lambda: _kw_demo(sc.Keywords.success,   "pattern installed")),
        ("Keywords.critical",  "bold + Colors.critical",
         lambda: _kw_demo(sc.Keywords.critical,  "do not skip the source")),
        ("Keywords.violet",    "bold + Colors.violet",
         lambda: _kw_demo(sc.Keywords.violet,    "GSE-One")),
    ])
    st_space("v", 3)

    # ── 6. Emphasis ──────────────────────────────────────────────────────
    _section_header(
        "6. Emphasis — punch lines and questions",
        "Closing punch line for `ptn_takeaways` and question highlight "
        "for the debrief slide of `ptn_exercise_flow`.",
    )

    _showcase([
        ("Emphasis.closing",  "body + highlight + bold",
         lambda: st_write(sc.Emphasis.closing,
                          "This is why we need a methodology.")),
        ("Emphasis.question", "body + primary + bold + center",
         lambda: st_write(sc.Emphasis.question,
                          "What did you notice?")),
    ])
    st_space("v", 3)

    # ── 7. StatHero ──────────────────────────────────────────────────────
    _section_header(
        "7. StatHero — slide centerpiece statistic",
        "Three variants of the hero stat (GIANT size, bold, centered) "
        "differentiated by colour. Used by `ptn_stat_hero` and "
        "composed inside `ptn_evidence_insight`.",
    )

    _showcase([
        ("StatHero.default",  "GIANT + bold + highlight + center",
         lambda: st_write(sc.StatHero.default,  "+19%")),
        ("StatHero.primary",  "GIANT + bold + primary + center",
         lambda: st_write(sc.StatHero.primary,  "7h")),
        ("StatHero.critical", "GIANT + bold + critical + center",
         lambda: st_write(sc.StatHero.critical, "21%")),
    ])
    st_space("v", 3)

    # ── 8. Table ─────────────────────────────────────────────────────────
    _section_header(
        "8. Table — comparison-table text styles",
        "Text styles for `ptn_comparison_table` cells. ~36 pt base "
        "with hyphenation to avoid overflow. Pair with `Cells.table_"
        "*_cell` for the container side.",
    )

    _showcase([
        ("Table.header_text",  "pt36 + bold + accent + hyphens",
         lambda: st_write(sc.Table.header_text,  "Day")),
        ("Table.cell_text",    "pt36 + hyphens",
         lambda: st_write(sc.Table.cell_text,
                          "GenAI fundamentals")),
        ("Table.label_text",   "pt36 + bold + primary + hyphens",
         lambda: st_write(sc.Table.label_text,   "Day 1")),
        ("Table.label_active", "pt36 + bold + highlight + hyphens",
         lambda: st_write(sc.Table.label_active, "Day 2 (current)")),
    ])
    st_space("v", 3)

    # ── 9. Citation ──────────────────────────────────────────────────────
    _section_header(
        "9. Citation — bibliographic source attribution",
        "Base citation style + composed footer variant. The composed "
        "form `Citation.source` factors the 45 ad-hoc occurrences of "
        "`source = citation + large + center_txt`.",
    )

    _showcase([
        ("Citation.base",   "muted green + italic",
         lambda: st_write(sc.Citation.base,
                          "Karpathy 2025")),
        ("Citation.source", "base + large + center",
         lambda: st_write(sc.Citation.source,
                          "— METR (2025), arXiv:2507.09089")),
    ])
    st_space("v", 3)

    # ── 10. Callouts ─────────────────────────────────────────────────────
    _section_header(
        "10. Callouts — framed container variants",
        "Four variants of the `ptn_callout` container. Each = "
        "background tint + 4 px coloured left border + medium "
        "padding. Pair with the matching `Keywords.*` for the inline "
        "label inside.",
    )

    def _callout(container_style, label_kw, label, body):
        with st_block(container_style):
            st_write(s.large, (label_kw, label))
            st_space("v", 0.3)
            st_write(s.large, body)

    _showcase([
        ("Callouts.info",     "info_bg + 4px primary border + md pad",
         lambda: _callout(sc.Callouts.info,     sc.Keywords.primary,
                          "Knowledge Capitalization",
                          "Each cycle compounds prior learnings.")),
        ("Callouts.warning",  "warning_bg + 4px highlight border + md pad",
         lambda: _callout(sc.Callouts.warning,  sc.Keywords.warn,
                          "AI productivity paradox",
                          "Senior devs felt 20% faster, measured 19% slower.")),
        ("Callouts.critical", "critical_bg + 4px critical border + md pad",
         lambda: _callout(sc.Callouts.critical, sc.Keywords.critical,
                          "Do not skip the source",
                          "Evidence without citation undermines credibility.")),
        ("Callouts.success",  "success_bg + 4px success border + md pad",
         lambda: _callout(sc.Callouts.success,  sc.Keywords.success,
                          "Pattern installed",
                          "Run `stx patterns install --preset slides`.")),
    ])
    st_space("v", 3)

    # ── 11. CellTints ────────────────────────────────────────────────────
    _section_header(
        "11. CellTints — coloured cell backgrounds",
        "Three tints for grid cells, semantically encoded: "
        "**primary** = neutral / existing, **accent** = novelty / "
        "AI-native, **active** = current focus / you are here. Used "
        "by `ptn_categorized_grid` and its timeline variant.",
    )

    def _tint_box(tint_style, label):
        with st_block(tint_style
                      + s.container.paddings.small_padding
                      + s.center_txt):
            st_write(s.large, label)

    _showcase([
        ("CellTints.primary", "rgba primary + 1px border + radius 10",
         lambda: _tint_box(sc.CellTints.primary, "Existing item")),
        ("CellTints.accent",  "rgba accent + 1px border + radius 10",
         lambda: _tint_box(sc.CellTints.accent,  "AI-native item")),
        ("CellTints.active",  "rgba active + 2px highlight border",
         lambda: _tint_box(sc.CellTints.active,  "You are here")),
    ])
    st_space("v", 3)

    # ── 12. Cells ────────────────────────────────────────────────────────
    _section_header(
        "12. Cells — bordered / centered / table / card containers",
        "Container styles for `st_grid(cell_styles=…)`. Covers the 4 "
        "most common cell shapes plus 3 card variants pre-composed "
        "with the CellTints palette.",
    )

    def _cell(cell_style, label):
        with st_block(cell_style):
            st_write(s.large, label)

    _showcase([
        ("Cells.bordered",          "solid + small pad + v-center",
         lambda: _cell(sc.Cells.bordered,          "Plain bordered")),
        ("Cells.bordered_centered", "bordered + center_txt",
         lambda: _cell(sc.Cells.bordered_centered, "Bordered + centered")),
        ("Cells.centered",          "v-center + center_txt",
         lambda: _cell(sc.Cells.centered,          "Just centered")),
        ("Cells.table_header_cell", "accent tint + sm pad + center",
         lambda: _cell(sc.Cells.table_header_cell, "Day")),
        ("Cells.table_normal_cell", "primary tint + sm pad + center",
         lambda: _cell(sc.Cells.table_normal_cell, "Morning")),
        ("Cells.table_active_cell", "active tint + sm pad + center",
         lambda: _cell(sc.Cells.table_active_cell, "Today")),
        ("Cells.card_primary",      "primary tint + md pad + center",
         lambda: _cell(sc.Cells.card_primary,      "AgileGen")),
        ("Cells.card_accent",       "accent tint + md pad + center",
         lambda: _cell(sc.Cells.card_accent,       "SE 3.0")),
        ("Cells.card_active",       "active tint + md pad + center",
         lambda: _cell(sc.Cells.card_active,       "GSE-One")),
    ])
    st_space("v", 3)

    # ── 13. PageFill ─────────────────────────────────────────────────────
    _section_header(
        "13. PageFill — viewport-filling page layouts",
        "Page-level flex containers (min-height ≈ 85 vh) that ensure "
        "slides fill the projector vertically. The live render is a "
        "schematic, not actual 85 vh.",
    )

    def _layout_diagram(label, content_align):
        with st_block(
            s.container.borders.solid_border
            + Style(
                "min-height: 80px; display: flex; "
                f"flex-direction: column; justify-content: {content_align}; "
                "align-items: center; padding: 6px;",
                f"layout_diag_{content_align}",
            )
        ):
            st_write(s.medium + s.center_txt + s.italic,
                     f"[{label}]")

    _showcase([
        ("PageFill.top",            "flex col + justify-flex-start",
         lambda: _layout_diagram("content at top", "flex-start")),
        ("PageFill.center",         "flex col + justify-center + align-center",
         lambda: _layout_diagram("content centered", "center")),
        ("PageFill.center_wide",    "center + gap 2rem",
         lambda: _layout_diagram("center, wide gap", "center")),
        ("PageFill.center_noalign", "center vertical only",
         lambda: _layout_diagram("center vert, no align", "center")),
    ])
    st_space("v", 3)

    # ── 14. Grid ─────────────────────────────────────────────────────────
    _section_header(
        "14. Grid — column templates and gap presets",
        "`cols` presets are plain strings (use in `st_grid(cols=…)`). "
        "`gap_*` presets are Style instances composable into "
        "`cell_styles`.",
    )

    def _mini_grid(cols_str):
        with st_grid(cols=cols_str, gap="4px",
                     cell_styles=bs.sample_box) as g:
            for i in range(3 if "auto-fit" not in cols_str else 4):
                with g.cell():
                    st_write(s.medium + s.center_txt, f"cell {i+1}")

    def _gap_demo(gap_style):
        with st_grid(cols="1fr 1fr 1fr", gap=None,
                     cell_styles=gap_style + bs.sample_box) as g:
            for i in range(3):
                with g.cell():
                    st_write(s.medium + s.center_txt, "·")

    _showcase([
        ("Grid.responsive_2col",   "repeat(auto-fit, minmax(350px, 1fr))",
         lambda: _mini_grid(sc.Grid.responsive_2col)),
        ("Grid.responsive_3col",   "repeat(auto-fit, minmax(280px, 1fr))",
         lambda: _mini_grid(sc.Grid.responsive_3col)),
        ("Grid.responsive_4col",   "repeat(auto-fit, minmax(220px, 1fr))",
         lambda: _mini_grid(sc.Grid.responsive_4col)),
        ("Grid.title_with_tooltip", "\"95% 5%\"",
         lambda: _mini_grid(sc.Grid.title_with_tooltip)),
        ("Grid.image_text_split",  "\"1fr 2fr\"",
         lambda: _mini_grid(sc.Grid.image_text_split)),
        ("Grid.morning_afternoon", "\"1fr 1fr\"",
         lambda: _mini_grid(sc.Grid.morning_afternoon)),
        ("Grid.three_equal",       "\"1fr 1fr 1fr\"",
         lambda: _mini_grid(sc.Grid.three_equal)),
        ("Grid.gap_8",  "gap: 8px",  lambda: _gap_demo(sc.Grid.gap_8)),
        ("Grid.gap_24", "gap: 24px", lambda: _gap_demo(sc.Grid.gap_24)),
    ])
    st_space("v", 3)

    # ── 15. DocPage ──────────────────────────────────────────────────────
    _section_header(
        "15. DocPage — documentation-manual styles",
        "Manual-specific styles for `docs/` patterns: monospace API "
        "headings, muted descriptions, file labels, walkthrough step "
        "labels, CLI command titles.",
    )

    _showcase([
        ("DocPage.mono_heading",      "Large + bold + monospace + violet",
         lambda: st_write(sc.DocPage.mono_heading,
                          "st_grid(cols, gap, cell_styles)", tag=t.div)),
        ("DocPage.description_muted", "large + italic + muted",
         lambda: st_write(sc.DocPage.description_muted,
                          "Lay out content in a CSS grid container.")),
        ("DocPage.file_label",        "medium + italic + muted",
         lambda: st_write(sc.DocPage.file_label,
                          "bck_intro.py")),
        ("DocPage.step_label",        "violet + bold + large",
         lambda: st_write(sc.DocPage.step_label,
                          "Step 1.")),
        ("DocPage.cmd_title",         "violet + bold + Large",
         lambda: st_write(sc.DocPage.cmd_title,
                          "$ stx patterns install")),
    ])
    st_space("v", 3)

    # ── 16. make_banner_header() helper ──────────────────────────────────
    _section_header(
        "16. make_banner_header(color_from, color_to) — helper",
        "Parametric gradient header replacing the 9 ad-hoc bandeaux "
        "observed in the audit. Returns a Style that can wrap any "
        "container.",
    )

    def _banner(color_from, color_to, title):
        with st_block(sc.make_banner_header(color_from, color_to)):
            st_write(
                s.huge + s.bold + s.center_txt
                + Style("color: white;", "banner_white_txt"),
                title,
                tag=t.div,
            )

    _showcase([
        ("make_banner_header('#7AB8F5', '#a78bfa')",
         "blue → violet",
         lambda: _banner("#7AB8F5", "#a78bfa", "Module 1")),
        ("make_banner_header('#2EC4B6', '#F39C12')",
         "teal → amber",
         lambda: _banner("#2EC4B6", "#F39C12", "Module 2")),
        ("make_banner_header('#a78bfa', '#E74C3C')",
         "violet → red",
         lambda: _banner("#a78bfa", "#E74C3C", "Critical section")),
    ])
    st_space("v", 3)

    # ── Closing ──────────────────────────────────────────────────────────
    show_details("""\
        All bundles are aggregated under `Styles.project.<bundle>` for
        drop-in use, or importable individually via
        `from styles_consolidated import <Bundle>`.

        To wire into your project:
        1. Copy `streamtex-patterns/styles/styles_consolidated.py` to
           your project's `custom/styles.py` and edit the palette.
        2. Or subclass `Styles` and override only the colours.
        3. The 16 bundles cover every common need observed across the
           551 blocks audited on 2026-05-11 (ai4se6d + streamtex-docs).
    """)
    st_space("v", 1)


# ----------------------------------------------------------------------------
# Section-header helper (kept at bottom for narrative flow above)
# ----------------------------------------------------------------------------


def _section_header(title: str, explanation: str):
    """Emit a section sub-heading + short explanation paragraph."""
    st_write(bs.sub, title, toc_lvl="+1")
    st_space("v", 1)
    show_explanation(explanation)
    st_space("v", 1)
