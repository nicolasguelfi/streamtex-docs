"""Pack Engineering — bootstrap flow walked end-to-end."""

from streamtex import st_block, st_code, st_space, st_write
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem
from streamtex_design.components.callout import callout
from streamtex_design.components.comparison_table import comparison_table


DS = DesignSystem()


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    code_box = s.container.paddings.small_padding + s.container.borders.solid_border


bs = BlockStyles


def build():
    """Walk through the bootstrap sub-mode: N projects → new pack."""
    st_write((bs.heading, "Bootstrap: N projects → new pack"), toc_lvl="1", tag=t.div)
    st_space(10)
    st_write(
        bs.body + s.center_txt,
        "Bootstrap is the right sub-mode when you have ≥ 2 projects with "
        "overlapping visual idioms but no shared pack yet. The cycle "
        "extracts the recurring patterns, produces a brand-new pack, "
        "and rewrites the source projects to consume it.",
        tag=t.div,
    )
    st_space(20)

    # ---- Inputs ----
    st_write((bs.sub, "Inputs"), toc_lvl="+1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "Required: a list of project paths. Optional: a name for the new "
        "pack, a target path, the active design system. Defaults are "
        "sensible and inferred from the workspace.",
        tag=t.div,
    )
    st_space(10)
    with st_block(bs.code_box):
        st_code(
            code="""
/stx-pe:bootstrap projects/manual-a projects/manual-b projects/manual-c
/stx-pe:bootstrap --pack-name design-corporate projects/*
/stx-pe:bootstrap --target-path ../shared-design --min-projects 3 projects/*
""",
            language="bash",
        )
    st_space(20)

    # ---- The 7 steps ----
    st_write((bs.sub, "The 7 steps"), toc_lvl="+1", tag=t.div)
    st_space(10)
    comparison_table(
        design_system=DS,
        columns=["Step", "Description"],
        rows=[
            ("0. Detect",
             "Read pack-master-plan.yaml if present; otherwise initialize "
             "a fresh plan in the pilot project's docs/pack-engineering/."),
            ("1. DISCOVERY",
             "pack-miner AST-scans the consumer projects' blocks, "
             "clusters recurring idioms by similarity, scores them by "
             "coverage. Output: discovery.md."),
            ("G1 (gate)",
             "You review the candidates table and decide which clusters "
             "to keep, drop, or merge."),
            ("2. DESIGN",
             "pack-designer writes a full contract for each approved "
             "cluster (Visual / Structure / Styling rules / INVARIANTS "
             "/ PARAMS / INTERDITS / Bundles required). Output: design.md."),
            ("G2 (gate)",
             "Skippable in minimal dialog. Review conflicts and rejections."),
            ("3. IMPLEMENT",
             "pack-implementer scaffolds via stx component new, writes "
             "Python bodies, validates via stx component validate. One "
             "commit per component in the pack repo."),
            ("4. ADOPT",
             "Per-project loop: stx pack add <ref> + stx kit install "
             "<pack>:<kit>. No specialist agent — direct CLI."),
            ("G3 (gate)",
             "Review the retrofit dry-run plan."),
            ("5. RETROFIT",
             "pack-retrofitter rewrites consumer blocks to use the new "
             "components, runs headless smoke render to validate. "
             "Per-project commits."),
            ("G4 (gate)",
             "Conditional — only if smoke render fails on any block. "
             "Revert / accept / discuss."),
            ("6. AUDIT",
             "pack-auditor auto-runs: unused components, duplicates, "
             "bundle gaps, contract drift. Read-only."),
            ("7. PUBLISH",
             "Opt-in only — QCM at the end of the cycle."),
        ],
    )
    st_space(20)

    # ---- Outputs ----
    st_write((bs.sub, "What you get"), toc_lvl="+1", tag=t.div)
    st_space(10)
    callout(
        design_system=DS,
        variant="success",
        title="At termination of a successful bootstrap cycle",
        body=(
            "A new pack repo at <target-path> with components, design "
            "system, kit, and per-component commits. All N consumer "
            "projects updated: stx.toml declares the new pack, blocks "
            "rewritten to use its components. Pilot project "
            "docs/pack-engineering/ populated with the full audit trail "
            "(master plan + per-phase reports + decisions log)."
        ),
    )
    st_space(20)

    # ---- Recovery ----
    st_write((bs.sub, "If something goes wrong"), toc_lvl="+1", tag=t.div)
    st_space(10)
    callout(
        design_system=DS,
        variant="info",
        title="The cycle is resumable",
        body=(
            "If interrupted between phases (Ctrl-C, session ends), the "
            "next invocation reads phases_completed[-1] from the master "
            "plan and continues from the next phase. Retrofit defaults "
            "to dry-run; you can review the plan before any block is "
            "modified."
        ),
    )
