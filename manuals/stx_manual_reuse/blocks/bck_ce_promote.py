"""CE promotion flow — the four-branch routing from local to shared pack."""

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
    """Document the four-branch promotion routing."""
    st_write((bs.heading, "CE promotion flow"), toc_lvl="1", tag=t.div)
    st_space(10)
    st_write(
        bs.body + s.center_txt,
        "Once a captured component proves reusable across projects, "
        "promote it to a shared pack with stx component promote. Routing "
        "depends on the destination pack's type — four branches, one command:",
        tag=t.div,
    )
    st_space(20)

    # ---- Step 1 ----
    st_write((bs.sub, "Step 1 — CLI surface"), toc_lvl="+1", tag=t.div)
    st_space(10)
    with st_block(bs.code_box):
        st_code(
            code="""
# Promote `my_widget` to a pack declared in stx.toml
stx component promote my_widget --to=shared_pack

# Skip the auto-commit (branches that support it)
stx component promote my_widget --to=streamtex-design --no-commit
""",
            language="bash",
        )
    st_space(20)

    # ---- Step 2 ----
    st_write((bs.sub, "Step 2 — Four-branch routing"), toc_lvl="+1", tag=t.div)
    st_space(10)
    comparison_table(
        design_system=DS,
        columns=["Destination type", "Action", "Effect"],
        rows=[
            ("primary_local",
             "Copy only",
             "Copies the component file to the destination pack. No "
             "separate commit — the developer commits it with the project."),
            ("secondary_local_with_git",
             "Copy + commit",
             "Copies + creates a commit inside the destination pack's "
             "own .git directory."),
            ("git_remote",
             "Clone cache → branch → push → gh pr create",
             "Clones the upstream repo into a local cache, creates a "
             "topic branch, copies the component, pushes the branch, "
             "opens a pull request with gh pr create. Never pushes to "
             "main directly."),
            ("pypi",
             "Refused (PR001)",
             "PyPI is treated as read-only by automation. Promote to "
             "the upstream git pack instead, then bump the PyPI release "
             "manually."),
        ],
    )
    st_space(20)

    # ---- Step 3 ----
    st_write((bs.sub, "Step 3 — Pre-flight checks"), toc_lvl="+1", tag=t.div)
    st_space(10)
    callout(
        design_system=DS,
        variant="info",
        title="Before any copy",
        body=(
            "1. Component validation — the component must pass "
            "stx component validate (no CV0xx errors). "
            "2. Name collision — refuses if the destination pack already "
            "exports a component with the same name. "
            "3. Destination is writable — refuses if the resolved "
            "destination is PyPI (PR001) or if the git remote is unreachable."
        ),
    )
    st_space(20)

    # ---- Step 4 ----
    st_write((bs.sub, "Step 4 — After promotion"), toc_lvl="+1", tag=t.div)
    st_space(10)
    callout(
        design_system=DS,
        variant="success",
        title="Cleanup actions",
        body=(
            "Remove the local copy from the project's primary pack (it's "
            "now imported from the shared pack). Update stx.toml if the "
            "project should now pull the shared pack. For git_remote "
            "branches: review the auto-opened PR, update CHANGELOG and "
            "version bump in the shared pack, merge."
        ),
    )
