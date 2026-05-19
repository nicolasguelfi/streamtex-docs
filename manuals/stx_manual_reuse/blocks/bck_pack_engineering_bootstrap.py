"""Pack Engineering — bootstrap flow walked end-to-end.

Source: streamtex-claude/profiles/project/pack-engineering/skills/pe-bootstrap.md
+ pe-go.md.
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
    """Walk through the bootstrap sub-mode : N projects -> new pack."""
    with st_block(s.center_txt):
        st_write((bs.heading, "Bootstrap : N projects → new pack"), toc_lvl="1")
        st_space(15)
        st_write(
            bs.body,
            "**Bootstrap** is the right sub-mode when you have ≥ 2 "
            "projects with overlapping visual idioms but no shared "
            "pack yet. The cycle extracts the recurring patterns, "
            "produces a brand-new pack, and rewrites the source "
            "projects to consume it.",
        )
        st_space(15)

    # ---- Inputs ----
    st_write((bs.sub, "Inputs"), toc_lvl="+1")
    st_space(10)
    st_write(
        bs.body,
        "Required : a list of project paths. Optional : a name for "
        "the new pack, a target path, the active design system. "
        "Defaults are sensible and inferred from the workspace.",
    )
    st_space(10)

    with st_block(bs.code):
        st_code(
            code="""
/stx-pe:bootstrap projects/manual-a projects/manual-b projects/manual-c
/stx-pe:bootstrap --pack-name design-corporate projects/*
/stx-pe:bootstrap --target-path ../shared-design --min-projects 3 projects/*
""",
            language="bash",
        )
    st_space(15)

    # ---- The 7 steps ----
    st_write((bs.sub, "The 7 steps"), toc_lvl="+1")
    st_space(10)

    with st_grid(cols="1fr 4fr", gap="8px", cell_styles=bs.cell) as g:
        for step, desc in [
            ("0. Detect",
             "Read `pack-master-plan.yaml` if present ; otherwise "
             "initialize a fresh plan in the pilot project's "
             "`docs/pack-engineering/`."),
            ("1. DISCOVERY",
             "`pack-miner` AST-scans the consumer projects' blocks, "
             "clusters recurring idioms by similarity, scores them "
             "by coverage. Output : `discovery.md`."),
            ("G1",
             "**Gate** : you review the candidates table and decide "
             "which clusters to keep, drop, or merge."),
            ("2. DESIGN",
             "`pack-designer` writes a full contract for each "
             "approved cluster (Visual / Structure / Styling rules / "
             "INVARIANTS / PARAMS / INTERDITS / Bundles required). "
             "Conflicts and rejections recorded. Output : `design.md`."),
            ("G2",
             "**Gate** (skippable in minimal dialog) : review "
             "conflicts and rejections."),
            ("3. IMPLEMENT",
             "`pack-implementer` scaffolds via `stx component new`, "
             "writes Python bodies, validates via `stx component "
             "validate`. One commit per component in the pack repo."),
            ("4. ADOPT",
             "Per-project loop : `stx pack add <ref>` + "
             "`stx kit install <pack>:<kit>`. No specialist agent — "
             "direct CLI."),
            ("G3",
             "**Gate** : review the retrofit dry-run plan."),
            ("5. RETROFIT",
             "`pack-retrofitter` rewrites consumer blocks to use the "
             "new components, runs headless smoke render to validate. "
             "Per-project commits."),
            ("G4",
             "**Gate** (conditional) : only if smoke render fails on "
             "any block. Revert / accept / discuss."),
            ("6. AUDIT",
             "`pack-auditor` auto-runs : unused components, "
             "duplicates, bundle gaps, contract drift. Read-only."),
            ("7. PUBLISH",
             "Opt-in only — QCM at the end of the cycle."),
        ]:
            with g.cell():
                st_write(bs.body + s.bold, step)
            with g.cell():
                st_write(bs.body, desc)
    st_space(15)

    # ---- Outputs ----
    st_write((bs.sub, "What you get"), toc_lvl="+1")
    st_space(10)
    st_write(
        bs.body,
        "At termination of a successful bootstrap cycle :\n\n"
        "- A new pack repo at `<target-path>` with components, "
        "design system, kit, and per-component commits.\n"
        "- All N consumer projects updated : `stx.toml` declares the "
        "new pack, blocks rewritten to use its components.\n"
        "- Pilot project `docs/pack-engineering/` populated with the "
        "full audit trail (master plan + per-phase reports + "
        "decisions log).",
    )
    st_space(15)

    # ---- Recovery ----
    st_write((bs.sub, "If something goes wrong"), toc_lvl="+1")
    st_space(10)
    st_write(
        bs.body,
        "The cycle is **resumable**. If interrupted between phases "
        "(Ctrl-C, session ends), the next invocation reads "
        "`phases_completed[-1]` from the master plan and continues "
        "from the next phase. Retrofit defaults to `dry-run` ; you "
        "can review the plan before any block is modified.",
    )
