"""Banner Configuration — BannerMode and BannerConfig reference."""

from streamtex import (
    st_write, st_space,
)
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Banner configuration block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    feature = s.project.titles.feature_title


bs = BlockStyles


def build():
    """Banner Configuration — modes, presets, and custom config."""
    st_write(bs.heading, "Banner Configuration", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        The banner is the header bar displayed at the top of every
        page in a StreamTeX book. It shows the project title,
        navigation progress, and page count.

        BannerConfig controls its appearance and behavior. Pass it
        to st_book() via the banner= parameter.
    """)
    st_space("v", 2)

    # --- BannerMode ---
    st_write(bs.sub, "BannerMode", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        BannerMode is an enum with three values that control
        how the banner is rendered:

        - **FULL** \u2014 Full-height banner with title, progress bar,
        and page count. Best for formal documents and manuals.

        - **COMPACT** \u2014 Slim banner with a condensed layout. Shows
        the title and a thin progress indicator. Suitable for
        presentations and lightweight projects.

        - **HIDDEN** \u2014 No banner at all. The content starts
        immediately at the top of the page. Use when you need
        maximum vertical space.
    """)
    st_space("v", 2)

    # --- Presets ---
    st_write(bs.sub, "BannerConfig Presets", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        BannerConfig provides factory methods for common setups.
        Each preset returns a fully configured BannerConfig instance.
    """)
    st_space("v", 1)

    show_code("""\
        from streamtex import BannerConfig

        # Full banner with all features enabled
        banner = BannerConfig.full()

        # Compact banner with slim layout
        banner = BannerConfig.compact()

        # Hidden banner (no banner rendered)
        banner = BannerConfig.hidden()
    """, language="python")
    st_space("v", 2)

    # --- Custom BannerConfig ---
    st_write(bs.sub, "Custom BannerConfig", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        For fine-grained control, create a BannerConfig directly.
        You can set the mode, color, and toggle individual features.
    """)
    st_space("v", 1)

    show_code("""\
        from streamtex import BannerConfig, BannerMode

        banner = BannerConfig(
            mode=BannerMode.FULL,
            color="rgba(211, 47, 47, 0.8)",
            show_progress=True,
            show_page_count=True,
        )
    """, language="python")
    st_space("v", 2)

    # --- Visual description of each mode ---
    st_write(bs.sub, "What Each Mode Looks Like", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        - **FULL mode** \u2014 A tall header bar spanning the full width.
        Displays the project title centered, a horizontal progress
        bar below the title, and a page counter (e.g. "3 / 12")
        on the right side. Background uses the configured color.

        - **COMPACT mode** \u2014 A thin strip at the top of the page.
        The title appears left-aligned in a smaller font. A narrow
        progress line runs along the bottom edge of the strip.
        Page count is hidden by default.

        - **HIDDEN mode** \u2014 Nothing is rendered. The page content
        begins at the very top with no header spacing.
    """)
    st_space("v", 2)

    # --- Usage in st_book() ---
    st_write(bs.sub, "Usage in st_book()", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Pass the BannerConfig instance to st_book() using the
        banner= keyword argument.
    """)
    st_space("v", 1)

    show_code("""\
        from streamtex import st_book, BannerConfig

        st_book(
            [bck_intro, bck_chapter_1, bck_chapter_2],
            banner=BannerConfig.full(),
        )

        # Or with a custom config
        st_book(
            [bck_intro, bck_chapter_1, bck_chapter_2],
            banner=BannerConfig(
                mode=BannerMode.COMPACT,
                color="rgba(25, 118, 210, 0.9)",
                show_progress=True,
                show_page_count=False,
            ),
        )
    """, language="python")
    st_space("v", 2)

    show_details("""\
        The banner color accepts any valid CSS color value:
        named colors, hex, rgb(), rgba(), or hsl().

        If no banner= argument is provided, st_book() defaults
        to BannerConfig.full().
    """)
    st_space("v", 3)

    # --- st_chrome_banner() ---
    st_write(bs.sub, "st_chrome_banner()", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        st_chrome_banner() displays a dismissible banner at the top
        of the page recommending Google Chrome when the user is
        visiting with a different browser.

        It is called automatically by st_book() (chrome_banner=True
        by default). You can also call it manually in book.py for
        standalone pages that do not use st_book().
    """)
    st_space("v", 1)

    show_code("""\
        from streamtex import st_chrome_banner

        # Called automatically by st_book() — no action needed.
        # For standalone pages without st_book():
        st_chrome_banner()""")
    st_space("v", 1)

    show_details("""\
        The banner is injected as a fixed-position element in the
        parent Streamlit frame. It does not interfere with block
        numbering or the Table of Contents.

        Users can dismiss the banner by clicking the X button.

        To disable the automatic banner in st_book(), pass
        chrome_banner=False.
    """)
    st_space("v", 1)
