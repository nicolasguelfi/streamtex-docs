"""Composing by Atoms — pages that follow the tree (st_book paginate_by=).

Covers: paginate_by = "entry" | N | "depth:N" | "leaf", the
[book.defaults] key, st_include(page=True | False), what ?page= means,
what does not change, and a live page map computed on an example tree.
"""

import streamtex as stx
from streamtex import st_block, st_list, st_space, st_write
from streamtex.enums import ListTypes as lt
from streamtex.pagewalk import page_starts
from custom.styles import Styles as s
from blocks.helpers import show_code, show_details, show_explanation


class BlockStyles:
    """Pages styles."""
    sub = s.project.titles.section_subtitle
    feature = s.project.titles.feature_title
    term = s.medium + s.text.weights.bold_weight
    body = s.medium


bs = BlockStyles

#: The example module, one entry: path of each inclusion inside the entry
#: (child ordinals) -> block name. () is the entry itself.
_TREE = {
    (): "lists.course",
    (0,): "lists.intro",
    (0, 0): "atoms.title",
    (0, 1): "atoms.agenda",
    (1,): "atoms.motivation",
    (2,): "lists.rag",
    (2, 0): "lists.rag_basics",
    (2, 0, 0): "atoms.rag_definition",
    (2, 0, 1): "atoms.rag_example",
    (2, 1): "composites.rag_pipeline",
}

#: The page maps shown live: (label, paginate_by, page= overrides).
_CASES = [
    ('paginate_by=1', 1, {}),
    ('paginate_by=2', 2, {}),
    ('paginate_by="leaf"', "leaf", {}),
    ('"leaf" + page=False on lists.intro', "leaf", {(0,): False}),
    ('"leaf" + page=True on lists.rag_basics', "leaf", {(2, 0): True}),
]


def _nodes(overrides: dict) -> dict:
    """The tree in the form the page-cache build records it."""
    out = {}
    for path in _TREE:
        children = sum(1 for q in _TREE if len(q) == len(path) + 1 and q[:len(path)] == path)
        out[path] = {"depth": len(path), "page": overrides.get(path), "children": children}
    return out


def build():
    st_write(bs.sub, "Pages that follow the tree — paginate_by", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        In the paginated view one `st_book` entry is one page. With list
        blocks as entries, a page would be a whole top-level list.
        `st_book(..., paginate=True, paginate_by=…)` lets the pages follow
        the composition tree instead — even for a module given as one root
        list block:

        - `"entry"` (default) — one page per entry, as before;
        - `N` or `"depth:N"` — pages down to depth N (an entry has depth 0,
          what it includes depth 1, …);
        - `"leaf"` — one page per leaf: an inclusion that includes no other
          block (an atom or a composite).
    """)
    st_space("v", 1)

    show_code("""\
        # book.py
        st_book([blocks.bck_course], paginate=True, paginate_by="leaf")

        # a local override, inside a list block
        st_include(bck_intro, page=False)        # stays on the enclosing page
        st_include(bck_pipeline, page=True)      # starts a page with its whole subtree""")
    st_space("v", 1)

    show_code("""\
        # stx.toml — once for every book of the project (a book's own argument wins)
        [book.defaults]
        paginate_by = "depth:2\"""", language="toml", line_numbers=False)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Live page maps
    # ------------------------------------------------------------------
    st_write(bs.feature, "Live — the page map of an example tree")
    st_space("v", 1)

    show_code("""\
        lists.course                      # the entry (depth 0)
        ├── lists.intro                   # depth 1
        │   ├── atoms.title               # depth 2
        │   └── atoms.agenda
        ├── atoms.motivation              # depth 1, a leaf
        └── lists.rag                     # depth 1
            ├── lists.rag_basics          # depth 2
            │   ├── atoms.rag_definition  # depth 3
            │   └── atoms.rag_example
            └── composites.rag_pipeline   # depth 2, a leaf""", language="text", line_numbers=False)
    st_space("v", 1)

    st_write(s.large, "Each row gives the inclusion that starts each page, computed live by "
                      "streamtex.pagewalk.page_starts, the function the page-cache build "
                      "uses. With \"entry\" the whole tree is one page.")
    st_space("v", 1)

    stx.st_table({
        "setting": [label for label, _, _ in _CASES],
        "pages": [str(len(page_starts(_nodes(over), mode))) for _, mode, over in _CASES],
        "each page starts at": [
            " | ".join(_TREE[p] for p in page_starts(_nodes(over), mode))
            for _, mode, over in _CASES
        ],
    })
    st_space("v", 1)

    st_write(s.large, "Content met before the first page start (here, with page=False on "
                      "lists.intro, the title and the agenda) belongs to the first page.")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # What changes, what does not
    # ------------------------------------------------------------------
    st_write(bs.feature, "What changes, what does not")
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(l_style=bs.body, li_style=bs.body, list_type=lt.unordered) as lst:
            with lst.item():
                st_write(bs.body, (bs.term, "The same for every value"),
                         " — the arrows, the marker numbers, the TOC, the HTML export and "
                         "the PDF. Pages only cut the loading of the flattening.")
            with lst.item():
                st_write(bs.body, (bs.term, "?page=n"),
                         " — the n-th page of the current page map, so its meaning changes "
                         "with paginate_by. ?marker=<key> and ?slide=n are the durable links.")
            with lst.item():
                st_write(bs.body, (bs.term, "The presenter stays on the same slide"),
                         " — when the page map changes (a list block edited, paginate_by "
                         "changed), the page that holds the current slide becomes the "
                         "current page.")
            with lst.item():
                st_write(bs.body, (bs.term, "A page renders its part only"),
                         " — the other leaves are not executed; the rest of the entry runs "
                         "without being drawn. A break at the head of a page draws no rule "
                         "nor spacer in the app.")
            with lst.item():
                st_write(bs.body, (bs.term, "Titles"),
                         " — a continuation page takes the title of its entry; it is never "
                         "taken for a footer. The navigation widget also shows on pages "
                         "without markers.")
    st_space("v", 1)

    show_details("""\
        **A block's position can depend on its page.** With
        `PresentationConfig(center_content=True, enforce_ratio=False)`, a
        page shorter than the screen is centred vertically. Composing pages
        from the tree changes which blocks are alone on their page: a title
        atom alone on its page starts lower than the same atom at the head
        of a longer page.
    """)
    st_space("v", 2)
