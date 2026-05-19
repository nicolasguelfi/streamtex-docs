"""End-to-end pack consumption — from `stx project new` to capture/promote.

Port of the legacy `bck_install_flow` block from `stx_manual_patterns`,
updated for the 0.7.x reuse architecture (packs / components / DS / kits).
"""

from streamtex import *
from streamtex.enums import Tags as t
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
    """How packs get into a project — soup-to-nuts walkthrough."""
    with st_block(s.center_txt):
        st_write(("Pack consumption: end-to-end flow", bs.heading), tag=t.div, toc_lvl="1")
        st_space(10)
        st_write(
            "From an empty directory to a curated set of components, "
            "design system, and kit — without locking the project into "
            "any specific catalog.",
            bs.body,
        )
        st_space(15)

    # ---- Step 1: project bootstrap ----
    st_write(("Step 1 — Bootstrap a project", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "`stx project new` scaffolds a project, optionally with a "
        "primary local pack (`./mypack/`) and a starter kit. Three "
        "flags steer pack-related bootstrap:",
        bs.body,
    )
    st_space(10)

    with st_block(bs.cell):
        st_code(
            """
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
    st_space(10)

    st_write(
        "Post-scaffold, `stx.toml` records the declared packs, the "
        "chosen design system, and (if a kit was installed) the kit "
        "reference. `mypack/` exists as a sub-folder and is installed "
        "editable via `uv pip install -e ./mypack`.",
        bs.body,
    )
    st_space(15)

    # ---- Step 2: add packs to an existing project ----
    st_write(("Step 2 — Add packs to an existing project", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "`stx pack add` covers the 3 pack sources symmetrically. "
        "Where the legacy system needed a separate clone/link/set "
        "trichotomy, all three now go through one command:",
        bs.body,
    )
    st_space(10)

    with st_block(bs.cell):
        st_code(
            """
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
    st_space(15)

    # ---- Step 3: install a kit ----
    st_write(("Step 3 — Install a kit (DS + components)", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "A **kit** is a TOML manifest bundling a design system "
        "reference + a curated list of components. Installing a kit "
        "writes `[design_system].use` and `[kit].use` to `stx.toml`. "
        "The components themselves remain importable from the pack — "
        "the kit just declares **which subset is recommended**.",
        bs.body,
    )
    st_space(10)

    with st_block(bs.cell):
        st_code(
            """
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
    st_space(15)

    # ---- Step 4: capture a new component locally ----
    st_write(("Step 4 — Capture a new component", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "When a project's blocks invent a recurring visual idiom not "
        "covered by any installed pack, capture it as a component "
        "inside the project's primary local pack:",
        bs.body,
    )
    st_space(10)

    with st_block(bs.cell):
        st_code(
            """
# Scaffold a new component into the primary local pack (./mypack/)
stx component new my_widget --granularity composition

# Or scaffold a new component into a specific pack
stx component new my_widget --pack mypack

# Validate every component in the project (no argument = all)
stx component validate
""",
            language="bash",
        )
    st_space(10)

    st_write(
        "The scaffold creates a `components/my_widget.py` module with "
        "the docstring contract (Visual / Structure / Styling rules / "
        "INVARIANTS / PARAMS / INTERDITS / When to use / NOT to use / "
        "bundles required), the `__component_meta__` TypedDict, and a "
        "stub function. Edit the docstring, implement the function, "
        "then validate.",
        bs.body,
    )
    st_space(15)

    # ---- Step 5: promote a component to a shared pack ----
    st_write(("Step 5 — Promote to a shared pack (Q12)", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "Once a captured component proves reusable across projects, "
        "promote it to a shared pack with `stx component promote`. "
        "Routing depends on the destination pack's type (Q12, "
        "four branches):",
        bs.body,
    )
    st_space(10)

    with st_grid(cols="1fr 3fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write(("primary_local", bs.body))
        with g.cell():
            st_write(
                "Copy only — the developer commits with the project. "
                "No separate commit.",
                bs.body,
            )
        with g.cell():
            st_write(("secondary_local_with_git", bs.body))
        with g.cell():
            st_write(
                "Copy + QCM commit in the pack's own repo.",
                bs.body,
            )
        with g.cell():
            st_write(("git_remote", bs.body))
        with g.cell():
            st_write(
                "Clone cache → branch → push → `gh pr create`. "
                "Never push to main directly.",
                bs.body,
            )
        with g.cell():
            st_write(("pypi", bs.body))
        with g.cell():
            st_write(
                "Refused (PR001). Promote to the upstream **git** "
                "pack instead, then bump the PyPI release manually.",
                bs.body,
            )
    st_space(15)

    with st_block(bs.cell):
        st_code(
            """
# Promote to a writable local pack (plain copy)
stx component promote my_widget --to=shared_pack

# Promote to a git remote pack (opens a PR)
stx component promote my_widget --to=streamtex-design
""",
            language="bash",
        )
    st_space(15)

    # ---- Step 6: persistence — what lives where ----
    st_write(("Step 6 — Persistence model", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "Three files capture pack-related state in a project, all "
        "versioned with the project:",
        bs.body,
    )
    st_space(10)

    with st_grid(cols="1fr 3fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write(("stx.toml", bs.body))
        with g.cell():
            st_write(
                "`[[packs]]` declarations + `[design_system].use` + "
                "`[kit].use` + `[resolution].prefer`. The single "
                "source of truth for pack intent.",
                bs.body,
            )
        with g.cell():
            st_write(("pyproject.toml", bs.body))
        with g.cell():
            st_write(
                "Lists installed Python deps including git packs. "
                "Optionally `[tool.uv.sources]` for editable links.",
                bs.body,
            )
        with g.cell():
            st_write(("uv.lock", bs.body))
        with g.cell():
            st_write(
                "Resolved, deterministic versions per package. "
                "Regenerated by `stx pack sync` (= `uv sync`).",
                bs.body,
            )
    st_space(15)

    st_write(
        "On a fresh `git clone`, run `stx pack sync` once — it "
        "regenerates the lockfile-driven environment from `stx.toml` "
        "+ `pyproject.toml`. No extra cache, no drift bookkeeping.",
        bs.body,
    )
    st_space(15)

    # ---- Recap cheatsheet ----
    st_write(("Recap", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_block(bs.cell):
        st_code(
            """
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
