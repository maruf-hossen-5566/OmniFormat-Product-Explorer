import time
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
from logger import setup_logger

logger = setup_logger(__name__)


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

    if not query and not data:
        st.divider()
        st.space("stretch")
        st.markdown(
            ":blue[🚫 No data yet. Enter a query and click “Scrape” to see results here.]",
            text_alignment="center",
        )
    elif query and data:
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
        if st.button("Clear Results", type="primary", key="clear-results-btn", width="stretch"):
            st.session_state.clear()
            st.rerun()


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
                logger.info("Successfully scraped and parsed data.")
                started_at = st.session_state.get("started_at", 0)
                if started_at:
                    logger.info(
                        f"Scraping took '{round(time.time() - started_at)}' seconds."
                    )
                    st.session_state.started_at = None
                st.rerun()
        except Exception as e:
            logger.exception("Failed at run 'scraping'.")
            st.session_state.clear()
            raise e
        finally:
            st.session_state.scraping_in_progress = False
            driver = st.session_state.get("driver")
            if driver:
                driver.quit()
            st.rerun()


def layout():
    try:
        states_initialization()
        hero_section()
        query_input()

        stop_button()

        with st.container(horizontal_alignment="center"):
            with st.spinner("Scraping in progress..."):
                run_scraping()
        data_preview()
    except Exception as error:
        logger.exception("Failed at run 'layout'.")
        st.session_state.clear()
        try:
            st.error(error)
        except Exception as e:
            logger.exception(f"Failed to display error.\n{e}")
        # st.rerun()
        raise error
