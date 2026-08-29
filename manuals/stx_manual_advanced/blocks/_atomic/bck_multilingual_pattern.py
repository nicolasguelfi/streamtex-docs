"""Multilingual Documents — the leaves + T()/TF() + language-in-the-address pattern.

Covers: where the text lives (leaves), how it is resolved (T / TF),
where the language comes from (STX_LANG > ?lang= > default), the double
export, the i18n quality gate, and the reference implementation (POSTAIR).
"""

from streamtex import st_write, st_space, st_block, st_list
from streamtex.enums import Tags as t
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
        StreamTeX has **no i18n API** — and a bilingual document does not
        need one. The pattern below ships EN/FR presentations with three
        things the library already provides: a parameter passed to every
        block (`block_kwargs`), a language read from the address, and one
        static export per language. It was built for the POSTAIR / AI Day
        2026 decks (Université du Luxembourg) and is described here as the
        reference way to do it.

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
        Two tiny helpers resolve a leaf. `T()` returns a string; `TF()`
        returns a **sequence of `st_write` fragments** — strings and
        `(style, text)` tuples — to unpack in a single call. Both live in
        one shared module (`postair_lang.py` in the reference project).
    """)
    st_space("v", 1)

    show_code("""\
        LANGS = ("en", "fr")
        DEFAULT = "en"

        def T(node, lang: str | None = None) -> str:
            if isinstance(node, str):
                # A bare string is an unfinished migration, not a missing
                # translation: fail now, not in front of the audience.
                raise TypeError(f"bare string passed to T(): {node[:60]!r}")
            if not isinstance(node, dict) or "en" not in node:
                raise TypeError(f"invalid leaf: {node!r}")
            lang = lang or current_lang()
            value = node.get(lang)
            return node[DEFAULT] if value is None else value   # "" is a value

        def TF(node, lang: str | None = None) -> tuple:
            value = T(node, lang)
            return (value,) if isinstance(value, str) else tuple(value)

        # In a block
        def build(lang: str = "en", **_):
            st_write(s.large, T(TITLE, lang), toc_lvl="1")
            st_write(s.medium, *TF(YOUR_TURN, lang))""")
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.medium, (bs.param_label, "Fallback, never a hole"), " — a missing translation shows the English text on screen. The gate (step 5) is what makes the absence loud — before the rehearsal, not in the room.")
            with l.item(): st_write(s.medium, (bs.param_label, "A bare string raises"), " — `T(\"Welcome\")` is a `TypeError`. Every projected string goes through a leaf, so an inventory of bare literals (step 5) is the exact list of what is left to migrate.")
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
        address and reloading. Resolution order:
    """)
    st_space("v", 1)

    show_code("""\
        import os
        import streamlit as st

        ENV_KEY, QUERY_KEY = "STX_LANG", "lang"

        def _query_lang() -> str | None:
            try:
                value = st.query_params.get(QUERY_KEY)
            except Exception:            # headless export: no script context
                return None
            return value if value in LANGS else None   # a bad suffix never breaks a deck

        def current_lang() -> str:
            \"\"\"export > address > default\"\"\"
            lang = os.environ.get(ENV_KEY) or _query_lang() or DEFAULT
            if lang not in LANGS:
                raise ValueError(f"language {lang!r} not in {LANGS}")
            return lang

        def with_lang(url: str, lang: str) -> str:
            \"\"\"A link to another deck, in *lang*: the language travels in the address.\"\"\"
            sep = "&" if "?" in url else "?"
            return f"{url}{sep}{QUERY_KEY}={lang}"

        # book.py — the single entry point into the blocks
        st_book([...], block_kwargs={"lang": current_lang()}, paginate=True)""")
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
        behind one hub) are the implementation this chapter describes:

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
