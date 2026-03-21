"""StreamTeX Collection - Test Hub with Modern Design."""

import importlib.util
import tomllib
from pathlib import Path

import blocks
import setup  # noqa: F401  (side-effect: adds project dir to sys.path)
import streamlit as st
from custom.themes import dark

import streamtex as stx
import streamtex.styles as sts
from streamtex import TOCConfig, NumberingMode, st_book, PdfConfig, PresentationProfile, ViewMode

_doc_version = tomllib.loads((Path(__file__).parent.parent.parent / "pyproject.toml").read_text()).get("project", {}).get("version", "?")
_spec = importlib.util.spec_from_file_location("bck_changelog",
    str(Path(__file__).parent.parent / "shared-blocks" / "blocks" / "bck_changelog.py"))
_bck_changelog = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bck_changelog)

_logo = str(Path(__file__).parent.parent / "shared-blocks" / "logo-stx.png")
st.set_page_config(
    page_title="StreamTeX - Collection",
    page_icon=_logo,
    layout="wide",
    initial_sidebar_state="expanded"
)
sts.theme = dark

# Display the collection home (single page: header + cards)
toc = TOCConfig(numbering=NumberingMode.SIDEBAR_ONLY, toc_position=None, search=True, sidebar_max_level=2)

st_book([
    blocks.bck_home,

    # Changelog (shared block)
    _bck_changelog,
], toc_config=toc, paginate=False,
   inspector=stx.InspectorConfig(enabled=True),
   pdf_config=PdfConfig(
       margin_top="0", margin_bottom="0",
       margin_left="0", margin_right="0",
   ),
   view_modes=[ViewMode.PAGINATED, ViewMode.CONTINUOUS],
   doc_version=_doc_version,
   presentation_profiles=PresentationProfile.desktop_mobile_preset())
