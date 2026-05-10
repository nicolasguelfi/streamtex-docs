"""Gallery — callout pattern variants (info / warning / critical / success).

# @pattern: manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation


class BlockStyles:
    """Callouts gallery styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    body_c = s.large + s.center_txt
    keyword = s.bold + s.project.colors.primary_violet
    accent = s.bold + s.project.colors.accent_teal
    highlight = s.bold + s.project.colors.highlight_amber
    critical = s.bold + s.project.colors.warning_red
    success = s.bold + s.project.colors.success_green


bs = BlockStyles


def build():
    """Render the four callout variants with live demos."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Callouts Gallery — info / warning / critical / success",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    show_explanation("""\
        The `callout` pattern is a small framed container that lifts
        a piece of content out of the surrounding flow. The variant
        is encoded by the **inline label color**, never by a custom
        container — this keeps visual rhythm uniform across slides.
        About **68 occurrences** in the `ai4se6d` corpus.
    """)
    st_space("v", 2)

    show_code("""\
class BlockStyles:
    body_c = s.Large + s.center_txt + s.text.wrap.hyphens
    accent = s.bold + s.project.colors.accent      # info
    highlight = s.bold + s.project.colors.highlight  # warning
    critical = s.bold + s.project.colors.critical  # critical
    success = s.bold + s.project.colors.success    # success

with st_block(s.project.containers.callout):
    st_write(bs.<variant>, "<Label>")
    st_space("v", 0.5)
    st_write(bs.body_c, "<Body line>")""")
    st_space("v", 2)

    # ---- info variant ----
    st_write(bs.sub, "info — neutral emphasis / definition", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.tip_callout):
        st_write(bs.accent, "Knowledge Capitalization")
        st_space("v", 0.5)
        st_write(bs.body_c,
                 "Practice of preserving methodology learnings across "
                 "projects, so each cycle compounds prior knowledge.")
    st_space("v", 2)

    # ---- warning variant ----
    st_write(bs.sub, "warning — risk / caveat / paradox", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.note_callout):
        st_write(bs.highlight, "AI productivity paradox")
        st_space("v", 0.5)
        st_write(bs.body_c,
                 "Senior developers using AI assistants felt 20% faster "
                 "while measurements showed they were 19% slower.")
    st_space("v", 2)

    # ---- critical variant ----
    st_write(bs.sub, "critical — hard warning", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.bad_callout):
        st_write(bs.critical, "Do not skip the source")
        st_space("v", 0.5)
        st_write(bs.body_c,
                 "An evidence_insight slide without a citation undermines "
                 "credibility and breaks the pattern's contract.")
    st_space("v", 2)

    # ---- success variant ----
    st_write(bs.sub, "success — confirmation / win", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.good_callout):
        st_write(bs.success, "Pattern installed")
        st_space("v", 0.5)
        st_write(bs.body_c,
                 "`stx patterns install --preset slides` brings 7 core "
                 "atoms and 5 templates into your project.")
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "core/callout.md"),
             (bs.accent, " for full details — INVARIANTS, PARAMS, INTERDITS."))
    st_space("v", 1)
