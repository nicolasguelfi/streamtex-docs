"""End-to-end install flow — source resolution, picker, sync, project bootstrap.

# @pattern: ptn_feature_walkthrough
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation


class BlockStyles:
    """Install-flow page styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    step = s.project.titles.body + s.bold + s.project.colors.primary_violet
    body = s.large
    callout = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.container.layouts.vertical_center_layout
        + s.center_txt
    )


bs = BlockStyles


def build():
    """How patterns actually get into a project — soup-to-nuts walkthrough."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Installing Patterns: End-to-End Flow",
                 tag=t.div, toc_lvl="1")
        st_space("v", 1)
        st_write(bs.body,
                 "From an empty project to a curated, versioned set of "
                 "design patterns — without imposing anything.")
        st_space("v", 2)

    # ---- Principle: subjective and opt-in --------------------------------
    st_write(bs.sub, "Guiding principle: subjective, opt-in",
             toc_lvl="+1")
    st_space("v", 1)
    show_explanation("""\
        Pattern selection is a *taste call*. A project that needs
        callouts and stat heroes has very little overlap with a project
        that needs API reference cards. So nothing is installed
        automatically: every install is either an **interactive pick**
        in a TTY, or an **explicit flag** in a script.

        Default-no everywhere. CI/non-TTY runs never get a hidden
        install.
    """)
    st_space("v", 2)

    # ---- Step 1: source resolution --------------------------------------
    st_write(bs.sub, "Step 1 — Where do patterns come from?",
             toc_lvl="+1")
    st_space("v", 1)
    show_explanation("""\
        Patterns live in the `streamtex-patterns` repository, separate
        from the library and consumer projects. The CLI finds it via a
        4-level resolution chain (R4), no environment variable involved.
    """)
    st_space("v", 1)
    show_code("""\
# R4 resolution order (first match wins):
#   L1  --source PATH                       (CLI override)
#   L2  <project>/stx.toml  [patterns].source     (or pyproject.toml)
#   L3  <workspace>/stx.toml  [patterns].source
#   L4  <workspace>/streamtex-patterns/     (auto-discover sibling)

# Debug what the resolver finds:
stx patterns source show
""", language="bash")
    st_space("v", 1)
    show_explanation("""\
        If R4 lands on nothing, three commands fix it — each addresses
        a different situation. They are interchangeable: pick whichever
        matches your setup.
    """)
    st_space("v", 1)
    show_code("""\
# (a) You don't have a clone yet, the official repo is fine
stx patterns source clone

# (b) You already have a clone somewhere; share it across workspaces
stx patterns source link /Users/me/dev/streamtex-patterns

# (c) You have a fork or a custom path; record it without cloning
stx patterns source set ../shared/patterns
""", language="bash")
    st_space("v", 2)

    # ---- Step 2: choose patterns ----------------------------------------
    st_write(bs.sub, "Step 2 — Pick patterns to install",
             toc_lvl="+1")
    st_space("v", 1)
    show_explanation("""\
        Pattern selection is a *composition*, not a single choice. You
        usually want one or more **presets** as a starting point, maybe
        add a few **individual patterns** on top, and possibly
        **exclude** a handful that don't fit. The CLI supports this on
        both sides:

        * **Interactive** — a menu-driven picker that lets you add
          presets, add individuals, remove from the resolved set, toggle
          'all', inspect a summary, and confirm.
        * **Declarative** — composable flags. `--preset` can be repeated;
          `--pattern` adds extras; `--exclude` subtracts. `--all` is the
          only exclusive flag (it implies "every pattern", still subject
          to `--exclude`).
    """)
    st_space("v", 1)
    show_code("""\
# Interactive composite picker (TTY) — menu loop, state persists across
# actions, summary view available, done/cancel at any time.
stx patterns install
stx patterns install --tag slide    # flat picker narrowed by tag

# Declarative — preferred for CI/scripts and reproducibility.
stx patterns install --preset slides
stx patterns install --preset slides --preset docs        # multi-preset
stx patterns install --preset slides --exclude ptn_takeaways
stx patterns install --preset slides --pattern ptn_inline_emphasis
stx patterns install --pattern ptn_callout,ptn_stat_hero
stx patterns install --all
stx patterns install --all --exclude ptn_takeaways        # all except some
""", language="bash")
    st_space("v", 1)
    show_explanation("""\
        Without any flag, **in a non-TTY context** the command refuses
        with a clear error — no hidden defaults, no surprise install.
        Pass any combination of `--preset / --pattern / --all / --exclude`
        to keep automation working.
    """)
    st_space("v", 2)

    # ---- Step 3: persistence + sync -------------------------------------
    st_write(bs.sub, "Step 3 — Persistence: intent vs cache",
             toc_lvl="+1")
    st_space("v", 1)
    show_explanation("""\
        Every install records two artefacts in the project:

        * **`.patterns-meta.json`** — execution cache: SHA per pattern,
          drift baseline. Not normally versioned.
        * **`<project>/stx.toml`  [patterns.selection]** — *your intent*
          (preset name, hand-picked list, or `all`). **Versioned with
          the project.**

        On a fresh `git clone`, the cache is missing but the intent is
        present in `stx.toml` — `stx patterns sync` rebuilds the same
        set deterministically.
    """)
    st_space("v", 1)
    show_code("""\
# Project's stx.toml after a composite install
# (`stx patterns install --preset slides --pattern ptn_a --exclude ptn_x`):
[patterns]
source = "../../streamtex-patterns"

[patterns.selection]
presets = ["slides"]              # taken in full
individuals = ["ptn_a"]           # extra on top
excludes = ["ptn_x"]              # subtracted from the union
all = false                       # true = "everything, subject to excludes"
""", language="toml")
    st_space("v", 1)
    show_code("""\
# Day-to-day lifecycle:
stx patterns status       # what is installed, has anything drifted?
stx patterns sync         # apply intent (install missing, refresh)
stx patterns update       # pull source-side updates, drift-aware
stx patterns diff ptn_x   # local-vs-source for one pattern
stx patterns remove ptn_x # uninstall
""", language="bash")
    st_space("v", 2)

    # ---- Step 4: bootstrap from project creation ------------------------
    st_write(bs.sub, "Step 4 — Bootstrap from `stx install --project`",
             toc_lvl="+1")
    st_space("v", 1)
    show_explanation("""\
        When you scaffold a brand-new project with the workspace install
        command, an **opt-in prompt** offers to set patterns up in one
        go. Two questions, both default to NO:

        1. If no source is reachable: *"Clone the streamtex-patterns
           repo into the workspace now?"* — runs `stx patterns source
           clone` if accepted.
        2. *"Pick design patterns to install in this project now
           (interactive)?"* — opens the picker if accepted; selected
           patterns land in `.claude/custom/streamtex-patterns/` and
           the intent is written to the project's `stx.toml`.

        Skip the entire sequence with `--no-patterns`. The prompt is
        also silent in non-TTY contexts.
    """)
    st_space("v", 1)
    show_code("""\
# Full happy path
stx install --project hello
#  → ... project scaffolded ...
#  → Design patterns (optional)
#    No patterns repository detected for this workspace.
#    Clone streamtex-patterns into the workspace now? [y/N]: y
#  → Cloned https://.../streamtex-patterns.git → .../streamtex-patterns
#    Pick design patterns to install now (interactive)? [y/N]: y
#  → [opens picker]
#  → Installed 4 pattern(s) into .claude/custom/streamtex-patterns

# Skip the patterns offer entirely
stx install --project hello --no-patterns
""", language="bash")
    st_space("v", 2)

    # ---- Recap ----------------------------------------------------------
    st_write(bs.sub, "Recap (cheatsheet)", toc_lvl="+1")
    st_space("v", 1)
    show_code("""\
# Source not reachable?
stx patterns source show          # diagnose
stx patterns source clone         # … and bring one in

# Pick patterns
stx patterns install              # interactive
stx patterns install --preset X   # declarative

# Re-apply on a fresh clone of the project
stx patterns sync

# Refresh from upstream
stx patterns update
""", language="bash")
    st_space("v", 1)
