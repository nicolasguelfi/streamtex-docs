"""Pack distribution — git, PyPI, local. Three channels, three life-cycles."""

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
    code = s.container.paddings.small_padding + s.container.borders.solid_border


bs = BlockStyles


def build():
    """Walk through the three distribution channels for a pack."""
    st_write((bs.heading, "Pack distribution"), toc_lvl="1", tag=t.div)
    st_space(10)
    st_write(
        bs.body + s.center_txt,
        "A pack travels through three channels — git, PyPI, local — each "
        "with its own audience and release cadence. The CLI handles all "
        "three symmetrically via stx pack add.",
        tag=t.div,
    )
    st_space(20)

    # ---- Channels at a glance ----
    st_write((bs.sub, "Channels at a glance"), toc_lvl="+1", tag=t.div)
    st_space(10)
    comparison_table(
        design_system=DS,
        columns=["Channel", "Use it when", "Add it with"],
        rows=[
            ("Local",
             "Project-internal pack (./mypack/) or shared directory under "
             "team control. No release cadence — edits are immediate.",
             "stx pack add local:./mypack  (or --dev for editable)"),
            ("Git",
             "Public or private repo shared across projects/teams. "
             "Versioning by git tag (or branch/SHA).",
             "stx pack add git:github.com/org/pack@v0.2.0"),
            ("PyPI",
             "Stable, widely-distributed pack with semver. Adds a release "
             "step (build + upload) on top of git.",
             "stx pack add pypi:streamtex-academic@>=1.0,<2.0"),
        ],
    )
    st_space(20)

    # ---- Git release flow ----
    st_write((bs.sub, "Git release flow"), toc_lvl="+1", tag=t.div)
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
    st_space(20)

    # ---- PyPI release flow ----
    st_write((bs.sub, "PyPI release flow"), toc_lvl="+1", tag=t.div)
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
    callout(
        design_system=DS,
        variant="warn",
        title="PR001 — PyPI is read-only for automation",
        body=(
            "Promoting a captured component to a PyPI pack is refused by "
            "stx component promote. Promote to the upstream git pack "
            "first, then bump the PyPI release manually."
        ),
    )
    st_space(20)

    # ---- Local (no release) ----
    st_write((bs.sub, "Local — no release step"), toc_lvl="+1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "Local packs (type=\"local\" in stx.toml) have no version concept "
        "— the working copy on disk is the truth. Two sub-cases:",
        tag=t.div,
    )
    st_space(10)
    comparison_table(
        design_system=DS,
        columns=["Sub-case", "Description"],
        rows=[
            ("primary_local",
             "The ./mypack/ sub-folder created by stx project new (unless "
             "--no-mypack). One primary per project. Used as the default "
             "destination for stx component new. Travels with the project's "
             "git history."),
            ("secondary_local_with_git",
             "A local pack with its own .git/ directory (e.g. /Users/me/"
             "shared_pack/). stx component promote can copy a captured "
             "component into it AND commit into the pack's own repo "
             "(stx component promote <name> --to=shared_pack)."),
        ],
    )
    st_space(15)
    callout(
        design_system=DS,
        variant="info",
        title="Editable install",
        body=(
            "stx pack add <path> --dev writes [tool.uv.sources] in the "
            "project's pyproject.toml so edits in the pack are picked up "
            "immediately by stx run."
        ),
    )
