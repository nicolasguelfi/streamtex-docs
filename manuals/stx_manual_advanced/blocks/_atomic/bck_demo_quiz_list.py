"""Demo list block — two atoms in order (Composing by Atoms chapter).

Not an entry of the book: the chapter includes it live. Its build() only
holds the order of its items; st_sequence draws the separator between two
of them, never before the first nor after the last.
"""

import streamtex as stx
from streamtex import SlideBreakConfig, SlideBreakMode, st_sequence

bck_demo_quiz_question = stx.load_atomic_block("bck_demo_quiz_question", __file__)
bck_demo_quiz_answer = stx.load_atomic_block("bck_demo_quiz_answer", __file__)

ITEMS = [bck_demo_quiz_question, bck_demo_quiz_answer]

# A compact rule, so the demo fits in the page. Without separator=, the
# module's standard break is drawn (its settings, no marker).
COMPACT_RULE = SlideBreakConfig(mode=SlideBreakMode.RULE_ONLY, marker=False,
                                rule_margin_top="1em", rule_margin_bottom="1em")


class BlockStyles:
    """A list block has no styles: the items carry them."""
    pass


bs = BlockStyles


def build(*args, **kwargs):
    st_sequence(ITEMS, *args, separator=COMPACT_RULE, **kwargs)
