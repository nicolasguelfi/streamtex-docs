"""Block — Access control of a deployed project (stx deploy lock / unlock / passwd / auth-status).

The mode table, the commands' help and the parsed passwords file are read
from the library at render time, so they always match the installed stx.
"""

import tomllib

from streamtex import *
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Access control block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.container.layouts.vertical_center_layout
    )
    txt = s.big
    head = s.bold + s.big
    mode = s.project.colors.accent_teal + s.big
    callout_title = s.project.titles.tip_label
    warn_title = s.project.titles.warning_label
bs = BlockStyles


# The passwords file shown below, parsed live by the library's own reader.
_SAMPLE_PASSWORDS = """\
# .stx-passwords.toml — plain passwords: git-ignored
# [default]: when no section has the service's name
[default]
live = "open sesame"              # label "default"
html = "COHORT1:first-pw,COHORT2:second-pw"

# The section of the service docs-intro, in the
# table form (for a password with ':' or ',')
[docs-intro.live]
TEACHER = "t:e,a"
COHORT1 = { password = "pw-2026", valid_until = "2027-01-31" }

[docs-intro.html]
COHORT1 = "pw-2026"
"""


def _auth_api():
    """The access-control module of the installed stx, or None without streamtex[cli]."""
    try:
        from streamtex.cli import deploy_auth_cmd
    except ImportError:
        return None
    return deploy_auth_cmd


def _help(cmd, name: str) -> str:
    """The --help text of a click command, as `stx deploy <name> --help` prints it."""
    import click

    with click.Context(cmd, info_name=f"stx deploy {name}") as ctx:
        return cmd.get_help(ctx)


def _parsed_faces(api) -> str:
    """What `stx deploy lock` prints (and auth-status shows) for each section of the sample."""
    data = tomllib.loads(_SAMPLE_PASSWORDS)
    lines = []
    for section in ("default", "docs-intro"):
        lines.append(f"[{section}]")
        for face in api.FACES:
            entries = api.parse_password_spec(data[section][face], f"[{section}].{face}")
            lines.append(f"  {face}: {api.describe_face(api.encode_face(entries))}")
    return "\n".join(lines)


def _refusals(api) -> str:
    """The messages of the mistakes `lock` and `passwd` refuse (nothing is sent to Coolify)."""
    import click

    cases = [
        ("A label twice", "A:one,A:two"),
        ("Two labels share a password", "A:same,B:same"),
        ("A label with a space", "MY COHORT:pw"),
        (f"{api.MAX_PASSWORDS + 1} passwords", ",".join(f"L{i}:pw{i}" for i in range(api.MAX_PASSWORDS + 1))),
    ]
    out = []
    for title, spec in cases:
        try:
            api.parse_password_spec(spec, "[default].live")
            out.append(f"{title}: accepted")
        except click.ClickException as e:
            out.append(f"{title}:\n  {e.message}")
    return "\n".join(out)


def build():
    api = _auth_api()

    with st_block(s.center_txt):
        st_write(bs.heading, "Access Control", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation(
            "A deployed service is public: anyone with its address reads it. Since 0.7.44, "
            "**stx deploy lock / unlock / passwd / auth-status** protect a Coolify application "
            "with one of three **modes**: a login screen run by the container's own nginx, the "
            "keypad inside the Streamlit app, or Coolify's HTTP Basic Authentication. The modes "
            "form a registry: the table below is read from it."
        )
        st_space("v", 2)

        # --- Modes ---
        st_write(bs.sub, "The three modes", toc_lvl="+1")
        st_space("v", 1)

        if api is None:
            show_details("Install `streamtex[cli]` to display the registry of modes.")
        else:
            with st_grid(cols="1.3fr 1.2fr 3fr 1.2fr", cell_styles=bs.cell) as g:
                for title in ("Mode", "Level", "What it is", "Applies with"):
                    with g.cell(): st_write(bs.head, title)
                for mode in api.AUTH_MODES.values():
                    with g.cell(): st_write(bs.mode, mode.name)
                    with g.cell(): st_write(bs.txt, mode.level)
                    with g.cell(): st_write(bs.txt, mode.summary)
                    with g.cell(): st_write(bs.txt, "at once" if mode.instant else "restart")
        st_space("v", 1)

        show_details(
            "**proxy** = checked before the request reaches Streamlit (nginx or Coolify's Traefik): "
            "nothing of the app is sent before the password. **application** = checked by the "
            "Streamlit app itself. **restart**: every mode is an environment variable or a Coolify "
            "setting, so it applies when the container restarts — `lock`, `unlock` and `passwd` "
            "restart the application and its replicas themselves, unless `--no-restart`."
        )
        st_space("v", 2)

        # --- Which one ---
        st_write(bs.sub, "Which one to choose", toc_lvl="+1")
        st_space("v", 1)

        with st_block(s.project.containers.tip_callout):
            with st_list(list_type=lt.unordered, text_align="left") as l:
                with l.item():
                    st_write(s.large, (s.bold, "session — the login screen (default of lock). "),
                             "A course, a client, several groups: one password per cohort, each with a "
                             "label and an optional last valid day, on the app (/) and on the static "
                             "export (/html/) separately. One sign-in per browser covers every tab.")
                with l.item():
                    st_write(s.large, (s.bold, "stx-password — the keypad. "),
                             "A light deterrent for a demo: a sequence of letters and digits clicked or "
                             "typed on a 6x6 grid. Only the app is behind it: /html/ stays open.")
                with l.item():
                    st_write(s.large, (s.bold, "basic — Coolify's Basic Authentication. "),
                             "One user name and password for the whole domain, asked by the browser's "
                             "pop-up. Nothing to configure in the project.")
        st_space("v", 1)

        show_details(
            "When the login screen guards the app (`STX_AUTH_LIVE` or `STX_AUTH_HTML` set and the app "
            "face not `open`), the keypad is **not shown** even if `STX_PASSWORD` is set: visitors are "
            "asked once, by the server. `lock`, the app log and the container log say so."
        )
        st_space("v", 2)

        # --- Commands ---
        st_write(bs.sub, "The commands", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "TARGET is a service name, a subdomain or a Coolify UUID; without it, the applications are "
            "listed and you pick one. Run the commands where `stx deploy` finds the Coolify "
            "credentials: `.stx-deploy.env` (current directory, then its parent), then `.env`, the "
            "environment variables, then `.stx-deploy.json`. Each command prints where each "
            "credential came from."
        )
        st_space("v", 1)

        show_code("""\
            # Login screen on both faces, passwords from ./.stx-passwords.toml
            stx deploy lock docs-intro

            # Only the app (/); the static export (/html/) stays open
            stx deploy lock docs-intro --faces live

            # Another section of the file; restart later (stx deploy update docs-intro --quick)
            stx deploy lock docs-intro --section course-2026 --no-restart

            # The keypad (the sequence is prompted: it stays out of the shell history)
            stx deploy lock docs-intro --mode stx-password

            # Coolify's HTTP Basic Authentication
            stx deploy lock docs-intro --mode basic --user teacher

            # After editing .stx-passwords.toml: apply it again
            stx deploy passwd docs-intro

            # Every mode and its state (labels and end dates, never a secret)
            stx deploy auth-status docs-intro

            # Turn every mode off, or only some
            stx deploy unlock docs-intro
            stx deploy unlock docs-intro --mode stx-password
        """, language="bash", line_numbers=False)
        st_space("v", 1)

        if api is not None:
            show_explanation("The options, as the installed stx prints them:")
            st_space("v", 1)
            helps = [
                _help(api.lock_cmd, "lock"),
                _help(api.passwd_cmd, "passwd"),
                _help(api.unlock_cmd, "unlock"),
                _help(api.auth_status_cmd, "auth-status"),
            ]
            show_code("\n\n".join(helps), language="text", line_numbers=False)
            st_space("v", 1)

        show_details(
            "`auth-status` reads the application's settings and shows, per mode, `off` or what is on: "
            "for the login screen, each face's labels and end dates (`(expired)` once past); for the "
            "keypad, `on` or `set, not shown`; for basic, the user name. It never prints a password "
            "or a hash. `unlock` only touches the modes that are on. Basic Authentication through "
            "Coolify's API was tried on Coolify 4.0.0-beta.468; if your Coolify ignores the change, "
            "the command says so — set it in the dashboard (Configuration > General)."
        )
        st_space("v", 2)

        # --- Passwords file ---
        st_write(bs.sub, "The passwords file: .stx-passwords.toml", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "The login screen reads its passwords from `.stx-passwords.toml` at the root of the "
            "project (`--path`, `--file`). The section is the one named after the service, else "
            "`[default]` (`--section` picks another). Each face — `live` for the app, `html` for "
            "the static export — holds a password, a list `\"LABEL:pw,LABEL:pw\"`, or a table "
            "whose entries may carry a `valid_until` date."
        )
        st_space("v", 1)

        show_code(_SAMPLE_PASSWORDS, language="toml", line_numbers=False)
        st_space("v", 1)

        if api is not None:
            show_explanation(
                "What `lock` prints for each face of this file — read by the library's own reader:"
            )
            st_space("v", 1)
            show_code(_parsed_faces(api), language="text", line_numbers=False)
            st_space("v", 1)

            show_explanation("What it refuses before anything reaches Coolify:")
            st_space("v", 1)
            show_code(_refusals(api), language="text", line_numbers=False)
            st_space("v", 1)

        with st_block(s.project.containers.note_callout):
            st_write(bs.warn_title, "Never in git, never in the image")
            st_space("v", 1)
            with st_list(list_type=lt.unordered, text_align="left") as l:
                with l.item():
                    st_write(s.large, "Passwords are hashed with scrypt ", (s.bold, "on your machine"),
                             "; only the hashes reach Coolify (as STX_AUTH_LIVE / STX_AUTH_HTML, the "
                             "base64 of one LABEL:scrypt$...[:YYYY-MM-DD] line per password).")
                with l.item():
                    st_write(s.large, "Keep ", (s.bold, ".stx-passwords.toml"), " out of git: the "
                             ".gitignore that stx project new writes lists it (add it by hand in an older "
                             "project); lock and passwd warn when git does not ignore it, and stx deploy "
                             "preflight fails.")
                with l.item():
                    st_write(s.large, "The generated .dockerignore excludes it (with .env and "
                             ".stx-deploy.env), so a local docker build never copies it into an image.")
        st_space("v", 1)

        show_details(
            "**valid_until** is the last valid day (UTC), included. **Labels**: letters, digits, `-` and "
            "`_`. At most " + (str(api.MAX_PASSWORDS) if api else "32") + " passwords per face: each one "
            "is tried at login. **Changing** a password ends the sessions opened with the old one; "
            "**removing** an entry ends only its own sessions — the other cohorts stay signed in."
        )
        st_space("v", 2)

        # --- Faces and what stays open ---
        st_write(bs.sub, "Faces, sessions and what stays open", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=3, cell_styles=bs.cell) as g:
            for title in ("Address", "Login screen (session)", "Keypad (stx-password)"):
                with g.cell(): st_write(bs.head, title)

            with g.cell(): st_write(bs.mode, "/  (the app)")
            with g.cell(): st_write(bs.txt, "Face live: its own form and cookie")
            with g.cell(): st_write(bs.txt, "Behind the keypad")

            with g.cell(): st_write(bs.mode, "/html/  (static export)")
            with g.cell(): st_write(bs.txt, "Face html: its own form (/html/_login) and cookie")
            with g.cell(): st_write(s.project.colors.warning_red + bs.txt, "Open")

            with g.cell(): st_write(bs.mode, "/app/static/  (media)")
            with g.cell(): st_write(bs.txt, "With the app, unless STX_AUTH_PUBLIC_MEDIA=1")
            with g.cell(): st_write(s.project.colors.warning_red + bs.txt, "Open")

            with g.cell(): st_write(bs.mode, "/_stcore/health")
            with g.cell(): st_write(s.project.colors.success_green + bs.txt, "Always open (probes)")
            with g.cell(): st_write(s.project.colors.success_green + bs.txt, "Open")
        st_space("v", 1)

        show_details(
            "A face's cookie is refused on the other face. With `--faces live` the html face is set to "
            "`open`; a face left without a value once the other is set is **closed**. The session cookie "
            "is signed, HttpOnly and Secure, and lasts 12 hours (`STX_AUTH_SESSION_HOURS`). The form is "
            "shown in the visitor's language (English or French). **Rate limit**: nginx accepts a burst "
            "of 50 form submissions per address, then 50 per minute, and answers 429 beyond."
        )
        st_space("v", 2)

        # --- Requirements ---
        st_write(bs.sub, "Requirements and failures", toc_lvl="+1")
        st_space("v", 1)

        with st_block(s.project.containers.bad_callout):
            with st_list(list_type=lt.unordered, text_align="left") as l:
                with l.item():
                    st_write(s.large, "The login screen needs the deployment files generated by streamtex "
                             "0.7.44 or later (nginx.conf and entrypoint.sh). A project keeps its own "
                             "copies: run ", (s.bold, "stx deploy diff"), " and adopt the new templates first.")
                with l.item():
                    st_write(s.large, "It needs nginx: with STX_SERVE_MODE=streamlit-only the container "
                             "refuses to start, since nothing would protect the app.")
                with l.item():
                    st_write(s.large, "If the login service cannot be found in the installed streamtex, the "
                             "site is closed (503) and the reason goes to /app/STX_ERRORS.txt — never "
                             "silently open.")
        st_space("v", 2)

        # --- Keypad ---
        st_write(bs.sub, "The keypad, and a local preview", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "With `STX_PASSWORD` set, `st_book` first shows a 6x6 grid of A-Z and 0-9 and six circles. "
            "The sequence is the password upper-cased, other characters dropped (`hello` gives "
            "H-E-L-L-O). Visitors click or type it; it is recognised **anywhere** in the stream of keys, "
            "so wrong keys before it do not matter. The circles only show colours, never the keys. "
            "Locally the gate is off; `STX_GATE=1` previews it with the sequence S-T-X."
        )
        st_space("v", 1)

        show_code("""\
            STX_GATE=1 stx run                 # preview: type S T X
            STX_PASSWORD=demo stx run          # the real sequence: D E M O
        """, language="bash", line_numbers=False)
        st_space("v", 1)

        show_details(
            "The app also reads the project's `.env`: a `STX_PASSWORD` line there turns the keypad on "
            "locally as well. The static export and the cache warm-up never run the gate, which is why "
            "/html/ is not protected by it."
        )
