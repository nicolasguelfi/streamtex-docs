"""Report Issues & Feedback — how to get help and report bugs.

Covers both manual GitHub issue creation and AI-assisted
issue filing via /stx-issue:* Claude commands.
"""

from streamtex import st_write, st_space, st_block, st_grid, st_list, st_code
import streamtex as stx
from streamtex.styles import Style
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_explanation, show_code, st_slide_break


class BlockStyles:
    """Feedback block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    label = s.bold + s.Large
    body = s.large
    cmd_card = Style(
        "background: rgba(142, 68, 223, 0.06); "
        "border-left: 3px solid #8E44DF; "
        "padding: 16px 20px; border-radius: 0 6px 6px 0;",
        "feedback_cmd_card"
    )
    cmd_name = Style(
        "color: #8E44DF; font-weight: bold;", "feedback_cmd_name"
    ) + s.large
    cmd_desc = s.medium


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

        You can create issues **manually on GitHub** or use
        the **Claude AI commands** described below to file them
        directly from your editor.
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

    # --- Claude AI commands ---
    st_write(bs.sub, "File issues with Claude AI", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    st_write(
        bs.body,
        "If you use Claude Code, you can file GitHub issues "
        "directly from your editor with the ",
        (s.bold, "/stx-issue"),
        " commands. Environment metadata (OS, Python version, "
        "StreamTeX version) is collected automatically.",
    )
    st_space("v", 1)

    with st_grid(
        cols="repeat(auto-fit, minmax(280px, 1fr))",
        grid_style=stx.StxStyles.container.grid.gap_24,
    ):
        _cmd_card(
            "/stx-issue:bug",
            "Report a bug with auto-collected environment info. "
            "Describe the problem and Claude creates the GitHub issue.",
        )
        _cmd_card(
            "/stx-issue:feature",
            "Request a new feature. Describe the use case and "
            "Claude opens a structured feature request.",
        )
        _cmd_card(
            "/stx-issue:question",
            "Ask a question about StreamTeX. Claude creates a "
            "GitHub issue with the question template.",
        )
        _cmd_card(
            "/stx-issue:docs",
            "Suggest a documentation improvement. Point out "
            "what is missing or unclear.",
        )
        _cmd_card(
            "/stx-issue:comment",
            "Add a comment to an existing issue. "
            "Provide the issue number and your message.",
        )
        _cmd_card(
            "/stx-issue:list",
            "List open issues for the repository. "
            "Filter by label or status.",
        )

    st_space("v", 2)

    # --- Example usage ---
    st_write(
        s.project.titles.subsection_title,
        "Example: reporting a bug with Claude",
        toc_lvl="+1",
    )
    st_space("v", 1)

    st_write(
        bs.body,
        "In Claude Code, simply type the command followed by "
        "a description of your problem:",
    )
    st_space("v", 1)

    show_code("""\
/stx-issue:bug

st_grid throws a KeyError when using breakpoint="600px"
with more than 4 columns. The error happens in grid.py
line 142. Expected: columns should wrap below the
breakpoint. Actual: crash with KeyError on "grid_cols".
""", language="text", line_numbers=False)
    st_space("v", 1)

    show_explanation("""\
        Claude will automatically add your **OS**, **Python version**,
        **StreamTeX version**, and **uv version** to the issue.
        It creates a properly formatted GitHub issue with the
        bug report template — no need to fill in forms manually.
    """)
    st_space("v", 1)

    st_write(
        bs.body,
        "Other examples:",
    )
    st_space("v", 0.5)

    show_code("""\
# Request a feature
/stx-issue:feature I'd like st_write to support markdown tables natively

# Ask a question
/stx-issue:question How do I configure PDF margins for A3 format?

# Improve documentation
/stx-issue:docs The export section is missing an example for PDF with custom headers

# Comment on an existing issue
/stx-issue:comment 42 I can confirm this bug also happens on macOS 15.3

# List open issues
/stx-issue:list
""", language="text", line_numbers=False)
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


# ── Helpers ────────────────────────────────────────────────────────

def _cmd_card(name: str, description: str):
    """Claude command card."""
    with st_block(bs.cmd_card):
        st_write(bs.cmd_name, name)
        st_space("v", 0.3)
        st_write(bs.cmd_desc, description)
