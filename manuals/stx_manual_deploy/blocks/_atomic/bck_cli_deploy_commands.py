"""Atomic block — CLI Deploy Commands reference."""

import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details
import textwrap


class BlockStyles:
    """CLI deploy commands styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles


def build():
    """CLI Deploy Commands — stx deploy subcommands."""
    with st_block(s.center_txt):
        st_write(bs.heading, "CLI Deploy Commands", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            The stx deploy command group handles all deployment
            workflows. Each subcommand targets a specific platform
            or deployment step.
        """)
        st_space("v", 2)

        # --- stx deploy preflight ---
        st_write(bs.sub, "stx deploy preflight", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Run pre-deployment checks before deploying to any
            platform. Validates project structure, dependencies,
            and configuration files.
        """)
        st_space("v", 1)

        show_code(textwrap.dedent("""\
            stx deploy preflight
        """), language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy docker ---
        st_write(bs.sub, "stx deploy docker", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Build a Docker image and run it locally.
            Uses the repository Dockerfile with the correct
            FOLDER build-arg for your project.
        """)
        st_space("v", 1)

        show_code(textwrap.dedent("""\
            # Build and run with default settings
            stx deploy docker

            # Specify a custom port
            stx deploy docker --port 8502
        """), language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy render ---
        st_write(bs.sub, "stx deploy render", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Deploy your project to Render.com. Generates the
            render.yaml blueprint and triggers the deployment
            pipeline.
        """)
        st_space("v", 1)

        show_code(textwrap.dedent("""\
            stx deploy render
        """), language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy huggingface ---
        st_write(bs.sub, "stx deploy huggingface", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Deploy your project to HuggingFace Spaces.
            Pushes the project as a Streamlit Space with the
            correct app configuration.
        """)
        st_space("v", 1)

        show_code(textwrap.dedent("""\
            stx deploy huggingface
        """), language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy status ---
        st_write(bs.sub, "stx deploy status", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Check the current deployment status across all
            configured platforms. Reports build state, URL,
            and last deployment timestamp.
        """)
        st_space("v", 1)

        show_code(textwrap.dedent("""\
            stx deploy status
        """), language="bash", line_numbers=False)
        st_space("v", 2)
