import streamlit as st
import streamtex as stx
from streamtex import *
from streamtex.styles import Style as ns
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Forms and session state demo styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    content = s.large
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Forms & Session State", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            st.form() groups inputs (no rerun between entries).

            st.session_state persists data across reruns.

            StreamTeX content re-renders reading the current state.
        """)
        st_space("v", 2)

        # --- Section 1: Basic form ---
        st_write(bs.sub, "Basic Form", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
with st.form("bck26_profile_form"):
    name = st.text_input("Name", value="Ada Lovelace")
    age = st.number_input("Age", 0, 120, 25)
    submitted = st.form_submit_button("Submit")
if submitted:
    with st_block(s.project.containers.result_box):
        st_write(s.large + s.bold, f"Name: {name}")
        st_br()
        st_write(s.large, f"Age: {age}")""")
        st_space("v", 1)

        with st.form("bck26_profile_form"):
            name = st.text_input("Name", value="Ada Lovelace")
            age = st.number_input("Age", 0, 120, 25)
            submitted = st.form_submit_button("Submit")
        if submitted:
            with st_block(s.project.containers.result_box):
                st_write(s.large + s.bold, f"Name: {name}")
                st_br()
                st_write(s.large, f"Age: {age}")
        st_space("v", 2)

        # --- Section 2: Session state counter ---
        st_write(bs.sub, "Session State Counter", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
if "bck26_counter" not in st.session_state:
    st.session_state.bck26_counter = 0
if st.button("Increment", key="bck26_incr"):
    st.session_state.bck26_counter += 1
count = st.session_state.bck26_counter
size = min(12 + count * 4, 96)
with st_block(s.project.containers.result_box):
    st_write(ns(f"font-size: {size}px;") + s.bold,
             f"Count: {count}")""")
        st_space("v", 1)

        if "bck26_counter" not in st.session_state:
            st.session_state.bck26_counter = 0
        if st.button("Increment", key="bck26_incr"):
            st.session_state.bck26_counter += 1
        count = st.session_state.bck26_counter
        size = min(12 + count * 4, 96)
        with st_block(s.project.containers.result_box):
            st_write(ns(f"font-size: {size}px;") + s.bold,
                     f"Count: {count}")
        st_space("v", 2)

        # --- Section 3: Form with styled feedback ---
        st_write(bs.sub, "Form with Styled Feedback", toc_lvl="+1")
        st_space("v", 1)

        show_code(file="examples/state/form_validation.py")
        st_space("v", 1)

        with st.form("bck26_validation_form"):
            password = st.text_input("Enter a password", type="password")
            validated = st.form_submit_button("Validate")
        if validated:
            if len(password) >= 8:
                with st_block(s.project.containers.good_callout):
                    st_write(s.project.titles.tip_label, "Valid")
                    st_space("v", 1)
                    st_write(s.large, "Strong password!")
            else:
                with st_block(s.project.containers.bad_callout):
                    st_write(s.project.titles.warning_label, "Invalid")
                    st_space("v", 1)
                    st_write(s.large,
                             f"Too short ({len(password)}/8 characters).")
        st_space("v", 2)

        # --- Section 4: Persistent list ---
        st_write(bs.sub, "Persistent List", toc_lvl="+1")
        st_space("v", 1)

        show_code(file="examples/state/persistent_list.py")
        st_space("v", 1)

        if "bck26_items" not in st.session_state:
            st.session_state.bck26_items = []
        with st.form("bck26_add_item_form"):
            new_item = st.text_input("New item")
            added = st.form_submit_button("Add to list")
        if added and new_item:
            st.session_state.bck26_items.append(new_item)
        if st.session_state.bck26_items:
            with st_block(s.project.containers.result_box):
                with st_list(list_type=lt.ordered, li_style=s.large) as l:
                    for item in st.session_state.bck26_items:
                        with l.item():
                            st_write(item)
        st_space("v", 2)

        show_details("""\
            st.form() prevents reruns between input changes.

            st.session_state persists values across reruns.

            StreamTeX content re-renders each time, reading the latest state.

            Use unique keys for all widgets to avoid conflicts.
        """)
        st_space("v", 2)

        # --- Section 5: Values that survive pagination (0.7.40) ---
        st_write(bs.sub, "Values that Survive Pagination — kept_widget()", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            In a paginated book a widget lives on ONE page. Streamlit purges
            a widget's session key as soon as a rerun ends without that
            widget — so its value holds one page, then falls back to the
            default on the next one.

            stx.kept_widget(name, default) returns the key= and on_change=
            of the two-key pattern: the widget keeps its own key and copies
            its value, on change, into a plain session key the purge never
            touches. stx.kept_value(name) reads it back, on any page.
        """)
        st_space("v", 1)

        show_code("""\
# Page 1 — the widget (no value= / index=: the kept value is its initial state)
st.radio("Language", ["en", "fr"],
         **stx.kept_widget("bck26_lang", default="en"))

# Any page, before or after — the value, even when the widget is not shown
lang = stx.kept_value("bck26_lang", "en")""")
        st_space("v", 1)

        st.radio("Language", ["en", "fr"],
                 **stx.kept_widget("bck26_lang", default="en"))
        with st_block(s.project.containers.result_box):
            st_write(s.large, "kept_value(\"bck26_lang\") = ",
                     (s.bold, str(stx.kept_value("bck26_lang", "en"))),
                     " — change it, then turn the page: the value stays.")
        st_space("v", 1)

        show_details("""\
            kept_widget(name, default=None) -> dict with key and on_change;
            kept_value(name, default=None) returns the default before the
            widget was ever shown.

            Do not pass value= / index= to the widget: Streamlit would
            reset it each time the page is shown again.

            Keep the language of a projected document in the address
            instead (see Multilingual Documents): kept_widget is for the
            reader's choices inside a session.
        """)

