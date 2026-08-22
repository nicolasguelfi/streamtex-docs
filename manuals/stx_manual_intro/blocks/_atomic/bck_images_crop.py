from streamtex import *
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Image crop demo styles."""
    sub = s.project.titles.section_subtitle
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        # Edge cropping
        st_write(bs.sub, "Edge cropping — crop=", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Cut a percentage of each edge of an image at display time —
            a status bar, a banner, a margin of a screenshot — without
            producing a cropped derivative at the source.

            crop takes four percentages in **CSS inset order**
            (top, right, bottom, left), the same convention as
            clip-path, margin and padding. Each value is the percentage
            of the image's *natural* dimension removed from that edge.
            width designates the **visible zone** (the crop result).
        """)
        st_space("v", 1)

        show_code(file="examples/crop/crop_usage.py")
        st_space("v", 1)

        st_write(s.medium, "The full source image (1000 x 600):")
        st_space("v", 1)
        st_image(uri="crop/crop_demo_screenshot.png", width="500px",
                 alt="Full demo screenshot with status bar, sidebar and banner")
        st_space("v", 1)

        st_write(s.medium, "The same image with crop=(5, 20, 15, 10) — "
                           "only the 700 x 480 content zone remains:")
        st_space("v", 1)
        st_image(uri="crop/crop_demo_screenshot.png", width="500px",
                 crop=(5, 20, 15, 10),
                 alt="Demo screenshot cropped to its content zone")
        st_space("v", 1)

        show_details("""\
            **How the natural dimensions are found** (priority order):

            1. natural_size=(W, H) given by the caller — used as-is, no
               file read, no network access. **Mandatory for http(s)
               URIs** in this version.
            2. Local files — bitmap sizes read via Pillow, SVG sizes
               parsed from width/height or the viewBox. Cached by
               (path, mtime) like the base64 encoding.
            3. Images served via configure_image_path (the "served,
               never inlined" pattern) — the bytes are located on the
               server's disk via the optional fs_root= parameter of
               configure_image_path, or automatically via Streamlit's
               app/static serving convention. The served URL emission
               is unchanged (never inlined).

            **Failure behavior**: invalid values (outside [0, 100),
            top+bottom >= 100, left+right >= 100), an explicit height=
            combined with crop=, natural_size= without crop=, or
            unreadable dimensions each raise an explicit error — never a
            silently empty or distorted rendering.

            The crop is pure CSS (no JavaScript) and passes through the
            HTML export untouched. It combines with overlay= (the badge
            anchors on the visible zone), link=, managed images and
            st_zoom.
        """)
        st_space("v", 2)
