"""Report Issues & Feedback — how to get help and report bugs."""

from streamtex import st_write, st_space, st_block, st_list, st_code
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_explanation, st_slide_break


class BlockStyles:
    """Feedback block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    label = s.bold + s.Large
    body = s.large


bs = BlockStyles


def build():
    """Render the Report Issues & Feedback section."""
    st_space("v", 1)
    st_write(bs.heading, "Report Issues & Feedback", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        Found a bug? Have a suggestion? We'd love to hear from you.
        StreamTeX uses GitHub Issues with pre-filled templates to make
        it easy to report problems and request features.
    """)
    st_space("v", 2)

    # --- Bug Reports ---
    st_write(bs.sub, "Bug Reports", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    st_write(
        bs.body,
        "When you encounter an error, open a ",
        (s.bold, "Bug Report"),
        " on GitHub. To help us fix it quickly, please include:",
    )
    st_space("v", 1)

    with st_list(list_type="ol") as l:
        with l.item(): st_write(bs.body, "The ", (s.bold, "full error traceback"), " (copy-paste from the terminal)")
        with l.item(): st_write(bs.body, "The ", (s.bold, "command you ran"), " (e.g. stx project new, /stx-designer:init, stx run)")
        with l.item(): st_write(bs.body, "Your ", (s.bold, "StreamTeX version"))
    st_space("v", 1)

    st_write(bs.body, "Get your version with:")
    st_space("v", 1)
    st_code(code="uv pip show streamtex | grep Version", language="bash")
    st_space("v", 2)

    # --- Feature Requests ---
    st_write(bs.sub, "Feature Requests", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    st_write(
        bs.body,
        "Have an idea for a new feature? Open a ",
        (s.bold, "Feature Request"),
        " on GitHub. Describe the problem you're trying to solve "
        "and how you'd like the feature to work.",
    )
    st_space("v", 2)

    # --- Links ---
    st_write(bs.sub, "Links", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_block(s.project.containers.good_callout):
        st_write(bs.label, "Where to go", tag=t.div)
        st_space("v", 1)
        with st_list(list_type="ul") as l:
            with l.item(): st_write(bs.body, (s.bold, "Bug report"), " — github.com/nicolasguelfi/streamtex/issues (select Bug Report template)")
            with l.item(): st_write(bs.body, (s.bold, "Feature request"), " — github.com/nicolasguelfi/streamtex/issues (select Feature Request template)")
            with l.item(): st_write(bs.body, (s.bold, "Questions & discussions"), " — github.com/nicolasguelfi/streamtex/discussions")
            with l.item(): st_write(bs.body, (s.bold, "Documentation"), " — streamtex.onrender.com")
    st_space("v", 1)

    st_slide_break()
