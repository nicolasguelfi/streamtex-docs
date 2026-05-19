"""Live gallery — renders every `streamtex_design` component for real.

This block is the manual's self-demonstration: each section calls the
matching component from the `streamtex-design` pack with realistic
inputs, so a reader sees the actual rendering — not a screenshot, not a
code block. Grouped by `__component_meta__["granularity"]`.
"""

from streamtex import *
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem
from streamtex_design.components import (
    # primitives
    callout, cite, inline_emphasis, slide_heading,
    # compositions
    api_reference_card, card_grid, categorized_grid, comparison_table,
    composite_block, manual_section, takeaways, term_definition_list,
    # blocks
    evidence_insight, exercise_flow, feature_walkthrough,
    narrative_transition, stat_hero, title_slide,
)


DS = DesignSystem()


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    section = s.bold + s.large
    label = s.bold + s.medium
    body = s.large
    demo_frame = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.container.margins.medium_margin
    )


bs = BlockStyles


def _demo(label: str, render):
    """Render a labeled demo frame around a component call."""
    st_write((label, bs.label))
    with st_block(bs.demo_frame):
        render()
    st_space(8)


def build():
    """The 18-component live gallery, grouped by granularity."""
    with st_block(s.center_txt):
        st_write(("Live gallery — `streamtex_design` v0.1.0", bs.heading))
        st_space(15)
        st_write(
            "Every section below is a real call to the component, with the "
            "`default` design system passed as the `design_system` kwarg. "
            "What you see is what the component renders — no screenshots.",
            bs.body,
        )

    # === Primitives (4) ===
    st_space(20)
    st_write(("Primitives (4)", bs.section))
    st_space(10)

    _demo(
        "callout(variant='info')",
        lambda: callout(
            design_system=DS,
            variant="info",
            title="Knowledge capitalisation",
            body="Components are Python modules — diffable, testable, importable.",
        ),
    )
    _demo(
        "callout(variant='warn')",
        lambda: callout(
            design_system=DS,
            variant="warn",
            title="Don't bypass INVARIANTS",
            body="Adjust only within `PARAMS`. Refuse `INTERDITS`.",
        ),
    )
    _demo(
        "cite(source=...)",
        lambda: cite(
            design_system=DS,
            source="PLAN.md §5.6bis — pack lifecycle states",
        ),
    )
    _demo(
        "inline_emphasis(variant='strong')",
        lambda: inline_emphasis(
            design_system=DS,
            text="reuse architecture",
            variant="strong",
        ),
    )
    _demo(
        "slide_heading(title, subtitle)",
        lambda: slide_heading(
            design_system=DS,
            title="Three layers",
            subtitle="lib · packs · consumer projects",
        ),
    )

    # === Compositions (8) ===
    st_space(20)
    st_write(("Compositions (8)", bs.section))
    st_space(10)

    _demo(
        "card_grid(items=...)",
        lambda: card_grid(
            design_system=DS,
            items=[
                ("Pack", "Python package shipping components, DS, kits."),
                ("Component", "Python module + structured docstring + meta."),
                ("Design system", "Class implementing DesignSystemProtocol."),
                ("Kit", "TOML manifest: 1 DS + curated components."),
            ],
        ),
    )
    _demo(
        "categorized_grid(categories={...})",
        lambda: categorized_grid(
            design_system=DS,
            categories={
                "Lifecycle states (PR codes)": [
                    ("PR001", "Promotion to pypi refused."),
                    ("PR002", "Pack declared but not installed."),
                    ("PR003", "Manifest cassé (unreadable)."),
                    ("PR004", "Entry-point collision."),
                ],
                "Validation families": [
                    ("PV001-PV010", "Pack manifest."),
                    ("CV001-CV011", "Component docstring + meta."),
                    ("DV001-DV006", "Design system Protocol."),
                ],
            },
        ),
    )
    _demo(
        "comparison_table(columns, rows)",
        lambda: comparison_table(
            design_system=DS,
            columns=["", "Before (patterns)", "After (reuse arch)"],
            rows=[
                ("Format", "Markdown .md", "Python .py module"),
                ("Distribution", "Sibling repo", "Pack via entry-point"),
                ("Multi-source", "Single repo", "N packs in stx.toml"),
                ("Capture target", ".claude/custom/", "./mypack/"),
            ],
        ),
    )
    _demo(
        "takeaways(items=...)",
        lambda: takeaways(
            design_system=DS,
            lead="Wave 4 acceptance summary",
            items=[
                "streamtex 0.7.0 published to PyPI.",
                "streamtex-design v0.1.0 ships 18 components / 3 DS / 4 kits.",
                "streamtex-claude v0.2.0 ships the reuse-architecture skill.",
                "docs-patterns.streamtex.org serves the new manual.",
            ],
            numbered=True,
        ),
    )
    _demo(
        "term_definition_list(items=...)",
        lambda: term_definition_list(
            design_system=DS,
            items=[
                ("Primary local pack",
                 "The `[[packs]] type=\"local\" primary=true` entry — default capture destination."),
                ("Granularity tag",
                 "`primitive` / `composition` / `block`. A tag, not a constraint."),
                ("Resolution prefer",
                 "Sort order over discovered packs — never a filter."),
            ],
        ),
    )
    _demo(
        "api_reference_card(signature, description, returns)",
        lambda: api_reference_card(
            design_system=DS,
            signature="discover_packs(stx_toml_path: Path | None = None) -> list[DiscoveredPack]",
            description=(
                "Enumerate every pack visible from entry-points and the "
                "project's stx.toml. Each result carries a `state` "
                "reflecting the five PLAN §5.6bis lifecycle states."
            ),
            returns="list[DiscoveredPack]",
        ),
    )
    _demo(
        "manual_section(number, title, intro, body=callable)",
        lambda: manual_section(
            design_system=DS,
            number=4,
            title="Capture and promote",
            intro=(
                "PROTOTYPE captures a new component into the primary local "
                "pack; INTEGRATE promotes it to a shared pack via the "
                "Q12 4-branch routing helper."
            ),
            body=lambda: takeaways(
                design_system=DS,
                items=[
                    "Local primary: copy only.",
                    "Local secondary w/ .git: copy + QCM commit.",
                    "Git remote: branch + push + gh pr create.",
                    "PyPI: refused (PR001).",
                ],
                numbered=False,
            ),
        ),
    )
    _demo(
        "composite_block(title, explanation, demo=callable, code=...)",
        lambda: composite_block(
            design_system=DS,
            title="composite_block — meta example",
            explanation=(
                "Combines a section title, an explanation card, an "
                "executable demo cell, and a code cell. Useful for "
                "showing 'what + why + how' in one block."
            ),
            demo=lambda: callout(
                design_system=DS,
                variant="success",
                title="Demo cell",
                body="The `demo=` kwarg accepts any callable; here it renders a callout.",
            ),
            code='callout(design_system=DS, variant="success", title="...", body="...")',
        ),
    )

    # === Blocks (6) ===
    st_space(20)
    st_write(("Blocks (6)", bs.section))
    st_space(10)

    _demo(
        "title_slide(title, subtitle, metadata)",
        lambda: title_slide(
            design_system=DS,
            title="StreamTeX 0.7.0",
            subtitle="Reuse architecture milestone",
            metadata="2026-05-19 · Wave 4 of 4",
        ),
    )
    _demo(
        "stat_hero(value, body)",
        lambda: stat_hero(
            design_system=DS,
            value="−6 345",
            body="lines removed by MIG-6 (legacy streamtex.patterns module + tests).",
        ),
    )
    _demo(
        "narrative_transition(marker, framing, bridging)",
        lambda: narrative_transition(
            design_system=DS,
            marker="From legacy to reuse",
            framing="Markdown catalog → Python packs",
            bridging=(
                "Same purpose (reusable design recipes), different mechanism "
                "(import vs scan)."
            ),
        ),
    )
    _demo(
        "exercise_flow(steps=...)",
        lambda: exercise_flow(
            design_system=DS,
            steps=[
                "`stx project new my-app --kit streamtex_design:project-default`",
                "Edit `blocks/bck_hello.py` — import a component.",
                "`stx run` to render locally.",
                "`stx component new <name>` to capture a new one into mypack.",
            ],
            orientation="horizontal",
        ),
    )
    _demo(
        "feature_walkthrough(steps=[(label, prose, code), ...])",
        lambda: feature_walkthrough(
            design_system=DS,
            steps=[
                (
                    "Discover",
                    "Read installed packs via the streamtex.packs entry point.",
                    "from streamtex.core.discovery import discover_packs\\npacks = discover_packs()",
                ),
                (
                    "Validate",
                    "Run the aggregate validator across packs / components / DS / kits.",
                    "stx validate --strict",
                ),
                (
                    "Capture",
                    "Promote a tested component to the project's primary local pack.",
                    "stx component new evidence_slide",
                ),
            ],
        ),
    )
    _demo(
        "evidence_insight(value, caption, insights, source) — composed",
        lambda: evidence_insight(
            design_system=DS,
            value="2 113",
            caption="streamtex tests passing on 0.7.0",
            insights=[
                "−112 tests deleted with the patterns module (MIG-6).",
                "+10 tests added for stx project new modernisation (MIG-3).",
                "+8 tests added for _add_default_design_pack (MIG-4).",
                "+2 tests added for the multi-pack matrix (Phase 2b).",
            ],
            source="streamtex 0.7.0 CHANGELOG",
        ),
    )

    st_space(20)
    st_write(("End of gallery — 18/18 components rendered.", bs.section + s.center_txt))
