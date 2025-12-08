import time
import streamlit as st


def query_input():
    with st.form("search-form", border=False):
        query = st.text_input(
            "Enter Your Search Query",
            key="primary-search-input",
            placeholder="e.g. Books, Laptop, T-Shirts, etc.",
            max_chars=99,
        )
        submitted = st.form_submit_button(
            "Start Scraping", type="primary", width="stretch"
        )

    if submitted:
        if not query.strip():
            st.warning("Please fill in the search input properly.")
            st.session_state.clear()
            return

        st.session_state.query = query
        st.session_state.query_submitted = True
        st.session_state.scraping_in_progress = True
        st.session_state.started_at = time.time()
    else:
        st.session_state.query_submitted = False
        st.session_state.scraping_in_progress = False
