"""Block helpers for stx_manual_developer — config injection pattern."""

from streamtex import (
    BlockHelperConfig, set_block_helper_config,
    show_code, show_code_inline, show_explanation, show_details,  # noqa: F401
    st_write, st_block, st_space,
)
from custom.styles import Styles as s


class ProjectBlockHelperConfig(BlockHelperConfig):
    """Inject developer project's styles into all helpers."""

    def get_code_style(self):
        return s.project.containers.code_box

    def get_code_inline_style(self):
        return None

    def get_explanation_style(self):
        return s.project.containers.explanation_box

    def get_details_style(self):
        return s.project.containers.details_box


set_block_helper_config(ProjectBlockHelperConfig())
