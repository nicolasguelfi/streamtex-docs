"""End-to-end pack consumption — from `stx project new` to capture/promote."""

from streamtex import st_block, st_code, st_space, st_write
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem
from streamtex_design.components.comparison_table import comparison_table


DS = DesignSystem()


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    code_box = s.container.paddings.small_padding + s.container.borders.solid_border


bs = BlockStyles


def build():
    """How packs get into a project — soup-to-nuts walkthrough."""
    st_write((bs.heading, "Pack consumption: end-to-end flow"), tag=t.div, toc_lvl="1")
    st_space(10)
    st_write(
        bs.body + s.center_txt,
        "From an empty directory to a curated set of components, design "
        "system, and kit — without locking the project into any specific "
        "catalog.",
        tag=t.div,
    )
    st_space(20)

    # ---- Step 1 ----
    st_write((bs.sub, "Step 1 — Bootstrap a project"), toc_lvl="+1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "stx project new scaffolds a project, optionally with a primary "
        "local pack (./mypack/) and a starter kit:",
        tag=t.div,
    )
    st_space(10)
    with st_block(bs.code_box):
        st_code(
            code="""
# Vanilla project (creates ./mypack/ as the primary local pack)
stx project new my-app

# Project that pulls a starter kit from streamtex-design
stx project new my-app --kit streamtex-design:project-default

# Project that pulls multiple packs (kit pack + an extra one)
stx project new my-app \\
    --kit streamtex-design:slides-modern-dark \\
    --pack github.com/your-org/your-pack

# Skip the primary local pack (only consume external packs)
stx project new my-app --kit streamtex-design:manual-default --no-mypack
""",
            language="bash",
        )
    st_space(15)
    st_write(
        bs.body,
        "Post-scaffold, stx.toml records the declared packs, the chosen "
        "design system, and (if a kit was installed) the kit reference.",
        tag=t.div,
    )
    st_space(20)

    # ---- Step 2 ----
    st_write((bs.sub, "Step 2 — Add packs to an existing project"), toc_lvl="+1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "stx pack add covers the 3 pack sources symmetrically — git, "
        "local path, and PyPI all go through one command:",
        tag=t.div,
    )
    st_space(10)
    with st_block(bs.code_box):
        st_code(
            code="""
# Add a git pack at a specific revision (tag, branch, or SHA)
stx pack add git:https://github.com/streamtex/streamtex-design@v0.2.0

# Add a local pack inside the project, then mark it primary
stx pack add local:./mypack
stx pack set-primary mypack

# Add a local pack on disk (any absolute path)
stx pack add local:/Users/me/shared

# Add a PyPI pack with a version specifier
stx pack add pypi:streamtex-academic@>=1.0,<2.0

# Editable install for local dev iteration (plain path + --dev)
stx pack add /Users/me/dev/my-fork --dev
""",
            language="bash",
        )
    st_space(20)

    # ---- Step 3 ----
    st_write((bs.sub, "Step 3 — Install a kit (DS + components)"), toc_lvl="+1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "A kit is a TOML manifest bundling a design system reference + a "
        "curated list of components. Installing a kit writes "
        "[design_system].use and [kit].use to stx.toml.",
        tag=t.div,
    )
    st_space(10)
    with st_block(bs.code_box):
        st_code(
            code="""
# Apply a kit (records design_system + kit reference)
stx kit install streamtex-design:slides-modern-dark

# Switch the active design system without re-installing the kit
stx ds switch streamtex-design:modern_light

# List available kits across all installed packs
stx kit list

# Inspect a kit's content
stx kit show streamtex-design:slides-modern-dark
""",
            language="bash",
        )
    st_space(20)

    # ---- Step 4 ----
    st_write((bs.sub, "Step 4 — Capture a new component"), toc_lvl="+1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "When a project's blocks invent a recurring visual idiom not "
        "covered by any installed pack, capture it as a component inside "
        "the project's primary local pack:",
        tag=t.div,
    )
    st_space(10)
    with st_block(bs.code_box):
        st_code(
            code="""
# Scaffold a new component into the primary local pack (./mypack/)
stx component new my_widget --granularity composition

# Or scaffold a new component into a specific pack
stx component new my_widget --pack mypack

# Validate every component in the project (no argument = all)
stx component validate
""",
            language="bash",
        )
    st_space(20)

    # ---- Step 5 ----
    st_write((bs.sub, "Step 5 — Promote to a shared pack"), toc_lvl="+1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "Once a captured component proves reusable across projects, "
        "promote it to a shared pack with stx component promote. Routing "
        "depends on the destination pack's type:",
        tag=t.div,
    )
    st_space(10)
    comparison_table(
        design_system=DS,
        columns=["Destination type", "Behaviour"],
        rows=[
            ("primary_local",
             "Copy only — the developer commits with the project. No "
             "separate commit."),
            ("secondary_local_with_git",
             "Copy + QCM commit in the pack's own repo."),
            ("git_remote",
             "Clone cache → branch → push → gh pr create. Never push "
             "to main directly."),
            ("pypi",
             "Refused (PR001). Promote to the upstream git pack instead, "
             "then bump the PyPI release manually."),
        ],
    )
    st_space(15)
    with st_block(bs.code_box):
        st_code(
            code="""
# Promote to a writable local pack (plain copy)
stx component promote my_widget --to=shared_pack

# Promote to a git remote pack (opens a PR)
stx component promote my_widget --to=streamtex-design
""",
            language="bash",
        )
    st_space(20)

    # ---- Step 6 ----
    st_write((bs.sub, "Step 6 — Persistence model"), toc_lvl="+1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "Three files capture pack-related state in a project, all "
        "versioned with the project:",
        tag=t.div,
    )
    st_space(10)
    comparison_table(
        design_system=DS,
        columns=["File", "Role"],
        rows=[
            ("stx.toml",
             "[[packs]] declarations + [design_system].use + [kit].use + "
             "[resolution].prefer. The single source of truth for pack intent."),
            ("pyproject.toml",
             "Lists installed Python deps including git packs. Optionally "
             "[tool.uv.sources] for editable links."),
            ("uv.lock",
             "Resolved, deterministic versions per package. Regenerated "
             "by stx pack sync (= uv sync)."),
        ],
    )
    st_space(20)

    # ---- Recap ----
    st_write((bs.sub, "Recap"), toc_lvl="+1", tag=t.div)
    st_space(10)
    with st_block(bs.code_box):
        st_code(
            code="""
# Bootstrap
stx project new my-app --kit streamtex-design:project-default

# Inspect
stx pack list                          # what is declared + state
stx component list                     # browse components (--pack to filter)
stx kit list                           # browse kits

# Iterate
stx component new my_widget            # capture locally
stx pack add git:https://github.com/x/y@v1  # add an external pack
stx pack sync                          # refresh after edits

# Promote
stx component promote my_widget --to=shared_pack

# Validate
stx validate --strict                  # CI-grade gate (PR/CV/DV/KV/BV)
""",
            language="bash",
        )
