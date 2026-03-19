"""AI Image Generation — Usage patterns (declarative + interactive).

Part 8: Advanced — Shows how to use st_ai_image() in blocks and
st_ai_image_widget() for interactive generation.
"""

from streamtex import st_write, st_space, st_block, st_grid, st_image, st_list
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

    # ── ImageMetadata ─────────────────────────────────────────
    st_write(bs.sub, "ImageMetadata", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    show_explanation("""\
        Every generated or managed image has a JSON sidecar file
        containing an ImageMetadata dataclass. It records the full
        provenance: prompt, provider, model, size, quality, version
        number, and timestamp.
    """)
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        st_write(s.bold + s.large, "ImageMetadata Fields", tag=t.div)
        st_space("v", 1)
        with st_list(list_type="ul") as l:
            with l.item(): st_write(bs.body, (s.bold, "name"), " — semantic name (e.g. 'hero_intro')")
            with l.item(): st_write(bs.body, (s.bold, "version"), " — current version number (int)")
            with l.item(): st_write(bs.body, (s.bold, "timestamp"), " — ISO 8601 creation time")
            with l.item(): st_write(bs.body, (s.bold, "source_type"), " — 'local', 'url', or 'ai_generated'")
            with l.item(): st_write(bs.body, (s.bold, "original_path"), " — original source path or URL")
            with l.item(): st_write(bs.body, (s.bold, "prompt"), " — AI prompt (None for non-AI images)")
            with l.item(): st_write(bs.body, (s.bold, "provider"), " — AI provider name")
            with l.item(): st_write(bs.body, (s.bold, "model"), " — AI model identifier")
            with l.item(): st_write(bs.body, (s.bold, "size"), " — AI generation size")
            with l.item(): st_write(bs.body, (s.bold, "quality"), " — AI generation quality")
            with l.item(): st_write(bs.body, (s.bold, "base_image"), " — path to base image for img2img")
            with l.item(): st_write(bs.body, (s.bold, "revised_prompt"), " — provider-revised prompt")
    st_space("v", 1)

    show_code("""\
        from streamtex.ai.metadata import ImageMetadata, load_metadata, metadata_path_for

        # Load metadata for a managed image
        json_path = metadata_path_for("static/images/managed/hero_banner.png")
        meta = load_metadata(json_path)

        if meta:
            print(f"Name: {meta.name}, Version: {meta.version}")
            print(f"Provider: {meta.provider}, Model: {meta.model}")
            print(f"Prompt: {meta.prompt}")
            print(f"Generated at: {meta.timestamp}")""", language="python")
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

    # ── Unified Editable Mode (NEW) ─────────────────────────────
    st_write(bs.sub, "Unified Editable Mode — st_image(editable=True)", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_block(s.project.containers.good_callout):
        st_write(bs.feature_title, "Recommended Approach", tag=t.div)
        st_space("v", 1)
        st_write(
            bs.body,
            "The unified ",
            (s.bold, "st_image(editable=True)"),
            " replaces separate st_ai_image() calls. It works with ",
            (s.bold, "any image"),
            " — local, URL, or AI-generated — and adds an editor "
            "panel with AI generation, img2img, and version history.",
        )
    st_space("v", 1)

    show_code("""\
        # blocks/bck_hero.py — unified editable image
        from streamtex import st_image, st_write, st_space
        from custom.styles import Styles as s

        def build():
            st_write(s.huge + s.bold, "Hero Section", tag=t.div)
            st_space("v", 2)

            # Editable AI image — editor panel with generate + history
            st_image(
                uri="hero_banner.png",
                editable=True,
                name="hero_banner",
                prompt="A futuristic city skyline at sunset, digital art",
                provider="openai",
                width="100%",
            )""", language="python")
    st_space("v", 2)

    # ── Image-to-Image ────────────────────────────────────────
    st_write(bs.sub, "Image-to-Image (img2img)", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    show_explanation("""\
        The editor panel includes an "Use current as base" checkbox.
        When enabled, the current image is sent to the AI provider
        as a reference for the new generation. All three providers
        support img2img: OpenAI (images.edit), Google (edit_image),
        and fal.ai (image-to-image model).
    """)
    st_space("v", 1)

    show_code("""\
        # Programmatic img2img via generate_image()
        from streamtex.ai import generate_image
        from pathlib import Path

        base = Path("static/images/managed/hero_banner.png").read_bytes()
        path = generate_image(
            "Same scene but with neon lights and rain",
            provider="openai",
            base_image=base,
        )""", language="python")
    st_space("v", 2)

    # ── Version History ───────────────────────────────────────
    st_write(bs.sub, "Version History API", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    show_explanation("""\
        Every generation or replacement creates a versioned archive.
        The History tab in the editor panel lets users browse and
        restore previous versions. The API is also available
        programmatically.
    """)
    st_space("v", 1)

    show_code("""\
        from streamtex import (
            save_image_version, get_current_image,
            list_image_versions, rollback_image, rename_image,
        )

        # Save a new version (returns version number)
        ver = save_image_version("hero_banner", image_bytes,
                                 source_type="ai", prompt="...",
                                 provider="openai")

        # List all versions
        versions = list_image_versions("hero_banner")

        # Rollback to a previous version
        rollback_image("hero_banner", version=2)

        # Rename (renames all versions + metadata)
        rename_image("hero_banner", "main_hero")""", language="python")
    st_space("v", 2)

    # ── Deprecation Note ──────────────────────────────────────
    with st_block(s.project.containers.note_callout):
        st_write(s.project.titles.warning_label, "Migration Note", tag=t.div)
        st_space("v", 1)
        st_write(
            bs.body,
            (s.bold, "st_ai_image()"),
            " and ",
            (s.bold, "st_ai_image_widget()"),
            " still work but are deprecated in favor of ",
            (s.bold, "st_image(editable=True, prompt=...)"),
            ". Existing code continues to function — st_ai_image() "
            "now internally passes editable=True to st_image().",
        )
    st_space("v", 2)

    # ── Complete Example ──────────────────────────────────────
    st_write(bs.sub, "Complete Example — From Generation to Traceability", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    show_explanation("""\
        This example shows the full workflow: generate an AI image,
        display it with the editable panel, and inspect the JSON
        metadata file created automatically for traceability.
    """)
    st_space("v", 1)

    # Step 1: Code example
    st_write(s.bold + s.large, "1. Block code", tag=t.div)
    st_space("v", 1)

    show_code("""\
        # blocks/bck_hero.py — complete editable AI image example
        from streamtex import st_image, st_write, st_space
        from streamtex.enums import Tags as t
        from custom.styles import Styles as s

        def build():
            st_write(s.huge + s.bold + s.center_txt,
                     "Welcome", tag=t.div, toc_lvl="1")
            st_space("v", 2)

            # Display an image with the AI editor panel.
            # - If a managed version exists (from a previous generation),
            #   it is displayed automatically instead of the original URI.
            # - The editor panel lets the user generate a new AI image,
            #   replace from URL/file, and browse version history.
            st_image(
                uri="images/hero_banner.png",
                editable=True,
                name="hero_banner",
                prompt="A futuristic city at sunset, digital art style",
                provider="openai",
                width="100%",
                alt="Hero banner image",
            )""", language="python")
    st_space("v", 2)

    # Step 2: Live demo
    st_write(s.bold + s.large, "2. Live result (editable)", tag=t.div)
    st_space("v", 1)

    st_write(
        bs.body,
        "The image below uses ",
        (s.bold, "editable=True"),
        ". Click ",
        (s.bold, "Edit Image"),
        " to open the editor panel, then the ",
        (s.bold, "AI Generate"),
        " tab to create a new version.",
    )
    st_space("v", 1)

    st_image(
        uri="ai/ai_openai_demo.png",
        editable=True,
        name="ai_usage_demo",
        prompt="A futuristic city at sunset, digital art style",
        provider="openai",
        width="400px",
        alt="AI generation demo image",
    )
    st_space("v", 2)

    # Step 3: JSON traceability
    st_write(s.bold + s.large, "3. Traceability — JSON metadata", tag=t.div)
    st_space("v", 1)

    st_write(
        bs.body,
        "Each generated or replaced image gets a ",
        (s.bold, ".json sidecar"),
        " file in ",
        (s.bold, "static/images/managed/"),
        " that records full provenance:",
    )
    st_space("v", 1)

    show_code("""\
        // static/images/managed/hero_banner.json
        {
          "name": "hero_banner",
          "version": 1,
          "timestamp": "2026-03-10T15:45:09.272394+00:00",
          "source_type": "ai_generated",
          "original_path": "static/images/ai/c0a84cc973412ca8.png",
          "prompt": "A futuristic city at sunset, digital art style",
          "provider": "openai",
          "model": "gpt-image-1",
          "size": "1024x1024",
          "quality": "standard",
          "base_image": null,
          "revised_prompt": null
        }""", language="json")
    st_space("v", 1)

    show_explanation("""\
        When you regenerate or replace the image, the current version
        is archived as hero_banner_v1.png + .json, and the new image
        becomes the current version (v2, v3, ...). Use the History
        tab in the editor panel — or the rollback_image() API — to
        restore any previous version.
    """)
    st_space("v", 1)

    st_slide_break(marker_label="AI Image: Version History")
