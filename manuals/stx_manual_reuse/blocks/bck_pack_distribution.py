"""Pack distribution — git, PyPI, local. Three channels, three life-cycles.

Source: streamtex/cli/pack_cmd.py + PLAN §6.2.
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
    """Walk through the three distribution channels for a pack."""
    with st_block(s.center_txt):
        st_write(("Pack distribution", bs.heading))
        st_space(15)
        st_write(
            "A pack travels through three channels — git, PyPI, "
            "local — each with its own audience and release "
            "cadence. The CLI handles all three symmetrically via "
            "`stx pack add`.",
            bs.body,
        )
        st_space(15)

    # ---- Comparison table ----
    st_write(("Channels at a glance", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_grid(cols="1fr 2fr 2fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write(("Channel", bs.cell_head))
        with g.cell():
            st_write(("Use it when", bs.cell_head))
        with g.cell():
            st_write(("Add it with", bs.cell_head))

        for chan, when, how in [
            ("Local",
             "Project-internal pack (`./mypack/`) or shared "
             "directory under team control. No release cadence — "
             "edits are immediate.",
             "stx pack add local:./mypack  (or --dev for editable)"),
            ("Git",
             "Public or private repo shared across projects/teams. "
             "Versioning by git tag (or branch/SHA). Most common "
             "channel for organisation-wide packs.",
             "stx pack add git:github.com/org/pack@v0.2.0"),
            ("PyPI",
             "Stable, widely-distributed pack with semver. Adds a "
             "release step (build + upload) on top of git.",
             "stx pack add pypi:streamtex-academic@>=1.0,<2.0"),
        ]:
            with g.cell():
                st_write(chan, bs.body + s.bold)
            with g.cell():
                st_write(when, bs.body)
            with g.cell():
                st_write(how, bs.body)
    st_space(15)

    # ---- Git release flow ----
    st_write(("Git release flow", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            """
# Inside the pack repository
# 1) Bump version in pyproject.toml + _pack_manifest.toml
# 2) Update CHANGELOG.md
# 3) Commit, tag, push
git add pyproject.toml mypack/_pack_manifest.toml CHANGELOG.md
git commit -m "release: 0.2.0"
git tag v0.2.0
git push origin main --tags

# Consumers pick up the new version
stx pack add git:github.com/org/mypack@v0.2.0
stx pack sync
""",
            language="bash",
        )
    st_space(15)

    # ---- PyPI release flow ----
    st_write(("PyPI release flow", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            """
# Build distributions
uv build

# Upload to PyPI (token in env or interactive)
uv publish --token "$PYPI_TOKEN"

# Consumers pick up by spec
stx pack add pypi:mypack@>=0.2.0,<1.0
stx pack sync
""",
            language="bash",
        )
    st_space(15)

    st_write(
        "Promoting a captured component to a PyPI pack is "
        "**refused** by `stx component promote` (error `PR001`) — "
        "promote to the upstream **git** pack first, then bump the "
        "PyPI release manually. PyPI is treated as read-only by the "
        "automation.",
        bs.body,
    )
    st_space(15)

    # ---- Local (no release) ----
    st_write(("Local — no release step", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "Local packs (`type=\"local\"` in `stx.toml`) have no "
        "version concept — the working copy on disk is the truth. "
        "Two sub-cases:",
        bs.body,
    )
    st_space(10)

    with st_grid(cols="1fr 3fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write(("primary_local", bs.body + s.bold))
        with g.cell():
            st_write(
                "The `./mypack/` sub-folder created by "
                "`stx project new` (unless `--no-mypack`). One "
                "primary per project. Used as the default "
                "destination for `stx component new`. Travels with "
                "the project's git history.",
                bs.body,
            )
        with g.cell():
            st_write(("secondary_local_with_git", bs.body + s.bold))
        with g.cell():
            st_write(
                "A local pack with its own `.git/` directory (e.g. "
                "`/Users/me/shared_pack/`). `stx component promote` "
                "can copy a captured component into it AND commit "
                "into the pack's own repo (`stx component promote "
                "<name> --to=shared_pack`).",
                bs.body,
            )
    st_space(15)

    st_write(
        "Editable install for active local iteration: "
        "`stx pack add <path> --dev` — writes `[tool.uv.sources]` "
        "in the project's `pyproject.toml` so edits in the pack are "
        "picked up immediately by `stx run`.",
        bs.body,
    )
