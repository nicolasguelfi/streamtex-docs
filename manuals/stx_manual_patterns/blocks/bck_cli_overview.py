"""`stx patterns` CLI reference — install / update / promote.

# @pattern: api_reference_card
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation


class BlockStyles:
    """CLI reference styles."""
    heading = (
        s.project.titles.section_title
        + s.text.fonts.font_monospace
        + s.center_txt
    )
    lead = s.project.titles.body + s.center_txt
    sub = s.project.titles.section_subtitle
    keyword = s.bold + s.project.colors.primary_violet
    accent = s.bold + s.project.colors.accent_teal
    body = s.project.titles.body
    cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.container.layouts.vertical_center_layout
    )


bs = BlockStyles


# Subcommands of `stx patterns`
SUBCOMMANDS = [
    ("install",  "--preset NAME | --pattern A,B,...",
     "Copy patterns from the source catalog into the project."),
    ("update",   "(no args)",
     "Refresh installed patterns; uses drift detection."),
    ("status",   "(no args)",
     "List installed patterns with their SHA + drift state."),
    ("promote",  "<pattern>",
     "Push a locally-edited pattern back to the source catalog."),
    ("reindex",  "(no args)",
     "Regenerate `_pattern_library.md` and per-project indexes."),
    ("diff",     "<pattern>",
     "Show local-vs-source diff for a single pattern."),
]

RELATED = ["stx claude update", "stx project init", "stx project upgrade"]


def build():
    """Reference card for the top-level `stx patterns` CLI."""
    with st_block(s.center_txt):
        st_write(bs.heading,
                 "stx patterns <subcommand> [options]",
                 tag=t.div, toc_lvl="1")
        st_space("v", 1)
        st_write(bs.lead,
                 "Manage the StreamTeX pattern catalog inside a project "
                 "(install, update, status, promote).")
        st_space("v", 2)

        # ---- Subcommands ----
        st_write(bs.sub, "Subcommands", toc_lvl="+1")
        st_space("v", 0.5)
        with st_grid(cols="1fr 2fr 3fr", gap="8px") as g:
            with g.cell(bs.cell):
                st_write(bs.body, (bs.keyword, "name"))
            with g.cell(bs.cell):
                st_write(bs.body, (bs.accent, "options"))
            with g.cell(bs.cell):
                st_write(bs.body, (s.bold, "description"))
            for name, opts, doc in SUBCOMMANDS:
                with g.cell(bs.cell):
                    st_write(bs.body, (bs.keyword, name))
                with g.cell(bs.cell):
                    st_write(bs.body, (bs.accent, opts))
                with g.cell(bs.cell):
                    st_write(bs.body, doc)
        st_space("v", 2)

        # ---- Common flags ----
        st_write(bs.sub, "Common flags", toc_lvl="+1")
        st_space("v", 0.5)
        with st_grid(cols="1fr 1fr 3fr", gap="8px") as g:
            with g.cell(bs.cell):
                st_write(bs.body, (bs.keyword, "--source"))
            with g.cell(bs.cell):
                st_write(bs.body, (bs.accent, "PATH"))
            with g.cell(bs.cell):
                st_write(bs.body,
                         "Override the pattern source path (top of "
                         "the resolution cascade).")
            with g.cell(bs.cell):
                st_write(bs.body, (bs.keyword, "--mode"))
            with g.cell(bs.cell):
                st_write(bs.body, (bs.accent, "copy | symlink"))
            with g.cell(bs.cell):
                st_write(bs.body,
                         "Install mode. `symlink` is for pattern authors "
                         "iterating live; `copy` (default) is for "
                         "consumer projects.")
            with g.cell(bs.cell):
                st_write(bs.body, (bs.keyword, "--force"))
            with g.cell(bs.cell):
                st_write(bs.body, (bs.accent, "(flag)"))
            with g.cell(bs.cell):
                st_write(bs.body,
                         "Override drift refusals. Use with caution.")
            with g.cell(bs.cell):
                st_write(bs.body, (bs.keyword, "--dry-run"))
            with g.cell(bs.cell):
                st_write(bs.body, (bs.accent, "(flag)"))
            with g.cell(bs.cell):
                st_write(bs.body,
                         "Print actions without writing files. Useful "
                         "before an update on a busy project.")
        st_space("v", 2)

        # ---- Returns / exit codes ----
        st_write(bs.sub, "Exit codes", toc_lvl="+1")
        st_space("v", 0.5)
        st_write(bs.body, "0 = success, "
                          "1 = generic error, "
                          "2 = drift refused (run `stx patterns diff` "
                          "or use `--force`).")
        st_space("v", 2)

        # ---- Examples ----
        st_write(bs.sub, "Examples", toc_lvl="+1")
        st_space("v", 0.5)
        show_explanation("""\
            Typical session — install the docs preset, audit, then
            update later.
        """)
        st_space("v", 0.5)
        show_code("""\
# Install patterns for a manual project
stx patterns install --preset docs

# See what's installed and whether anything drifted
stx patterns status

# Refresh against upstream
stx patterns update

# I edited callout.md locally and want to share it
stx patterns promote callout
""", language="bash")
        st_space("v", 2)

        # ---- See also ----
        st_write(bs.sub, "See also", toc_lvl="+1")
        st_space("v", 0.5)
        st_write(bs.body, (bs.keyword, "Related commands: "),
                 ", ".join(RELATED))
        st_space("v", 1)
