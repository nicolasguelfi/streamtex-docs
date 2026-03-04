"""The Atomic Block Pattern — composite and atomic block architecture."""

from streamtex import (
    st_write, st_space,
)
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Atomic blocks pattern styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    feature = s.project.titles.feature_title


bs = BlockStyles


def build():
    """The Atomic Block Pattern — explain composite/atomic architecture."""
    st_write(bs.heading, "The Atomic Block Pattern", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        StreamTeX uses a composite/atomic pattern to organize blocks.
        Composite blocks wire multiple atomic blocks together,
        while atomic blocks are self-contained, single-topic units.

        This architecture promotes reusability, testability, and
        clean separation of concerns.
    """)
    st_space("v", 2)

    # --- Composite blocks ---
    st_write(bs.sub, "Composite Blocks", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A composite block loads and includes multiple atomic blocks.
        It acts as a section organizer: it decides which sub-topics
        appear and in what order. Composite blocks live directly
        in the blocks/ directory.
    """)
    st_space("v", 2)

    # --- Atomic blocks ---
    st_write(bs.sub, "Atomic Blocks", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        An atomic block covers a single topic. It has its own
        BlockStyles class and build() function. Atomic blocks
        live in the blocks/_atomic/ subdirectory. They can be
        loaded by any composite block via load_atomic_block().
    """)
    st_space("v", 2)

    # --- Directory structure ---
    st_write(bs.sub, "Directory Structure", toc_lvl="+1")
    st_space("v", 1)

    show_code("""\
        blocks/
        \u251c\u2500\u2500 bck_my_section.py          # Composite: loads and includes atoms
        \u2514\u2500\u2500 _atomic/
            \u251c\u2500\u2500 bck_topic_a.py         # Atomic: one topic
            \u2514\u2500\u2500 bck_topic_b.py         # Atomic: another topic
    """, language="text", line_numbers=False)
    st_space("v", 2)

    # --- Composite block code ---
    st_write(bs.sub, "Composite Block Code", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A composite block imports streamtex, loads each atomic
        block by name, and includes them in build(). The BlockStyles
        class is typically empty since styling lives in the atoms.
    """)
    st_space("v", 1)

    show_code("""\
        import streamtex as stx
        from streamtex import st_include

        bck_topic_a = stx.load_atomic_block("bck_topic_a", __file__)
        bck_topic_b = stx.load_atomic_block("bck_topic_b", __file__)

        class BlockStyles:
            pass

        def build():
            st_include(bck_topic_a)
            st_include(bck_topic_b)
    """, language="python")
    st_space("v", 2)

    # --- Atomic block code ---
    st_write(bs.sub, "Atomic Block Code", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        An atomic block follows the standard block structure:
        a BlockStyles class for local styling and a build()
        function that renders the content.
    """)
    st_space("v", 1)

    show_code("""\
        \"\"\"Atomic block \u2014 Topic A.\"\"\"

        from streamtex import *
        from streamtex.enums import Tags as t
        from custom.styles import Styles as s
        from blocks.helpers import show_code, show_explanation

        class BlockStyles:
            heading = s.project.titles.section_title + s.center_txt
            sub = s.project.titles.section_subtitle
        bs = BlockStyles

        def build():
            st_write(bs.heading, "Topic A", tag=t.div, toc_lvl="1")
            st_space("v", 1)
            show_explanation("Content for topic A.")
    """, language="python")
    st_space("v", 2)

    # --- Benefits ---
    st_write(bs.sub, "Benefits", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Reusability \u2014 An atomic block can be included by multiple
        composite blocks across different manuals.

        Testability \u2014 Each atomic block can be tested in isolation.
        Its build() function is self-contained.

        Modularity \u2014 Adding or removing a sub-topic is a one-line
        change in the composite block. No refactoring needed.

        Readability \u2014 Composite blocks act as a table of contents
        for the section, making the structure immediately clear.
    """)
    st_space("v", 2)

    # --- When to use ---
    st_write(bs.sub, "When to Use", toc_lvl="+1")
    st_space("v", 1)

    show_details("""\
        Use the atomic pattern whenever a section has two or more
        sub-topics. If a block file grows beyond a single focused
        topic, split it into a composite with atomic children.

        For simple, single-topic sections, a standalone block
        (no _atomic/ directory) is perfectly fine.
    """)
    st_space("v", 1)
