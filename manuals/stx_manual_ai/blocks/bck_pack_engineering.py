"""Pack Engineering via Claude — the /stx-pe namespace.

Source: streamtex-claude/profiles/project/pack-engineering/.
"""

from streamtex import *
from custom.styles import Styles as s


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    code = s.container.paddings.small_padding + s.container.borders.solid_border
    cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
    )


bs = BlockStyles


def build():
    """Introduce Pack Engineering as a Claude-driven AI workflow."""
    with st_block(s.center_txt):
        st_write(("Pack Engineering via Claude", bs.heading))
        st_space(15)
        st_write(
            "Once you've produced several StreamTeX documents and "
            "noticed the same visual idioms repeating across them, "
            "**Pack Engineering (PE)** is the Claude-driven workflow "
            "that turns those scattered patterns into a versioned, "
            "shared design pack — automatically.",
            bs.body,
        )
        st_space(15)

    # ---- What it does ----
    st_write(("What PE does for you", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "Hand Claude a list of your projects ; it analyses them with "
        "an AST-based miner, designs contracts for each recurring "
        "pattern, scaffolds the pack via `stx component new`, "
        "validates with `stx component validate`, rewrites your "
        "source projects' blocks to use the new pack, and runs a "
        "headless smoke render to verify nothing visually broke.",
        bs.body,
    )
    st_space(15)

    # ---- The single agent you talk to ----
    st_write(("One agent, six specialists", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "You only ever interact with **`pack-orchestrator`**. It "
        "auto-classifies your prompt into one of six sub-modes "
        "(bootstrap / specialize / refine / audit / adopt / publish), "
        "surfaces validation gates at the critical moments, and "
        "delegates each phase to an invisible specialist agent. You "
        "never need to learn the names of the specialists.",
        bs.body,
    )
    st_space(15)

    # ---- The /stx-pe namespace ----
    st_write(("The /stx-pe namespace", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "Seven slash commands are installed by `stx claude install` "
        "(project profile) :",
        bs.body,
    )
    st_space(10)

    with st_grid(cols="1fr 4fr", gap="8px", cell_styles=bs.cell) as g:
        for cmd, desc in [
            ("/stx-pe:go",
             "Auto-detects the right sub-mode from your prompt + "
             "workspace state."),
            ("/stx-pe:bootstrap",
             "Force bootstrap : N projects → brand-new pack."),
            ("/stx-pe:specialize",
             "Force fork : upstream pack + N projects → "
             "domain-specific fork."),
            ("/stx-pe:refine",
             "Force refine : capture emerged patterns into the "
             "active pack."),
            ("/stx-pe:audit",
             "Read-only health check of an existing pack."),
            ("/stx-pe:adopt",
             "Wire an existing pack into N projects without "
             "extraction."),
            ("/stx-pe:publish",
             "Release the pack : semver bump, tag, optional PyPI."),
        ]:
            with g.cell():
                st_write(cmd, bs.body + s.bold)
            with g.cell():
                st_write(desc, bs.body)
    st_space(15)

    # ---- Indirect routing via /stx-ce:task ----
    st_write(("Indirect routing", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "You don't need to memorize the `/stx-pe:` namespace. The "
        "general-purpose `/stx-ce:task` command auto-detects pack "
        "engineering intent from your free-text description :",
        bs.body,
    )
    st_space(10)

    with st_block(bs.code):
        st_code(
            """
# These all route to /stx-pe automatically :
/stx-ce:task "extract a shared pack from projects/manual-*"
/stx-ce:task "audit my pack and find unused components"
/stx-ce:task "specialize streamtex-design for our domain"
/stx-ce:task "refine my pack with the new patterns from the last sprint"
""",
            language="bash",
        )
    st_space(15)

    # ---- The 4 gates ----
    st_write(("Four validation gates", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "PE is not fire-and-forget — it pauses for your validation "
        "at four critical moments :\n\n"
        "- **G1 (post-DISCOVERY)** : you review the candidate "
        "components before committing to design.\n"
        "- **G2 (post-DESIGN)** : you review contracts and conflicts "
        "before implementation. Skippable in minimal dialog mode.\n"
        "- **G3 (pre-RETROFIT)** : you review the rewrite plan as a "
        "dry-run before any of your blocks are modified.\n"
        "- **G4 (post-RETROFIT smoke fail)** : conditional — only "
        "fires if a rewritten block fails the headless render.",
        bs.body,
    )
    st_space(15)

    # ---- Where to read more ----
    st_write(("Where to read more", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "Full mechanism in the **Reuse Architecture** manual : the "
        "Pack Engineering section walks through the bootstrap, "
        "specialize, and refine flows end-to-end, with all the gates "
        "and outputs documented.",
        bs.body,
    )
