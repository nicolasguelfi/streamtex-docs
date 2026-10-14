"""Composing by Atoms — hot reload of included blocks and the page cache.

Covers: blocks reached through st_include and the project modules they
import reload with the page (no restart, no sys.modules purge, no rev
key), the opt-out, the limits, and where the page cache lives.
"""

from streamtex import st_block, st_list, st_space, st_write
from streamtex.enums import ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_details, show_explanation


class BlockStyles:
    """Hot reload styles."""
    sub = s.project.titles.section_subtitle
    feature = s.project.titles.feature_title
    term = s.medium + s.text.weights.bold_weight
    body = s.medium


bs = BlockStyles


def build():
    st_write(bs.sub, "Hot reload of included blocks", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        **Reloading the page is enough.** Every block reached through
        `st_include` — in any directory, at any depth, `_atomic/` blocks
        and list blocks included — is watched; when its file changed, it
        is executed again **in place**: the same module object gets the new
        code, so a list block's `ITEMS` and the entries given to `st_book`
        see it at once.

        The **project modules those blocks import** are followed too, at
        any depth: a `shared/` folder, a pack installed outside
        `site-packages`, your `custom/` modules. A changed one is executed
        again in place, then every module and block that imports it. The
        standard library, installed packages, StreamTeX and Streamlit are
        not followed.
    """)
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(l_style=bs.body, li_style=bs.body, list_type=lt.unordered) as lst:
            with lst.item():
                st_write(bs.body, (bs.term, "No server restart"),
                         " — edit an atom, reorder a list block's ITEMS, change a shared "
                         "helper: reload the page.")
            with lst.item():
                st_write(bs.body, (bs.term, "No workaround"),
                         " — no sys.modules purge in book.py, no rev key in block_kwargs to "
                         "force a new cache.")
            with lst.item():
                st_write(bs.body, (bs.term, "A failing file"),
                         " — a syntax error in an edited block is reported once, in red, "
                         "where it is included; the next reload after the fix picks it up.")
    st_space("v", 1)

    show_code("""\
        # Opt-out, in book.py (default: on)
        import streamtex as stx
        stx.set_include_reload(False)

        # or from the environment, which wins over the call
        #   STX_INCLUDE_RELOAD=0 stx run""")
    st_space("v", 1)

    st_write(s.large, "Turned off, the included files are still watched by the page cache "
                      "(it is rebuilt when one changed); only the re-execution stops.")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Limits
    # ------------------------------------------------------------------
    st_write(bs.feature, "Limits")
    st_space("v", 1)

    with st_block(s.project.containers.details_box):
        with st_list(l_style=bs.body, li_style=bs.body, list_type=lt.unordered) as lst:
            with lst.item():
                st_write(bs.body, (bs.term, "Module code runs again"),
                         " — a class defined in a reloaded module is a new class object: "
                         "instances made before (kept in st.session_state or a cache) are "
                         "no longer isinstance of it. A module-level variable starts again "
                         "from the value its file assigns.")
            with lst.item():
                st_write(bs.body, (bs.term, "Only what st_include reaches"),
                         " — book.py is Streamlit's main script and runs again at every "
                         "rerun. A module that only book.py or setup.py imports is not "
                         "followed by StreamTeX: Streamlit itself reloads the modules of the "
                         "book's folder it watches; one outside that folder needs a server "
                         "restart.")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # The page cache
    # ------------------------------------------------------------------
    st_write(bs.feature, "Where the page cache lives")
    st_space("v", 1)

    show_explanation("""\
        The paginated view keeps the TOC, the markers, the page titles and
        the search index in a page cache. It belongs to the module's
        `book.py`:

        - the file is `<book dir>/.stx_cache/page_cache.json`
          (`page_cache-<fp>.json` with `block_args` / `block_kwargs`), next
          to `book.py`;
        - its key includes the entries and their mtimes, that `book.py`,
          every `custom/**/*.py` and the library version;
        - the blocks reached through `st_include` and the data files the
          blocks read are checked separately: their mtimes are stored with
          the cache, which is discarded as soon as one of them changed.
    """)
    st_space("v", 1)

    show_details("""\
        **Layouts with entries outside `<book dir>/blocks/`** (for instance a
        `content/` or `lists/` folder shared by several modules): each module
        now gets its own cache, so modules no longer overwrite each other's,
        and one cold rebuild happens after the upgrade. Caches written by
        older versions next to the entries' parent folder are orphans:
        `rm -r <entries parent>/.stx_cache`. For the standard layout nothing
        moves. `stx cache warmup` and `stx run --set --fresh` act on the file
        the app reads.
    """)
    st_space("v", 2)
