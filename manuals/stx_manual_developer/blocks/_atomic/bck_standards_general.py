"""Atomic block — General coding standards."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """General coding standards styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Coding Standards", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            These coding standards apply to all StreamTeX source code,
            block files, and documentation projects. Following them
            ensures consistency, theme compatibility, and correct
            export behaviour across the entire ecosystem.
        """)
        st_space("v", 2)

        # --- stx vs st ---
        st_write(bs.sub, "stx vs st: when to use which", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Use StreamTeX functions (st_write, st_block, st_grid, st_list,
            st_code, st_image, etc.) for all content rendering. Only use
            raw Streamlit calls (st.button, st.selectbox, st.slider,
            st.text_input) for interactive widgets that StreamTeX does
            not wrap.
        """)
        st_space("v", 1)

        show_code("""\
            # CORRECT — StreamTeX for content
            st_write(style, "Hello, world!")
            with st_block(container_style):
                st_write(style, "Inside a styled block")

            # CORRECT — raw st for interactivity
            if st.button("Click me"):
                st.toast("Clicked!")

            # WRONG — never use st.write or st.markdown for content
            st.write("Don't do this")
            st.markdown("Or this")\
        """, language="python")
        st_space("v", 2)

        # --- No raw HTML/CSS ---
        st_write(bs.sub, "No raw HTML or CSS", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Never write raw HTML or inline CSS strings. Always use
            the Style composition system. Styles are built from the
            Style constructor, composed with + and -, and applied
            through StreamTeX rendering functions.
        """)
        st_space("v", 1)

        show_code("""\
            # CORRECT — Style composition
            bold_blue = Style("font-weight: bold; color: #3366cc;", "bold_blue")
            st_write(bold_blue, "Styled text")

            # WRONG — raw HTML
            st.html('<span style="font-weight:bold;color:#3366cc;">text</span>')\
        """, language="python")
        st_space("v", 2)

        # --- No hardcoded black/white ---
        st_write(bs.sub, "No hardcoded black or white", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Never hardcode color: black, color: white, background: #000,
            or background: #fff. Streamlit handles light/dark themes
            automatically. Hardcoded values break theme switching.
            Use semantic colours from your project styles instead.
        """)
        st_space("v", 2)

        # --- Naming conventions ---
        st_write(bs.sub, "Naming conventions", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Element")
            with g.cell(): st_write(s.bold + s.large, "Convention")
            with g.cell(): st_write(s.large, "Files")
            with g.cell(): st_write(s.large, "snake_case (e.g. my_module.py)")
            with g.cell(): st_write(s.large, "Block files")
            with g.cell(): st_write(s.large, "Prefix with bck_ (e.g. bck_intro.py)")
            with g.cell(): st_write(s.large, "Style names")
            with g.cell(): st_write(s.large, "Descriptive (e.g. section_title, code_box)")
            with g.cell(): st_write(s.large, "Classes")
            with g.cell(): st_write(s.large, "PascalCase (e.g. BlockStyles)")
            with g.cell(): st_write(s.large, "Functions")
            with g.cell(): st_write(s.large, "snake_case (e.g. build, _render)")
        st_space("v", 2)

        # --- Block architecture ---
        st_write(bs.sub, "Block architecture", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Every block file must define a BlockStyles class and a
            build() function. The BlockStyles class holds all styles
            used by the block. The build() function renders the content.
            Create a shorthand bs = BlockStyles for concise access.
        """)
        st_space("v", 1)

        show_code("""\
            class BlockStyles:
                heading = s.project.titles.section_title + s.center_txt
                sub = s.project.titles.section_subtitle

            bs = BlockStyles

            def build():
                st_write(bs.heading, "My Section", tag=t.div, toc_lvl="1")
                st_write(bs.sub, "Subsection", toc_lvl="+1")\
        """, language="python")
        st_space("v", 2)

        # --- Style reuse ---
        st_write(bs.sub, "Style reuse", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Define a style once and reuse it everywhere. Place
            project-wide styles in custom/styles.py. Place block-local
            styles in the BlockStyles class. Never duplicate CSS strings
            across multiple locations.
        """)
        st_space("v", 2)

        # --- One st_write for inline text ---
        st_write(bs.sub, "One st_write with tuples for mixed-style text",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            To render inline text with mixed styles, pass a tuple of
            (style, text) pairs to a single st_write() call. Multiple
            st_write() calls stack vertically as separate blocks.
        """)
        st_space("v", 1)

        show_code("""\
            # CORRECT — single call, inline mix
            st_write(base_style, (bold, "Name: "), (normal, "StreamTeX"))

            # WRONG — two calls create two blocks
            st_write(bold, "Name: ")
            st_write(normal, "StreamTeX")\
        """, language="python")
        st_space("v", 2)

        # --- Lint after every change ---
        st_write(bs.sub, "Lint after every change", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            After every code change, run the linter before committing.
            This catches import errors, unused variables, and style
            violations early.
        """)
        st_space("v", 1)

        show_code("uv run ruff check", language="bash")
        st_space("v", 2)

        # --- Export-aware functions ---
        st_write(bs.sub, "Export-aware functions", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            StreamTeX wraps several Streamlit functions to support
            HTML export. Always use the stx-prefixed version so that
            content is captured during export.
        """)
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Use this")
            with g.cell(): st_write(s.bold + s.large, "Instead of")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx.st_dataframe()")
            with g.cell(): st_write(s.large, "st.dataframe()")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "st_write()")
            with g.cell(): st_write(s.large, "st.write()")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "st_code()")
            with g.cell(): st_write(s.large, "st.code()")
        st_space("v", 2)

        show_details("""\
            The full coding standards reference lives in
            .claude/references/coding_standards.md inside the
            streamtex-docs repository. When in doubt, consult that
            file — it is the single source of truth.
        """)
