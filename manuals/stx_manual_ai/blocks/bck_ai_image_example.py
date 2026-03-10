"""AI Image Generation — Complete worked example with editable mode and traceability.

Part 8: Advanced — End-to-end example: insert an AI-generated image in
editable mode, then display the JSON metadata sidecar for traceability.
"""

import json
import os
from pathlib import Path

from streamtex import st_write, st_space, st_block, st_grid, st_image, st_code, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, st_slide_break


class BlockStyles:
    """AI Image Example block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    label = s.project.colors.ai_violet + s.bold + s.Large
    body = s.large


bs = BlockStyles

# Resolve paths relative to this manual
_manual_dir = Path(__file__).resolve().parent.parent
_managed_dir = _manual_dir / "static" / "images" / "managed"


def build():
    """Render the AI Image complete example section."""
    st_space("v", 1)
    st_write(bs.heading, "Complete Example — Editable AI Image", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        This example shows the full workflow: insert an AI-generated
        image with editable=True, let the user regenerate or replace
        it, and inspect the JSON metadata file that StreamTeX creates
        automatically for traceability.
    """)
    st_space("v", 2)

    # ── Step 1: The Code ──────────────────────────────────────
    st_write(bs.sub, "Step 1 — Block Code", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    show_code("""\
        # blocks/bck_hero.py — editable AI image with traceability
        from streamtex import st_image, st_write, st_space
        from streamtex.enums import Tags as t
        from custom.styles import Styles as s

        class BlockStyles:
            heading = s.huge + s.bold + s.center_txt
            body = s.large

        bs = BlockStyles

        def build():
            st_write(bs.heading, "Hero Section", tag=t.div, toc_lvl="1")
            st_space("v", 2)

            # Editable AI image — click the pencil icon to:
            #   - Regenerate with a new prompt
            #   - Switch provider (OpenAI / Google / fal.ai)
            #   - Use current image as base (img2img)
            #   - Browse version history
            st_image(
                uri="hero_banner.png",   # Initial or fallback image
                editable=True,           # Enables the editor panel
                name="hero_banner",      # Semantic name → managed folder
                prompt="A futuristic cityscape at sunset with neon "
                       "lights reflecting on glass buildings, "
                       "digital art, wide angle, cinematic",
                provider="openai",       # Default provider
                width="100%",
            )
            # StreamTeX creates:
            #   static/images/managed/hero_banner.png  (the image)
            #   static/images/managed/hero_banner.json (metadata)""",
        language="python")
    st_space("v", 2)

    # ── Step 2: Live Result ───────────────────────────────────
    st_write(bs.sub, "Step 2 — Live Result (editable)", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    st_write(
        bs.body,
        "Below is a live editable image. Click the ",
        (s.bold, "pencil icon"),
        " to open the editor panel where you can regenerate, "
        "change the prompt, switch provider, or browse version history.",
    )
    st_space("v", 1)

    st_image(
        uri="ai/ai_openai_demo.png",
        editable=True,
        name="demo_ai_example",
        prompt="A futuristic cityscape at sunset with neon "
               "lights reflecting on glass buildings, "
               "digital art, wide angle, cinematic",
        provider="openai",
        width="100%",
    )
    st_space("v", 2)

    # ── Step 3: JSON Metadata ─────────────────────────────────
    st_write(bs.sub, "Step 3 — JSON Metadata (traceability)", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    show_explanation("""\
        Every time an image is generated or replaced via the editor,
        StreamTeX writes a JSON sidecar file next to the image.
        This file records the full provenance: prompt, provider,
        model, size, quality, timestamp, and version number.
    """)
    st_space("v", 1)

    # Try to load the actual metadata file for the demo image
    _meta_path = _managed_dir / "demo_ai_example.json"
    if os.path.isfile(_meta_path):
        with open(_meta_path, encoding="utf-8") as f:
            meta = json.load(f)
        meta_json = json.dumps(meta, indent=2, ensure_ascii=False)
        _label = "Live metadata from static/images/managed/demo_ai_example.json"
    else:
        # Show a representative example if the file doesn't exist yet
        meta_json = json.dumps({
            "name": "demo_ai_example",
            "version": 1,
            "timestamp": "2026-03-10T14:32:07.123456+00:00",
            "source_type": "ai_generated",
            "original_path": "static/images/ai/a3f8b2c1e9d0.png",
            "prompt": "A futuristic cityscape at sunset with neon "
                      "lights reflecting on glass buildings, "
                      "digital art, wide angle, cinematic",
            "provider": "openai",
            "model": "gpt-image-1",
            "size": "1024x1024",
            "quality": "standard",
            "base_image": None,
            "revised_prompt": None,
        }, indent=2, ensure_ascii=False)
        _label = "Example metadata (generate the image above to see the real file)"

    with st_block(s.project.containers.ai_callout):
        st_write(bs.label, "Metadata Sidecar — hero_banner.json", tag=t.div)
        st_space("v", 1)
        st_write(bs.body, _label)
        st_space("v", 1)
        st_code(code=meta_json, language="json")
    st_space("v", 2)

    # ── Metadata Fields Explained ──────────────────────────────
    st_write(bs.sub, "Metadata Fields", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_grid(cols="repeat(auto-fit, minmax(320px, 1fr))", gap="16px") as g:
        with g.cell():
            with st_block(s.project.containers.explanation_box):
                st_write(s.bold + s.large, "Identity & Versioning", tag=t.div)
                st_space("v", 1)
                with st_list(list_type="ul") as l:
                    with l.item(): st_write(bs.body, (s.bold, "name"), " — semantic identifier (matches the file name)")
                    with l.item(): st_write(bs.body, (s.bold, "version"), " — auto-incremented on each generation")
                    with l.item(): st_write(bs.body, (s.bold, "timestamp"), " — ISO 8601 UTC creation time")
                    with l.item(): st_write(bs.body, (s.bold, "source_type"), " — 'local', 'url', or 'ai_generated'")
        with g.cell():
            with st_block(s.project.containers.details_box):
                st_write(s.bold + s.large, "AI Generation Details", tag=t.div)
                st_space("v", 1)
                with st_list(list_type="ul") as l:
                    with l.item(): st_write(bs.body, (s.bold, "prompt"), " — exact prompt sent to the provider")
                    with l.item(): st_write(bs.body, (s.bold, "provider"), " — openai, google, or fal")
                    with l.item(): st_write(bs.body, (s.bold, "model"), " — model identifier used")
                    with l.item(): st_write(bs.body, (s.bold, "size"), " — generation resolution")
                    with l.item(): st_write(bs.body, (s.bold, "quality"), " — standard or hd")
                    with l.item(): st_write(bs.body, (s.bold, "base_image"), " — source for img2img (null if from scratch)")
                    with l.item(): st_write(bs.body, (s.bold, "revised_prompt"), " — provider-revised prompt (OpenAI)")
    st_space("v", 2)

    # ── Key Takeaways ─────────────────────────────────────────
    with st_block(s.project.containers.good_callout):
        st_write(bs.label, "Key Takeaways", tag=t.div)
        st_space("v", 1)
        with st_list(list_type="ul") as l:
            with l.item(): st_write(bs.body, (s.bold, "One function"), " — st_image(editable=True) handles display + editing + generation")
            with l.item(): st_write(bs.body, (s.bold, "Full traceability"), " — every generation creates a JSON sidecar with prompt, provider, model, timestamp")
            with l.item(): st_write(bs.body, (s.bold, "Version history"), " — previous versions are archived; rollback via the editor or API")
            with l.item(): st_write(bs.body, (s.bold, "No runtime dependency"), " — generated images are committed to static/; no API key needed at deploy time")
    st_space("v", 1)

    st_slide_break()
