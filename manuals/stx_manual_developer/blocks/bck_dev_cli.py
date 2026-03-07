"""Composite block — CLI Architecture."""

import streamtex as stx
from streamtex import st_include

bck_cli_architecture = stx.load_atomic_block("bck_cli_architecture", __file__)
bck_cli_adding_commands = stx.load_atomic_block("bck_cli_adding_commands", __file__)


class BlockStyles:
    pass


bs = BlockStyles


def build():
    st_include(bck_cli_architecture)
    st_include(bck_cli_adding_commands)
