"""Title slide — presentation landing page."""
from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    subtitle = s.project.titles.subtitle + s.center_txt
    info = s.project.titles.caption + s.center_txt
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_space("v", 4)
        st_write(bs.title, "My Presentation", tag=t.div, toc_lvl="1")
        st_space("v", 2)
        st_write(bs.subtitle, "Built with StreamTeX", tag=t.div)
        st_space("v", 3)
        st_write(bs.info, "Use PageDown / PageUp to navigate")
        st_space("v", 4)

    st_slide_break(marker_label="Title")
