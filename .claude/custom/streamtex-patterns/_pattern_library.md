# Pattern Library — streamtex-docs

This folder catalogs the **streamtex-patterns** (reusable graphic design
primitives) installed for the `streamtex-docs` manuals project.

> **Preset**: `docs` (= `core` + `docs` scope).
>
> **Source**: these patterns come from the central
> [`streamtex-patterns`](../../../stx.toml) repo. See `.patterns-meta.json`
> for the exact source paths and SHA of each installed pattern.
>
> To update from the central repo: `stx patterns update`.
> To check drift: `stx patterns status`.
> To promote a local edit upstream: `stx patterns promote <name>`.

Each pattern is one `.md` file at the root of this folder. The table below
is **auto-generated** by `stx patterns install/update` from each pattern's
frontmatter.

<!-- BEGIN AUTO -->
| Name | Description | Tags | Extrapolable |
|---|---|---|---|
| ptn_api_reference_card | Reference card for one StreamTeX API function — signature, params, return, example | docs, api, reference | ✓ |
| ptn_callout | Highlighted box for emphasized content (info / warning / critical / success variants) | callout, container, emphasis | ✓ |
| ptn_card_grid | Grid of equal-size cards with title and body, used for taxonomies and inventories | grid, cards, taxonomy | ✓ |
| ptn_cite | Inline source citation with author, year, and optional URL — placed under a quote, stat, or claim | citation, evidence, footer | ✗ |
| ptn_comparison_table | Multi-column comparison table with header row and aligned rows | grid, table, comparison | ✓ |
| ptn_composite_block | Composite block aggregating several atomic sub-blocks via st_include | docs, manual, composition, atomic | ✓ |
| ptn_feature_walkthrough | Multi-step feature presentation — numbered steps, each with explanation, code, and demo | docs, manual, walkthrough, tutorial | ✓ |
| ptn_inline_emphasis | Inline keyword/label/accent variants for mixed-style text inside a single st_write | inline, text, emphasis | ✓ |
| ptn_manual_section | Documentation section — heading + sub + explanation + code snippet + live demo | docs, manual, demo, code | ✓ |
| ptn_slide_heading | Two-cell heading row (title + tooltip icon) at the top of a slide | atom, heading, layout | ✓ |
| ptn_takeaways | Numbered list of 3–5 key takeaways with bold lead and explanation | list, summary, conclusion | ✓ |
| ptn_term_definition_list | Vertical list of `term — definition` rows for glossaries, notations, abbreviation tables | list, glossary, reference, definitions | ✓ |
<!-- END AUTO -->

## Application rules (manual)

### Priority

1. If the user explicitly names a pattern, apply it.
2. If multiple patterns match the request, ask the user to choose.
3. If no pattern matches, generate the block freely; if the rendering looks
   reusable, propose `/stx-pattern:new` to capture it.

### Manual-oriented combinations

This project is the **StreamTeX documentation** itself: blocks are
expected to teach a feature, an API, or a workflow. Typical combinations
seen across the manuals (`stx_manual_intro`, `stx_manual_advanced`,
`stx_manual_ai`, `stx_manual_ce`, `stx_manual_deploy`,
`stx_manual_developer`):

- `ptn_manual_section` (heading + sub + explanation + code + live demo) is
  the **canonical** building block — use it for nearly every feature
  illustration.
- `ptn_feature_walkthrough` for end-to-end, **sequential** tutorials
  (Quick Start, "first block", "import a marp deck").
- `ptn_api_reference_card` for **single-symbol** reference entries
  (`st_grid`, `Style`, `st_book`, …).
- `ptn_composite_block` to aggregate several atomic sub-blocks (under a
  sibling `_atomic/` folder) into one TOC entry while keeping each file
  small and focused.
- `ptn_slide_heading` + `ptn_card_grid` / `ptn_comparison_table` for taxonomy or
  feature-comparison sections.
- `ptn_slide_heading` + `ptn_callout` (`info` / `warning` / `critical` /
  `success`) + optional `ptn_cite` for tips, gotchas, and evidence-backed
  claims.
- `ptn_takeaways` to close a manual chapter.

### Manuals conventions

- The doc engine renders code via `show_code()`, the live render via
  `show_explanation()`, and extra notes via `show_details()`. Patterns
  that include a "code + demo" slot (e.g. `ptn_manual_section`,
  `ptn_feature_walkthrough`) should map onto these helpers — do not bypass
  them with raw `st_code` / `st.code`.
- Each manual block file is `bck_*.py` and exposes a `def build():` — a
  composite block uses `st_include` to mount its `_atomic/` siblings.
- Atomic sub-blocks live in a sibling `_atomic/<topic>/` folder so the
  TOC remains shallow.

### Project palette

This project uses the project styles defined in `custom/styles.py`. When
a pattern's code skeleton uses generic colors or fonts, **adapt** them
to the manuals' palette via `s.project.*` (titles, containers, colors,
cell backgrounds). Never hardcode hex colors or font sizes — always
reach into `custom/styles.py` first; if a style is missing there,
propose adding it.

### Cite shorthand

Sources are added through `from streamtex.bib import cite`. Use the
existing manual-level bibliography — do not duplicate citations inline.

### Fallback for unknown references

If a pattern mentions another pattern that is not yet in this catalog
(for instance, a `slides`-only pattern referenced from a `docs`
pattern), generate the equivalent inline and propose `/stx-pattern:new`
to capture the missing pattern, or switch the project preset to a wider
one if cross-cutting needs grow.
