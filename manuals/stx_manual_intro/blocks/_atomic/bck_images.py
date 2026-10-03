from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Image demo styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

# Sample image URLs for portability
theImageURL = "https://picsum.photos/seed/streamtex1/400/250"
theImageURL2 = "https://picsum.photos/seed/streamtex2/400/250"

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Images", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # Basic image
        st_write(bs.sub, "st_image with URL", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Display images from URLs, local paths, or base64
            with st_image().
        """)
        st_space("v", 1)

        show_code("""\
theImageURL = "https://picsum.photos/seed/streamtex1/400/250"
st_image(uri=theImageURL, alt="Sample landscape image")""")
        st_space("v", 1)

        st_image(uri=theImageURL, alt="Sample landscape image")
        st_space("v", 2)

        # Width and height
        st_write(bs.sub, "Width and height control", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Control image dimensions with width and height parameters.
        """)
        st_space("v", 1)

        show_code("""\
st_image(uri=theImageURL,
         width="200px", height="150px",
         alt="Resized image")""")
        st_space("v", 1)

        st_image(uri=theImageURL,
                 width="200px", height="150px",
                 alt="Resized image")
        st_space("v", 2)

        # Styled image
        st_write(bs.sub, "Image with style", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Apply StreamTeX styles (borders, padding) to images.
        """)
        st_space("v", 1)

        bordered_img = (s.container.borders.solid_border
                        + s.container.paddings.tiny_padding)
        show_code("""\
bordered_img = (s.container.borders.solid_border
                + s.container.paddings.tiny_padding)
st_image(bordered_img,
         uri=theImageURL2, width="300px",
         alt="Bordered image")""")
        st_space("v", 1)

        st_image(bordered_img, uri=theImageURL2,
                 width="300px", alt="Bordered image")
        st_space("v", 2)

        # Image with link
        st_write(bs.sub, "Image as a link", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Wrap an image in a clickable link with the link parameter.
        """)
        st_space("v", 1)

        theURL = "https://docs.streamlit.io"
        show_code("""\
theURL = "https://docs.streamlit.io"
st_image(uri=theImageURL2, width="300px",
         link=theURL,
         alt="Click to visit Streamlit docs")""")
        st_space("v", 1)

        st_image(uri=theImageURL2, width="300px",
                 link=theURL,
                 alt="Click to visit Streamlit docs")
        st_space("v", 2)

        # configure_image_path
        st_write(bs.sub, "configure_image_path()", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Sets the base path for resolving relative image filenames.
        """)
        st_space("v", 1)

        show_code('configure_image_path("app/static/images")')
        st_space("v", 1)

        show_details("""\
            Defaults: width="100%", height="auto", link="", hover=True.

            Always set the alt parameter for accessibility.
            The alt text is used by screen readers
            and displayed when images fail to load.
        """)
        st_space("v", 2)

        # Editable image
        st_write(bs.sub, "Editable Image", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Add editable=True to any st_image() call to enable an
            interactive editor panel. Users can rename the image,
            replace it from a URL or local file, generate a new version
            with AI, and browse the version history.
        """)
        st_space("v", 1)

        show_code("""\
# Editable image — editor panel appears below the image
st_image(uri=theImageURL, editable=True, name="demo_edit",
         width="300px", alt="Editable demo image")""")
        st_space("v", 1)

        st_image(uri=theImageURL, editable=True, name="demo_edit",
                 width="300px", alt="Editable demo image")
        st_space("v", 1)

        show_details("""\
            editable=True requires a name parameter (used for file
            management and version history). The editor panel is
            automatically hidden during HTML/PDF export.

            AI generation requires streamtex[ai] and provider
            configuration — see the AI manual for details.
        """)
        st_space("v", 2)

        # Bounds relative to the window (0.7.37)
        st_write(bs.sub, "Window bounds — max_vw= / max_vh=", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Bound one image by the window, per call: max_vw is a
            percentage of the window width, max_vh of the window height.
            The image takes min(width, max_vw vw, max_vh vh x ratio) —
            the largest size inside every bound, never distorted. The
            ratio is read from the local or served file (or from
            natural_size=, or from the cropped zone when crop= is set).
        """)
        st_space("v", 1)

        show_code("""\
st_image(uri="crop/crop_demo_screenshot.png",
         max_vh=30,
         alt="Never taller than 30% of the window")""")
        st_space("v", 1)

        st_image(uri="crop/crop_demo_screenshot.png",
                 max_vh=30,
                 alt="Never taller than 30% of the window")
        st_space("v", 1)

        show_details("""\
            height must stay "auto" with a bound (an explicit height= is
            refused: the bounds already fix the size). A remote URI
            without natural_size= has no readable ratio: the bounds then
            become CSS max-width / max-height (the image is never
            enlarged). st_video is not covered.
        """)
        st_space("v", 2)

        # Explicit placement (0.7.37)
        st_write(bs.sub, "Placement — align=", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            By default an image follows the alignment of its container
            (this whole page is inside st_block(s.center_txt), so its
            images are centred). align="left" | "center" | "right" places
            one image locally, contradicting its container.
        """)
        st_space("v", 1)

        show_code("""\
st_image(uri=theImageURL, width="200px", align="left",
         alt="Placed on the left of a centred container")""")
        st_space("v", 1)

        st_image(uri=theImageURL, width="200px", align="left",
                 alt="Placed on the left of a centred container")
        st_space("v", 1)

        show_details("""\
            Design decision: placement is always written with align=.
            The text-align inside a style passed to st_image does NOT
            place the image — it applies to the `<img>` itself, so

                st_image(s.center_txt, uri=..., ...)   # does NOT centre

            leaves the image wherever its container puts it. Write
            st_image(uri=..., align="center") instead. Reinterpreting
            text-align would have moved images in existing documents
            (102 blocks of one project changed their HTML when it was
            tried), so the library keeps the explicit parameter.
        """)

