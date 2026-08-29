"""st_book(block_args=, block_kwargs=) — one parameter for every block.

Covers: the forwarding contract, the recommended build() signature,
the reference example (a language passed to every build), and the
interaction with the pagination cache.
"""

from streamtex import st_write, st_space, st_block, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Block kwargs section styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    param_label = s.medium + s.text.weights.bold_weight


bs = BlockStyles


def build():
    st_write(bs.heading, "st_book — block_args & block_kwargs", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        `st_book()` renders every block by calling its `build()` function.
        Two parameters let you hand the **same values to every block** —
        without globals, without session state, without importing the
        `book.py` from the blocks:

        - `block_args` — a tuple of positional arguments;
        - `block_kwargs` — a dict of keyword arguments.

        They are forwarded verbatim, to every block **and** to the
        `separator` module, as `st_include(module, *block_args, **block_kwargs)`.
    """)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # The reference example: a language passed to every build()
    # ------------------------------------------------------------------
    st_write(bs.sub, "The reference example — a language for every build()", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The canonical use is a **document-wide parameter that changes what
        the blocks render** — the projected language of a bilingual deck.
        `book.py` decides it once; every block receives it as `lang`.
    """)
    st_space("v", 1)

    show_code("""\
        # book.py
        import os
        from streamtex import st_book

        # Static export: one pass per language, driven by an environment
        # variable. Live app: see the "Multilingual Documents" chapter for
        # reading it from the address (?lang=fr).
        lang = os.environ.get("STX_LANG", "en")

        st_book(
            [blocks.bck_title, blocks.bck_agenda, blocks.bck_closing],
            block_kwargs={"lang": lang},
            paginate=True,
        )""")
    st_space("v", 1)

    show_code("""\
        # blocks/bck_agenda.py
        from streamtex import st_write
        from custom.styles import Styles as s

        AGENDA = {"en": "Agenda", "fr": "Programme"}

        def build(lang: str = "en", **_):
            st_write(s.large, AGENDA.get(lang, AGENDA["en"]), toc_lvl="1")""")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # The recommended block signature
    # ------------------------------------------------------------------
    st_write(bs.sub, "The recommended build() signature", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.medium, (bs.param_label, "Give every forwarded parameter a default"), " — `def build(lang: str = \"en\")`. A block must stay callable with no arguments: tests, `st_include()` from a composite block, and `stx` tools call `build()` bare.")
            with l.item(): st_write(s.medium, (bs.param_label, "Accept and ignore the rest"), " — `**_` lets `book.py` add a second parameter later (`theme`, `audience`…) without touching every block that does not care.")
            with l.item(): st_write(s.medium, (bs.param_label, "Pass it on"), " — a composite block forwards it to its atomic blocks: `st_include(bck_part, lang=lang)`.")
            with l.item(): st_write(s.medium, (bs.param_label, "Keep the values plain"), " — strings, numbers, booleans, lists, dicts. The pagination cache fingerprints them (below); an object whose `repr` embeds a memory address would invalidate the cache on every run.")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Interaction with the pagination cache
    # ------------------------------------------------------------------
    st_write(bs.sub, "Interaction with the pagination cache", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        In paginated mode `st_book()` builds the TOC, the markers, the page
        titles and the search index **once**, in a cache keyed by the
        modules, their mtimes and the library version. Since the kwargs
        change what the blocks render, the cache key also includes a
        **fingerprint of `block_args` / `block_kwargs`**:

        - `block_kwargs={"lang": "fr"}` gets its own TOC / markers / titles —
          the sidebar is never the English one left by a previous run;
        - the persistent file is `.stx_cache/page_cache-<fp>.json`, one per
          variant, so `stx cache warmup` run once per language keeps every
          language warm;
        - a project that forwards nothing keeps `page_cache.json` and the
          exact same key as before.
    """)
    st_space("v", 2)

    show_details("""\
        **Migration note.** Passing unknown keyword arguments directly to
        `st_book(...)` — `st_book(blocks, theme="dark")` — still forwards them
        but is deprecated and emits a `DeprecationWarning`. Use
        `block_kwargs={"theme": "dark"}`: the explicit contract gives IDE
        support and a clear `TypeError` at the call site instead of a crash
        deep inside a block.
    """)
    st_space("v", 2)
