from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """AI image editor styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Image Editor & Model Capabilities",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- 1. Editor overview ---
        st_write(bs.sub, "The 4-tab image editor", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            When `st_image(editable=True, name="...")` is used, a
            collapsible editor panel appears below the image with
            four tabs:

            **Source** — Rename the image, replace from a local path or URL.

            **AI Generate** — Select provider/model, size and quality
            (populated dynamically from ModelCapabilities), edit the
            prompt, toggle img2img mode.

            **History** — Browse all versions, rollback to a previous one.

            **Display** — Adjust how the image renders: proportional
            zoom slider (10-200%), manual width/height with CSS units
            (px, %, vw, vh), and a keep-ratio toggle.
        """)
        st_space("v", 2)

        # --- 2. Display tab ---
        st_write(bs.sub, "Display tab — zoom and sizing", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The Display tab lets you control image rendering without
            changing the source image. Settings are persisted in the
            image metadata JSON and applied automatically on every render.
        """)
        st_space("v", 1)

        show_code("""\
# Display settings are stored in the metadata JSON:
# static/images/managed/hero_title.json
{
    "name": "hero_title",
    "display_zoom": 35,          # Proportional zoom (%)
    "display_width": null,       # Manual width (CSS value, e.g. "80%", "400px")
    "display_height": null,      # Manual height (CSS value)
    "display_keep_ratio": true   # Preserve aspect ratio
}

# Priority: manual width/height > zoom > original st_image(width=)
# The zoom slider overrides the width parameter from st_image()
# Manual width/height override both""", language="json")
        st_space("v", 2)

        # --- 3. Model Capabilities ---
        st_write(bs.sub, "ModelCapabilities — dynamic size/quality", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Each AI provider declares its supported sizes and quality
            levels per model. The image editor queries these dynamically
            to populate the size/quality dropdowns — no more rejected
            requests from using an unsupported size.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex.ai.providers.registry import get_model_capabilities

# Query capabilities for a specific model
caps = get_model_capabilities("openai", "gpt-image-1")
print(caps.sizes)           # ["1024x1024", "1024x1536", "1536x1024"]
print(caps.qualities)       # ["auto", "low", "medium", "high"]
print(caps.default_size)    # "1536x1024"
print(caps.default_quality) # "auto"

# Different model, different capabilities
caps = get_model_capabilities("openai", "dall-e-3")
print(caps.sizes)           # ["1024x1024", "1024x1792", "1792x1024"]
print(caps.qualities)       # ["standard", "hd"]""", language="python")
        st_space("v", 2)

        # --- 4. Adding a new provider ---
        st_write(bs.sub, "Adding model capabilities to a provider", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# In streamtex/ai/providers/my_provider.py
from .base import AIImageProvider, AIImageResult, ModelCapabilities

class MyProvider(AIImageProvider):
    name = "my_provider"

    @classmethod
    def available_models(cls) -> list[str]:
        return ["model-v1", "model-v2"]

    @classmethod
    def model_capabilities(cls, model=None) -> ModelCapabilities:
        if model == "model-v2":
            return ModelCapabilities(
                sizes=["512x512", "1024x1024", "2048x2048"],
                qualities=["draft", "standard", "hd"],
                default_size="1024x1024",
                default_quality="standard",
            )
        # Default for model-v1
        return ModelCapabilities(
            sizes=["512x512", "1024x1024"],
            qualities=["standard"],
        )""", language="python")
        st_space("v", 2)

        show_details("""\
            ModelCapabilities is a dataclass with four fields:
            `sizes` (list of "WxH" strings), `qualities` (list of
            quality level strings), `default_size`, and `default_quality`.

            The image editor calls `get_model_capabilities(provider, model)`
            from the registry. If the provider doesn't override
            `model_capabilities()`, the base class returns a generic
            fallback (1024x1024, standard).

            When adding a new AI model to an existing provider, just
            add a branch in `model_capabilities()` — the editor UI
            adapts automatically.
        """)
