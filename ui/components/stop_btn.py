import time
import streamlit as st
from logger import setup_logger

logger = setup_logger(__name__)


def stop_button():
    driver = st.session_state.get("driver")
    in_progress = st.session_state.get("scraping_in_progress")
    if not in_progress and not driver:
        return

    with st.container(horizontal_alignment="center"):
        if st.button("Stop / Reset"):
            driver = st.session_state.get("driver")
            if driver:
                logger.info("Closing the browser...")
                started_at = st.session_state.get("started_at", 0)
                if started_at:
                    logger.info(
                        f"Scraping took '{round(time.time() - started_at)}' seconds."
                    )
                driver.quit()
            st.session_state.clear()
            st.rerun()
    st.divider()
