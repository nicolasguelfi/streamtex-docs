"""`stx patterns` CLI reference — install / update / promote.

# @pattern: ptn_api_reference_card
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation


class BlockStyles:
    """CLI reference styles."""
    heading = (
        s.project.titles.section_title
        + s.text.fonts.font_monospace
        + s.center_txt
    )
    lead = s.project.titles.body + s.center_txt
    sub = s.project.titles.section_subtitle
    keyword = s.bold + s.project.colors.primary_violet
    accent = s.bold + s.project.colors.accent_teal
    body = s.project.titles.body
    cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.container.layouts.vertical_center_layout
    )


bs = BlockStyles


# Subcommands of `stx patterns`, grouped by intent.
LIFECYCLE_CMDS = [
    ("install",  "(no args, TTY) | --preset N (repeatable) | --pattern A,B | --all | --exclude X,Y",
     "Pick patterns to install. No args + a terminal → menu-driven "
     "composite picker (multi-preset + add-individual + remove). Flags are "
     "fully composable: --preset can be repeated, --pattern adds extras on "
     "top, --exclude subtracts (also from --all). --all is exclusive with "
     "--preset/--pattern. Non-TTY without flags is refused."),
    ("sync",     "(no args)",
     "Idempotent: honours the recorded intent in stx.toml "
     "[patterns.selection] (or .patterns-meta.json) to install missing + "
     "update existing. Perfect after `git clone`."),
    ("update",   "(no args) | <name>...",
     "Refresh installed patterns from the source; drift-aware."),
    ("status",   "(no args)",
     "List installed patterns with their SHA + drift state."),
    ("diff",     "<pattern>",
     "Show local-vs-source diff for a single pattern."),
    ("remove",   "<pattern>",
     "Uninstall a pattern (file + meta entry)."),
]

SOURCE_CMDS = [
    ("source show",  "(no args)",
     "Print the R4 resolution chain — what was tried, what matched, "
     "what was skipped — and the resolved source path if any."),
    ("source clone", "[--url U] [--branch B] [--target D] [--force]",
     "Git-clone the patterns repo into <workspace>/streamtex-patterns. "
     "URL defaults to [repos.streamtex-patterns].url in stx.toml, else the "
     "official repo."),
    ("source link",  "<path> [--force]",
     "Symlink <workspace>/streamtex-patterns to an existing local clone — "
     "share one checkout across workspaces, or iterate on pattern files live."),
    ("source set",   "<path> [--scope project|workspace] [--allow-missing]",
     "Record [patterns].source = <path> in stx.toml (or pyproject.toml's "
     "[tool.patterns]) without cloning anything. Preserves comments."),
]

CATALOG_CMDS = [
    ("list",     "[--remote|--local] [--preset N] [--tag T] [--format ...]",
     "Show patterns available remotely (in the source) or locally (installed)."),
    ("presets",  "[--format table|json|names]",
     "List the named presets declared by the source repo."),
    ("validate", "[<name>] [--all] [--remote] [--verbose]",
     "Validate pattern files against the A2 spec (CI also runs this)."),
]

AUTHORING_CMDS = [
    ("init",     "<name> --scope core|slides|docs|projects/<id>",
     "Scaffold a new pattern file in the source repo (A2 template)."),
    ("promote",  "<pattern> [--message M] [--no-commit] [--allow-dirty]",
     "Push a locally-edited pattern back to the source repo (+ commit)."),
]

RELATED = ["stx install --project (opt-in patterns prompt)",
           "stx claude update", "stx project new"]


def _render_cmd_grid(commands):
    """Render a `(name, options, description)` list as a 3-column grid."""
    with st_grid(cols="1fr 2fr 3fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write(bs.body, (bs.keyword, "name"))
        with g.cell():
            st_write(bs.body, (bs.accent, "options"))
        with g.cell():
            st_write(bs.body, (s.bold, "description"))
        for name, opts, doc in commands:
            with g.cell():
                st_write(bs.body, (bs.keyword, name))
            with g.cell():
                st_write(bs.body, (bs.accent, opts))
            with g.cell():
                st_write(bs.body, doc)


def build():
    """Reference card for the top-level `stx patterns` CLI."""
    with st_block(s.center_txt):
        st_write(bs.heading,
                 "stx patterns <subcommand> [options]",
                 tag=t.div, toc_lvl="1")
        st_space("v", 1)
        st_write(bs.lead,
                 "Manage the StreamTeX pattern catalog inside a project — "
                 "interactive picker, declarative flags, drift-aware sync.")
        st_space("v", 2)

        # ---- Lifecycle ----
        st_write(bs.sub, "Lifecycle (day-to-day)", toc_lvl="+1")
        st_space("v", 0.5)
        _render_cmd_grid(LIFECYCLE_CMDS)
        st_space("v", 2)

        # ---- Source management ----
        st_write(bs.sub, "Source management (where do patterns come from?)",
                 toc_lvl="+1")
        st_space("v", 0.5)
        _render_cmd_grid(SOURCE_CMDS)
        st_space("v", 2)

        # ---- Catalog inspection ----
        st_write(bs.sub, "Catalog inspection", toc_lvl="+1")
        st_space("v", 0.5)
        _render_cmd_grid(CATALOG_CMDS)
        st_space("v", 2)

        # ---- Authoring ----
        st_write(bs.sub, "Authoring (contributors)", toc_lvl="+1")
        st_space("v", 0.5)
        _render_cmd_grid(AUTHORING_CMDS)
        st_space("v", 2)

        # ---- Common flags ----
        st_write(bs.sub, "Common flags", toc_lvl="+1")
        st_space("v", 0.5)
        with st_grid(cols="1fr 1fr 3fr", gap="8px", cell_styles=bs.cell) as g:
            with g.cell():
                st_write(bs.body, (bs.keyword, "--source"))
            with g.cell():
                st_write(bs.body, (bs.accent, "PATH"))
            with g.cell():
                st_write(bs.body,
                         "Override the pattern source path (top of "
                         "the resolution cascade).")
            with g.cell():
                st_write(bs.body, (bs.keyword, "--mode"))
            with g.cell():
                st_write(bs.body, (bs.accent, "copy | symlink"))
            with g.cell():
                st_write(bs.body,
                         "Install mode. `symlink` is for pattern authors "
                         "iterating live; `copy` (default) is for "
                         "consumer projects.")
            with g.cell():
                st_write(bs.body, (bs.keyword, "--force"))
            with g.cell():
                st_write(bs.body, (bs.accent, "(flag)"))
            with g.cell():
                st_write(bs.body,
                         "Override drift refusals. Use with caution.")
            with g.cell():
                st_write(bs.body, (bs.keyword, "--dry-run"))
            with g.cell():
                st_write(bs.body, (bs.accent, "(flag)"))
            with g.cell():
                st_write(bs.body,
                         "Print actions without writing files. Useful "
                         "before an update on a busy project.")
        st_space("v", 2)

        # ---- Returns / exit codes ----
        st_write(bs.sub, "Exit codes", toc_lvl="+1")
        st_space("v", 0.5)
        st_write(bs.body, "0 = success, "
                          "1 = generic error, "
                          "2 = drift refused (run `stx patterns diff` "
                          "or use `--force`).")
        st_space("v", 2)

        # ---- Examples ----
        st_write(bs.sub, "Examples", toc_lvl="+1")
        st_space("v", 0.5)
        show_explanation("""\
            Fresh project: bring the catalog in, then pick interactively.
        """)
        st_space("v", 0.5)
        show_code("""\
# 1. Make sure a patterns source is reachable for this workspace
stx patterns source show          # see what R4 resolves
stx patterns source clone         # one-time clone if nothing matched

# 2. Pick patterns to install (interactive composite picker)
stx patterns install              # menu: add presets, add individuals,
                                  # remove, toggle all, summary, done
stx patterns install --tag slide  # flat picker narrowed by tag

# 3. Declarative composite (CI, scripts, or reproducibility) — all
#    selectors are composable except --all (which is exclusive with
#    --preset/--pattern but still accepts --exclude).
stx patterns install --preset docs
stx patterns install --preset slides --preset docs       # multi-preset
stx patterns install --preset slides --exclude ptn_takeaways
stx patterns install --preset slides --pattern ptn_inline_emphasis
stx patterns install --all --exclude ptn_takeaways
stx patterns install --pattern ptn_callout,ptn_stat_hero

# 4. Day-to-day: check drift, refresh, reapply intent on a fresh clone
stx patterns status
stx patterns update
stx patterns sync                 # rebuilds from stx.toml [patterns.selection]

# 5. Pattern authors: edit locally, share back
stx patterns promote ptn_callout
""", language="bash")
        st_space("v", 2)

        # ---- See also ----
        st_write(bs.sub, "See also", toc_lvl="+1")
        st_space("v", 0.5)
        st_write(bs.body, (bs.keyword, "Related commands: "),
                 ", ".join(RELATED))
        st_space("v", 1)
