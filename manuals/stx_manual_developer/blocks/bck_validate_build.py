"""Block — stx validate --build, project rules and render snapshots (0.7.36)."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Validate --build block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    table_cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.container.layouts.vertical_center_layout
    )

bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Validating the Real Build", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            An import check only proves that every block module loads.
            A block that raises at run time (a wrong keyword, a bad enum
            member), an image that resolves to nothing (an empty frame,
            no error) or an image inlined as megabytes of base64 all
            pass it. Since streamtex 0.7.36, **stx validate --build**
            runs the real build() of every block of every book.py and
            reports what would reach the screen.
        """)
        st_space("v", 2)

        # --- Running ---
        st_write(bs.sub, "Running the build check", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Run it in the project's own environment, so that the blocks
            import the same packages as the app. Each book.py runs in
            its own subprocess under Streamlit's AppTest (no browser),
            with a checking st_book that sets up the bibliography, the
            TOC and the markers, then calls every block's build() with
            the book's own block_args / block_kwargs.
        """)
        st_space("v", 1)

        show_code("""\
            # Every book.py of the project (root, modules/*, trainings/** ...)
            uv run stx validate --build

            # Only some books (--book is repeatable)
            uv run stx validate --build --book manuals/stx_manual_ai/book.py \\
                                        --book manuals/stx_manual_developer/book.py

            # Seconds allowed per book (default: 180)
            uv run stx validate --build --timeout 300

            # Warnings count as errors (exit 2)
            uv run stx validate --build --strict\
        """, language="bash")
        st_space("v", 2)

        # --- What is reported ---
        st_write(bs.sub, "What is reported", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=3, cell_styles=bs.table_cell) as g:
            with g.cell(): st_write(s.bold + s.large, "Finding")
            with g.cell(): st_write(s.bold + s.large, "Level")
            with g.cell(): st_write(s.bold + s.large, "Why it matters")
            with g.cell(): st_write(s.large, "build() raises an exception")
            with g.cell(): st_write(s.large, "error")
            with g.cell(): st_write(s.large, "The block stops rendering at that line")
            with g.cell(): st_write(s.large, "Image URI that resolves to nothing")
            with g.cell(): st_write(s.large, "warning")
            with g.cell(): st_write(s.large, "An empty frame, with no error in the app")
            with g.cell(): st_write(s.large, "Image inlined as base64 above 512 KB")
            with g.cell(): st_write(s.large, "warning")
            with g.cell(): st_write(s.large, "Serve it: configure_image_path + set_static_sources")
            with g.cell(): st_write(s.large, "Styled st_block with an empty body (static check)")
            with g.cell(): st_write(s.large, "warning")
            with g.cell(): st_write(s.large, "Renders nothing in the app, a box in the export")
        st_space("v", 1)

        show_code("""\
            Build (2 book(s), real build() of every block)
              manuals/stx_manual_ai/book.py: 45 block(s)
                inlined 1131 KB project_blocks.bck_ai_image_overview: images/ai/ai_openai_demo.png — serve it (configure_image_path + set_static_sources)
              manuals/stx_manual_developer/book.py: 15 block(s) OK\
        """, language="text", wrap=True)
        st_space("v", 1)

        show_details("""\
            Exit code: 0 when everything passes, 1 with warnings only,
            2 with at least one error (or with warnings under --strict).
            A book that cannot even be imported is reported as FAIL with
            its exception.
        """)
        st_space("v", 2)

        # --- Project rules ---
        st_write(bs.sub, "Project rules: [[validate.rules]]", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            A convention written in prose is checked by nothing. Declare
            it in stx.toml and stx validate runs it, with or without
            --build. A rule is either a glob plus a forbid regex (every
            match is a violation, reported path:line) or a require regex
            (every file without a match is a violation), or a run
            command (a non-zero exit fails). severity is "error"
            (default) or "warning".
        """)
        st_space("v", 1)

        show_code("""\
            # stx.toml
            [[validate.rules]]
            id = "no-hex"
            message = "no hexadecimal colour in a block — the colour is a role"
            glob = "blocks/**/bck_*.py"
            forbid = '#[0-9a-fA-F]{6}\\b'

            [[validate.rules]]
            id = "has-heading"
            glob = "blocks/bck_*.py"
            require = 'toc_lvl="1"'

            [[validate.rules]]
            run = "uv run python tools/verify.py --all"
            severity = "warning"\
        """, language="toml")
        st_space("v", 1)

        show_explanation("""\
            Each rule is reported under its id. A rule without id is
            shown as rule-<n>, its 1-based position in the file — the
            third rule above appears as rule-3.
        """)
        st_space("v", 1)

        show_code("""\
            Project rules (3)
              no-hex: 2 violation(s) — no hexadecimal colour in a block — the colour is a role
                blocks/bck_intro.py:14
                blocks/bck_intro.py:27
              has-heading: OK
              rule-3: OK\
        """, language="text")
        st_space("v", 2)

        # --- Local copies of public functions ---
        st_write(bs.sub, "Local copies of library functions", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            stx validate also lists, as information only, every
            top-level def st_* of the project that streamtex itself
            exports — typically a local helper kept after the library
            adopted it. It neither fails nor warns: a local copy may be
            a deliberate specialisation, and the author decides.
        """)
        st_space("v", 1)

        show_code("""\
            Library functions defined locally (information)
              i blocks/helpers.py:42 defines st_hover_tooltip, which streamtex provides — keep it if it is a deliberate specialisation\
        """, language="text", wrap=True)
        st_space("v", 2)

        # --- Snapshots ---
        st_write(bs.sub, "Render snapshots: --snapshot and --against",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            For a refactoring pass that must not change what readers
            see, record a fingerprint of the HTML each block emits
            before the change, then compare after it. Base64 media are
            hashed before the fingerprint is taken. Every block that
            renders differently is a warning, listed by book.
        """)
        st_space("v", 1)

        show_code("""\
            # Before the change: write {book: {block: sha256}} to a JSON file
            uv run stx validate --build --snapshot before.json

            # After the change: compare every block with the snapshot
            uv run stx validate --build --against before.json\
        """, language="bash")
        st_space("v", 1)

        show_code("""\
              manuals/stx_manual_ai/book.py: 1 block(s) render differently from the snapshot
                project_blocks.bck_profile_install\
        """, language="text")
        st_space("v", 1)

        with st_block(s.project.containers.warning_callout):
            st_write(s.project.titles.warning_label, "Limit of the fingerprint")
            st_space("v", 1)
            st_write(s.large,
                     "The fingerprint covers the HTML that StreamTeX emits "
                     "itself (st_write, st_block, st_grid, st_code, "
                     "st_image ...). Text rendered by ",
                     (s.bold, "st_markdown()"), " — and therefore the body "
                     "of ", (s.bold, "show_explanation()"), " and ",
                     (s.bold, "show_details()"),
                     " — goes through st.markdown and is NOT in the "
                     "fingerprint: a change in that text is not reported. "
                     "Review those changes in the diff.")
        st_space("v", 2)

        # --- Star import ---
        st_write(bs.sub, "from streamtex import * exports the API only",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Since streamtex 0.7.36 the package defines __all__: the star
            import brings exactly the public names (st_write, st_block,
            Style, ...) and no sub-module. Before, it also exported 50
            sub-modules, and streamtex/list.py shadowed the builtin list
            in every block that star-imported streamtex. Sub-modules
            stay importable explicitly.
        """)
        st_space("v", 1)

        show_code("""\
            from streamtex import *

            names = list(("a", "b"))       # the builtin list again (0.7.36+)

            # A sub-module is imported explicitly
            from streamtex.enums import Tags as t
            import streamtex.styles as sts

            # Code that must still run on streamtex 0.7.35 or older
            names = [*("a", "b")]\
        """, language="python")
        st_space("v", 2)
