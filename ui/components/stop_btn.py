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
        empty = st.empty()
        if empty.button("Stop / Reset"):
            empty.empty()
            empty.markdown(":blue[Stopping the process...]", text_alignment="center")
            if st.session_state.get("driver"):
                logger.info("Closing the browser...")
                st.session_state.driver.quit()
                started_at = st.session_state.get("started_at", 0)
                if started_at:
                    logger.info(
                        f"Scarping cancelled in '{round(time.time() - started_at)}' seconds."
                    )
            st.session_state.clear()
            st.rerun()
    st.divider()
