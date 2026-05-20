"""Pack Engineering — overview of the orchestrated pack lifecycle."""

from streamtex import st_block, st_code, st_space, st_write
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem
from streamtex_design.components.callout import callout
from streamtex_design.components.term_definition_list import term_definition_list


DS = DesignSystem()


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    code_box = s.container.paddings.small_padding + s.container.borders.solid_border


bs = BlockStyles


def build():
    """Introduce the Pack Engineering (PE) lifecycle and its six sub-modes."""
    st_write((bs.heading, "Pack Engineering — overview"), toc_lvl="1", tag=t.div)
    st_space(10)
    st_write(
        bs.body + s.center_txt,
        "When the project's library grows beyond manual capture, Pack "
        "Engineering (PE) is the orchestrated lifecycle that takes N "
        "existing projects and produces (or enriches) a shared pack — "
        "with full audit trail, validation gates, and automatic retrofit "
        "of the consumer projects.",
        tag=t.div,
    )
    st_space(20)

    # ---- Where PE fits ----
    st_write((bs.sub, "Where PE fits"), toc_lvl="+1", tag=t.div)
    st_space(10)
    callout(
        design_system=DS,
        variant="info",
        title="The bridge between CE capture and pack publication",
        body=(
            "PE sits between CE capture (project-local, one component at "
            "a time) and pack publication (versioned release to PyPI). "
            "It turns a folder of authored blocks into a reusable, "
            "versioned design pack — and rewrites the source projects "
            "to consume it."
        ),
    )
    st_space(20)

    # ---- Six sub-modes ----
    st_write((bs.sub, "Six sub-modes"), toc_lvl="+1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "The same 7-step sequencer (DISCOVERY → DESIGN → IMPLEMENT → "
        "ADOPT → RETROFIT → AUDIT → PUBLISH) runs in six different "
        "ways depending on where you are in the lifecycle:",
        tag=t.div,
    )
    st_space(10)
    term_definition_list(
        design_system=DS,
        items=[
            ("bootstrap",
             "N projects with shared idioms but no pack — extract a "
             "brand-new pack from scratch."),
            ("specialize",
             "Upstream pack almost fits but lacks domain specifics — "
             "fork with extensions while preserving upstream as dep."),
            ("refine",
             "Active pack + new blocks since the last cycle — "
             "incrementally capture emerged patterns."),
            ("audit",
             "Read-only health check: unused components, duplicates, "
             "bundle gaps, contract drift."),
            ("adopt",
             "Wire an existing pack into N projects (stx pack add + "
             "stx kit install) without extraction or retrofit."),
            ("publish",
             "Mature pack ready for release: semver bump, CHANGELOG, "
             "git tag, optional PyPI publish."),
        ],
    )
    st_space(20)

    # ---- Orchestrator ----
    st_write((bs.sub, "One orchestrator, six specialists"), toc_lvl="+1", tag=t.div)
    st_space(10)
    callout(
        design_system=DS,
        variant="success",
        title="You only ever talk to one agent: pack-orchestrator",
        body=(
            "It auto-detects the right sub-mode from your prompt + "
            "workspace state, surfaces 4 fundamental gates (G1-G4) at "
            "the critical moments, and delegates the work to six "
            "invisible specialists — pack-miner, pack-designer, "
            "pack-implementer, pack-retrofitter, pack-auditor, "
            "pack-publisher. You never need to know they exist."
        ),
    )
    st_space(20)

    # ---- The 4 gates ----
    st_write((bs.sub, "Four fundamental gates"), toc_lvl="+1", tag=t.div)
    st_space(10)
    term_definition_list(
        design_system=DS,
        items=[
            ("G1",
             "post-DISCOVERY — review the candidates table before "
             "committing to design."),
            ("G2",
             "post-DESIGN — review contracts and conflicts before "
             "implementation. Skippable in dialog_level: minimal."),
            ("G3",
             "pre-RETROFIT — review the dry-run plan before rewriting "
             "consumer blocks."),
            ("G4",
             "post-RETROFIT smoke fail (conditional) — only if headless "
             "render of rewritten blocks fails."),
        ],
    )
    st_space(20)

    # ---- Invocation ----
    st_write((bs.sub, "Invocation"), toc_lvl="+1", tag=t.div)
    st_space(10)
    with st_block(bs.code_box):
        st_code(
            code="""
# Auto-detect sub-mode from prompt + workspace state
/stx-pe:go projects/manual-a projects/manual-b

# Forced sub-modes
/stx-pe:bootstrap projects/*
/stx-pe:specialize git:streamtex-design@v0.4 projects/*
/stx-pe:refine
/stx-pe:audit ../streamtex-design
/stx-pe:adopt pypi:streamtex-design projects/*
/stx-pe:publish ../streamtex-design

# Indirect routing via the ad-hoc task command
/stx-ce:task "extract a pack from projects A B C"
""",
            language="bash",
        )
    st_space(15)
    callout(
        design_system=DS,
        variant="info",
        title="Next blocks",
        body=(
            "The next blocks walk through the bootstrap flow end-to-end "
            "and the refine flow for incremental enrichment."
        ),
    )
