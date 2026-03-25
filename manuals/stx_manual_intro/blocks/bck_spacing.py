"""Section Spacing — Configurable margins around blocks and sections."""
from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Section Spacing", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            Section spacing controls margins around blocks (in st_book) and
            between sections within a block (between st_slide_break calls).

            Two pure types: **Spacing** (value object for margins) and
            **SpacingConfig** (bundles block + section spacing).

            5-level override hierarchy:
            Built-in > Book (global) > Profile > Block > Call-site.
        """)
        st_space("v", 2)

        # --- Book-level ---
        st_write(bs.sub, "Book-Level Configuration", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Call **set_spacing()** once in book.py to configure margins
            globally. block.top/bottom control inter-block gaps;
            section.top/bottom control gaps between slide_break sections.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import Spacing, SpacingConfig, set_spacing

# Replace per-block st_space("v", N) calls with one global config
set_spacing(SpacingConfig(
    block=Spacing(top=2, bottom=0),       # margins between blocks
    section=Spacing(top=2),               # margins between sections within blocks
))""")
        st_space("v", 2)

        # --- Block-level ---
        st_write(bs.sub, "Block-Level Override", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Inside a build() function, call **set_block_spacing()** to override
            section spacing for that specific block. It is automatically reset
            by st_book after build() returns.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import set_block_spacing, Spacing

def build():
    set_block_spacing(Spacing(top=0, left="10%", right="10%"))
    # All sections in THIS block use these margins
    # Reset automatically by st_book after build()""")
        st_space("v", 2)

        # --- Per-break ---
        st_write(bs.sub, "Per-Break Override", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Pass a **spacing** parameter directly to st_slide_break() or
            st_write() (with toc_lvl) for per-break control.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import st_slide_break, Spacing

# Large gap + indented section
st_slide_break("Section 2", spacing=Spacing(
    top="200px",
    left="15%",
    right="15%",
))

# Tight section — no extra gap
st_slide_break("Section 3", spacing=Spacing(top=0))""")
        st_space("v", 2)

        # --- Spacing fields ---
        st_write(bs.sub, "Spacing Fields", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            | Field | Type | Description |
            |-------|------|-------------|
            | top | int or str or None | Vertical space before (int=st_space units, str=CSS) |
            | bottom | int or str or None | Vertical space after |
            | left | str or None | Left margin (CSS: "5%", "2em", "40px") |
            | right | str or None | Right margin (CSS value) |
            | width | int or None | Content width % (block-level only) |

            All fields default to None (= inherit from parent level).
        """)
