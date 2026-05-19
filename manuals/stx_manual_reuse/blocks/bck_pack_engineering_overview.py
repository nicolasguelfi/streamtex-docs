"""Pack Engineering — overview of the orchestrated pack lifecycle.

Source: streamtex-claude/profiles/project/pack-engineering/skills/pe-*.md.
"""

from streamtex import *
from custom.styles import Styles as s


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    code = s.container.paddings.small_padding + s.container.borders.solid_border
    cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
    )


bs = BlockStyles


def build():
    """Introduce the Pack Engineering (PE) lifecycle and its six sub-modes."""
    with st_block(s.center_txt):
        st_write((bs.heading, "Pack Engineering — overview"), toc_lvl="1")
        st_space(15)
        st_write(
            bs.body,
            "When the project's library grows beyond manual capture, "
            "**Pack Engineering (PE)** is the orchestrated lifecycle "
            "that takes N existing projects and produces (or enriches) "
            "a shared pack — with full audit trail, validation gates, "
            "and automatic retrofit of the consumer projects.",
        )
        st_space(15)

    # ---- Where PE fits ----
    st_write((bs.sub, "Where PE fits"), toc_lvl="+1")
    st_space(10)
    st_write(
        bs.body,
        "PE sits between **CE capture** (project-local, one component "
        "at a time) and **pack publication** (versioned release to "
        "PyPI). It is the bridge that turns a folder of authored "
        "blocks into a reusable, versioned design pack — and rewrites "
        "the source projects to consume it.",
    )
    st_space(15)

    # ---- Six sub-modes ----
    st_write((bs.sub, "Six sub-modes"), toc_lvl="+1")
    st_space(10)
    st_write(
        bs.body,
        "The same 7-step sequencer (DISCOVERY → DESIGN → IMPLEMENT → "
        "ADOPT → RETROFIT → AUDIT → PUBLISH) runs in six different "
        "ways depending on where you are in the lifecycle:",
    )
    st_space(10)

    with st_grid(cols="1fr 4fr", gap="8px", cell_styles=bs.cell) as g:
        for mode, desc in [
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
             "Read-only health check : unused components, duplicates, "
             "bundle gaps, contract drift."),
            ("adopt",
             "Wire an existing pack into N projects (`stx pack add` + "
             "`stx kit install`) without extraction or retrofit."),
            ("publish",
             "Mature pack ready for release : semver bump, CHANGELOG, "
             "git tag, optional PyPI publish."),
        ]:
            with g.cell():
                st_write(bs.body + s.bold, mode)
            with g.cell():
                st_write(bs.body, desc)
    st_space(15)

    # ---- The single user-facing agent ----
    st_write((bs.sub, "One orchestrator, six specialists"), toc_lvl="+1")
    st_space(10)
    st_write(
        bs.body,
        "**You only ever talk to one agent : `pack-orchestrator`.** It "
        "auto-detects the right sub-mode from your prompt + workspace "
        "state, surfaces 4 fundamental gates (G1-G4) at the critical "
        "moments, and delegates the work to six invisible specialists "
        "— `pack-miner`, `pack-designer`, `pack-implementer`, "
        "`pack-retrofitter`, `pack-auditor`, `pack-publisher`. You "
        "never need to know they exist.",
    )
    st_space(15)

    # ---- The 4 gates ----
    st_write((bs.sub, "Four fundamental gates"), toc_lvl="+1")
    st_space(10)

    with st_grid(cols="1fr 4fr", gap="8px", cell_styles=bs.cell) as g:
        for gate, desc in [
            ("G1",
             "post-DISCOVERY — review the candidates table before "
             "committing to design."),
            ("G2",
             "post-DESIGN — review contracts and conflicts before "
             "implementation. Skippable in `dialog_level: minimal`."),
            ("G3",
             "pre-RETROFIT — review the dry-run plan before "
             "rewriting consumer blocks."),
            ("G4",
             "post-RETROFIT smoke fail (conditional) — only if "
             "headless render of rewritten blocks fails."),
        ]:
            with g.cell():
                st_write(bs.body + s.bold, gate)
            with g.cell():
                st_write(bs.body, desc)
    st_space(15)

    # ---- Invocation ----
    st_write((bs.sub, "Invocation"), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
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

    st_write(
        bs.body,
        "The next blocks walk through the **bootstrap** flow end-to-"
        "end and the **refine** flow for incremental enrichment.",
    )
