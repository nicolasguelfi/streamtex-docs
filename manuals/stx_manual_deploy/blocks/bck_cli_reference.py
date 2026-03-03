"""Composite block — CLI Reference for Deployment."""

import streamtex as stx
from streamtex import st_include

bck_cli_deploy_commands = stx.load_atomic_block("bck_cli_deploy_commands", __file__)
bck_cli_publish_commands = stx.load_atomic_block("bck_cli_publish_commands", __file__)


class BlockStyles:
    """Composite block styles."""
    pass


def build():
    """Include atomic blocks for CLI reference."""
    st_include(bck_cli_deploy_commands)
    st_include(bck_cli_publish_commands)
