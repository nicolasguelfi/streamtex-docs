"""Video introduction — embedded YouTube demo + playlist link."""

import streamlit as st
from streamtex import st_write, st_space, st_html
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import st_slide_break

_VIDEO_URL = "https://www.youtube.com/embed/FTkw_9LGWYA"
_PLAYLIST_URL = (
    "https://www.youtube.com/watch?v=FTkw_9LGWYA"
    "&list=PLY94DCgRcAmsUBWwl7yYVm6Sd4hyvWoK2&index=1"
)


class BlockStyles:
    """Video intro styles."""
    heading = s.project.titles.section_title + s.center_txt
    body = s.large


bs = BlockStyles


def build():
    """Render the video introduction with embedded YouTube player."""
    st_space("v", 1)
    st_write(bs.heading, "See StreamTeX in Action", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(
        bs.body + s.center_txt,
        "Watch a quick demo to see what StreamTeX can do — "
        "from project creation to final document.",
        tag=t.div,
    )
    st_space("v", 1)

    # Embedded YouTube video (responsive 16:9 iframe)
    st_html(
        '<div style="position:relative;width:100%;max-width:800px;'
        'margin:0 auto;aspect-ratio:16/9;">'
        f'<iframe src="{_VIDEO_URL}" '
        'style="position:absolute;top:0;left:0;width:100%;height:100%;'
        'border:none;border-radius:8px;" '
        'allow="accelerometer;autoplay;clipboard-write;encrypted-media;'
        'gyroscope;picture-in-picture;web-share" '
        'allowfullscreen></iframe>'
        '</div>',
        height=500,
    )
    st_space("v", 2)

    # Playlist button
    st.link_button(
        "▶️  Watch all tutorials — YouTube Playlist",
        _PLAYLIST_URL,
        use_container_width=True,
    )

    st_space("v", 2)
    st_slide_break()
