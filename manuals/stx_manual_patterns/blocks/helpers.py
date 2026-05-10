"""Block helpers for stx_manual_patterns — config injection pattern.

Re-exports library helpers (show_code, show_explanation, show_details)
with the project's container styles wired in. Blocks import from here:

    from blocks.helpers import show_code, show_explanation, show_details
"""

from streamtex import (
    BlockHelperConfig, set_block_helper_config,
    show_code, show_code_inline, show_explanation, show_details,  # noqa: F401
    st_slide_break, SlideBreakConfig, SlideBreakMode, set_slide_break_config,  # noqa: F401
)
from custom.styles import Styles as s


# ============================================================================
# Style configuration (one-time setup at import)
# ============================================================================

class ProjectBlockHelperConfig(BlockHelperConfig):
    """Inject patterns manual styles into all helpers."""

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
# Presentation helpers — re-exported from streamtex
# ============================================================================
set_slide_break_config(SlideBreakConfig(
    mode=SlideBreakMode.FULL,
    space="5vh",
    rule_margin_top="5em",
    rule_margin_bottom="5em",
    thickness="3px",
    color="167, 139, 250",
    opacity=0.5,
    marker=True,
))
