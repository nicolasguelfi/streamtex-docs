"""CE promotion flow — the four-branch routing from local to shared pack.

Source: streamtex/cli/component_cmd.py promote_cmd + Q12 4-branch routing.
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
    cell_head = s.bold + s.large


bs = BlockStyles


def build():
    """Document the four-branch promotion routing (Q12)."""
    with st_block(s.center_txt):
        st_write(("CE promotion flow", bs.heading))
        st_space(15)
        st_write(
            "Once a captured component proves reusable across "
            "projects, promote it to a shared pack with "
            "`stx component promote`. Routing depends on the "
            "destination pack's **type** (Q12) — four branches, "
            "one command:",
            bs.body,
        )
        st_space(15)

    # ---- Step 1: CLI ----
    st_write(("Step 1 — CLI surface", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            """
# Promote `my_widget` to a pack declared in stx.toml
stx component promote my_widget --to=shared_pack

# Skip the auto-commit (branches that support it)
stx component promote my_widget --to=streamtex-design --no-commit
""",
            language="bash",
        )
    st_space(15)

    # ---- Step 2: routing ----
    st_write(("Step 2 — Four-branch routing", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_grid(cols="1fr 1fr 3fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write(("Destination type", bs.cell_head))
        with g.cell():
            st_write(("Action", bs.cell_head))
        with g.cell():
            st_write(("Effect", bs.cell_head))

        for dest, action, effect in [
            ("primary_local",
             "Copy only",
             "Copies the component file to the destination pack. "
             "No separate commit — the developer commits it with "
             "the project. Used when the destination pack lives "
             "inside the project itself (e.g. `./mypack/` itself)."),
            ("secondary_local_with_git",
             "Copy + commit",
             "Copies + creates a commit inside the destination "
             "pack's own .git directory. Used when the destination "
             "is a sibling local pack (`/Users/me/shared_pack/`) "
             "tracked in its own repo."),
            ("git_remote",
             "Clone cache → branch → push → gh pr create",
             "Clones the upstream repo into a local cache, creates "
             "a topic branch, copies the component, pushes the "
             "branch, opens a pull request with `gh pr create`. "
             "Never pushes to main directly."),
            ("pypi",
             "Refused (PR001)",
             "PyPI is treated as read-only by automation. Promote "
             "to the upstream **git** pack instead, then bump the "
             "PyPI release manually."),
        ]:
            with g.cell():
                st_write(dest, bs.body + s.bold)
            with g.cell():
                st_write(action, bs.body)
            with g.cell():
                st_write(effect, bs.body)
    st_space(15)

    # ---- Step 3: pre-flight checks ----
    st_write(("Step 3 — Pre-flight checks", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "Before any copy, `stx component promote` runs:\n\n"
        "1. **Component validation** — the component must pass "
        "`stx component validate` (no `CV0xx` errors).\n"
        "2. **Name collision** — refuses if the destination pack "
        "already exports a component with the same name (use a "
        "different name or remove the duplicate first).\n"
        "3. **Destination is writable** — refuses if the resolved "
        "destination is PyPI (`PR001`) or if the git remote is "
        "unreachable.",
        bs.body,
    )
    st_space(15)

    # ---- Step 4: after promotion ----
    st_write(("Step 4 — After promotion", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "Once the destination pack has the component, two cleanup "
        "actions are typical:\n\n"
        "- Remove the local copy from the project's primary pack "
        "(it's now imported from the shared pack).\n"
        "- Update `stx.toml` if the project should now pull the "
        "shared pack (it already does if the pack was declared).\n"
        "- For `git_remote` branches: review the auto-opened PR, "
        "update CHANGELOG and version bump in the shared pack, "
        "merge.",
        bs.body,
    )
