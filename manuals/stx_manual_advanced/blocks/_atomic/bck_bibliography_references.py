import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details
from streamtex.bib import cite, st_bibliography, export_bibtex, get_bib_registry
from streamtex.bib import parse_bibtex_string
from streamtex import BibRefs  # noqa: F401 — API coverage
from custom.bib_refs import st_refs

class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    feature = s.project.titles.feature_title
    content = s.large
    cite_demo = ns(
        "background-color: rgba(74,144,217,0.06); border-radius: 8px; padding: 16px 20px;",
        "cite_demo"
    )

bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Bibliography & References",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            StreamTeX provides a built-in bibliography system.

            Load references from BibTeX, JSON, RIS, or CSL-JSON files.

            Cite inline with hover preview. Render formatted bibliographies in APA, IEEE, MLA, Chicago, or Harvard style.
        """)
        st_space("v", 3)

        # --- Section 1: Loading References ---
        st_write(bs.sub, "1. Loading References", toc_lvl="+1")
        st_space("v", 2)

        show_code(file="examples/bib/loading_references.py")
        st_space("v", 2)

        show_details("""\
            Supported import formats: .bib (BibTeX), .json (JSON array), .ris (RIS/Zotero), .csl-json (CSL-JSON/Mendeley).

            Add custom formats with register_bib_parser("ext", parser_function).

            References are loaded once per st_book() render and cached in the BibRegistry singleton.
        """)
        st_space("v", 3)

        # --- Section 2: Inline Citations ---
        st_write(bs.sub, "2. Inline Citations with cite() and st_refs", toc_lvl="+1")
        st_space("v", 2)

        show_code(file="examples/bib/inline_citations.py")
        st_space("v", 2)

        # Live demo — using st_refs
        with st_block(bs.cite_demo):
            st_write(s.project.titles.tip_label, "Live result (using st_refs):")
            st_space("v", 1)
            st_write(s.big,
                "The Transformer architecture ",
                st_refs.vaswani2017attention,
                " revolutionized NLP. "
                "Pre-trained models like BERT ",
                st_refs.devlin2019bert,
                " extended this to transfer learning."
            )
            st_space("v", 2)
            st_write(s.big,
                "Scaling laws ",
                st_refs.brown2020language,
                " showed that larger models achieve remarkable few-shot performance, "
                "building on foundational work in deep learning ",
                cite("lecun2015deep", "goodfellow2016deep"),
                "."
            )

        st_space("v", 2)

        show_details("""\
            st_refs.key is equivalent to cite("key") but enables IDE autocompletion.

            For multi-key citations, use cite("key1", "key2") → (Author1; Author2, Year).

            Hover over citations above to see the preview card. Click Copy or Open.
        """)
        st_space("v", 3)

        # --- Section 3: Citation Styles ---
        st_write(bs.sub, "3. Citation Styles", toc_lvl="+1")
        st_space("v", 2)

        show_code("""\
from streamtex.bib import CitationStyle

# (Vaswani et al., 2017) — default
BibConfig(citation_style=CitationStyle.AUTHOR_YEAR)

# [1]
BibConfig(citation_style=CitationStyle.NUMERIC)

# ^1 (superscript)
BibConfig(citation_style=CitationStyle.SUPERSCRIPT)""")
        st_space("v", 3)

        # --- Section 4: Import Formats ---
        st_write(bs.sub, "4. Import Formats", toc_lvl="+1")
        st_space("v", 2)

        cell_style = (s.container.borders.solid_border
                      + s.container.paddings.small_padding)
        header_style = sg.create("A1:D1", cell_style + s.bold + s.large + s.project.colors.primary_blue)
        data_style = sg.create("A2:D5", cell_style + s.large)

        with st_grid(cols=4, cell_styles=header_style + data_style) as g:
            for col in ["Format", "Extension", "Source", "Function"]:
                with g.cell():
                    st_write(col)
            for row in [
                ("BibTeX", ".bib", "LaTeX / Google Scholar", "load_bibtex()"),
                ("JSON", ".json", "Custom / API", "load_bib_json()"),
                ("RIS", ".ris", "Zotero / Mendeley / EndNote", "load_bib_ris()"),
                ("CSL-JSON", ".csl-json", "Zotero native export", "load_bib_csl_json()"),
            ]:
                for cell in row:
                    with g.cell():
                        st_write(cell)

        st_space("v", 2)

        show_code(file="examples/bib/import_formats.py")
        st_space("v", 3)

        # --- Section 5: Extensible Fields ---
        st_write(bs.sub, "5. Extensible Fields", toc_lvl="+1")
        st_space("v", 2)

        show_explanation("""\
            BibEntry has 20+ standard fields (title, authors, year, journal, doi, etc.).

            Any unknown fields from your source files are preserved in the 'extra' dict.

            Access them with entry.get_field("custom_field").
        """)
        st_space("v", 1)

        show_code(file="examples/bib/extensible_fields.py")
        st_space("v", 3)

        # --- Section 6: Registry Info ---
        st_write(bs.sub, "6. Registry Status", toc_lvl="+1")
        st_space("v", 2)

        reg = get_bib_registry()
        all_entries = reg.get_all_entries()
        cited_entries = reg.get_cited_entries()

        gap_style = ns("gap:16px;", "reg_gap")
        with st_grid(cols=3, grid_style=gap_style) as g:
            with g.cell():
                stx.st_metric("Registered", str(len(all_entries)))
            with g.cell():
                stx.st_metric("Cited", str(len(cited_entries)))
            with g.cell():
                stx.st_metric("Available keys", str(len(reg.list_keys())))

        st_space("v", 2)

        if all_entries:
            st_write(bs.feature, "Registered entries:")
            st_space("v", 1)
            for entry in all_entries:
                st_write(s.big, f"  {entry.key}",
                         (s.project.colors.neutral_gray, f" ({entry.entry_type}) "),
                         (s.italic, entry.title[:60] + ("..." if len(entry.title) > 60 else "")))

        st_space("v", 3)

        # --- Section 7: Output Formats (BibFormat) ---
        st_write(bs.sub, "7. Output Formats (BibFormat)", toc_lvl="+1")
        st_space("v", 2)

        show_explanation("""\
            StreamTeX supports 5 bibliography output formats via BibFormat enum.
            Each format styles author names, titles, journals, and dates differently.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex.bib import BibFormat

# APA (default) — Author, A. B. (Year). Title. Journal, Vol(Num), Pages.
BibConfig(format=BibFormat.APA)

# MLA — Author. "Title." Journal, vol. Vol, no. Num, Year, pp. Pages.
BibConfig(format=BibFormat.MLA)

# IEEE — [1] A. Author, "Title," Journal, vol. Vol, no. Num, pp. Pages, Year.
BibConfig(format=BibFormat.IEEE)

# Chicago — Author. "Title." Journal Vol, no. Num (Year): Pages.
BibConfig(format=BibFormat.CHICAGO)

# Harvard — Author Year, 'Title', Journal, vol. Vol, no. Num, pp. Pages.
BibConfig(format=BibFormat.HARVARD)""")
        st_space("v", 2)

        show_details("""\
            The format is set once in BibConfig and applies to all st_bibliography() calls.

            You can also override per-call: st_bibliography(format=BibFormat.IEEE).

            Each format handles edge cases (missing fields, et al. for 3+ authors).
        """)
        st_space("v", 3)

        # --- Section 8: Rendered Bibliography ---
        st_write(bs.sub, "8. Rendered Bibliography (APA)", toc_lvl="+1")
        st_space("v", 2)

        show_code("""\
from streamtex.bib import st_bibliography

st_bibliography(
    title="References",
    toc_lvl="1",
    only_cited=True,  # Only show entries cited via cite()
    format=BibFormat.APA,
)""")
        st_space("v", 2)

        st_bibliography(
            title="",
            style=bs.cite_demo,
            only_cited=True,
        )

        st_space("v", 3)

        # --- Section 9: BibTeX Export ---
        st_write(bs.sub, "9. BibTeX Export", toc_lvl="+1")
        st_space("v", 2)

        show_code("""\
from streamtex.bib import export_bibtex

bibtex_str = export_bibtex(only_cited=True)
st.download_button("Download .bib", bibtex_str, "references.bib")""")
        st_space("v", 1)

        bibtex_str = export_bibtex(only_cited=True)
        if bibtex_str:
            st.download_button(
                "Download cited references (.bib)",
                bibtex_str,
                "cited_references.bib",
                mime="application/x-bibtex",
                key="bck_bib_download",
            )

        st_space("v", 3)

        # --- Section 10: st_refs & IDE Autocompletion ---
        st_write(bs.sub, "10. st_refs & IDE Autocompletion", toc_lvl="+1")
        st_space("v", 2)

        show_explanation("""\
            st_refs maps attribute access to cite() calls with full IDE autocompletion.

            Generate a typed Python module from your .bib file, then import st_refs
            from there. Your IDE shows all keys with docstrings (title, authors, year).
        """)
        st_space("v", 1)

        show_code(file="examples/bib/st_refs_autocompletion.py")
        st_space("v", 2)

        show_details("""\
            The generated .py contains @property definitions with docstrings for each key.

            Unknown keys (added after generation) still work via __getattr__ fallback — just without completion.

            Regenerate with the same command when you add or modify bibliography entries.
        """)
        st_space("v", 3)

        # --- Section 11: Custom Parsers ---
        st_write(bs.sub, "11. Custom Parsers (register_bib_parser)", toc_lvl="+1")
        st_space("v", 2)

        show_explanation("""\
            You can extend the bibliography system with custom parsers for
            any file format. Register a parser function that takes a file path
            and returns a list of BibEntry objects.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex.bib import register_bib_parser, BibEntry

def parse_custom_format(filepath: str) -> list[BibEntry]:
    \"\"\"Parse a custom bibliography format.\"\"\"
    entries = []
    with open(filepath) as f:
        for line in f:
            # Parse your custom format here
            key, title, author, year = line.strip().split("|")
            entries.append(BibEntry(
                key=key, title=title, authors=[author], year=year
            ))
    return entries

# Register for .custom extension
register_bib_parser("custom", parse_custom_format)

# Now load_bib() auto-detects .custom files
# load_bib("references.custom")""")
        st_space("v", 2)

        show_details("""\
            The parser function receives the file path and must return List[BibEntry].

            The format name is used for file extension detection in load_bib().

            Built-in parsers: bib (BibTeX), json (JSON), ris (RIS), csl-json (CSL-JSON).
        """)
        st_space("v", 3)

        # --- Section 12: set_bib_config() ---
        st_write(bs.sub, "12. set_bib_config() — Global Configuration", toc_lvl="+1")
        st_space("v", 2)

        show_explanation("""\
            set_bib_config() sets the global bibliography configuration using
            the dependency injection (DI) pattern. Call it once in book.py
            before any citation or bibliography rendering.

            BibConfig controls the output format, citation style, hover
            behavior, sorting, and locale.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex.bib import BibConfig, BibFormat, CitationStyle, set_bib_config

# Configure bibliography globally
set_bib_config(BibConfig(
    format=BibFormat.IEEE,
    citation_style=CitationStyle.NUMERIC,
    hover_enabled=True,
    hover_show_abstract=True,
    sort_by="year",       # "author" | "year" | "key" | "citation_order"
    locale="en",          # "en" or "fr"
))""")
        st_space("v", 2)

        show_details("""\
            st_book() accepts a bib_config= parameter that calls set_bib_config()
            internally. You only need to call set_bib_config() directly when not
            using st_book(), or when you want to change the config mid-render.

            Use get_bib_config() to read the current configuration.
        """)
        st_space("v", 3)

        # --- Section 13: format_entry() ---
        st_write(bs.sub, "13. format_entry() — Custom Entry Formatting", toc_lvl="+1")
        st_space("v", 2)

        show_explanation("""\
            format_entry() formats a single BibEntry in a given BibFormat style.
            It returns an HTML string suitable for rendering.

            Use it when you need to display individual references outside of
            st_bibliography(), for example in tooltips or custom layouts.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex.bib import format_entry, BibFormat, get_bib_registry

reg = get_bib_registry()
entry = reg.get("vaswani2017attention")

# Format as APA
apa_html = format_entry(entry, BibFormat.APA)

# Format as IEEE with a citation number
ieee_html = format_entry(entry, BibFormat.IEEE, number=1)

# Use in st_write via raw HTML
st_write(s.medium, apa_html)""")
        st_space("v", 2)

        show_details("""\
            format_entry(entry, fmt, number) accepts:
            - entry: a BibEntry object
            - fmt: a BibFormat enum value (APA, MLA, IEEE, CHICAGO, HARVARD)
            - number: an integer used only by IEEE format for the [N] prefix

            The function returns an HTML string with italic tags for journals
            and hyperlinks for DOIs/URLs.
        """)
        st_space("v", 3)

        # --- Section 14: BibTeX that reads right (0.7.38) ---
        st_write(bs.sub, "14. BibTeX Values Read Right (TeX decoding)", toc_lvl="+1")
        st_space("v", 2)

        show_explanation("""\
            BibTeX values are TeX-decoded when they are read: accents
            (`\\'e`, `\\=o`, `{\\"O}`, `\\v{Z}`), symbols (`\\oe`, `\\ss`),
            escaped characters (`\\&`, `\\%`, `\\#`) and grouping braces
            (`{GPT}` → GPT). Author fields are read at any brace depth, so a
            name such as `{\\v{Z}}{\\'i}dek` no longer turns the whole field
            into "Unknown".

            An institutional author written with double braces,
            `{{United Nations}}`, is ONE name: it is shown whole ("United
            Nations", never "Nations") and listed in `BibEntry.institutional`.
            A long name can be cited short with the biblatex field
            `shortauthor = {UN}`: the citation reads "(UN, 2015)", the
            bibliography keeps "United Nations" (since 0.7.42).
        """)
        st_space("v", 1)

        demo_bib = r"""@article{zidek2021,
  author  = {{\v{Z}}{\'i}dek, Augustin and M{\"u}ller, J.},
  title   = {Protein \& {GPT} structure},
  journal = {Nature}, year = {2021}}
@techreport{un2015,
  author = {{United Nations}},
  title  = {Transforming our World: the 2030 Agenda},
  year   = {2015}}"""
        show_code("""\
from streamtex.bib import parse_bibtex_string

entries = parse_bibtex_string(r\"\"\"@article{zidek2021,
  author  = {{\\v{Z}}{\\'i}dek, Augustin and M{\\"u}ller, J.},
  title   = {Protein \\& {GPT} structure},
  journal = {Nature}, year = {2021}}
@techreport{un2015,
  author = {{United Nations}},
  title  = {Transforming our World: the 2030 Agenda},
  year   = {2015}}\"\"\")

for e in entries:
    st_write(s.medium, e.key, " — ", "; ".join(e.authors), " — ", e.title)""")
        st_space("v", 1)

        with st_block(bs.cite_demo):
            for e in parse_bibtex_string(demo_bib):
                st_write(s.medium, (s.bold, e.key), " — ", "; ".join(e.authors), " — ", e.title)
        st_space("v", 2)

        show_details("""\
            parse_bibtex_string() returns decoded values. BibEntry.institutional
            lists the authors given as {{...}}: ["United Nations"] above.
        """)
        st_space("v", 3)

        # --- Section 15: Ancient and original dates ---
        st_write(bs.sub, "15. Ancient and Original Dates (origdate)", toc_lvl="+1")
        st_space("v", 2)

        show_explanation("""\
            When an entry carries origdate (biblatex), or a negative /
            pre-1500 year, the citation code shows the original date:
            "c. 380 BCE" in English, "~380 av. J.-C." with
            BibConfig(locale="fr"). The edition year stays in the hover
            card and in the reference list.
        """)
        st_space("v", 1)

        show_code("""\
@book{plato_republic,
  author    = {Plato},
  title     = {The {R}epublic},
  publisher = {Hackett},
  year      = {2004},       % the edition you read
  origdate  = {-380}        % the original date: cited as "c. 380 BCE"
}""", language="latex", line_numbers=False)
        st_space("v", 3)

        # --- Section 16: strict mode and projection preset ---
        st_write(bs.sub, "16. BibConfig(strict=True) and BibConfig.projection()", toc_lvl="+1")
        st_space("v", 2)

        show_explanation("""\
            strict=True turns an unknown key in cite() into an error
            instead of printing [key?] — a typo is caught when the block is
            built (stx validate --build), not in front of the audience.

            BibConfig.projection(**overrides) is the preset for projected
            decks: hover cards 780 px wide with text x2. It is exactly
            BibConfig(card_width="780px", card_font_scale=2.0); any field
            can be overridden by keyword.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex.bib import BibConfig, BibFormat, CitationStyle

# Reading on a screen: fail on unknown keys
bib_config = BibConfig(
    format=BibFormat.APA,
    citation_style=CitationStyle.AUTHOR_YEAR,
    strict=True,
)

# Projecting in a room: large hover cards, strict too
bib_config = BibConfig.projection(strict=True)

# Written by hand, the preset is exactly
bib_config = BibConfig(card_width="780px", card_font_scale=2.0)

st_book([...], bib_sources=bib_sources, bib_config=bib_config)""")
        st_space("v", 2)

        show_details("""\
            Long URLs in st_bibliography() now wrap (overflow-wrap: anywhere)
            instead of widening the whole exported document. Nothing to
            change in a project.
        """)
        st_space("v", 3)

        # --- Migrating .bib files ---
        st_write(bs.sub, "Migrating your .bib files (0.7.38)", toc_lvl="+1")
        st_space("v", 2)

        show_explanation("""\
            Upgrading to 0.7.38 or later changes how some entries READ, never
            what you have to write. On the maintainer's own .bib files, 205 of
            421 entries render differently — every one of them was showing TeX
            commands or braces before. What to check after the upgrade:
        """)
        st_space("v", 1)

        with st_block(s.project.containers.explanation_box):
            with st_list(list_type="ul") as l:
                with l.item(): st_write(s.medium, (s.bold, "Workarounds to remove"), " — a title or an author typed with literal accents to dodge the old rendering can go back to TeX, or stay as is: both read the same now.")
                with l.item(): st_write(s.medium, (s.bold, "Institutions"), " — write an organisation as {{United Nations}} (double braces) so it is one name, not a surname and a first name; add shortauthor = {UN} to keep its citation short.")
                with l.item(): st_write(s.medium, (s.bold, "Ancient works"), " — add origdate (or a negative year) when the citation code should show the original date rather than the edition year; citation codes of those entries change.")
                with l.item(): st_write(s.medium, (s.bold, "Unknown keys"), " — turn on BibConfig(strict=True) once, run stx validate --build, fix the [key?] it reports.")
                with l.item(): st_write(s.medium, (s.bold, "Check the blocks"), " — stx validate --build --snapshot before.json on the old version, then --against before.json on the new one: the list of blocks whose rendering changed.")

