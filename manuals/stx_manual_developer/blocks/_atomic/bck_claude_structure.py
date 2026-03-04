from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Claude directory structure styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, ".claude/ Directory Structure",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- Overview ---
        st_write(bs.sub, "Overview", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The .claude/ directory contains all configuration and
            context files for Claude Code sessions. It defines
            the profile type, permissions, coding standards, and
            custom commands available during AI-assisted development.
        """)
        st_space("v", 2)

        # --- Directory tree ---
        st_write(bs.sub, "Directory layout", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
.claude/
 |-- .stx-profile              # Profile type identifier
 |-- settings.json              # Claude Code permission config
 |
 |-- references/                # Shared (read-only, from shared/references/)
 |    |-- coding_standards.md   # Full coding standards
 |    +-- streamtex_cheatsheet_en.md  # Syntax reference
 |
 |-- commands/
 |    |-- stx-guide.md          # Shared (read-only, from shared/commands/)
 |    +-- developer/
 |         |-- test-run.md      # /test-run command
 |         |-- lint.md          # /lint command
 |         +-- deploy.md        # /deploy command
 |
 |-- developer/
 |    +-- skills/
 |         |-- architecture.md  # Architecture knowledge
 |         +-- testing-patterns.md  # Testing patterns

CLAUDE.md                       # Root rules file (project root)""", language="text")
        st_space("v", 2)

        # --- .stx-profile ---
        st_write(bs.sub, ".stx-profile", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The .stx-profile file identifies the project type.
            It contains a single keyword: library, docs, or project.
            The stx claude commands use this to determine which
            profile template to apply.
        """)
        st_space("v", 1)

        show_code("""\
# .claude/.stx-profile
library""", language="text")
        st_space("v", 2)

        # --- settings.json ---
        st_write(bs.sub, "settings.json", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The settings.json file configures permissions for
            Claude Code. It controls which tools Claude can use,
            which directories it can access, and which commands
            it is allowed to run. This is a security boundary
            for AI-assisted development.
        """)
        st_space("v", 2)

        # --- references/ ---
        st_write(bs.sub, "references/", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The references directory contains documentation that
            Claude reads before generating any code:

            - **coding_standards.md**: the single source of truth for
              all coding conventions (style, naming, patterns).
            - **streamtex_cheatsheet_en.md**: a quick-reference for
              StreamTeX API syntax and common patterns.

            These files ensure Claude generates code that follows
            project conventions consistently.
        """)
        st_space("v", 2)

        # --- developer/skills/ ---
        st_write(bs.sub, "developer/skills/", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Skills provide domain-specific knowledge to Claude:

            - **architecture.md**: describes the module structure,
              dependency graph, and design patterns used.
            - **testing-patterns.md**: documents testing conventions,
              fixtures, and common test patterns.

            Claude loads these automatically when relevant tasks
            are detected.
        """)
        st_space("v", 2)

        # --- commands/ ---
        st_write(bs.sub, "commands/developer/", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Custom commands are markdown files that define
            slash-commands for Claude Code sessions:

            - **test-run.md**: /test-run — runs the test suite.
            - **lint.md**: /lint — runs the linter.
            - **deploy.md**: /deploy — runs deployment checks.

            Each file contains instructions that Claude follows
            when the corresponding command is invoked.
        """)
        st_space("v", 2)

        # --- CLAUDE.md ---
        st_write(bs.sub, "CLAUDE.md", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            **CLAUDE.md** sits at the project root (not inside .claude/).
            It is the root rules file that Claude Code reads at the
            start of every session. It contains:

            - **Project identity** and terminology.
            - **Mandatory environment rules** (always use uv run).
            - **Context loading requirements**.
            - **Key component references**.
            - **Workflow instructions**.
        """)
        st_space("v", 2)

        show_details("""\
            The .claude/ directory is committed to git and shared
            across all developers. This ensures consistent AI-assisted
            development experiences for the entire team.
        """)
