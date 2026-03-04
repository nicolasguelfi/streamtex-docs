"""Command: project-customize — Modify theme, colors, and navigation."""

from streamtex import st_write, st_space, st_block, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """project-customize block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    step_label = s.project.colors.ai_violet + s.bold + s.large


bs = BlockStyles


def build():
    """Render the project-customize command documentation."""
    st_space("v", 1)
    st_write(bs.heading, "Command: project-customize",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── Purpose ────────────────────────────────────────────────────
    show_explanation("""\
        /project:project-customize modifies the visual identity of an
        existing StreamTeX project. It can change color palettes, fonts,
        navigation style, and layout — all from a single natural
        language prompt. It reads the current styles, applies your
        changes, and preserves everything else.
    """)
    st_space("v", 2)

    # ── Example prompts ────────────────────────────────────────────
    st_write(bs.sub, "Example Prompts", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_block(s.project.containers.ai_callout):
        with st_list(list_type="ul") as l:
            with l.item():
                st_write(
                    s.large,
                    (s.bold, '"Change the color palette to an ocean theme"'),
                )
            with l.item():
                st_write(
                    s.large,
                    (s.bold, '"Add dark mode support with a toggle"'),
                )
            with l.item():
                st_write(
                    s.large,
                    (s.bold, '"Switch navigation from paginated to continuous"'),
                )
            with l.item():
                st_write(
                    s.large,
                    (s.bold, '"Use Inter font and increase heading sizes"'),
                )
    st_space("v", 2)

    # ── What it modifies ───────────────────────────────────────────
    st_write(bs.sub, "Files Modified", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    st_write(
        s.large,
        "The command targets three files, depending on the request:",
    )
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item():
            st_write(
                s.large,
                (s.bold, "custom/styles.py "),
                "— color classes, text styles, container styles",
            )
        with l.item():
            st_write(
                s.large,
                (s.bold, "custom/themes.py "),
                "— theme definitions and dark/light variants",
            )
        with l.item():
            st_write(
                s.large,
                (s.bold, ".streamlit/config.toml "),
                "— Streamlit theme colors, font, layout",
            )
    st_space("v", 2)

    # ── Step-by-step demo ──────────────────────────────────────────
    st_write(bs.sub, "Step-by-Step Demo", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    # Step 1
    with st_block(s.project.containers.tip_callout):
        st_write(bs.step_label, "Step 1 — Launch the command", tag=t.div)
        st_space("v", 1)
        show_code(
            "/project:project-customize",
            language="bash", line_numbers=False,
        )

    st_space("v", 1)

    # Step 2
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.step_label,
            "Step 2 — Describe the customization",
            tag=t.div,
        )
        st_space("v", 1)
        show_code("""\
            > Change to an ocean theme: deep navy backgrounds,
              teal accents, white text. Keep the current layout.""",
            language="bash", line_numbers=False)

    st_space("v", 1)

    # Step 3
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.step_label,
            "Step 3 — Review the changes",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            "The AI shows a diff of modified files before applying:",
        )
    st_space("v", 1)

    show_code("""\
        # custom/styles.py — before
        ai_violet = Style("color: #8B5CF6;", "ai_violet")

        # custom/styles.py — after
        ocean_navy = Style("color: #1E3A5F;", "ocean_navy")
        ocean_teal = Style("color: #14B8A6;", "ocean_teal")""",
        language="python")
    st_space("v", 2)

    # ── Tip ────────────────────────────────────────────────────────
    show_details("""\
        Tip: customize incrementally. Change one aspect at a time —
        colors first, then fonts, then layout. This makes it easy to
        revert if something does not look right, and gives the AI
        a focused task for each iteration.
    """)
    st_space("v", 1)
