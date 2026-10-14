"""Composing by Atoms — a live list block of two atoms.

The list block blocks/_atomic/bck_demo_quiz_list.py is shown (read from disk),
rendered with st_include(markers=False), and the registry entries its
two atoms place are read back. With markers=False they are neither stops
nor listed: the navigation bar shows the chapter's section around them.
"""

from pathlib import Path

import streamtex as stx
from streamtex import st_include, st_space, st_write
from streamtex.marker import marker_entries
from custom.styles import Styles as s
from blocks.helpers import show_code
import blocks


class BlockStyles:
    """Live demo styles."""
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    st_write(bs.sub, "Live demo — a list block of two atoms", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large, "The file blocks/_atomic/bck_demo_quiz_list.py of this manual, read "
                      "live. Its two atoms live in its own _atomic/ folder "
                      "(blocks/_atomic/_atomic/) and each opens with st_marker(…):")
    st_space("v", 1)

    quiz = blocks.bck_composing_by_atoms.bck_demo_quiz_list
    show_code(Path(quiz.__file__).read_text(encoding="utf-8"))
    st_space("v", 1)

    st_write(s.large, "Rendered here with st_include(bck_demo_quiz_list, "
                      "markers=False), so that the two demo markers do not become stops "
                      "of this manual:")
    st_space("v", 1)

    before = len(marker_entries())
    st_include(quiz, markers=False)
    added = marker_entries()[before:]
    st_space("v", 1)

    st_write(s.large, "The registry entries the two atoms just placed, read back live: "
                      "registered with their labels and anchors, but neither a stop nor "
                      "listed.")
    st_space("v", 1)
    stx.st_table({
        "label": [e["label"] for e in added],
        "stop": [str(e["stop"]) for e in added],
        "listed": [str(e["listed"]) for e in added],
        "anchor": [e["anchor"] for e in added],
    })
    st_space("v", 1)

    st_write(s.large, "Included with the default markers=True, the same list block would "
                      "add two stops and two rows to the marker list of this manual: one "
                      "per slide, which is what a deck wants. Here the counter of the "
                      "navigation bar and the marker list are unchanged.")
    st_space("v", 2)
