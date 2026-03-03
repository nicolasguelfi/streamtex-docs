"""Block helpers for stx_manual_ai — config injection pattern.

This module defines the project-specific style configuration and
re-exports the library helpers so that blocks can import from here:

    from blocks.helpers import show_code, show_explanation, show_details

No wrapper functions needed — the library functions use the global
config set by set_block_helper_config() at import time.
"""

from streamtex import (
    BlockHelperConfig, set_block_helper_config,
    show_code, show_code_inline, show_explanation, show_details,  # noqa: F401
    st_write, st_block, st_space,
)
from custom.styles import Styles as s


# ============================================================================
# Style configuration (one-time setup at import)
# ============================================================================

class ProjectBlockHelperConfig(BlockHelperConfig):
    """Inject AI project's styles into all helpers."""

    def get_code_style(self):
        return s.project.containers.code_box

    def get_code_inline_style(self):
        return None

    def get_explanation_style(self):
        return s.project.containers.explanation_box

    def get_details_style(self):
        return s.project.containers.details_box


set_block_helper_config(ProjectBlockHelperConfig())


# ============================================================================
# Project-specific helpers (unique to AI manual)
# ============================================================================

def show_ai_highlight(title: str, description: str):
    """AI feature highlight box with violet accent."""
    with st_block(s.project.containers.ai_callout):
        st_write(s.project.titles.feature_title, title)
        st_space("v", 1)
        st_write(s.large, description)


def show_good_bad(good_text: str, bad_text: str):
    """Side-by-side good/bad comparison."""
    with st_block(s.project.containers.good_callout):
        st_write(s.project.titles.subsection_title, "CORRECT")
        st_space("v", 1)
        st_write(s.large, good_text)
    st_space("v", 1)
    with st_block(s.project.containers.bad_callout):
        st_write(s.project.colors.error_red + s.bold, "WRONG")
        st_space("v", 1)
        st_write(s.large, bad_text)
