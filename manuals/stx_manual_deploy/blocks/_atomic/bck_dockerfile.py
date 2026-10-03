"""Atomic block — The StreamTeX Dockerfile explained."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details
import os

# _atomic/ → blocks/ → project root → manuals/ → repo root
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_repo_root = os.path.dirname(os.path.dirname(_project_root))
_dockerfile_path = os.path.join(_repo_root, "Dockerfile")
_dockerignore_path = os.path.join(_repo_root, ".dockerignore")

class BlockStyles:
    """Dockerfile block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Docker Local Deployment", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- 1. The Dockerfile ---
        st_write(bs.sub, "The StreamTeX Dockerfile", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "The repository includes a production-ready Dockerfile at the root. "
            "It uses a multi-stage strategy: install uv, sync dependencies in a cached layer, "
            "then copy the target project. The FOLDER build-arg selects which project to deploy."
        )
        st_space("v", 1)

        try:
            with open(_dockerfile_path) as f:
                dockerfile_content = f.read()
        except FileNotFoundError:
            dockerfile_content = "# Dockerfile not found at expected path"

        show_code(dockerfile_content, language="dockerfile")
        st_space("v", 2)

        # --- 2. Environment variables ---
        st_write(bs.sub, "Environment variables", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "The Dockerfile sets several ENV variables for headless operation and performance."
        )
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Variable")
            with g.cell(): st_write(s.bold + s.large, "Purpose")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "STREAMLIT_SERVER_HEADLESS=true")
            with g.cell():
                st_write(s.large, "Run without opening a browser")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "PYTHONDONTWRITEBYTECODE=1")
            with g.cell():
                st_write(s.large, "Skip .pyc file creation (smaller image)")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "PYTHONUNBUFFERED=1")
            with g.cell():
                st_write(s.large, "Real-time log output")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "UV_LINK_MODE=copy")
            with g.cell():
                st_write(s.large, "Copy files instead of hardlinks (Docker compat)")

        st_space("v", 2)

        # --- 3. .dockerignore ---
        st_write(bs.sub, "The .dockerignore file", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "The **.dockerignore** excludes files not needed in production images: "
            "**tests**, **IDE config**, **.git**, **.venv**, documentation markdown files, etc. "
            "This reduces image size and build time."
        )
        st_space("v", 1)

        try:
            with open(_dockerignore_path) as f:
                dockerignore_content = f.read()
        except FileNotFoundError:
            dockerignore_content = "# .dockerignore not found"

        show_code(dockerignore_content, language="text")
        st_space("v", 2)

        show_details(
            "The container exposes **port 8501** with a built-in **health check**.\n\n"
            "**uv** is installed from the official Docker image (ghcr.io/astral-sh/uv).\n\n"
            "Dependencies are installed in a **cached layer** for fast rebuilds."
        )
        st_space("v", 3)

        # --- 4. Generated deployment files (0.7.38) ---
        st_write(bs.sub, "Generated files: Dockerfile, entrypoint.sh, nginx.conf", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "For a project without them, **stx deploy** generates `Dockerfile`, "
            "`entrypoint.sh` and `nginx.conf` from templates. Since 0.7.38 the "
            "templates **never fail in silence**: when the cache warmup or the static "
            "export fails at start-up, the entrypoint writes the error to the container "
            "log (stderr) and appends a line to **/app/STX_ERRORS.txt** — outside the "
            "folder nginx serves, so the error log is never public — and the service "
            "still starts. The Dockerfile **no longer exports at build time**: the "
            "static HTML is generated once, by the entrypoint, for the active FOLDER "
            "(the build-time export ran twice and failed silently at the root of "
            "multi-module repositories)."
        )
        st_space("v", 1)

        show_explanation("The failure report of the current entrypoint template (read from the library):")
        st_space("v", 1)

        try:
            from streamtex.cli.deploy_cmd import generate_entrypoint
            _lines = generate_entrypoint().splitlines()
            _start = next(i for i, ln in enumerate(_lines) if ln.startswith("# A failure below"))
            _end = next(i for i, ln in enumerate(_lines) if "stx export html" in ln and "report_failure" in ln)
            entrypoint_excerpt = "\n".join(_lines[_start:_end + 1])
        except (ImportError, StopIteration):
            entrypoint_excerpt = "# install streamtex[cli] to display the template"
        show_code(entrypoint_excerpt, language="bash")
        st_space("v", 1)

        show_code("""\
            # After a start-up, look for a failure
            docker logs <container> 2>&1 | grep "\\[entrypoint\\] ERROR"
            docker exec <container> cat /app/STX_ERRORS.txt
        """, language="bash")
        st_space("v", 2)

        st_write(bs.sub, "Existing projects — stx deploy diff", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "**stx deploy** only generates these files when they are **missing**: a "
            "project keeps its own copy, and its own changes to it. Only newly "
            "generated files get the new templates. **stx deploy diff** shows, as a "
            "unified diff, how the project's `Dockerfile`, `entrypoint.sh` and "
            "`nginx.conf` differ from the current templates — nothing is written."
        )
        st_space("v", 1)

        show_code("""\
            stx deploy diff                 # the current project
            stx deploy diff path/to/project
        """, language="bash")
        st_space("v", 1)

        show_details(
            "Typical output: `entrypoint.sh: differs from the template` followed by the "
            "diff (template → project), or `identical to the template`, or "
            "`absent (stx deploy would generate it)`. To adopt the new template, delete "
            "the file and run stx deploy again, or merge the diff by hand to keep your "
            "own changes."
        )

