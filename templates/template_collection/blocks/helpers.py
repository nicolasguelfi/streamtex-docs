"""Block helpers — project-specific configuration."""

from streamtex import (
    BlockHelperConfig, set_block_helper_config,
    show_code, show_code_inline, show_explanation, show_details,  # noqa: F401
)


class ProjectBlockHelperConfig(BlockHelperConfig):
    """Override default styles with project-specific ones."""

    def get_code_style(self):
        return None

    def get_code_inline_style(self):
        return None

    def get_explanation_style(self):
        return None

    def get_details_style(self):
        return None


set_block_helper_config(ProjectBlockHelperConfig())
