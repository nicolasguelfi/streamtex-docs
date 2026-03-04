"""More Project Commands — course-generate, collection-new, project-upgrade."""

from streamtex import st_write, st_space, st_block, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Other project commands block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cmd_title = s.project.colors.ai_violet + s.bold + s.Large


bs = BlockStyles


def build():
    """Render the Other Project Commands section."""
    st_space("v", 1)
    st_write(bs.heading, "More Project Commands", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        Beyond project-init and project-customize, the Project category
        offers three more commands for generating courses, creating
        multi-project collections, and upgrading project boilerplate.
    """)
    st_space("v", 2)

    # ── Command 1: course-generate ─────────────────────────────────
    st_write(bs.sub, "/project:course-generate", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_block(s.project.containers.ai_callout):
        st_write(bs.cmd_title, "Generate book.py from CSV", tag=t.div)
        st_space("v", 1)
        st_write(
            s.large,
            "Creates a complete book.py orchestration file from a ",
            (s.bold, "blocks.csv "),
            "file. Each row in the CSV defines a block name, its title, ",
            "and the table-of-contents level.",
        )
    st_space("v", 1)

    st_write(
        s.large,
        (s.bold, "CSV format: "),
        "block_name, title, toc_level",
    )
    st_space("v", 1)

    show_code("""\
        # blocks.csv
        bck_01_title, Welcome to the Course, 0
        bck_02_overview, Course Overview, 1
        bck_03_fundamentals, Core Fundamentals, 1
        bck_04_data_types, Data Types, 2
        bck_05_functions, Functions, 2
        bck_06_oop, Object-Oriented Programming, 1
        bck_07_classes, Classes and Objects, 2
        bck_08_inheritance, Inheritance, 2
        bck_09_practice, Practice Exercises, 1
        bck_10_summary, Course Summary, 1""", language="python")
    st_space("v", 1)

    st_write(s.large, "The generated book.py:")
    st_space("v", 1)

    show_code("""\
        \"\"\"Auto-generated course orchestration.\"\"\"

        from streamtex import st_book

        blocks = [
            "bck_01_title",
            "bck_02_overview",
            "bck_03_fundamentals",
            "bck_04_data_types",
            "bck_05_functions",
            "bck_06_oop",
            "bck_07_classes",
            "bck_08_inheritance",
            "bck_09_practice",
            "bck_10_summary",
        ]

        st_book(blocks, paginate=True)""", language="python")
    st_space("v", 2)

    # ── Command 2: collection-new ──────────────────────────────────
    st_write(bs.sub, "/project:collection-new", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_block(s.project.containers.ai_callout):
        st_write(bs.cmd_title, "Create a Collection Hub", tag=t.div)
        st_space("v", 1)
        st_write(
            s.large,
            "Creates a multi-project collection that links several ",
            "StreamTeX manuals together into a unified hub. The hub ",
            "displays cards for each manual with links to their ",
            "deployed URLs.",
        )
    st_space("v", 1)

    show_code("""\
        /project:collection-new

        > Create a collection hub linking:
          - Introduction Manual (streamtex-intro.onrender.com)
          - Advanced Manual (streamtex-advanced.onrender.com)
          - Deploy Manual (streamtex-deploy.onrender.com)""",
        language="bash", line_numbers=False)
    st_space("v", 1)

    st_write(s.large, "The AI generates a collection book.py using st_collection:")
    st_space("v", 1)

    show_code("""\
        \"\"\"Collection hub — links all manuals together.\"\"\"

        from streamtex import st_collection

        config = {
            "title": "StreamTeX Documentation",
            "manuals": [
                {
                    "name": "Introduction",
                    "url": "https://streamtex-intro.onrender.com",
                    "description": "Getting started with StreamTeX",
                },
                {
                    "name": "Advanced",
                    "url": "https://streamtex-advanced.onrender.com",
                    "description": "Advanced features and patterns",
                },
                {
                    "name": "Deploy",
                    "url": "https://streamtex-deploy.onrender.com",
                    "description": "Deployment and CI/CD guide",
                },
            ],
        }

        st_collection(config)""", language="python")
    st_space("v", 2)

    # ── Command 3: project-upgrade ─────────────────────────────────
    st_write(bs.sub, "/project:project-upgrade", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_block(s.project.containers.ai_callout):
        st_write(bs.cmd_title, "Upgrade Project Boilerplate", tag=t.div)
        st_space("v", 1)
        st_write(
            s.large,
            "Updates your project's infrastructure files to the latest ",
            "StreamTeX patterns. It modifies boilerplate while ",
            (s.bold, "preserving your custom code"),
            ".",
        )
    st_space("v", 1)

    st_write(s.large, "Files updated by project-upgrade:")
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item():
            st_write(
                s.large,
                (s.bold, "setup.py "),
                "— updated to latest entry-point pattern",
            )
        with l.item():
            st_write(
                s.large,
                (s.bold, ".streamlit/config.toml "),
                "— new Streamlit config keys added",
            )
        with l.item():
            st_write(
                s.large,
                (s.bold, "blocks/__init__.py "),
                "— updated to latest ProjectBlockRegistry pattern",
            )
        with l.item():
            st_write(
                s.large,
                (s.bold, "blocks/helpers.py "),
                "— updated to latest BlockHelperConfig pattern",
            )
    st_space("v", 1)

    show_code("""\
        /project:project-upgrade

        Checking project version ...
          Current: streamtex X.Y.Z patterns
          Latest:  streamtex X.Y.Z patterns

        Upgrading ...
          setup.py ................... UPDATED (new entry point)
          .streamlit/config.toml ..... UPDATED (2 new keys)
          blocks/__init__.py ......... UPDATED (ProjectBlockRegistry)
          blocks/helpers.py .......... UPDATED (BlockHelperConfig DI)
          custom/styles.py ........... SKIPPED (custom code preserved)
          blocks/bck_*.py ............ SKIPPED (custom code preserved)

        Done: 4 files updated, 2 skipped (custom).""",
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Tip ────────────────────────────────────────────────────────
    show_details("""\
        Tip: run project-upgrade after updating the streamtex library
        to a new version. It ensures your boilerplate matches the
        latest conventions without touching your content blocks or
        custom styles. Always review the changes before committing.
    """)
    st_space("v", 1)
