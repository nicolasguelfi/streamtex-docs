"""FAQ — the recurring questions about packs / components / DS / kits.

Source: synthesised from Wave 4 follow-up + PLAN.md decision Qs.
"""

from streamtex import *
from custom.styles import Styles as s


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    body = s.large
    row = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
    )
    question = s.bold + s.large


bs = BlockStyles


QA = [
    ("Why Python packs instead of a markdown catalogue?",
     "Components are real Python modules — `from streamtex_design."
     "components import callout` works the same way as any other "
     "import. `git diff` shows actual changes, pytest tests it, "
     "basedpyright covers it, ruff lints it. No separate scan-time "
     "parser, no drift bookkeeping. The legacy markdown spec "
     "(format A2) survives as the **docstring contract** inside "
     "each component module."),
    ("Can a project consume more than one pack?",
     "Yes. The reuse architecture is **multi-pack by default**. "
     "Declare each pack as a `[[packs]]` entry in `stx.toml`. "
     "Components from any installed pack are importable; "
     "`stx component list` enumerates them all."),
    ("What's the difference between a kit and a design system?",
     "A **design system** is the visual palette (a Python class "
     "implementing `DesignSystemProtocol`). A **kit** bundles one "
     "DS with a curated subset of components — it's a starter "
     "selection, not a constraint. Installing a kit writes "
     "`[design_system].use` and `[kit].use` into `stx.toml`; you "
     "can later change the DS without re-installing the kit "
     "(`stx ds switch`)."),
    ("Is the component `granularity` enforced?",
     "No — it's a **tag, not a constraint**. The resolver "
     "doesn't filter on it. The granularity is set at creation "
     "time (`stx component new my_widget --granularity composition`) "
     "and documents intent."),
    ("What happens to the legacy `streamtex-patterns/` folder?",
     "It's removed entirely in 0.7.x. Migration: install "
     "`streamtex-design` (the official pack), install a kit "
     "matching your legacy preset, delete the folder. See the "
     "migration block for the full mapping."),
    ("Can I capture a component into a non-primary pack?",
     "Yes — `stx component new my_widget --pack <name>` accepts "
     "any local pack. Without `--pack`, the scaffold lands in the "
     "primary local pack (the one with `primary = true` in "
     "stx.toml). Capturing into a remote git or PyPI pack is "
     "refused — promotion goes through `stx component promote`."),
    ("How is a kit different from a 'preset' from the legacy system?",
     "A kit is **richer** — it bundles a DS, a curated component "
     "list, optionally a CLI template and project blueprints. "
     "The legacy preset only selected which patterns to install. "
     "The vocabulary `preset` is now reserved for the workspace "
     "preset (`stx install --preset standard|user|developer|…`) "
     "which is unrelated."),
    ("Why do I see `extrapolable=True` in `__component_meta__`?",
     "It signals to the AI agent that the component accepts "
     "extrapolation within `PARAMS` (e.g. adapting `kind=` to a "
     "different design language). `extrapolable=False` means the "
     "component is rigid — the AI must use it as-is or scaffold a "
     "new one."),
    ("Where does `mypack` come from? Why is it the default?",
     "`stx project new` scaffolds `./mypack/` as a sub-folder "
     "with `primary = true` — the default destination for capture. "
     "It's installed editable via `uv pip install -e ./mypack` so "
     "edits are immediate. You can opt out with `--no-mypack` "
     "(typical for projects that only consume external packs)."),
    ("Do I need `streamtex-design` to do anything useful?",
     "No — `streamtex-design` is the official reference pack but "
     "the architecture itself doesn't require it. You can ship a "
     "project with only `./mypack/` and a local DS. In practice, "
     "`streamtex-design` covers the universal primitives "
     "(callouts, headings, cards, comparison tables…) so most "
     "projects pull it as a starting point."),
]


def build():
    """Render the FAQ list."""
    with st_block(s.center_txt):
        st_write(("FAQ", bs.heading))
        st_space(15)
        st_write(
            "Recurring questions from the 0.7.x rollout.",
            bs.body,
        )
        st_space(15)
        for question, answer in QA:
            with st_block(bs.row):
                st_write((question, bs.question))
                st_write(answer, bs.body)
            st_space(8)
