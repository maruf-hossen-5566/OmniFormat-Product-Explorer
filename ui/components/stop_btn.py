import streamlit as st


def stop_button():
    if not st.session_state.get("scraping_in_progress") and not st.session_state.get(
        "driver"
    ):
        return

    with st.container(horizontal_alignment="center"):
        if st.button("Stop / Reset"):
            if st.session_state.get("driver"):
                st.session_state.driver.quit()
            st.session_state.clear()
            st.rerun()
    st.divider()
