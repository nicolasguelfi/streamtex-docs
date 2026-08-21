# Edge cropping — % cut from each edge, CSS inset order:
# (top, right, bottom, left) — same convention as clip-path/margin/padding.
# width designates the VISIBLE zone (the crop result), not the source.

# Local file: natural dimensions read automatically (Pillow / SVG viewBox)
st_image(uri="crop/crop_demo_screenshot.png", width="500px",
         crop=(5, 20, 15, 10),
         alt="Screenshot cropped to its content zone")

# Remote URI: pass the natural dimensions explicitly (v1)
st_image(uri="https://picsum.photos/seed/streamtex1/400/250",
         width="200px", crop=(10, 10, 10, 10),
         natural_size=(400, 250),
         alt="Remote image cropped by 10% on every edge")

# Dataclass form — named fields, no order to memorize
from streamtex import CropConfig
st_image(uri="captures/x.png", width="44vw",
         crop=CropConfig(top=4, bottom=10, left=6))
