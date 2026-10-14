"""Demo atom — the question of the quiz list block (Composing by Atoms chapter).

An atom: ONE slide, its named marker first, then its content in a box,
never a break inside. Included by ``bck_demo_quiz_list``.
"""

from streamtex import st_block, st_marker, st_write
from custom.styles import Styles as s


class BlockStyles:
    """Demo atom styles."""
    box = s.project.containers.explanation_box
    label = s.project.titles.feature_title


bs = BlockStyles


def build(**_):
    st_marker("Quiz · question")
    with st_block(bs.box):
        st_write(bs.label, "Atom 1 — the question")
        st_write(s.large, "What does a list block hold?")
