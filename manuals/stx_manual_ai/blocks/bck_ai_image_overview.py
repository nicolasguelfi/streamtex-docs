"""AI Image Generation — Overview and configuration of external AI providers.

Part 8: Advanced — Introduces the st_ai_image() / st_ai_image_widget()
functions and how to configure AI providers (OpenAI, Google Imagen, fal.ai).
"""

from streamtex import st_write, st_space, st_block, st_grid, st_image
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details, st_slide_break


class BlockStyles:
    """AI Image Overview block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    provider_title = s.project.colors.ai_violet + s.bold + s.Large
    feature_label = s.project.colors.tech_blue + s.bold + s.large
    body = s.large


bs = BlockStyles


def build():
    """Render the AI Image Generation overview section."""
    st_space("v", 1)
    st_write(bs.heading, "AI Image Generation", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        StreamTeX integrates with external AI providers to generate
        images directly from text prompts. You can use AI-generated
        images in two ways: declaratively in block code, or
        interactively via a widget in the browser.
    """)
    st_space("v", 2)

    # ── Supported Providers ─────────────────────────────────────
    st_write(bs.sub, "Supported Providers", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_grid(cols="repeat(auto-fit, minmax(280px, 1fr))", gap="16px") as g:
        with g.cell():
            with st_block(s.project.containers.ai_callout):
                st_write(bs.provider_title, "OpenAI", tag=t.div)
                st_space("v", 1)
                st_write(
                    bs.body,
                    "GPT-Image (gpt-image-1). High quality, ",
                    (s.bold, "prompt interpretation"), " with ",
                    (s.bold, "revised_prompt"), " feedback.",
                )
                st_space("v", 1)
                st_image(uri="ai/ai_openai_demo.png", width="100%")
        with g.cell():
            with st_block(s.project.containers.tip_callout):
                st_write(bs.provider_title, "Google Imagen", tag=t.div)
                st_space("v", 1)
                st_write(
                    bs.body,
                    "Imagen 4 (imagen-4.0-generate-001). ",
                    "Photorealistic output, strong on ",
                    (s.bold, "text-in-image"), " rendering.",
                )
                st_space("v", 1)
                st_image(uri="ai/ai_google_demo.png", width="100%")
        with g.cell():
            with st_block(s.project.containers.note_callout):
                st_write(bs.provider_title, "fal.ai", tag=t.div)
                st_space("v", 1)
                st_write(
                    bs.body,
                    "Stable Diffusion v3.5 Large. Open-source, ",
                    (s.bold, "fast generation"), ", ",
                    (s.bold, "customizable"), " parameters.",
                )
                st_space("v", 1)
                st_image(uri="ai/ai_fal_demo.png", width="100%")
    st_space("v", 2)

    # ── Configuration ──────────────────────────────────────────
    st_write(bs.sub, "Configuration", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    st_write(
        bs.body,
        "Configuration follows the same ",
        (s.bold, "DI pattern"),
        " as GSheetConfig and LinkConfig — call ",
        (s.bold, "set_ai_image_config()"),
        " once in your book.py:",
    )
    st_space("v", 1)

    show_code("""\
        # book.py — configure AI image generation
        from streamtex import set_ai_image_config, AIImageConfig

        set_ai_image_config(AIImageConfig(
            provider="openai",         # "openai" | "google" | "fal"
            default_size="1024x1024",  # Default image dimensions
            output_dir="static/images/ai",  # Where images are saved
            auto_generate=False,       # Manual mode (button required)
        ))""", language="python")
    st_space("v", 2)

    # ── API Keys ───────────────────────────────────────────────
    st_write(bs.sub, "API Keys", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    st_write(
        bs.body,
        "API keys are resolved from environment variables. Add them ",
        "to your ",
        (s.bold, ".env"),
        " file (local) or Render env vars (deployed):",
    )
    st_space("v", 1)

    show_code("""\
        # .env — one key per provider you use
        STX_OPENAI_API_KEY=sk-...
        STX_GOOGLE_AI_KEY=AIza...
        STX_FAL_KEY=fal-...""", language="bash", line_numbers=False)
    st_space("v", 1)

    show_details("""\
        Key resolution priority: explicit api_keys dict in AIImageConfig
        > STX_*_KEY env vars > provider default env vars
        (OPENAI_API_KEY, GOOGLE_AI_KEY, FAL_KEY).
    """)
    st_space("v", 1)

    # ── Installation ───────────────────────────────────────────
    st_write(bs.sub, "Installation", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    st_write(bs.body, "Install only the provider SDKs you need:")
    st_space("v", 1)

    show_code("""\
        # All providers
        uv add "streamtex[ai]"

        # Or individual providers
        uv add "streamtex[ai-openai]"
        uv add "streamtex[ai-google]"
        uv add "streamtex[ai-fal]" """, language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Generation Modes ───────────────────────────────────────
    st_write(bs.sub, "Manual vs Auto Mode", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_grid(cols="repeat(auto-fit, minmax(350px, 1fr))", gap="16px") as g:
        with g.cell():
            with st_block(s.project.containers.good_callout):
                st_write(bs.feature_label, "Manual Mode (default)", tag=t.div)
                st_space("v", 1)
                st_write(
                    bs.body,
                    "auto_generate=False. If the image is not cached, ",
                    "a placeholder with a ",
                    (s.bold, "Generate button"),
                    " is shown. No API call until you click.",
                )
        with g.cell():
            with st_block(s.project.containers.tip_callout):
                st_write(bs.feature_label, "Auto Mode", tag=t.div)
                st_space("v", 1)
                st_write(
                    bs.body,
                    "auto_generate=True. Images are generated ",
                    (s.bold, "immediately"), " if not cached. ",
                    "Use for batch generation or scripted workflows.",
                )
    st_space("v", 1)

    show_details("""\
        In both modes, generated images are cached on disk. The cache
        key is a hash of prompt + provider + size + quality + seed.
        Same parameters = same file = no API call on Streamlit reruns.
    """)
    st_space("v", 1)

    st_slide_break()
