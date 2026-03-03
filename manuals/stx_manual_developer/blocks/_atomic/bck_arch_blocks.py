import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details
import textwrap


class BlockStyles:
    """Block system styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cell = (s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout)
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "The Block System",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- 1. ProjectBlockRegistry ---
        st_write(bs.sub, "ProjectBlockRegistry", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            ProjectBlockRegistry lazy-loads block modules from a
            project's blocks/ directory. It scans for bck_*.py
            files and imports them on demand when accessed via
            __getattr__. This is the registry used in each
            project's blocks/__init__.py.
        """))
        st_space("v", 1)

        show_code("""\
# blocks/__init__.py
from pathlib import Path
from streamtex import ProjectBlockRegistry

registry = ProjectBlockRegistry(Path(__file__).parent)

def __getattr__(name: str):
    return registry.get(name)

# Usage: from blocks import bck_my_block
# The block is imported lazily on first access""")
        st_space("v", 2)

        # --- 2. LazyBlockRegistry ---
        st_write(bs.sub, "LazyBlockRegistry", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            LazyBlockRegistry extends the concept to multiple
            source directories with priority ordering. It searches
            directories in order, so project-local blocks override
            shared blocks. This enables the shared-blocks pattern.
        """))
        st_space("v", 1)

        show_code("""\
# LazyBlockRegistry searches directories in priority order:
#   1. project/blocks/       (highest priority)
#   2. shared-blocks/blocks/ (fallback)
#
# If bck_welcome.py exists in both, the project-local
# version wins.""")
        st_space("v", 2)

        # --- 3. load_atomic_block ---
        st_write(bs.sub, "load_atomic_block()", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            load_atomic_block() loads a single block module from
            the _atomic/ subdirectory relative to the caller's
            file location. It uses __file__ to resolve the path,
            so it always finds the correct _atomic/ directory.
        """))
        st_space("v", 1)

        show_code("""\
import streamtex as stx

# In blocks/bck_my_composite.py:
bck_part_a = stx.load_atomic_block("bck_part_a", __file__)
bck_part_b = stx.load_atomic_block("bck_part_b", __file__)

# This loads:
#   blocks/_atomic/bck_part_a.py
#   blocks/_atomic/bck_part_b.py""")
        st_space("v", 2)

        # --- 4. Composite pattern ---
        st_write(bs.sub, "The composite pattern", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            A composite block loads multiple atomic blocks and
            includes them in sequence using st_include(). This
            is the standard way to group related content into
            a single chapter or section.
        """))
        st_space("v", 1)

        show_code("""\
# blocks/bck_my_chapter.py (composite)
import streamtex as stx
from streamtex import st_include

bck_intro = stx.load_atomic_block("bck_intro", __file__)
bck_details = stx.load_atomic_block("bck_details", __file__)
bck_summary = stx.load_atomic_block("bck_summary", __file__)

class BlockStyles:
    pass

def build():
    st_include(bck_intro)
    st_include(bck_details)
    st_include(bck_summary)""")
        st_space("v", 2)

        # --- 5. BlockHelper DI pattern ---
        st_write(bs.sub, "BlockHelper dependency injection", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            The BlockHelper pattern uses dependency injection to
            configure show_code(), show_explanation(), and
            show_details() with project-specific styles.
            set_block_helper_config() injects the configuration
            so helpers render with the correct visual theme.
        """))
        st_space("v", 1)

        show_code("""\
# blocks/helpers.py
from streamtex import (
    BlockHelperConfig, set_block_helper_config,
    show_code, show_explanation, show_details,
)
from custom.styles import Styles as s

class ProjectBlockHelperConfig(BlockHelperConfig):
    def get_code_style(self):
        return s.project.containers.code_box
    def get_explanation_style(self):
        return s.project.containers.explanation_box
    def get_details_style(self):
        return s.project.containers.details_box

set_block_helper_config(ProjectBlockHelperConfig())""")
        st_space("v", 2)

        # --- 6. Static resolution ---
        st_write(bs.sub, "Static resolution with set_static_sources()", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            set_static_sources() configures multi-directory file
            lookup for static assets (images, code examples, etc.).
            When show_code(file=...) or st_image(src=...) is called,
            the system searches configured directories in order.
        """))
        st_space("v", 1)

        show_code("""\
# In book.py or project setup:
from streamtex import set_static_sources

set_static_sources([
    "static/",          # project-local assets (highest priority)
    "../shared/static/", # shared assets (fallback)
])

# Now show_code(file="examples/demo.py") searches:
#   1. static/examples/demo.py
#   2. ../shared/static/examples/demo.py""")
        st_space("v", 2)

        show_details(textwrap.dedent("""\
            ProjectBlockRegistry is for single-project use.
            LazyBlockRegistry is for multi-source resolution.

            Atomic blocks are self-contained and reusable.
            Composite blocks are assembly points.

            The DI pattern in helpers.py keeps block code clean:
            helpers know how to style themselves via the injected config.
        """))
