"""Book Defaults — [book.defaults] in stx.toml and doc_version="auto" (0.7.39)."""

from blocks.helpers import show_code, show_details, show_explanation
from custom.styles import Styles as s
from streamtex import *
from streamtex.book import BOOK_DEFAULT_KEYS
from streamtex.enums import Tags as t


class BlockStyles:
    """Book defaults chapter styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    param_label = s.medium + s.text.weights.bold_weight
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Book Defaults", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            A project made of several documents repeats the same book
            settings in every book.py: paginate, page width, zoom, the
            version shown in the export... Since 0.7.39 these settings can
            be declared once, in the `[book.defaults]` table of the
            project's `stx.toml`. Book configuration only: the content of a
            block keeps its explicit values, written in the block.
        """)
        st_space("v", 2)

        # --- 1. Declaring the defaults ---
        st_write(bs.sub, "Declaring [book.defaults]", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# stx.toml — at the root of the project
[book.defaults]
paginate = true
page_width = 80
zoom = 110
loading = false
doc_version = "auto"        # [project].version of pyproject.toml
lang = "auto"               # $STX_LANG > ?lang= > default (streamtex.i18n)
""", language="toml", line_numbers=False)
        st_space("v", 1)

        show_code("""\
# modules/my_deck/book.py — nothing repeated
from streamtex import st_book
import blocks

st_book([blocks.bck_title, blocks.bck_content])""")
        st_space("v", 2)

        # --- 2. The closed list of keys ---
        st_write(bs.sub, "The keys it accepts", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The list is closed — the book settings that never reach the
            content of a block. Any other key is ignored, with a warning in
            the log listing the allowed ones. Read live from the library:
        """)
        st_space("v", 1)

        with st_block(s.project.containers.explanation_box):
            with st_list(list_type="ul") as l:
                for key in sorted(BOOK_DEFAULT_KEYS):
                    with l.item():
                        st_write(s.medium, (bs.param_label, key))
        st_space("v", 2)

        # --- 3. Precedence ---
        st_write(bs.sub, "Explicit arguments win", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Anything the book passes — by keyword or by position — wins over
            `[book.defaults]`, which wins over the library defaults. The
            table is read from the nearest `stx.toml` above the book, and
            re-read when it changes (no restart needed).
        """)
        st_space("v", 1)

        show_code("""\
# stx.toml: [book.defaults] paginate = true, zoom = 110

st_book(blocks_list)                    # paginate=True, zoom=110 (stx.toml)
st_book(blocks_list, zoom=100)          # zoom=100: the book's own value wins
st_book(blocks_list, paginate=False)    # this document is continuous""")
        st_space("v", 2)

        # --- 4. doc_version="auto" ---
        st_write(bs.sub, "doc_version=\"auto\"", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            `doc_version="auto"` reads `[project].version` of the nearest
            `pyproject.toml` above the book — the version shown with the
            export stays in step with the project without a line of code.
            It works as an argument and as a `[book.defaults]` value.
        """)
        st_space("v", 1)

        show_code("""\
# Before: read by hand in book.py
import tomllib
from pathlib import Path
_doc_version = tomllib.loads(
    (Path(__file__).parent / "pyproject.toml").read_text()
).get("project", {}).get("version", "?")
st_book([...], doc_version=_doc_version)

# Since 0.7.39
st_book([...], doc_version="auto")""")
        st_space("v", 1)

        show_details("""\
            A broken `stx.toml` never breaks the book: the defaults are then
            ignored and a warning is logged. Without any `stx.toml` above the
            book, nothing changes. `help(st_book)` lists the same keys.
        """)
        st_space("v", 2)
