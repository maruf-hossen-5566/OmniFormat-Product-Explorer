import streamlit as st
from scraper.parser import parser
from scraper.scraper import scraper
from ui.components import hero
from ui.components.hero import hero_section
from ui.components.query_input import query_input
from ui.components.stop_btn import stop_button
from ui.components.tabs import (
    card_preview_tab,
    csv_preview_tab,
    json_preview_tab,
    data_preview_tabs,
    stc_preview_tab,
)


def states_initialization():
    if "driver" not in st.session_state:
        st.session_state.driver = None
    if "query" not in st.session_state:
        st.session_state.query = None
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False
    if "output" not in st.session_state:
        st.session_state.output = None
    if "scraping_in_progress" not in st.session_state:
        st.session_state.scraping_in_progress = False


def data_preview():
    query = st.session_state.get("query")
    data = st.session_state.get("output")
    driver = st.session_state.get("driver")

    if query and data:
        st.space("stretch")
        card_tab, json_tab, csv_tab, stc_tab = data_preview_tabs()
        with json_tab:
            json_preview_tab(query, data)
        with card_tab:
            card_preview_tab(query, data)
        with csv_tab:
            csv_preview_tab(query, data)
        with stc_tab:
            stc_preview_tab(query, data)
    else:
        st.divider()
        st.info(
            "🚫 No data yet. Enter a query and click “Scrape” to see results here.",
        )


def run_scraping():
    query = st.session_state.get("query")
    submitted = st.session_state.get("query_submitted")

    if submitted and query:
        st.session_state.scraping_in_progress = True
        try:
            raw_output = scraper(query)
            parsed_data = parser(raw_output)
            if parsed_data:
                st.session_state.output = parsed_data
        finally:
            st.session_state.scraping_in_progress = False
            st.rerun()


def layout():
    states_initialization()
    hero_section()
    query_input()

    stop_button()

    with st.container(horizontal_alignment="center"):
        with st.spinner("Scraping in progress..."):
            run_scraping()
    data_preview()
