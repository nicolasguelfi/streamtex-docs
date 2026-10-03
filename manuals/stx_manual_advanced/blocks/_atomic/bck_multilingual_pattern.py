"""Multilingual Documents — the leaves + T()/TF() + language-in-the-address pattern.

Covers: where the text lives (leaves), how it is resolved (T / TF),
where the language comes from (STX_LANG > ?lang= > default), the double
export, the i18n quality gate, and the reference implementation (POSTAIR).
Since 0.7.37 the helpers are provided by ``streamtex.i18n`` (explicit import,
not in the star import) and ``st_book(lang="auto")``.
"""

from streamtex import st_write, st_space, st_block, st_list
from streamtex.enums import Tags as t
from streamtex.i18n import T, with_lang
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Multilingual chapter styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    param_label = s.medium + s.text.weights.bold_weight


bs = BlockStyles


def build():
    st_write(bs.heading, "Multilingual Documents", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        A bilingual document needs no message catalog. The pattern below
        ships EN/FR presentations with a parameter passed to every block,
        a language read from the address, and one static export per
        language. It was built for the POSTAIR / AI Day 2026 decks
        (Université du Luxembourg); since streamtex 0.7.37 its helpers are
        part of the library, in the module `streamtex.i18n` (`T`, `TF`,
        `current_lang`, `with_lang`, `set_languages`), and
        `st_book(lang="auto")` hands the language to every block.

        These names are **not** exported by `from streamtex import *`:
        import them explicitly. A project that already defines its own `T`
        or `current_lang` keeps it — nothing in the library collides with it.

        Four decisions, in order: **where the text lives**, **how it is
        resolved**, **where the language comes from**, **how it is exported**.
    """)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # 1. Where the text lives — leaves
    # ------------------------------------------------------------------
    st_write(bs.sub, "1. Where the text lives — leaves {lang: …}", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A translatable string is a **leaf**: a dict indexed by language code.
        A leaf projected by one slide lives **in that block**, next to the
        facts it states; a leaf that appears in two blocks or more lives
        **once** in a shared lexicon. No `.po` files, no message ids: the
        translation sits where the reviewer reads it.
    """)
    st_space("v", 1)

    show_code("""\
        # blocks/bck_survey.py — the block owns its own text
        TITLE = {"en": "The survey, by show of hands",
                 "fr": "Le sondage, à main levée"}
        YOUR_TURN = {"en": ("Your turn — ", (KW, "join the survey")),
                     "fr": ("À vous — ", (KW, "rejoignez le sondage"))}

        # shared-blocks/my_i18n.py — what repeats across blocks
        UI = {
            "references": {"en": "References", "fr": "Références"},
            "next_deck":  {"en": "Next deck",  "fr": "Deck suivant"},
        }

        def ui(key: str, lang: str) -> str:
            return T(UI[key], lang)        # unknown key → KeyError, on purpose""")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # 2. How it is resolved — T() and TF()
    # ------------------------------------------------------------------
    st_write(bs.sub, "2. How it is resolved — T() and TF()", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Two helpers resolve a leaf. `T()` returns its text; `TF()` returns
        a **sequence of `st_write` fragments** — strings and
        `(style, text)` tuples — to unpack in a single call. Both come from
        `streamtex.i18n`, imported explicitly.
    """)
    st_space("v", 1)

    show_code("""\
        from streamtex.i18n import T, TF

        # T(entry, lang=None, *, strict=False)  — lang=None: current_lang()
        # TF(entry, lang=None, *, strict=False) — a tuple of fragments

        # In a block
        def build(lang: str = "en", **_):
            st_write(s.large, T(TITLE, lang), toc_lvl="1")
            st_write(s.medium, *TF(YOUR_TURN, lang))

        # strict=True: a bare string is refused (an unfinished migration)
        T("Welcome", strict=True)       # TypeError""")
    st_space("v", 1)

    st_write(s.medium, "Live — the same leaf, in each language:")
    st_space("v", 1)
    demo_leaf = {"en": "The survey, by show of hands",
                 "fr": "Le sondage, à main levée"}
    with st_block(s.project.containers.result_box):
        st_write(s.medium, (bs.param_label, 'T(leaf, "en") → '), T(demo_leaf, "en"))
        st_write(s.medium, (bs.param_label, 'T(leaf, "fr") → '), T(demo_leaf, "fr"))
        st_write(s.medium, (bs.param_label, 'T(leaf, "de") → '), T(demo_leaf, "de"),
                 "  (not a language of the leaf: the default language)")
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.medium, (bs.param_label, "Fallback, never a hole"), " — a missing translation shows the default language (then the first value of the leaf) on screen. The gate (step 5) is what makes the absence loud — before the rehearsal, not in the room.")
            with l.item(): st_write(s.medium, (bs.param_label, "A bare string, with strict=True, raises"), " — `T(\"Welcome\", strict=True)` is a `TypeError` (without `strict`, the library returns a bare string as is). Every projected string goes through a leaf, so an inventory of bare literals (step 5) is the exact list of what is left to migrate.")
            with l.item(): st_write(s.medium, (bs.param_label, "An empty string is a value"), " — `{\"en\": \" — the evidence\", \"fr\": \"\"}` is a template suffix French does not have; it must not fall back to English.")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # 3. Where the language comes from — the address
    # ------------------------------------------------------------------
    st_write(bs.sub, "3. Where the language comes from — the address", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        **No widget, no session state.** A language selector is a widget —
        and a widget never survives a static export, is one more thing to
        click in an auditorium, and has to be kept in sync across decks.
        Instead the language is *in the address*: `…/?lang=fr`. What you
        opened is what you project; changing language is editing the
        address and reloading. `current_lang()` resolves, in order:
        `$STX_LANG` > `?lang=` > default.
    """)
    st_space("v", 1)

    show_code("""\
        # book.py
        from streamtex import st_book
        from streamtex.i18n import set_languages, current_lang

        # The languages of the document and its default (default: ("en", "fr"), "en")
        set_languages(["en", "fr"], default="en")

        # Hands build(lang=...) to every block: the same as
        # block_kwargs={"lang": current_lang()}
        st_book([...], lang="auto", paginate=True)

        # An explicit code is accepted too: st_book([...], lang="fr")""")
    st_space("v", 1)

    show_code("""\
        from streamtex.i18n import with_lang

        # A link to another deck, in the same language: the language travels
        # in the address. An existing lang= is replaced; the other parameters
        # and the #fragment are kept.
        with_lang("https://example.org/deck2/?page=3#intro", "fr")
        # → "https://example.org/deck2/?page=3&lang=fr#intro"
        with_lang("https://example.org/deck2/?lang=en", "fr")
        # → "https://example.org/deck2/?lang=fr"
        """)
    st_space("v", 1)

    st_write(s.medium, (bs.param_label, "Live — "), "with_lang(\"https://example.org/deck2/?page=3#intro\", \"fr\") → ",
             with_lang("https://example.org/deck2/?page=3#intro", "fr"))
    st_space("v", 1)

    show_details("""\
        A language outside set_languages() in the address is ignored (a
        wrong suffix never breaks a projection); in `$STX_LANG` it raises
        (an export in an unknown language is a command error). An explicit
        "lang" in block_kwargs wins over st_book(lang=...).

        Projects that wrote these helpers themselves (as the reference
        project did, in postair_lang.py) can keep them: the library names
        live in streamtex.i18n and never enter the star import.
    """)
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.medium, (bs.param_label, "STX_LANG"), " — the static export: one pass per language. The same variable is read by `stx export html` for the `<html lang>` attribute, so one `STX_LANG=fr` drives both the content and the document language.")
            with l.item(): st_write(s.medium, (bs.param_label, "?lang=fr"), " — set by the per-language buttons of the hub / collection page and propagated by every \"Next deck\" link through `with_lang()`.")
            with l.item(): st_write(s.medium, (bs.param_label, "Default"), " — English. A deck opened with no parameter is the English deck.")
            with l.item(): st_write(s.medium, (bs.param_label, "Pagination cache"), " — the kwargs are part of the cache key: `?lang=fr` gets its own TOC, markers and page titles (see the previous section).")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # 4. Double export
    # ------------------------------------------------------------------
    st_write(bs.sub, "4. Double export — one static HTML per language", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The public reads `/html/en/…` and `/html/fr/…`. The Dockerfile (build
        time) and the entrypoint (start-up) run the same loop; `stx export
        html` reads `STX_LANG` for `<html lang>` and `--suffix` keeps both
        languages in one directory when you prefer that layout.
    """)
    st_space("v", 1)

    show_code("""\
        # entrypoint.sh — one export per language
        for lang in en fr; do
            STX_LANG=$lang uv run stx export html --output /app/static-html/$lang/ .
        done

        # Same, in a single directory: deck-en.html + deck-fr.html
        for lang in en fr; do
            STX_LANG=$lang uv run stx export html --suffix -$lang --output ./out .
        done

        # Explicit override of the document language, independent of the env
        stx export html --lang fr .""", language="bash", line_numbers=False)
    st_space("v", 1)

    show_details("""\
        **Bibliography.** `BibConfig(locale="fr")` switches the connector
        words of the formatted references and author-year citations
        (`Vaswani et Shazeer`, `Dans …`, `p.`, `n°`); build it from the same
        language: `BibConfig(locale=current_lang())` in `book.py`. The
        `st_bibliography(title=…)` heading is yours to translate —
        `ui("references", lang)` in the reference project.
    """)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # 5. The quality gate
    # ------------------------------------------------------------------
    st_write(bs.sub, "5. The quality gate — check_i18n", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The fallback keeps the screen clean; a **gate script** is what keeps
        the translation complete. The reference implementation
        (`_project/tools/check_i18n.py`) has five checks, none of which
        modifies the repository. The two that matter most: the English
        export must not change a byte during the translation work, and
        every leaf must carry every language.
    """)
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.medium, (bs.param_label, "--baseline / --regress"), " — snapshot the EN export (markers, TOC entries, text per marker, media) and compare on every run: the i18n work must not change what English projects.")
            with l.item(): st_write(s.medium, (bs.param_label, "--inventory"), " — AST scan of the blocks for bare English literals passed to `st_write` / `st_marker` / `label=` / `toc_label=`… and leaves without `fr`: the work-order of the migration.")
            with l.item(): st_write(s.medium, (bs.param_label, "--parity"), " — every leaf carries every language, non-empty, `fr != en` unless whitelisted; with `--with-export`, same number of markers and media in the EN and FR exports.")
            with l.item(): st_write(s.medium, (bs.param_label, "--words"), " — French bullets longer than 8 words when the English one has 8 or fewer: a warning, never red.")
            with l.item(): st_write(s.medium, (bs.param_label, "--drift <git-ref>"), " — leaves whose English changed since a reference commit while the French did not: the net against future drift.")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Reference implementation
    # ------------------------------------------------------------------
    st_write(bs.sub, "Reference implementation — POSTAIR", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The POSTAIR / AI Day 2026 decks (Université du Luxembourg, project
        `sumvadis-streamtex`, streamtex 0.7.25, eight paginated modules
        behind one hub) are the implementation this chapter describes; its
        helpers became `streamtex.i18n` in 0.7.37:

        - `modules/shared-blocks/postair_lang.py` — `LANGS`, `current_lang()`,
          `with_lang()`, `T()`, `TF()`;
        - `modules/shared-blocks/postair_i18n.py` — the shared lexicon
          (`ui()`, `term()` over a frozen glossary);
        - `modules/<deck>/book.py` — `st_book(..., block_kwargs={"lang": current_lang()})`;
        - `_project/tools/check_i18n.py` — the gate;
        - `Dockerfile` / `entrypoint.sh` — the per-language export loop.
    """)
    st_space("v", 2)

    show_details("""\
        **What the library does not do (by design).** No message catalog,
        no locale negotiation from the browser, no translated navigation
        chrome in the export (the sidebar labels and the search placeholder
        stay English). Each is a separate feature request; the pattern above
        does not need them to ship a bilingual document.
    """)
    st_space("v", 2)
