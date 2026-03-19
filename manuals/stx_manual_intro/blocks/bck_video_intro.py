"""Video introduction — embedded YouTube demo + playlist link."""

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
        "Go to our YouTube channel to watch a quick demo and see what StreamTeX can do — "
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

    # Playlist button (YouTube red, white bold text)
    st_html(
        f'<a href="{_PLAYLIST_URL}" target="_blank" '
        'style="display:block;width:100%;max-width:800px;margin:0 auto;'
        'padding:14px 24px;background:#FF0000;color:#fff;font-weight:bold;'
        'font-size:18px;text-align:center;text-decoration:none;'
        'border-radius:8px;">'
        '\u25b6\ufe0f  Watch all tutorials \u2014 YouTube Playlist'
        '</a>',
    )

    st_space("v", 2)
    st_slide_break(marker_label="Video Tutorials")
