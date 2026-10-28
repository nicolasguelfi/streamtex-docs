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
        verify = "shared.checks:verify"  # optional: checks each HTML export (0.7.74)
        media_per_site = true            # optional: each live site serves its own media (0.7.76)
        media_keep = ["downloads/*"]     # served besides what the HTML export shows

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
        open = ["html"]                  # explicit: an empty string is refused

        [CHAT1D.sites.chat1d-slides]     # one line per session, each with its level
        html = [
          { seance = "S1027", mot = "a-pass", limite = 120 },
          { seance = "S1103", mot = "b-pass" },   # no limite: "not open yet"
          { seance = "S1110", mot = "c-pass", limite = [["2026-11-10T09:00", 50], ["2026-11-10T14:00", "all"]] },
        ]

        [admin]                          # added to EVERY site, both faces
        live = "ADMIN:admin-pass"
        html = "ADMIN:admin-pass"        # the administrator, written once""",
              language="toml", line_numbers=False)
    st_space("v", 1)
    show_details("""\
        - Each face takes a list of accepted passwords, each with a label
        (it names the access in the server log) and an optional end date.
        - A later level overrides an earlier one, face by face; a face with
        no password at any level is an error, never an open site.
        - `[admin]` (streamtex 0.7.66) is added to the passwords of every
        face of every site, never in their place: the administrator's
        password is written once, and it always sees all the slides.
        - Each session has its level on the HTML face (streamtex 0.7.67):
        `limite = N` (slides 1 to N), `"all"`, a schedule in local time, or
        no `limite` — the session sees a "not open yet" page. The login
        service reads the schedule at each page: nothing runs on the server.
        - One login opens every site that holds the same password: the
        administrator logs in once per face; a password of one site stays
        valid there only.
        - No rule is set on what a password contains; only what the login
        screen could never match is refused (empty, whitespace, two labels
        sharing a password in one list).
        - `stx release passwd` writes the records without publishing again;
        a changed password closes the sessions of its label only, and no
        site process restarts: a participant of the live face stays
        connected (streamtex 0.7.69).
        - `STX_PASSWORDS_FILE=rehearsal.toml stx release …` reads another
        passwords file, for a rehearsal with dummy passwords; the real
        `.stx-passwords.toml` stays in place.
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
        stx release publish chat1d-slides    # or --group CHAT1D, or --all for every site
        stx release status                   # what each site serves, as a visitor
        stx release limit chat1d-slides 120 --label S1027   # writes its line, then applies it
        stx release limit chat1d-slides none --label S1103  # "not open yet"
        stx release rollback chat1d-slides   # undoes the last change: a limit, or a publication
        stx release remove old-site          # takes a site off the server (shows, then asks)
        stx release media-report chat1d-slides   # what media_per_site would serve, nothing sent
        stx release local up                 # both applications in Docker, for a trial""",
              language="bash", line_numbers=False)
    st_space("v", 2)

    show_details("""\
        - **Version check**: publishing is refused when the streamtex that
        exports here is not the live image's (stx-version), or comes from a
        working copy with uncommitted changes, or (streamtex 0.7.74) from
        an editable working copy with commits in `streamtex/` after its tag.
        `--allow-skew` publishes anyway for a trial, and `status` marks the
        site.
        - **Safety points** (streamtex 0.7.74): `publish` with no site and no
        group is refused, `--all` publishes every site; `setup --domains
        --dry-run` shows the domains each application would get, and writes
        nothing; the check after the switch logs in with a password still
        valid.
        - **The project's check of an export** (streamtex 0.7.74): `[release]
        verify = "module:function"` is called as `verify(site_name,
        html_dir)` after each HTML export, before anything is copied, in the
        project's environment. `None` accepts; a message, `False` or an
        exception refuses, and the site keeps serving what it served.
        - **Taking a site off the server** (streamtex 0.7.75): `stx release
        remove SITE` stops its program, drops its line of `ports.map`, removes
        its folders on both faces and its entry in `.stx-release.json`; it
        shows the list and asks first, and refuses a site still declared in
        `stx.toml` unless `--force`. Its domains stay until `stx release
        setup --domains` (which redeploys both applications): `remove`
        prints the command.
        - **Media per site** (streamtex 0.7.76): `[release] media_per_site =
        true` makes each site's live face serve under `/app/static/` only the
        files its HTML export shows (found again by content) and those
        `media_keep = ["downloads/*"]` names (in `[release]`, or in a site's
        table). Off by default; `stx release media-report SITE` shows the
        files kept and dropped first, and the files named in the site's own
        files that would not be kept. A rollback to an earlier release
        serves its whole folder again.
        - **What stays manual in Coolify**: mounting the host folder
        (Persistent Storage → Directory Mount) and replacing the Dockerfile
        of an existing application; `stx release setup` prints both steps.
        - **A public repository removes the paste** (streamtex 0.7.61): with
        `"repo": "owner/name"` in the target, `stx release lock` also writes
        `.stx-release/Dockerfile.live`; commit and push it, then
        `stx release rebuild`. `stx release setup --migrate live` moves an
        existing application to it (two runs, the volume mounted between
        them). The StreamTeX manuals work this way.
        - **A slide limit per site** (streamtex 0.7.65): `stx release limit
        SITE N` lets participants see slides 1 to N of the HTML face, N being
        the slide counter's number as projected (the block holding it is
        kept whole). Only the HTML face is exported again, from the release
        already published, and switched: no password is rewritten and the
        live face does not restart, so participants stay logged in. The
        limit is kept: every later publication applies it. Since 0.7.67,
        `--label` gives one session its own level, written on its line of
        `.stx-passwords.toml`; open sessions see it on their next page.
        - **Coming from the all-trainings prototype**: `stx release import
        --from state.json` takes its state over without republishing, and
        `stx release convert-passwords` rewrites its password file without
        changing a single password, checked site by site.
    """)
    st_space("v", 3)
