"""AI Image Generation — Usage patterns (declarative + interactive).

Part 8: Advanced — Shows how to use st_ai_image() in blocks and
st_ai_image_widget() for interactive generation.
"""

from streamtex import st_write, st_space, st_block, st_grid, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, st_slide_break


class BlockStyles:
    """AI Image Usage block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    feature_title = s.project.colors.ai_violet + s.bold + s.Large
    body = s.large


bs = BlockStyles


def build():
    """Render the AI Image Usage section."""
    st_space("v", 1)
    st_write(bs.heading, "Using AI Images in Blocks", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── Declarative Mode ───────────────────────────────────────
    st_write(bs.sub, "Declarative Mode — st_ai_image()", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    show_explanation("""\
        Use st_ai_image() directly in your block code. The image is
        generated once, saved to static/images/ai/, and reused on
        subsequent reruns. It delegates display to st_image(), so the
        export pipeline (HTML/PDF) works automatically.
    """)
    st_space("v", 1)

    show_code("""\
        # blocks/bck_hero.py — AI image in a block
        from streamtex import st_ai_image, st_write, st_space, st_grid
        from custom.styles import Styles as s

        class BlockStyles:
            heading = s.huge + s.bold + s.center_txt
            body = s.large

        bs = BlockStyles

        def build():
            st_write(bs.heading, "Neural Network Architecture", tag=t.div)
            st_space("v", 2)

            with st_grid(cols="repeat(auto-fit, minmax(350px, 1fr))", gap="24px") as g:
                with g.cell():
                    # AI-generated image — cached on disk after first generation
                    st_ai_image(
                        "A minimalist flat-design diagram of a deep neural "
                        "network with 3 hidden layers, dark background, "
                        "blue and violet nodes, clean vector style",
                        width="100%",
                        provider="openai",
                        size="1024x1024",
                    )
                with g.cell():
                    st_write(bs.body, "The architecture features ...")""", language="python")
    st_space("v", 2)

    # ── Claude Workflow ────────────────────────────────────────
    st_write(bs.sub, "Claude as Image Designer", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_block(s.project.containers.ai_callout):
        st_write(bs.feature_title, "How Claude Uses AI Images", tag=t.div)
        st_space("v", 1)
        st_write(
            bs.body,
            "When you ask Claude to create a presentation with images, "
            "it uses ",
            (s.bold, "generate_image()"),
            " to create the files, then references them with regular ",
            (s.bold, "st_image()"),
            " calls. The images are committed to your project — no API "
            "dependency at runtime.",
        )
    st_space("v", 1)

    show_code("""\
        # What Claude does behind the scenes:
        from streamtex.ai import generate_image

        # 1. Generate and save to static/images/ai/
        path = generate_image(
            "A futuristic city skyline at sunset, digital art",
            provider="openai",
        )
        # path = "static/images/ai/a3f8b2c1e9d0.png"

        # 2. Reference in the block with regular st_image()
        st_image(uri=path, width="100%")
        # The image file is now part of the project — no API needed""",
        language="python")
    st_space("v", 2)

    # ── Interactive Widget ─────────────────────────────────────
    st_write(bs.sub, "Interactive Mode — st_ai_image_widget()", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    show_explanation("""\
        For dynamic blocks where the end-user enters a prompt,
        use st_ai_image_widget(). It provides a text area, provider
        selector, generate button, and a save-to-project button.
    """)
    st_space("v", 1)

    show_code("""\
        # blocks/bck_image_lab.py — interactive image generation
        from streamtex import st_ai_image_widget, st_write, st_space
        from custom.styles import Styles as s

        class BlockStyles:
            heading = s.huge + s.bold + s.center_txt

        bs = BlockStyles

        def build():
            st_write(bs.heading, "Image Lab", tag=t.div, toc_lvl="2")
            st_space("v", 2)

            # Interactive widget — user types prompt + clicks Generate
            st_ai_image_widget(
                default_prompt="A serene mountain landscape at dawn",
                provider="openai",
                key="image_lab",
                show_save=True,   # Adds "Save to static/images/" button
            )""", language="python")
    st_space("v", 2)

    # ── Parameters Reference ───────────────────────────────────
    st_write(bs.sub, "Parameters Reference", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_grid(cols="repeat(auto-fit, minmax(350px, 1fr))", gap="16px") as g:
        with g.cell():
            with st_block(s.project.containers.explanation_box):
                st_write(s.bold + s.large, "st_ai_image()", tag=t.div)
                st_space("v", 1)
                with st_list(list_type="ul") as l:
                    with l.item(): st_write(bs.body, (s.bold, "prompt"), " — text description")
                    with l.item(): st_write(bs.body, (s.bold, "style"), " — StreamTeX Style object")
                    with l.item(): st_write(bs.body, (s.bold, "provider"), " — override default provider")
                    with l.item(): st_write(bs.body, (s.bold, "size"), " — e.g. '1024x1024'")
                    with l.item(): st_write(bs.body, (s.bold, "quality"), " — 'standard' or 'hd'")
                    with l.item(): st_write(bs.body, (s.bold, "model"), " — model override")
                    with l.item(): st_write(bs.body, (s.bold, "alt, link, hover, light_bg"), " — same as st_image")
        with g.cell():
            with st_block(s.project.containers.details_box):
                st_write(s.bold + s.large, "st_ai_image_widget()", tag=t.div)
                st_space("v", 1)
                with st_list(list_type="ul") as l:
                    with l.item(): st_write(bs.body, (s.bold, "default_prompt"), " — pre-filled prompt")
                    with l.item(): st_write(bs.body, (s.bold, "provider"), " — default provider")
                    with l.item(): st_write(bs.body, (s.bold, "key"), " — Streamlit widget key")
                    with l.item(): st_write(bs.body, (s.bold, "show_save"), " — Save button visible")
                    with l.item(): st_write(bs.body, (s.bold, "style, width, height"), " — display styles")
                    with l.item(): st_write(bs.body, (s.bold, "config"), " — AIImageConfig override")
    st_space("v", 2)

    # ── Caching ────────────────────────────────────────────────
    st_write(bs.sub, "Cache and Cost Control", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_block(s.project.containers.note_callout):
        st_write(s.project.titles.warning_label, "Important", tag=t.div)
        st_space("v", 1)
        st_write(
            bs.body,
            "Images are cached on disk using a ",
            (s.bold, "deterministic hash"),
            " of (prompt + provider + size + quality + seed). ",
            "Same parameters = same file = ",
            (s.bold, "zero API cost"),
            " on Streamlit reruns. Use ",
            (s.bold, "manual mode"),
            " (default) to avoid accidental generation.",
        )
    st_space("v", 1)

    st_slide_break()
