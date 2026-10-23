"""Block — Multi-document projects: stx release (streamtex 0.7.58, #136, #111).

The command list is read from the installed library at render time.
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """stx release block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cmd = s.project.colors.accent_teal + s.big
    txt = s.big
bs = BlockStyles


def _commands() -> list[tuple[str, str]]:
    """(name, one-line help) of every `stx release` command, from the installed library."""
    try:
        from streamtex.cli.release_cmd import release
    except ImportError:
        return []
    out = []
    for name, cmd in sorted(release.commands.items()):
        out.append((name, (cmd.help or "").strip().split("\n")[0]))
    return out


def build():
    st_write(bs.heading, "Multi-Document Projects — stx release", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        `stx deploy hetzner` puts ONE document online, one Coolify
        application per document. A project with many documents (a course
        catalogue: slides, packs, practicals, each in two languages) uses
        `stx release` instead: two long-lived Coolify applications for the
        whole project, a static one (nginx, the HTML exports) and a live one
        (one Streamlit process per document behind an nginx router). Each
        document is a site, `<site>.<domain>`, with up to two faces: the
        Streamlit app and the HTML version.
    """)
    st_space("v", 2)

    st_write(bs.sub, "What one publication does", toc_lvl="+1")
    st_space("v", 1)
    show_explanation("""\
        A committed repository is required (the release is the commit). The
        code snapshot is exported to HTML once per language on this machine
        and checked; the delta is copied over SSH (rsync --link-dest); the
        passwords are written; both faces of the site switch together;
        only that site's Streamlit process restarts; then what is actually
        served is checked, as a visitor. A failed check puts both faces back
        on the previous release. Two releases are kept per site.
    """)
    st_space("v", 2)

    st_write(bs.sub, "Declaring the sites", toc_lvl="+1")
    st_space("v", 1)
    show_code("""\
        # stx.toml
        [release]
        project = "trainings"            # media folder on the server, Coolify project
        langs = ["en", "fr"]             # one HTML export per language
        snapshot = ["content", "shared"] # in every code snapshot
        media = "assets"                 # copied once, linked into every snapshot

        [[release.sites]]
        site = "chat1d-slides"           # written, checked (DNS label, unique)
        book = "trainings/CHAT1D/slides/book.py"
        group = "CHAT1D"                 # its password group
        zoom = 80                        # optional: HTML face opens as at 80 % (0.7.63)

        [[release.sites]]
        site = "chat1d"                  # a home page: HTML only, published when named
        book = "trainings/CHAT1D/home/book.py"
        group = "CHAT1D"
        faces = ["html"]
        explicit = true

        # or, for a computed list:  sites_from = "shared.release:sites" """,
              language="toml", line_numbers=False)
    st_space("v", 1)
    show_details("""\
        - Other site keys: `faces` (default both), `paths` (its part of the
        code snapshot), `exclude`, `explicit`.
        - `zoom = 80` (streamtex 0.7.63, a positive percentage): the HTML
        face is exported with `stx export html --zoom 80`, so it opens as
        if the browser were at 80 %. The live face is unchanged.
    """)
    st_space("v", 2)

    st_write(bs.sub, "Passwords per site", toc_lvl="+1")
    st_space("v", 1)
    show_code("""\
        # .stx-passwords.toml (git-ignored): [default] → [group] → [group.sites.site]
        [default]
        live = "TRAINER:t-pass"
        html = [["PROMO-OCT", "oct-pass"], ["PROMO-NOV", "nov-pass", "2026-11-30"]]

        [CHAT1D]
        html = "PROMO-DEC:dec-pass:2026-12-31,GUEST:guest-pass"

        [CHAT1D.sites.chat1d]
        open = ["html"]                  # explicit: an empty string is refused""",
              language="toml", line_numbers=False)
    st_space("v", 1)
    show_details("""\
        - Each face takes a list of accepted passwords, each with a label
        (it names the access in the server log) and an optional end date.
        - A later level overrides an earlier one, face by face; a face with
        no password at any level is an error, never an open site.
        - `stx release passwd` writes the records without publishing again;
        changing them closes the open sessions of that face.
    """)
    st_space("v", 2)

    st_write(bs.sub, "Commands", toc_lvl="+1")
    st_space("v", 1)
    rows = _commands()
    if rows:
        with st_list() as l:
            for name, help_ in rows:
                with l.item():
                    st_write(bs.txt, (bs.cmd, f"stx release {name}"), f" — {help_}")
    st_space("v", 1)
    show_code("""\
        stx release lock                     # the live image's dependencies, from uv.lock
        stx release rebuild                  # public repository: Coolify rebuilds the live image
        stx release setup --target prod      # plan; --apply creates the two applications
        stx release server-config            # nginx -t, then reload without interruption
        stx release publish chat1d-slides    # or --group CHAT1D, or every site
        stx release status                   # what each site serves, as a visitor
        stx release rollback chat1d-slides
        stx release local up                 # both applications in Docker, for a trial""",
              language="bash", line_numbers=False)
    st_space("v", 2)

    show_details("""\
        - **Version check**: publishing is refused when the streamtex that
        exports here is not the live image's (stx-version), or comes from a
        working copy with uncommitted changes. `--allow-skew` publishes
        anyway for a trial, and `status` marks the site.
        - **What stays manual in Coolify**: mounting the host folder
        (Persistent Storage → Directory Mount) and replacing the Dockerfile
        of an existing application; `stx release setup` prints both steps.
        - **A public repository removes the paste** (streamtex 0.7.61): with
        `"repo": "owner/name"` in the target, `stx release lock` also writes
        `.stx-release/Dockerfile.live`; commit and push it, then
        `stx release rebuild`. `stx release setup --migrate live` moves an
        existing application to it (two runs, the volume mounted between
        them). The StreamTeX manuals work this way.
        - **Coming from the all-trainings prototype**: `stx release import
        --from state.json` takes its state over without republishing, and
        `stx release convert-passwords` rewrites its password file without
        changing a single password, checked site by site.
    """)
    st_space("v", 3)
