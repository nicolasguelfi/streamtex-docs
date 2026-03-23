"""Block helpers for stx_manual_ce — config injection pattern.

This module defines the project-specific style configuration and
re-exports the library helpers so that blocks can import from here:

    from blocks.helpers import show_code, show_explanation, show_details

No wrapper functions needed — the library functions use the global
config set by set_block_helper_config() at import time.
"""

from streamtex import (
    BlockHelperConfig, set_block_helper_config,
    show_code, show_code_inline, show_explanation, show_details,  # noqa: F401
)
from custom.styles import Styles as s


# ============================================================================
# Style configuration (one-time setup at import)
# ============================================================================

class ProjectBlockHelperConfig(BlockHelperConfig):
    """Inject CE project's styles into all helpers."""

    def get_code_style(self):
        return s.project.containers.code_box

    def get_code_inline_style(self):
        return None

    def get_explanation_style(self):
        return s.project.containers.explanation_box

    def get_details_style(self):
        return s.project.containers.details_box


set_block_helper_config(ProjectBlockHelperConfig())
