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
        st_write((bs.heading, "Pack distribution"), toc_lvl="1")
        st_space(15)
        st_write(
            bs.body,
            "A pack travels through three channels — git, PyPI, "
            "local — each with its own audience and release "
            "cadence. The CLI handles all three symmetrically via "
            "`stx pack add`.",
        )
        st_space(15)

    # ---- Comparison table ----
    st_write((bs.sub, "Channels at a glance"), toc_lvl="+1")
    st_space(10)

    with st_grid(cols="1fr 2fr 2fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write((bs.cell_head, "Channel"))
        with g.cell():
            st_write((bs.cell_head, "Use it when"))
        with g.cell():
            st_write((bs.cell_head, "Add it with"))

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
                st_write(bs.body + s.bold, chan)
            with g.cell():
                st_write(bs.body, when)
            with g.cell():
                st_write(bs.body, how)
    st_space(15)

    # ---- Git release flow ----
    st_write((bs.sub, "Git release flow"), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            code="""
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
    st_write((bs.sub, "PyPI release flow"), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            code="""
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
        bs.body,
        "Promoting a captured component to a PyPI pack is "
        "**refused** by `stx component promote` (error `PR001`) — "
        "promote to the upstream **git** pack first, then bump the "
        "PyPI release manually. PyPI is treated as read-only by the "
        "automation.",
    )
    st_space(15)

    # ---- Local (no release) ----
    st_write((bs.sub, "Local — no release step"), toc_lvl="+1")
    st_space(10)
    st_write(
        bs.body,
        "Local packs (`type=\"local\"` in `stx.toml`) have no "
        "version concept — the working copy on disk is the truth. "
        "Two sub-cases:",
    )
    st_space(10)

    with st_grid(cols="1fr 3fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write((bs.body + s.bold, "primary_local"))
        with g.cell():
            st_write(
                bs.body,
                "The `./mypack/` sub-folder created by "
                "`stx project new` (unless `--no-mypack`). One "
                "primary per project. Used as the default "
                "destination for `stx component new`. Travels with "
                "the project's git history.",
            )
        with g.cell():
            st_write((bs.body + s.bold, "secondary_local_with_git"))
        with g.cell():
            st_write(
                bs.body,
                "A local pack with its own `.git/` directory (e.g. "
                "`/Users/me/shared_pack/`). `stx component promote` "
                "can copy a captured component into it AND commit "
                "into the pack's own repo (`stx component promote "
                "<name> --to=shared_pack`).",
            )
    st_space(15)

    st_write(
        bs.body,
        "Editable install for active local iteration: "
        "`stx pack add <path> --dev` — writes `[tool.uv.sources]` "
        "in the project's `pyproject.toml` so edits in the pack are "
        "picked up immediately by `stx run`.",
    )
