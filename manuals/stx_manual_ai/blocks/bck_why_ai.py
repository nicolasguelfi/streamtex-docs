"""Why AI? — Comparison of traditional vs AI-assisted workflows."""

import textwrap

from streamtex import st_write, st_space, st_block, st_grid, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_explanation


class BlockStyles:
    """Why AI block styles."""
    heading = s.project.titles.section_title + s.center_txt
    col_title_bad = s.project.colors.error_red + s.bold + s.Large
    col_title_good = s.project.colors.success_green + s.bold + s.Large
    metric_label = s.large
    metric_value_bad = s.project.colors.error_red + s.bold + s.large
    metric_value_good = s.project.colors.success_green + s.bold + s.large


bs = BlockStyles


def build():
    """Render the Why AI comparison section."""
    st_space("v", 1)
    st_write(bs.heading, "Why AI-Powered Workflows?",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── Side-by-side comparison ───────────────────────────────────
    with st_grid(cols=2) as g:
        # Left: Traditional
        with g.cell():
            with st_block(s.project.containers.bad_callout):
                st_write(bs.col_title_bad, "Code-First (Traditional)",
                         tag=t.div)
                st_space("v", 1)
                with st_list(list_type="ul"):
                    st_write(
                        s.large,
                        (s.bold, "20+ minutes "),
                        "per styled block",
                    )
                    st_write(
                        s.large,
                        (s.bold, "Manual styling "),
                        "— write CSS by hand",
                    )
                    st_write(
                        s.large,
                        (s.bold, "Trial-and-error "),
                        "— tweak, reload, repeat",
                    )
                    st_write(
                        s.large,
                        (s.bold, "Must know the API "),
                        "— every function, every parameter",
                    )

        # Right: AI-Assisted
        with g.cell():
            with st_block(s.project.containers.good_callout):
                st_write(bs.col_title_good, "AI-Assisted (StreamTeX)",
                         tag=t.div)
                st_space("v", 1)
                with st_list(list_type="ul"):
                    st_write(
                        s.large,
                        (s.bold, "~3 minutes "),
                        "per styled block",
                    )
                    st_write(
                        s.large,
                        (s.bold, "Describe what you want "),
                        "— AI picks styles",
                    )
                    st_write(
                        s.large,
                        (s.bold, "Auto-styling "),
                        "— consistent, standards-compliant",
                    )
                    st_write(
                        s.large,
                        (s.bold, "Zero Python needed "),
                        "— natural language input",
                    )
    st_space("v", 2)

    # ── Clarification callout ─────────────────────────────────────
    show_explanation(textwrap.dedent("""\
        AI does not replace understanding — it accelerates creation.
        You still control the final output: review every generated
        block, adjust styles, and decide what ships. The AI handles
        the repetitive scaffolding so you can focus on content and
        design decisions.
    """))
    st_space("v", 1)
