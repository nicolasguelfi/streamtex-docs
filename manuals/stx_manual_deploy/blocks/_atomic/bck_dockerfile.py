"""Atomic block — The StreamTeX Dockerfile explained."""

from streamtex import *
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details
import os

# _atomic/ → blocks/ → project root → manuals/ → repo root
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_repo_root = os.path.dirname(os.path.dirname(_project_root))
# In the Docker image these files are copied to /app/repo-files (see
# Dockerfile); read that copy first, then fall back to the repo root.
_repo_files = os.environ.get("STX_REPO_FILES", "/app/repo-files")
_dockerfile_path = next(
    (p for p in (os.path.join(_repo_files, "Dockerfile"),
                 os.path.join(_repo_root, "Dockerfile"))
     if os.path.isfile(p)),
    os.path.join(_repo_root, "Dockerfile"),  # missing -> "not found" below
)
_dockerignore_path = next(
    (p for p in (os.path.join(_repo_files, ".dockerignore"),
                 os.path.join(_repo_root, ".dockerignore"))
     if os.path.isfile(p)),
    os.path.join(_repo_root, ".dockerignore"),  # missing -> "not found" below
)

def _generated(generator) -> str:
    """A deployment file as the installed library generates it for a new project."""
    try:
        from streamtex.cli import deploy_cmd
    except ImportError:
        return "# install streamtex[cli] to display the template"
    return getattr(deploy_cmd, generator)()


# (file name, generator in streamtex.cli.deploy_cmd, language)
_GENERATED = [
    ("Dockerfile", "generate_dockerfile", "dockerfile"),
    ("entrypoint.sh", "generate_entrypoint", "bash"),
    ("nginx.conf", "generate_nginx_conf", "nginx"),
    (".dockerignore", "generate_dockerignore", "text"),
]


def _latex_size() -> str:
    """The image size LaTeX adds, as the Dockerfile template's own comment states it."""
    import re

    m = re.search(r"about (\d+ [MG]B)", _generated("generate_dockerfile"))
    return f"about {m.group(1)} more in the image." if m else "a few hundred MB more in the image."


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
            "The manuals repository includes a production Dockerfile at its root, shown below "
            "as a worked example: install uv, sync the dependencies in a cached layer, then copy "
            "the manuals. The **FOLDER** environment variable, set at run time by Coolify, "
            "selects which manual the container serves. A project of your own gets a generated "
            "Dockerfile instead (see *Generated files* below)."
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
            "The Dockerfiles set several ENV variables for headless operation and performance. "
            "UV_NO_SOURCES_PACKAGE is set by the generated Dockerfile."
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
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "STREAMLIT_BROWSER_GATHERUSAGESTATS=false")
            with g.cell():
                st_write(s.large, "No usage statistics sent by Streamlit")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "UV_NO_SOURCES_PACKAGE=streamtex")
            with g.cell():
                st_write(s.large, "streamtex never comes from a local path (a stx dev link "
                         "source points outside the build context): the published wheel is "
                         "installed. Set as ENV, it holds for every uv command — the build "
                         "steps and the entrypoint's uv run — while local packs keep their source")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "STX_SERVE_MODE=dual")
            with g.cell():
                st_write(s.large, "Default serve mode (Nginx + Streamlit); Coolify can override it")

        st_space("v", 2)

        # --- 3. .dockerignore ---
        st_write(bs.sub, "The .dockerignore file", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "The **.dockerignore** excludes files not needed in production images: "
            "**tests**, **IDE config**, **.git**, **.venv**, documentation markdown files, etc. "
            "This reduces image size and build time. It also keeps **secret files** out of the "
            "image: `COPY . .` would otherwise copy `.env`, `.stx-deploy.env` (the Coolify token) "
            "and `.stx-passwords.toml` (plain passwords) into it. The `.dockerignore` that "
            "**stx deploy** generates (below) excludes these three; `stx deploy preflight` warns "
            "when a project's own `.dockerignore` misses one that is present."
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

        # --- 4. Generated deployment files (read live from the library) ---
        st_write(bs.sub, "Generated files: Dockerfile, entrypoint.sh, nginx.conf, .dockerignore",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "For a project without them, **stx deploy docker** (and **stx deploy huggingface**) "
            "generate `Dockerfile`, `entrypoint.sh`, `nginx.conf` and `.dockerignore` from templates. "
            "**stx deploy hetzner** does not: Coolify builds from the git repository, so generate the "
            "files (`stx deploy docker --build-only` also tests the image) and commit them first. The "
            "four files below are produced by the installed library at the moment this page renders: "
            "they are exactly what a new project receives."
        )
        st_space("v", 1)

        with st_block(s.project.containers.tip_callout):
            st_write(s.project.titles.tip_label, "What the templates do")
            st_space("v", 1)
            with st_list(list_type=lt.unordered, text_align="left") as l:
                with l.item():
                    st_write(s.large, (s.bold, "Dependencies: "),
                             "uv sync --no-dev with UV_NO_SOURCES_PACKAGE=streamtex (the published "
                             "streamtex, never a local path), then the stx CLI dependencies. Chromium "
                             "only when the project has playwright (the pdf extra).")
                with l.item():
                    st_write(s.large, (s.bold, "LaTeX only when needed: "),
                             "when a .py file of the project calls st_tikz, the build installs TeX Live "
                             "and dvisvgm — " + _latex_size() + " Without st_tikz, nothing is installed.")
                with l.item():
                    st_write(s.large, (s.bold, "Nothing exported at build time: "),
                             "the entrypoint warms the page cache and exports the static HTML at "
                             "start-up, once, for the active FOLDER.")
                with l.item():
                    st_write(s.large, (s.bold, "Never silent: "),
                             "when the cache warm-up or the export fails, the service still starts, the "
                             "error goes to the container log ([entrypoint] ERROR: ...) and a line is "
                             "appended to /app/STX_ERRORS.txt.")
                with l.item():
                    st_write(s.large, (s.bold, "Login screen inactive by default: "),
                             "nginx.conf includes the stx-auth snippets, which stay empty unless "
                             "stx deploy lock sets STX_AUTH_LIVE / STX_AUTH_HTML (see Access Control).")
        st_space("v", 1)

        with st_block(s.project.containers.bad_callout):
            st_write(s.project.titles.warning_label, "STX_ERRORS.txt is private since 0.7.41")
            st_space("v", 1)
            st_write(s.large,
                     "The error log is /app/STX_ERRORS.txt, outside /app/static-html/ that nginx serves "
                     "with autoindex. An entrypoint generated by streamtex 0.7.38 to 0.7.40 wrote it ",
                     (s.bold, "inside"), " that folder: it was public at /html/STX_ERRORS.txt. A "
                     "service deployed with one of those versions keeps its entrypoint — run ",
                     (s.bold, "stx deploy diff"), " and adopt the current template.")
        st_space("v", 1)

        for name, generator, language in _GENERATED:
            st_write(s.project.titles.subsection_title, name)
            st_space("v", 0.5)
            show_code(_generated(generator), language=language)
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
            "unified diff, how the project's `Dockerfile`, `entrypoint.sh`, "
            "`nginx.conf` and `.dockerignore` differ from the current templates — "
            "nothing is written."
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

