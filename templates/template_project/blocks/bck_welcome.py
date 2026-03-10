from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s


class BlockStyles:
    title = s.project.titles.main_title + s.center_txt
    subtitle = s.project.colors.accent + s.Large + s.center_txt
    description = s.large + s.center_txt + s.project.colors.muted
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_space("v", 3)
        st_write(bs.title, "My Project", tag=t.div, toc_lvl="1")
        st_space("v", 2)
        st_write(bs.subtitle, "Built with StreamTeX", tag=t.div)
        st_space("v", 3)
        with st_list(l_style=s.large, li_style=s.large):
            st_write(s.large, "This template demonstrates every major StreamTeX feature.")
            st_write(s.large, "Navigate with the sidebar Table of Contents or PageDown/PageUp keys.")
        st_space("v", 3)
