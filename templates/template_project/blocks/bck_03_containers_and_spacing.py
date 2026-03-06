from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    demo_block = s.project.containers.callout + s.center_txt
bs = BlockStyles


def build():
    st_write(bs.heading, "Containers & Spacing", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # --- st_block ---
    st_write(bs.sub, "st_block — Vertical Container", toc_lvl="+1")
    st_space("v", 1)

    show_code("""\
        with st_block(s.center_txt + s.large):
            st_write("Line 1 — stacked vertically")
            st_write("Line 2 — below line 1")
    """)
    st_space("v", 1)

    with st_block(bs.demo_block):
        st_write(s.large, "Line 1 — stacked vertically")
        st_write(s.large, "Line 2 — below line 1")
    st_space("v", 2)

    # --- st_span ---
    st_write(bs.sub, "st_span — Horizontal Container", toc_lvl="+1")
    st_space("v", 1)

    show_code("""\
        with st_span(s.bold + s.large):
            st_write("Left ")
            st_write("Right")
    """)
    st_space("v", 1)

    with st_span(s.bold + s.large):
        st_write("Left ")
        st_write("Right")
    st_space("v", 2)

    # --- Spacing ---
    st_write(bs.sub, "Spacing: st_space & st_br", toc_lvl="+1")
    st_space("v", 1)

    show_code("""\
        st_write(s.large, "Before vertical space")
        st_space("v", 3)          # 3em vertical gap
        st_write(s.large, "After vertical space")

        st_space("h", "40px")     # 40px horizontal gap

        st_write(s.large, "Line A")
        st_br()                   # simple line break
        st_write(s.large, "Line B")
    """)
    st_space("v", 1)

    with st_block(bs.demo_block):
        st_write(s.large, "Before vertical space")
        st_space("v", 3)
        st_write(s.large, "After vertical space")
    st_space("v", 1)

    with st_block(bs.demo_block):
        st_write(s.large, "Line A")
        st_br()
        st_write(s.large, "Line B")
    st_space("v", 2)

    # --- Slide break ---
    st_write(bs.sub, "Slide Break (Presentation Mode)", toc_lvl="+1")
    st_space("v", 1)

    show_code("""\
        from streamtex import st_slide_break

        st_write(s.large, "Section 1 content")
        st_slide_break()            # rule + full-viewport space + hidden marker
        st_write(s.large, "Section 2 — off-screen until PageDown")
    """)
    st_space("v", 2)

    st_space("v", 1)
    with st_block(s.project.containers.callout):
        st_write(s.project.colors.accent + s.bold, "Tip")
        with st_list(l_style=s.large, li_style=s.large):
            st_write(s.large, (s.bold, 'st_space("v", N)'), " — adds N em of vertical space")
            st_write(s.large, (s.bold, 'st_space("h", "Npx")'), " — adds horizontal space")
            st_write(s.large, (s.bold, "st_br()"), " — inserts a simple line break")
            st_write(s.large, (s.bold, "st_slide_break()"), " — presentation section separator with hidden marker")
    st_space("v", 1)
