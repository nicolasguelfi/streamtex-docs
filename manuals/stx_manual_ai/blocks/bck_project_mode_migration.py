"""Part 2 — Migrating from the classic (machine) mode to project mode."""

from streamtex import st_write, st_space, st_block
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Project-mode migration block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Migrating to project mode — projects first, global removal last."""
    st_space("v", 1)
    st_write(bs.heading, "Migrating to Project Mode", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        This guide moves a workspace from the classic machine mode
        (stx claude install in each project, shared commands copied
        into ~/.claude/commands) to project mode (each project declares
        its profile in stx.toml, stx claude sync keeps .claude/ in
        line). The order matters: migrate every project first, and
        remove the global commands last.
    """)
    st_space("v", 2)

    # --- Step 1 ---
    st_write(bs.sub, "Step 1 — Upgrade streamtex Everywhere", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Project mode needs streamtex 0.7.35 or newer, on every machine
        that works on the project. stx claude update run with
        streamtex 0.7.34 or older does not know .claude/stx.lock and
        removes it as an orphan.
    """)
    st_space("v", 1)

    show_code("""\
        # The CLI (install and upgrade use the same command)
        uv tool install "streamtex[cli]" -U

        # Check the version
        stx --version
    """, language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Step 2 ---
    st_write(bs.sub, "Step 2 — Declare the Profile in Each Project",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Read the profile installed today in .claude/.stx-profile and
        declare the same one in the project's stx.toml. Keep include
        and exclude empty for the first sync, so that the migration
        changes nothing else.
    """)
    st_space("v", 1)

    show_code("""\
        cd projects/my-deck
        cat .claude/.stx-profile      # e.g. presentation
    """, language="bash", line_numbers=False)
    st_space("v", 1)

    show_code("""\
        # projects/my-deck/stx.toml
        [claude]
        mode = "project"
        profile = "presentation"
        include = []
        exclude = []
    """, language="toml", line_numbers=False)
    st_space("v", 2)

    # --- Step 3 ---
    st_write(bs.sub, "Step 3 — Preview, then Sync", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The first sync over a classic install has no lock yet: a
        read-only installed file is taken as an stx copy and updated;
        a file you made writable and edited is kept and reported.
        Files stx never installed and .claude/custom/ are never
        touched. Run the dry run first and read the report.
    """)
    st_space("v", 1)

    show_code("""\
        stx claude sync --dry-run   # what would change — nothing written
        stx claude sync             # writes .claude/ and .claude/stx.lock
    """, language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Step 4 ---
    st_write(bs.sub, "Step 4 — Commit the Declaration and the Lock",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        stx never commits. sync completes .gitignore so that the
        installed copies are ignored while custom/, .stx-profile and
        stx.lock stay tracked. Commit the result yourself. If the
        copies were tracked before, untrack them in the same commit.
    """)
    st_space("v", 1)

    show_code("""\
        # Only if .claude/ was tracked before: untrack the copies
        git rm -r --cached .claude --quiet

        git add stx.toml .gitignore .claude/stx.lock .claude/.stx-profile .claude/custom
        git commit -m "chore: Claude profile in project mode"
    """, language="bash", line_numbers=False)
    st_space("v", 1)

    show_explanation("""\
        Repeat steps 2 to 4 in every project of the workspace,
        including the workspace root if it has a profile.
    """)
    st_space("v", 2)

    # --- Step 5 ---
    st_write(bs.sub, "Step 5 — Check the Duplicates", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        While the global copy is still in place, every migrated project
        loads its stx commands twice: from .claude/commands and from
        ~/.claude/commands. stx claude check lists those duplicates;
        they disappear in the next step.
    """)
    st_space("v", 1)

    show_code("""\
        stx claude check     # project-mode targets are checked through sync
        stx status           # same "Claude commands" report
    """, language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Step 6 ---
    st_write(bs.sub, "Step 6 — Remove the Global Commands, Last",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Only when every project has its own profile, remove the stx
        copies from ~/.claude/commands and turn the copy off, otherwise
        the next stx update copies them again. A file you changed in
        ~/.claude/commands is kept and listed.
    """)
    st_space("v", 1)

    show_code("""\
        stx claude global status        # current / outdated / obsolete / modified by you
        stx claude global remove        # dry run: what would be removed
        stx claude global remove --yes  # remove the stx copies
    """, language="bash", line_numbers=False)
    st_space("v", 1)

    show_code("""\
        # ~/.config/streamtex/config.toml
        [claude]
        global_commands = false
    """, language="toml", line_numbers=False)
    st_space("v", 2)

    with st_block(s.project.containers.bad_callout):
        st_write(s.project.colors.error_red + s.bold,
                 "Why the global removal comes last")
        st_space("v", 1)
        st_write(s.large,
                 "A project that still uses the classic mode has no local "
                 "copy of the shared commands (such as ",
                 (s.bold, "/stx-guide"),
                 "): removing ~/.claude/commands first leaves Claude Code "
                 "without them in that project. With the global copy off, ",
                 (s.bold, "stx claude check"),
                 " warns when no project of the workspace has a local "
                 "profile.")
    st_space("v", 2)

    # --- Other machines ---
    st_write(bs.sub, "On the Other Machines", toc_lvl="+1")
    st_space("v", 1)

    show_code("""\
        uv tool install "streamtex[cli]" -U   # streamtex 0.7.35+
        git pull
        stx claude sync                       # rebuilds .claude/ from stx.toml + stx.lock
        stx claude global remove --yes        # once every project is migrated
    """, language="bash", line_numbers=False)
    st_space("v", 2)

    show_details("""\
        To go back to the classic mode in one project, uninstall with
        stx claude sync --remove (custom/ and your edited files are
        kept), delete the [claude] section of stx.toml, then run
        stx claude install <profile>. To bring the global commands
        back, set global_commands = true (or pass --global-commands)
        and run stx update.
    """)
    st_space("v", 1)
