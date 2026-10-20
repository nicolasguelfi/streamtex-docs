"""Countdown racks — st_countdown: countdown, stopwatch and clock cards on a slide (streamtex 0.7.57)."""

from streamtex import *
from streamtex.enums import Tags as t

from blocks.helpers import show_code, show_details, show_explanation
from custom.styles import Styles as s


class BlockStyles:
    """Styles for the countdown racks chapter."""

    heading = s.project.titles.section_title + s.center_txt
    section = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Demonstrate st_countdown: chain and parallel racks, card types, alarms, editing."""

    st_write(bs.heading, "Countdown Racks", tag=t.h1, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""
        `st_countdown(steps, mode)` draws a grid of timer cards on a slide:
        session timers for an agenda, timed exercises, a break screen.
        Each card is a countdown, a stopwatch or a clock. Everything runs in
        the browser, the same way in the live app and in the HTML export;
        nothing runs before a click.
    """)
    st_space("v", 2)

    # --- 1. Chain ---
    st_write(bs.section, "Chain mode", toc_lvl="+1")
    st_space("v", 1)
    show_explanation("""
        In `"chain"` mode one card runs at a time: ▶ Start launches the
        first one, and each card that reaches zero starts the next. ▶ on a
        card pauses the others; ⏸ keeps the time left; ↺ resets the card.
        While a card runs it shows the wall time it will end at. A finished
        card shows its initial duration in the finished colour.
    """)
    st_space("v", 1)
    show_code("""\
        st_countdown([("Intro", 0.5), ("Talk", 1), ("Questions", 1.5)],
                     "chain", grid=(1, 3), rack_vh=34)""")
    st_space("v", 1)
    st_countdown([("Intro", 0.5), ("Talk", 1), ("Questions", 1.5)], "chain", grid=(1, 3), rack_vh=34)
    st_space("v", 2)

    # --- 2. Card types ---
    st_write(bs.section, "Card types", toc_lvl="+1")
    st_space("v", 1)
    show_explanation("""
        The second item of a step is its target; the third, an options
        dict. A `stopwatch` counts up, with an optional target in minutes,
        and keeps counting past it. A `clock` shows the time of an IANA
        time zone, with an optional target `"HH:MM"`. In a chain, the cards
        with an end are gates the chain waits for; the cards with no end
        run freely, and the chain passes them.
    """)
    st_space("v", 1)
    show_code("""\
        st_countdown([
            ("Luxembourg", None, {"type": "clock", "tz": "Europe/Luxembourg"}),
            ("Tokyo", None, {"type": "clock", "tz": "Asia/Tokyo"}),
            ("Exercise", 2, {"type": "stopwatch"}),     # target: 2 min
            ("Back at", "14:30", {"type": "clock", "tz": "Europe/Luxembourg"}),
        ], "chain", rack_vh=50)""")
    st_space("v", 1)
    st_countdown([
        ("Luxembourg", None, {"type": "clock", "tz": "Europe/Luxembourg"}),
        ("Tokyo", None, {"type": "clock", "tz": "Asia/Tokyo"}),
        ("Exercise", 2, {"type": "stopwatch"}),
        ("Back at", "14:30", {"type": "clock", "tz": "Europe/Luxembourg"}),
    ], "chain", rack_vh=50)
    st_space("v", 2)

    # --- 3. Parallel, alarms, break screen ---
    st_write(bs.section, "Parallel mode, alarms and the break screen", toc_lvl="+1")
    st_space("v", 1)
    show_explanation("""
        In `"parallel"` mode every card runs on its own. Alarms are opt-in:
        `CountdownConfig(alarm=...)` picks a timbre synthesised in the
        browser (bell, beep, chime, gong — no audio file, so an offline
        room rings too), and a step's third item overrides it for one card.
        An alarmed rack starts muted: the 🔔 of each card arms it, the
        global 🔔 arms them all, and the choice is remembered.
        `autostart=True` starts the rack the first time it is on screen.
    """)
    st_space("v", 1)
    show_code("""\
        st_countdown([("Team A", 5), ("Team B", 5, {"alarm": "gong", "duration": 6}),
                      ("Team C", 5, "off")],
                     "parallel", config=CountdownConfig(alarm="bell", alarm_volume=0.8))

        # a break screen: one card, starts when shown, no global buttons
        st_countdown([("Back in", 15)],
                     config=CountdownConfig(autostart=True, show_global_buttons=False))""")
    st_space("v", 1)
    st_countdown([("Team A", 5), ("Team B", 5, {"alarm": "gong", "duration": 6}), ("Team C", 5, "off")],
                 "parallel", rack_vh=30, config=CountdownConfig(alarm="bell", alarm_volume=0.8))
    st_space("v", 2)

    show_details("""
        - **Edit a value**: double-click the digits. A countdown takes its
        time left (`40` = 40 min, `40:30`), a stopwatch its target in
        minutes, a clock its target `HH:MM` (empty = no target). Enter or a
        click elsewhere applies, Escape cancels, ↺ restores the original.

        - **Size**: `grid=(rows, cols)` (default: the compact grid with the
        biggest cells), `rack_vh` (height of the grid in % of the window),
        `scale`, `label_scale`, `ends_scale`, `digits_width`. The digits are
        measured to fill their card; no scrollbar appears.

        - **Labels and colours**: `CountdownConfig(start_all_label=...,
        ends_at_label=..., since_label=..., color_running=..., card_css=...)`.
        Card labels are plain strings: translate them before the call.
        `CountdownConfig.resolve(local, json_path)` layers defaults, a dict
        and a JSON file, dropping what does not fit instead of failing.

        - **Export and PDF**: the racks work in the HTML export; a PDF shows
        them idle (labels and full durations).
    """)
    st_space("v", 3)
