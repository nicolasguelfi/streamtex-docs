"""Pack Engineering — refine flow for incremental enrichment.

Source: streamtex-claude/profiles/project/pack-engineering/skills/pe-refine.md.
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
    """Walk through the refine sub-mode : active pack + new blocks → enriched pack."""
    with st_block(s.center_txt):
        st_write((bs.heading, "Refine : capture emerged patterns"), toc_lvl="1")
        st_space(15)
        st_write(
            bs.body,
            "**Refine** is the incremental sibling of bootstrap. The "
            "current project already declares a pack ; you've kept "
            "writing blocks and new idioms have emerged. Refine "
            "captures only those NEW patterns into the existing pack "
            "— without re-doing the full analysis.",
        )
        st_space(15)

    # ---- Triggers ----
    st_write((bs.sub, "When to use refine"), toc_lvl="+1")
    st_space(10)
    st_write(
        bs.body,
        "Three signals warrant a refine cycle :\n\n"
        "- The current project's `stx.toml` declares a pack you "
        "control.\n"
        "- You've authored ≥ 3 new blocks since the last `mining_"
        "validated` entry in the master plan.\n"
        "- At least one of those new blocks contains a structure that "
        "feels like \"this should be a component\" — but isn't covered "
        "by the active pack.",
    )
    st_space(15)

    # ---- Invocation ----
    st_write((bs.sub, "Invocation"), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            code="""
# Refine the active pack — defaults to "blocks modified since last
# mining_validated"
/stx-pe:refine

# Custom cutoff date
/stx-pe:refine --since 2026-04-01

# Full re-scan (ignore --since)
/stx-pe:refine --full-scan

# Add to pack but skip the retrofit of current blocks
/stx-pe:refine --no-retrofit
""",
            language="bash",
        )
    st_space(15)

    # ---- What's different from bootstrap ----
    st_write((bs.sub, "What's different from bootstrap"), toc_lvl="+1")
    st_space(10)

    with st_grid(cols="1fr 4fr", gap="8px", cell_styles=bs.cell) as g:
        for diff, desc in [
            ("Single project",
             "Refine operates on the cwd's project only. To capture "
             "cross-project patterns, use bootstrap or specialize."),
            ("Dedup vs pack",
             "`pack-miner` invoked with the active pack included in "
             "the dedup set — only NEW clusters survive."),
            ("No `stx pack new`",
             "Step 3 IMPLEMENT adds components to the existing pack, "
             "not a fresh repo."),
            ("ADOPT skipped",
             "Pack already declared in `stx.toml` ; only the kit may "
             "need updating to include new components (QCM proposed)."),
            ("RETROFIT scoped",
             "Step 5 rewrites only the cwd's blocks that match the "
             "new clusters."),
            ("No AUDIT",
             "Refine is incremental — full audit is a separate "
             "cycle. A follow-up QCM offers `/stx-pe:audit` if you "
             "want one."),
            ("Patch bump",
             "Step 7 PUBLISH (opt-in) usually proposes a patch bump "
             "— refine adds but rarely changes."),
        ]:
            with g.cell():
                st_write(bs.body + s.bold, diff)
            with g.cell():
                st_write(bs.body, desc)
    st_space(15)

    # ---- The patch-bump rationale ----
    st_write((bs.sub, "Why refine usually means patch"), toc_lvl="+1")
    st_space(10)
    st_write(
        bs.body,
        "Per the PE semver policy : REMOVED → major, CHANGED → minor, "
        "ADDED only → patch. Refine adds new components but does not "
        "modify or remove existing ones — so a patch bump is the "
        "default. If a refine cycle ends up modifying an existing "
        "component (rare, requires explicit decision), the publisher "
        "surfaces the bump computation and the user can override.",
    )
    st_space(15)

    # ---- Typical session ----
    st_write((bs.sub, "Typical session"), toc_lvl="+1")
    st_space(10)
    st_write(
        bs.body,
        "A refine cycle on a single project typically takes 5-15 "
        "minutes : 1-2 min for discovery, 2-5 min for design + "
        "implement, 2-5 min for retrofit + smoke render. At the end, "
        "the pack contains the new components, the current project's "
        "matching blocks are rewritten, and a patch version bump is "
        "ready for publish.",
    )
