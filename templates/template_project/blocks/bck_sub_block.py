from streamtex import *
from custom.styles import Styles as s


class BlockStyles:
    pass
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(s.large + s.project.colors.accent,
                 "This text lives in a separate block file, "
                 "included via st_include().")
