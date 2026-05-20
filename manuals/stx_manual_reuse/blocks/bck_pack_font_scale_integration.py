"""Pack font-scale integration — rules for pack authors (0.7.5+).

Explains how a pack design system must reference the indexed responsive
scale in its style declarations, with before/after examples taken from
the streamtex-design 0.2.2 migration.
"""

from streamtex import st_block, st_code, st_grid, st_space, st_write
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem
from streamtex_design.components.callout import callout


DS = DesignSystem()


class BlockStyles:
    """Pack font-scale integration block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    code_box = Style(
        "background-color: rgba(167, 139, 250, 0.06); "
        "border: 1px solid rgba(167, 139, 250, 0.25); "
        "border-radius: 6px; padding: 10px;",
        "pfs_code_box",
    )
    side = Style(
        "background: rgba(149, 165, 166, 0.06); "
        "padding: 12px 14px; border-radius: 6px; height: 100%;",
        "pfs_side",
    )


bs = BlockStyles


def build():
    """Pack design systems must reference the indexed scale."""
    st_write((bs.heading, "Pack font-scale integration"),
             toc_lvl="1", tag=t.div)
    st_space(10)

    # ── 1. Lead callout ───────────────────────────────────────────────
    callout(
        design_system=DS,
        variant="info",
        title="Consuming the indexed scale from a pack",
        body=(
            "Since streamtex 0.7.5, every pack design system can — and "
            "should — reference the indexed responsive scale instead of "
            "hardcoded px or pt values. Consumers of the pack then inherit "
            "responsive behaviour for free, and per-document overrides "
            "(st_book(scale=...)) flow through automatically."
        ),
    )
    st_space(20)

    # ── 2. The rule ───────────────────────────────────────────────────
    st_write((bs.sub, "The rule"), toc_lvl="+1", tag=t.div)
    st_space(10)

    callout(
        design_system=DS,
        variant="warn",
        title="PD001 — Indexed scale references mandatory in pack styles",
        body=(
            "Pack design systems MUST use indexed scale references in "
            "font-size declarations — never hardcoded px. Use "
            "var(--stx-scale-K, fallback_pt) where K is the palier index. "
            "Sub-rule: fallback pt values should match the WORD_PROCESSOR "
            "curve desktop value at the chosen palier (default base = 18, "
            "anchored at palier 7) — when the streamtex package is "
            "missing, the fallback ensures graceful degradation at the "
            "right size."
        ),
    )
    st_space(20)

    # ── 3. Before / After ─────────────────────────────────────────────
    st_write((bs.sub, "Before / After — streamtex-design 0.2.2 migration"),
             toc_lvl="+1", tag=t.div)
    st_space(10)

    st_write(
        s.text_base,
        "The same callout body style, pre-0.2.2 (hardcoded px) and "
        "post-0.2.2 (indexed scale reference):",
        tag=t.div,
    )
    st_space(10)

    with st_grid(cols="1fr 1fr", gap="16px") as g:
        with g.cell():
            with st_block(bs.side):
                st_write(s.text_lg + s.bold + s.project.colors.warning_red,
                         "Before — 0.2.1")
                st_space("v", 0.5)
                with st_block(bs.code_box):
                    st_code(
                        code=(
                            "# streamtex_design/design_systems/default.py\n"
                            "_Callouts.body = Style(\n"
                            '    "font-size: 15px; '
                            'line-height: 1.5;",\n'
                            '    "callouts_body",\n'
                            ")"
                        ),
                        language="python",
                    )
                st_space("v", 0.5)
                st_write(
                    s.text_xs + s.project.colors.neutral_gray,
                    "Frozen at 15px on every breakpoint. Per-document "
                    "overrides have no effect.",
                )

        with g.cell():
            with st_block(bs.side):
                st_write(s.text_lg + s.bold + s.project.colors.success_green,
                         "After — 0.2.2")
                st_space("v", 0.5)
                with st_block(bs.code_box):
                    st_code(
                        code=(
                            "# streamtex_design/design_systems/default.py\n"
                            "_Callouts.body = Style(\n"
                            '    "font-size: '
                            'var(--stx-scale-5, 14pt); '
                            'line-height: 1.5;",\n'
                            '    "callouts_body",\n'
                            ")"
                        ),
                        language="python",
                    )
                st_space("v", 0.5)
                st_write(
                    s.text_xs + s.project.colors.neutral_gray,
                    "Resolves to palier 5 — responsive, override-friendly, "
                    "falls back to 14pt if default.css fails to load.",
                )
    st_space(20)

    # ── 4. The pattern ────────────────────────────────────────────────
    st_write((bs.sub, "The pattern in detail"), toc_lvl="+1", tag=t.div)
    st_space(10)

    st_write(
        s.text_base,
        "Pick the palier index that best matches the role of the text in "
        "the design system, then look up the WORD_PROCESSOR desktop value "
        "at that index for the fallback. The fallback only fires when the "
        "stylesheet has not loaded — it guarantees the pack never renders "
        "as 16px browser-default.",
        tag=t.div,
    )
    st_space(10)

    with st_block(bs.code_box):
        st_code(
            code=(
                "# Recommended palier choices for a generic design system"
                " (default base=18)\n"
                "var(--stx-scale-2,   10pt)   # captions (≈13.3px)\n"
                "var(--stx-scale-5,   14pt)   # small body / annotations"
                " (≈18.7px floor)\n"
                "var(--stx-scale-7,   18pt)   # primary body (= BASE)\n"
                "var(--stx-scale-10,  24pt)   # section title\n"
                "var(--stx-scale-12,  32pt)   # display heading\n"
                "var(--stx-scale-13,  36pt)   # hero\n"
                "var(--stx-scale-16,  60pt)   # giant hero\n"
                "var(--stx-scale-19, 128pt)   # display 1\n"
            ),
            language="css",
        )
    st_space(20)

    # ── 5. Canonical example ──────────────────────────────────────────
    st_write((bs.sub, "Canonical example — streamtex-design 0.2.3"),
             toc_lvl="+1", tag=t.div)
    st_space(10)

    callout(
        design_system=DS,
        variant="info",
        title="Pack migration reference",
        body=(
            "streamtex-design 0.2.3 is the canonical reference for this "
            "migration. Read its design_systems/default.py for the full "
            "before/after across every bundle (callouts, body, comparison_"
            "table, hero, …). Adapt the same palier choices to your own "
            "pack design systems."
        ),
    )

    st_space(20)
